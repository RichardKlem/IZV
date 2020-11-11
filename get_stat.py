import argparse
import logging
import pathlib

import matplotlib.pyplot as plt
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


def plot_stat(data_source, fig_location=None, show_figure=False, regions=None):
    """

    :param data_source:
    :param fig_location:
    :param show_figure:
    :return:
    """
    processed_data = {}  # Dictionary of all results.
    fig = plt.figure(figsize=(17, 26), tight_layout=True)
    plt.title('Nehodovost v krajích podle roku', size=30)
    axes = []
    main_ax = fig.add_subplot(111)
    for i, year in enumerate(range(16, 21)):
        year_mask = [int(data_source[i][0][-7:-5]) == year for i in range(data_source.shape[0])]
        year_data = data_source[year_mask]
        one_year = {}  # Dictionary of result in one year.
        for region in regions:
            region_mask = [year_data[i][-1] == region for i in range(year_data.shape[0])]
            one_year[region] = year_data[region_mask].shape[0]
        processed_data[year] = one_year

        axes.append(fig.add_subplot(int(511 + i)))
        axes[i].set_xlabel("Kraje", size=20)
        axes[i].set_ylabel("Počet nehod", size=20)
        axes[i].bar(processed_data[year].keys(), processed_data[year].values())

    """
    plt.subplot(511)
    plt.bar(processed_data[16].keys(), processed_data[16].values())
    plt.subplot(512)
    plt.bar(processed_data[17].keys(), processed_data[17].values())
    plt.subplot(513)
    plt.bar(processed_data[18].keys(), processed_data[18].values())
    plt.subplot(514)
    plt.bar(processed_data[19].keys(), processed_data[19].values())
    plt.subplot(515)
    plt.bar(processed_data[20].keys(), processed_data[20].values())"""
    if show_figure:
        plt.show()
    if fig_location:
        pathlib.Path(fig_location).mkdir(parents=True, exist_ok=True)



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
    plot_stat(data_source=data, fig_location=fig_loc, show_figure=show_fig, regions=regions)

