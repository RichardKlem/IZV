#!/usr/bin/python
import os
import re
import sys
import urllib.request
from zipfile import ZipFile

import requests
from bs4 import BeautifulSoup

from constants import DATA_FILES, DATA_WEB_ROOT, NUMS_REGIONS, REGIONS_NUMS

MIN_PYTHON = (3, 8)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)


class DataDownloader:
    parsed_regions = ()

    def __init__(
        self,
        url="https://ehw.fit.vutbr.cz/izv/",
        folder="data",
        cache_filename="data_{0}.pkl.gz",
    ):
        """
        Proper files are downloaded into given folder. Returns nothing.
        :param url: Source of files to download.
        :param folder: Name of the directory with data.
        :param cache_filename:
        """
        self.url = url
        self.folder = folder if folder.endswith(os.path.sep) else folder + os.path.sep
        self.cash_filename = cache_filename

    def download_data(self):
        """
        Downloads all data files from the given url into the given folder.
        """
        # Create the data folder if not exists
        if not os.path.isdir(self.folder):
            os.mkdir(self.folder)

        # Look for every data files
        downloaded_files = os.walk(self.folder).__next__()[2]

        # Get data file names from the given url
        [
            urllib.request.urlretrieve(
                self.url + DATA_WEB_ROOT + DATA_FILES[year],
                self.folder + DATA_FILES[year],
            )
            for year in DATA_FILES.keys()
            if DATA_FILES[year] not in downloaded_files
        ]

    def parse_region_data(self, region):
        """
        Downloads all data files for the given region, if they are not already downloaded.
        Then for the given region, function parses data. The returned structure looks like this:
            tuple(list[str], list[np.ndarray]) where
                the list of string equals to the list of the header elements,
                the list of NumPy arrays equals to the list of data.
            The length of the both list is the same. Also shape property of all NumPy arrays is
            the same.
        :param region: The three-char shortcut of the region name.
        :return: Tuple of two lists, described above.
        """
        # Download data
        downloader.download_data()

        zipfile = ZipFile(self.folder + "datagis2016.zip", "r")
        for file in zipfile.filelist:
            try:
                filename = int(file.filename[:2])
            except ValueError:
                continue
            if filename == REGIONS_NUMS[region]:
                print(zipfile.read(file.filename).decode('1250').split(os.linesep)[0])

    def get_list(self, regions=REGIONS_NUMS.keys()):
        """
        :param regions: A list of three-char shortcuts of regions to process. If None,
        all regions are processed.
        :return: Tuple of two lists, described above.
        """
        print(regions)


if __name__ == "__main__":
    # region, data = DataDownloader().get_list(['PHA', 'JHM', 'VYS'])
    # for region, data in (region, data):
    #    print(region, data.shape)
    downloader = DataDownloader()
    downloader.parse_region_data("PHA")
