"""
auspectra696.py
696 project

Handles the primary functions
"""
# !/usr/bin/env python3

#code ==> reformat code to comply with conventions

from __future__ import print_function
import sys
from argparse import ArgumentParser
import numpy as np
import matplotlib.pyplot as plt
import os
import numpy as np
import matplotlib.pyplot as plt
import xlrd
import pandas as pd
import collections as cl
import six


SUCCESS = 0
INVALID_DATA = 1
IO_ERROR = 2

DEFAULT_DATA_FILE_NAME = 'data/LongerTest.xlsx'


def warning(*objs):
    """Writes a message to stderr."""
    print("WARNING: ", *objs, file=sys.stderr)


def parse_cmdline(argv):
    """
    Returns the parsed argument list and return code.
    `argv` is a list of arguments, or `None` for ``sys.argv[1:]``.
    """
    if argv is None:
        argv = sys.argv[1:]

    # initialize the parser object:
    parser = ArgumentParser(description='Reads CHANGE to yours from examples help '
                                        '')
    parser.add_argument("-w", "--workbook", help="The location (directory and file name) of the Excel file with "
                                                      " The default file is {}, "
                                                 "located in the directory".format(DEFAULT_DATA_FILE_NAME),
                        default=DEFAULT_DATA_FILE_NAME)
    parser.add_argument("-n", "--normalize", help="Normalize data to max absorbance (default is true).",
                        action='store_true')
    args = None
    try:
        args = parser.parse_args(argv)
        args.wb_data = xlrd.open_workbook(input("Enter a file name (LongerTest.xlsx for testing purposes):  "))
    except IOError as e:
        warning("Problems reading file:", e)
        parser.print_help()
        return args, IO_ERROR

    return args, SUCCESS


def data_analysis(wb_data):
    sheet1 = wb_data.sheet_by_index(0)
    r = sheet1.nrows
    c = sheet1.ncols
    xLimLflt = sheet1.cell(1,0).value #must be less than 400
    xLimL = int(xLimLflt)

    #Upper limit
    xLimUflt = sheet1.cell(r-1,0).value
    xLimU = int(xLimUflt)

    #dict for extracted or calculated values from data
    data = cl.OrderedDict({'Sample ID': [],
                           'lambdaMax (nm)': [],
                           'Amax': [],
                           'Size (nm)': []
                           })

    print(r,c)

def plot_data(data_stats):
    pass


def main(argv=None):
    args, ret = parse_cmdline(argv)
    if ret != SUCCESS:
        return ret

    data_stats = data_analysis(args.wb_data)

    #
    # # get the name of the input file without the directory it is in, if one was specified
    # base_out_fname = os.path.basename(args.csv_data_file)
    # # get the first part of the file name (omit extension) and add the suffix
    # base_out_fname = os.path.splitext(base_out_fname)[0] + '_stats'
    # # add suffix and extension
    # out_fname = base_out_fname + '.csv'
    # np.savetxt(out_fname, data_stats, delimiter=',')
    # print("Wrote file: {}".format(out_fname))
    #
    # # send the base_out_fname and data to a new function that will plot the data
    # plot_stats(base_out_fname, data_stats)
    return SUCCESS  # success


if __name__ == "__main__":
    status = main()
    sys.exit(status)
