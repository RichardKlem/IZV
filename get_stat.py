import argparse
# import logging
import os
import time

import matplotlib.pyplot as plt

# from constants import DATA_HEADER, REGIONS_NUMS
from download import REGIONS_NUMS, DataDownloader

# from utils import PROFILE_LOG_LEVEL
# from utils.logging import get_stat_logger as gsl


parser = argparse.ArgumentParser(description='Get_stat parser')
parser.add_argument("--fig_location", action="store", default=None,
                    help="If used, save figure in the given folder.")
parser.add_argument("--show_figure", action="store_true", default=None,
                    help="If set, show window with figure.")
parser.add_argument("-r", "--regions", action="store", default=None, nargs='+',
                    help="")


def touch(path):
    basedir = os.path.dirname(path)
    if not os.path.exists(basedir) and basedir != '':
        os.makedirs(basedir)

    with open(path, 'a'):
        os.utime(path, None)


def plot_stat(data_source, fig_location=None, show_figure=False, regions=None):
    """

    :param regions:
    :param data_source:
    :param fig_location:
    :param show_figure:
    :return:
    """
    processed_data = {}  # Dictionary of all results.
    fig = plt.figure(figsize=(8.27, 11.69))
    plt.title('Nehodovost v krajích podle roku', size=20)
    plt.tick_params(
        axis='both',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        bottom=False,  # ticks along the bottom edge are off
        left=False,  # ticks along the top edge are off
        labelbottom=False,
        labelleft=False
    )

    # start = time.perf_counter()
    axes = []
    # fig.add_subplot(111)
    for i, year in enumerate(range(16, 21)):
        year_mask = [int(data_source[i][0][-7:-5]) == year for i in range(data_source.shape[0])]
        year_data = data_source[year_mask]
        one_year = {}  # Dictionary of result in one year.
        for region in regions:
            region_mask = [year_data[i][-1] == region for i in range(year_data.shape[0])]
            one_year[region] = year_data[region_mask].shape[0]
        processed_data[year] = one_year

        # Calculate position
        pairs = [(region, processed_data[year][region]) for region in regions]
        pairs.sort(key=lambda x: x[1], reverse=True)

        # Get first elements - regions - sorted in reversed order
        sorted_regions = [pair[0] for pair in pairs]

        # Place position values where the region sit at.
        positions = [0 for i in range(len(sorted_regions))]

        for index, region in enumerate(regions):
            positions[index] = sorted_regions.index(region)

        axes.append(fig.add_subplot(int(511 + i)))
        axes[i].set_xlabel("Kraje", size=15)
        axes[i].set_ylabel("Počet nehod", size=15)
        bars = axes[i].bar(processed_data[year].keys(), processed_data[year].values())
        new_top_lim = axes[i].get_ylim()[1] * 1.2
        axes[i].set_ylim(bottom=0, top=new_top_lim)
        # axes[i].grid(b=True, axis='y', which='major', alpha=0.4)
        # axes[i].yaxis.set_minor_locator(MultipleLocator(new_top_lim / 10))

        for bar_index, bar in enumerate(bars):
            axes[i].text(
                bar.get_x() + bar.get_width() / 2.,
                bar.get_height() + axes[i].get_ylim()[1] / 30,
                positions[bar_index] + 1,
                ha='center',
                va='bottom', size=13)

    if fig_location:
        touch(fig_location)
        plt.savefig(fig_location)
    if show_figure:
        fig.tight_layout()
        plt.show()

    # end = time.perf_counter()
    # gsl.profile(f"Time: {end - start:0.4f} s")


if __name__ == '__main__':
    # Start measuring time
    start = time.perf_counter()

    # Parse args and get values
    args = parser.parse_args()
    fig_loc = args.fig_location
    show_fig = args.show_figure
    regs = args.regions

    # Check if the input is valid
    if not regs:
        regs = list(REGIONS_NUMS.keys())
    if not set(regs).issubset(set(REGIONS_NUMS.keys())):
        # gsl.log(logging.ERROR, f"Passed region does not exist!\nYou have passed {regs} "
        #                        f"while only these: {list(REGIONS_NUMS.keys())} are supported.")
        print(f"Passed region does not exist!\nYou have passed {regs} "
              f"while only these: {list(REGIONS_NUMS.keys())} are supported.")
        exit(-1)
    _, data = DataDownloader().get_list(regs)
    plot_stat(data_source=data, fig_location=fig_loc, show_figure=show_fig, regions=regs)
    # End measuring time
    end = time.perf_counter()
    # gsl.profile(f"Time: {end - start:0.4f} s")
