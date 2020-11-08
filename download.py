#!/usr/bin/python
import os
import re
import sys
import urllib.request

import requests
from bs4 import BeautifulSoup

from constants import REGIONS

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
        :param folder:Path to the output directory.
        :param cache_filename:
        """
        self.url = url
        self.folder = folder
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
        req = requests.get(self.url, headers={"User-Agent": ""})
        soup = BeautifulSoup(req.text, "html.parser")
        pages = soup.findAll("a", attrs={"href": re.compile(r"data/datagis(?:-rok-)?\d{4}.zip$")})
        zipfilenames = [pages[i].attrs["href"] for i in range(len(pages))]
        [
            urllib.request.urlretrieve(
                self.url + zipfilenames[i],
                self.folder + os.path.sep + zipfilenames[i][5:],
            )
            for i in range(len(zipfilenames))
            if zipfilenames[i][5:] not in downloaded_files
        ]

    def parse_region_data(self, region):
        """
        Downloads all data files for the given region, if they are not already downloaded.
        Then for the given region, function parses data. The returned structure looks like this:
            tuple(list[str], list[np.ndarray]) where
                the list of string equals to the list of region three-char shortcuts,
                the list of NumPy arrays equals to the list of data.
            The length of the both list is the same. Also shape property of all NumPy arrays is
            the same.
        :param region: The three-char shortcut of the region name.
        :return: Tuple of two lists, described above.
        """
        ...

    def get_list(self, regions=REGIONS.keys()):
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
    downloader.download_data()
