# AUTOGENERATED! DO NOT EDIT! File to edit: ../../notebooks/api/10_spice.kernels.ipynb.

# %% auto 0
__all__ = ['KERNEL_STORAGE', 'dataset_ids', 'df', 'df2', 'datasets', 'NAIF_URL', 'BASE_URL', 'GENERIC_STORAGE', 'GENERIC_URL',
           'generic_kernel_names', 'generic_kernel_paths', 'is_start_valid', 'is_stop_valid', 'download_one_url',
           'Subsetter', 'get_metakernel_and_files', 'list_kernels_for_day', 'download_generic_kernels',
           'load_generic_kernels', 'show_loaded_kernels']

# %% ../../notebooks/api/10_spice.kernels.ipynb 3
import warnings
import zipfile
from datetime import timedelta
from io import BytesIO
from itertools import repeat
from multiprocessing import Pool, cpu_count
from pathlib import Path

import requests
import spiceypy as spice
from astropy.time import Time
from dask.distributed import Client
from tqdm.auto import tqdm
from tqdm.contrib.concurrent import process_map
from yarl import URL

import pandas as pd
from fastcore.test import test_fail
from fastcore.utils import store_attr
from ..config import config
from ..utils import nasa_time_to_iso, url_retrieve

# %% ../../notebooks/api/10_spice.kernels.ipynb 5
KERNEL_STORAGE = config.storage_root / "spice_kernels"
KERNEL_STORAGE.mkdir(exist_ok=True, parents=True)

# %% ../../notebooks/api/10_spice.kernels.ipynb 7
dataset_ids = {
    "bc": "bc/bc_spice",
    "cassini": "co-s_j_e_v-spice-6-v1.0/cosp_1000",
    "clementine": "clem1-l-spice-6-v1.0/clsp_1000",
    "dart": "dart/dart_spice",
    "dawn": "dawn-m_a-spice-6-v1.0/dawnsp_1000",
    "di": "di-c-spice-6-v1.0/disp_1000",
    "ds1": "ds1-a_c-spice-6-v1.0/ds1sp_1000",
    "epoxi": "dif-c_e_x-spice-6-v1.0/epxsp_1000",
    "em16": "em16/em16_spice",
    "grail": "grail-l-spice-6-v1.0/grlsp_1000",
    "hayabusa": "hay-a-spice-6-v1.0/haysp_1000",
    "insight": "insight/insight_spice",
    "juno": "jno-j_e_ss-spice-6-v1.0/jnosp_1000",
    "ladee": "ladee/ladee_spice",
    "lro": "lro-l-spice-6-v1.0/lrosp_1000",
    "maven": "maven/maven_spice",
    "opportunity": "mer1-m-spice-6-v1.0/mer1sp_1000",
    "spirit": "mer2-m-spice-6-v1.0/mer2sp_1000",
    "messenger": "mess-e_v_h-spice-6-v1.0/messsp_1000",
    "mars2020": "mars2020/mars2020_spice",
    "mex": "mex-e_m-spice-6-v2.0/mexsp_2000",
    "mgs": "mgs-m-spice-6-v1.0/mgsp_1000",
    "ody": "ody-m-spice-6-v1.0/odsp_1000",
    "mro": "mro-m-spice-6-v1.0/mrosp_1000",
    "msl": "msl-m-spice-6-v1.0/mslsp_1000",
    "near": "near-a-spice-6-v1.0/nearsp_1000",
    "nh": "nh-j_p_ss-spice-6-v1.0/nhsp_1000",
    "orex": "orex/orex_spice",
    "rosetta": "ro_rl-e_m_a_c-spice-6-v1.0/rossp_1000",
    "stardust": "sdu-c-spice-6-v1.0/sdsp_1000",
    "venus_climate_orbiter": "vco/vco_spice",
    "vex": "vex-e_v-spice-6-v2.0/vexsp_2000",
    "vo": "vo1_vo2-m-spice-6-v1.0/vosp_1000",
}

df = pd.DataFrame({"shorthand": dataset_ids.keys(), "path": dataset_ids.values()})

df2 = pd.read_html("https://naif.jpl.nasa.gov/naif/data_archived.html")[6]
df2.columns = df2.iloc[0]
df2 = df2.drop(0).reset_index(drop=True)
df2 = df2.drop(["Archive Readme", "Archive Link", "Subset Link"], axis=1)
df = df.join(df2)
datasets = df.set_index("shorthand")

# %% ../../notebooks/api/10_spice.kernels.ipynb 10
def is_start_valid(
        mission: str,  # mission shorthand label of datasets dataframe
        start: Time,  # start time in astropy.Time format
):
    return Time(datasets.at[mission, "Start Time"]) <= start


