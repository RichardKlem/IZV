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
from utils.logging import PROFILE_LOG_LEVEL
from utils.logging import data_downloader_logger as ddl

MIN_PYTHON = (3, 8)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)


class DataDownloader:
    parsed_regions = {}

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
        for key in REGIONS_NUMS.keys():
            self.parsed_regions[key] = None

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
        self.download_data()

        zipfiles = [ZipFile(self.folder + data_file, "r") for data_file in DATA_FILES.values()]

        data_array = np.array([])
        data_list = []
        for file in zipfiles:  # Walk through all the years
            for filelist in file.filelist:  # Walk through all the regions
                try:
                    filename = int(filelist.filename[:2])
                except ValueError:
                    continue
                if filename == REGIONS_NUMS[region]:
                    ddl.debug(f"Processing {filelist.filename} inside {file}.")
                    # Process all the records in the region
                    for i, row in enumerate(file.read(filelist.filename).decode('1250').split(
                            os.linesep)):
                        row = row.split(';')
                        if len(row) != 64:
                            continue
                        data_list.append(row)
                    part_array = np.array(data_list)
                    try:
                        np.vstack((data_array, part_array))
                    except ValueError:
                        data_array = part_array
                    break  # There should be only one file for each region.
            # Append the column with the region shortcut
            data_array = np.column_stack((data_array, (np.full(data_array.shape[0], region))))

        return DATA_HEADER, data_array

    def get_list(self, regions=None):
        """
        :param regions: A list of three-char shortcuts of regions to process. If None,
        all regions are processed.
        :return: Tuple of two lists, described above.
        """
        if not regions:
            REGIONS_NUMS.keys()
        elif not isinstance(regions, list):
            regions = [regions]

        concat_array = np.array([])
        for region in regions:
            # Data are in the memory
            if self.parsed_regions[region]:
                ddl.debug("Data tuple in attribute.")
                array = self.parsed_regions[region]
            # Data are not in the memory, but they are in cache files
            elif self.cash_filename.format(region) in os.walk(self.folder).__next__()[2]:
                ddl.debug("Data tuple in cache.")
                with gzip.GzipFile(self.folder + self.cash_filename.format(region), 'r') as f:
                    array = pickle.load(f)
            # Data are not in the memory nor in the cached files, they have to be parsed
            else:
                ddl.debug("Data tuple must be parsed before.")
                # Get data tuple
                _, array = self.parse_region_data(region)
                # Save data into a cache file
                with gzip.GzipFile(self.folder + self.cash_filename.format(region), 'w') as f:
                    pickle.dump(array, f)
            # For the first array of data, they will be rather saved into concat_array instead of
            # appending into for that moment empty array.
            try:
                concat_array = np.vstack((concat_array, array))
            except ValueError:
                concat_array = array
        return DATA_HEADER, concat_array


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    # Start measuring time
    start = time.perf_counter()

    downloader = DataDownloader()
    print(downloader.get_list(["PHA", "JHM"]))

    # End measuring time
    end = time.perf_counter()
    ddl.profile(f"Time: {end - start:0.4f} s")
