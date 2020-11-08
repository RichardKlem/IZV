import argparse

from download import DataDownloader

parser = argparse.ArgumentParser(description='Get_stat parser')
parser.add_argument("--fig_location", action="store", default=None,
                    help="If used, save figure in the given folder.")
parser.add_argument("--show_figure", action="store_true", default=None,
                    help="If set, show window with figure.")


def plot_stat(data_source, fig_location=None, show_figure=False):
    """

    :param data_source:
    :param fig_location:
    :param show_figure:
    :return:
    """


if __name__ == '__main__':
    region, data = DataDownloader().get_list(['PHA', 'JHM', 'VYS'])
