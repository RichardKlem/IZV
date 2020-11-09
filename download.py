#!/usr/bin/python
import gzip
import logging
import os
import pickle
import sys
import time
import urllib.request
from zipfile import ZipFile

import numpy as np

from constants import DATA_FILES, DATA_HEADER, DATA_WEB_ROOT, REGIONS_NUMS

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
        :return: Tuple of the Python list and NumPy array, like described above.
        """
        # Download data
        downloader.download_data()

        zipfiles = [ZipFile(self.folder + data_file, "r") for data_file in DATA_FILES.values()]

        data_array = np.ndarray
        data_list = []
        for file in zipfiles:  # Walk through all the years
            for filelist in file.filelist:  # Walk through all the regions
                try:
                    filename = int(filelist.filename[:2])
                except ValueError:
                    continue
                if filename == REGIONS_NUMS[region]:
                    logging.info(f"Processing {filelist.filename}.")
                    print(f"Processing {filelist.filename} inside {file}.")
                    # Process all the records in the region

                    for i, row in enumerate(file.read(filelist.filename).decode('1250').split(
                            os.linesep)):
                        if len(row.split(';')) != 64:
                            continue
                        data_list.append(row.split(';'))
                    data_array = np.vstack(data_list)
                    break  # There should be only one file for each region.
                break

            data_array = np.column_stack((data_array, (np.full(data_array.shape[0], REGIONS_NUMS[
                region]))))

        return DATA_HEADER, data_array

    def get_list(self, regions=REGIONS_NUMS.keys()):
        """
        :param regions: A list of three-char shortcuts of regions to process. If None,
        all regions are processed.
        :return: Tuple of two lists, described above.
        """
        print(regions)


if __name__ == "__main__":
    downloader = DataDownloader()

    with gzip.GzipFile(downloader.cash_filename.format("ej"), 'w') as f:
        pickle.dump(downloader.parse_region_data("PHA"), f)