def is_stop_valid(
        mission: str,  # mission shorthand label of datasets dataframe
        stop: Time,  # stop time in astropy.Time format
):
    return Time(datasets.at[mission, "Stop Time"]) >= stop

# %% ../../notebooks/api/10_spice.kernels.ipynb 13
NAIF_URL = URL("https://naif.jpl.nasa.gov")
BASE_URL = NAIF_URL / "cgi-bin/subsetds.pl"

# %% ../../notebooks/api/10_spice.kernels.ipynb 15
def download_one_url(url, local_path, overwrite: bool = False):
    if local_path.exists() and not overwrite:
        return
    local_path.parent.mkdir(exist_ok=True, parents=True)
    url_retrieve(url, local_path)


class Subsetter:
    """Class to manage retrieving subset SPICE kernel lists

    Attributes
    ----------
    kernel_names: List of
    """

    def __init__(
            self,
            mission: str,  # mission shorthand in datasets dataframe
            start: str,  # start time in either ISO or yyyy-jjj format
            stop=None,  # stop time in either ISO or yyyy-jjj format
            save_location=None,  # overwrite default storing in planetarpy archive
    ):
        store_attr()
        self.initialize()

    def initialize(self):
        r = self.r
        if r.ok:
            z = zipfile.ZipFile(BytesIO(r.content))
        else:
            raise IOError("SPICE Server request returned status code: {r.status_code}")
        self.z = z
        # these files only exist "virtually" in the zip object, but are needed to
        # extract them:
        self.urls_file = [n for n in z.namelist() if n.startswith("urls_")][0]
        self.metakernel_file = [n for n in z.namelist() if n.lower().endswith(".tm")][0]
        with self.z.open(self.urls_file) as f:
            self.kernel_urls = f.read().decode().split()

    @property
    def r(self):
        return requests.get(BASE_URL, params=self.payload, stream=True)

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        try:
            self._start = Time(value)
        except ValueError:
            self._start = Time(nasa_time_to_iso(value))

    @property
    def stop(self):
        return self._stop

    @stop.setter
    def stop(self, value):
        if not value:
            self._stop = self.start + timedelta(days=1)
        else:
            try:
                self._stop = Time(value)
            except ValueError:
                self._stop = Time(nasa_time_to_iso(value))

    @property
    def payload(self):
        """Put payload together while checking for working time format.

        If Time(self.start) doesn't work, then we assume that the date must be in the
        Time-unsupported yyyy-jjj format, which can be converted by `nasa_time_to_iso`
        from `planetarypy.utils`.
        """
        if not (is_start_valid(self.mission, self.start) and is_stop_valid(self.mission, self.stop)):
            raise ValueError("One of start/stop is outside the supported date-range. See `datasets`.")
        p = {
            "dataset": dataset_ids[self.mission],
            "start": self.start.iso,
            "stop": self.stop.iso,
            "action": "Subset",
        }
        return p

    @property
    def kernel_names(self):
        "Return list of names of kernels for the given time range."
        return [str(Path(URL(url).parent.name) / URL(url).name) for url in self.kernel_urls]

    def get_local_path(
            self,
            url,  # kernel url to determine local storage path
    ) -> Path:  # full local path where kernel in URL will be stored
        """Calculate local storage path from Kernel URL, using `save_location` if given.

        If self.save_location is None, the `planetarypy` archive is being used.
        """
        u = URL(url)
        basepath = (KERNEL_STORAGE / self.mission if not self.save_location else self.save_location)
        return basepath / u.parent.name / u.name

    def _non_blocking_download(self, overwrite: bool = False):
        with Client() as client:
            futures = []
            for url in tqdm(self.kernel_urls, desc="Kernels downloaded"):
                local_path = self.get_local_path(url)
                if local_path.exists() and not overwrite:
                    print(local_path.parent.name, local_path.name, "locally available.")
                    continue
                local_path.parent.mkdir(exist_ok=True, parents=True)
                futures.append(client.submit(url_retrieve, url, local_path))
            return [f.result() for f in futures]

    def _concurrent_download(self, overwrite: bool = False):
        paths = [self.get_local_path(url) for url in self.kernel_urls]
        args = zip(self.kernel_urls, paths, repeat(overwrite))
        results = process_map(download_one_url, args, max_workers=cpu_count() - 2)

    def download_kernels(
        self,
        overwrite: bool = False,  # switch to control if kernels should be downloaded over existing ones
        non_blocking: bool = False,
        quiet: bool = False,
    ):
        if non_blocking:
            return self._non_blocking_download(overwrite)
        # sequential download
        for url in tqdm(self.kernel_urls, desc="Kernels downloaded"):
            local_path = self.get_local_path(url)
            if local_path.exists() and not overwrite:
                if not quiet:
                    print(local_path.parent.name, local_path.name, "locally available.")
                continue
            local_path.parent.mkdir(exist_ok=True, parents=True)
            url_retrieve(url, local_path)

    def get_metakernel(self) -> Path:  # return path to metakernel file
        """Get metakernel file from NAIF and adapt path to match local storage.

        Use `save_location` if given, otherwise `planetarypy` archive.
        """
        basepath = (KERNEL_STORAGE / self.mission if not self.save_location else self.save_location)
        savepath = basepath / self.metakernel_file
        with open(savepath, "w") as outfile, self.z.open(self.metakernel_file) as infile:
            for line in infile:
                linestr = line.decode()
                if "'./data'" in linestr:
                    linestr = linestr.replace("'./data'", f"'{savepath.parent}'")
                outfile.write(linestr)
        return savepath

