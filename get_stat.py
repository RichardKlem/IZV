import argparse
import logging

import numpy as np

from constants import DATA_HEADER, REGIONS_NUMS
from download import DataDownloader
from utils.logging import get_stat_logger as gsl

parser = argparse.ArgumentParser(description='Get_stat parser')
parser.add_argument("--fig_location", action="store", default=None,
                    help="If used, save figure in the given folder.")
parser.add_argument("--show_figure", action="store_true", default=None,
                    help="If set, show window with figure.")
parser.add_argument("-r", "--regions", action="store", default=None, nargs='+',
                    help="")


def plot_stat(data_source, fig_location=None, show_figure=False):
    """

    :param data_source:
    :param fig_location:
    :param show_figure:
    :return:
    """


if __name__ == '__main__':
    # Parse args and get values
    args = parser.parse_args()
    fig_loc = args.fig_location
    show_fig = args.show_figure
    regions = args.regions

    # Check if the input is valid
    if not set(regions).issubset(set(REGIONS_NUMS.keys())):
        gsl.log(logging.ERROR, f"Passed region does not exist!\nYou have passed {args.regions} "
                               f"while only these: {list(REGIONS_NUMS.keys())} are supported.")
        exit(-1)

    _, data = DataDownloader().get_list(regions)
    processed_data = {}
    for year in range(16, 21):
        mask = [int(data[i][0][-7:-5]) == year for i in range(data.shape[0])]
        processed_data[year] = data[mask].shape
    print(processed_data)



    mask = [np.logical_and(data[i][-1] == 'PHA', data[i][0][-7:-5] == '16') for i in range(
            data.shape[0])]

    filtered_data = data[mask]
    print(filtered_data)
    print(len(filtered_data))