# %% ../../notebooks/api/10_spice.kernels.ipynb 43
def get_metakernel_and_files(
        mission: str,  # mission shorthand from datasets dataframe
        start: str,  # start time as iso-string, or yyyy-jjj
        stop: str,  # stop time as iso-string or yyyy-jjj
        save_location: str = None,  # override storage into planetarypy archive
        quiet: bool = False,  # suppress kernel-wise feedback
) -> Path:  # pathlib.Path to metakernel file with corrected data path.
    "For a given mission and start/stop times, download the kernels and get metakernel path"
    subset = Subsetter(mission, start, stop, save_location)
    subset.download_kernels(non_blocking=True, quiet=quiet)
    return subset.get_metakernel()

# %% ../../notebooks/api/10_spice.kernels.ipynb 45
def list_kernels_for_day(
        mission: str,  # mission shorthand from datasets dataframe
        start: str,  # start time as iso-string, or yyyy-jjj
        stop: str = "",  # stop time as iso-string or yyyy-jjj
) -> list:  # list of kernel names
    subset = Subsetter(mission, start, stop)
    return subset.kernel_names

# %% ../../notebooks/api/10_spice.kernels.ipynb 52
GENERIC_STORAGE = KERNEL_STORAGE / "generic"
GENERIC_STORAGE.mkdir(exist_ok=True, parents=True)
GENERIC_URL = NAIF_URL / "pub/naif/generic_kernels/"

generic_kernel_names = [
    "lsk/naif0012.tls",
    "pck/pck00010.tpc",
    "pck/de-403-masses.tpc",
    "spk/planets/de430.bsp",
    "spk/satellites/mar097.bsp",
]
generic_kernel_paths = [GENERIC_STORAGE.joinpath(i) for i in generic_kernel_names]

# %% ../../notebooks/api/10_spice.kernels.ipynb 53
def download_generic_kernels(overwrite=False):
    "Download all kernels as required by generic_kernel_list."
    dl_urls = [GENERIC_URL / i for i in generic_kernel_names]
    for dl_url, savepath in zip(dl_urls, generic_kernel_paths):
        if savepath.exists() and not overwrite:
            print(savepath.name, "already downloaded. Use `overwrite=True` to download again.")
            continue
        savepath.parent.mkdir(exist_ok=True, parents=True)
        url_retrieve(dl_url, savepath)

# %% ../../notebooks/api/10_spice.kernels.ipynb 55
def load_generic_kernels():
    """Load all kernels in generic_kernels list.

    Loads pure planetary bodies meta-kernel without spacecraft data.

    Downloads any missing generic kernels.
    """
    if any([not p.exists() for p in generic_kernel_paths]):
        download_generic_kernels()
    for kernel in generic_kernel_paths:
        spice.furnsh(str(kernel))

# %% ../../notebooks/api/10_spice.kernels.ipynb 58
def show_loaded_kernels():
    "Print overview of loaded kernels."
    count = spice.ktotal("all")
    if count == 0:
        print("No kernels loaded at this time.")
    else:
        print("The loaded files are:\n(paths relative to kernels.KERNEL_STORAGE)\n")
    for which in range(count):
        out = spice.kdata(which, "all", 100, 100, 100)
        print("Position:", which)
        p = Path(out[0])
        print("Path", p.relative_to(KERNEL_STORAGE))
        print("Type:", out[1])
        print("Source:", out[2])
        print("Handle:", out[3])
        # print("Found:", out[4])
