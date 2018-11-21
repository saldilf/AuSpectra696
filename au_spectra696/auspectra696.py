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

DEFAULT_DATA_FILE_NAME = 'LongerTest.xlsx'


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
        #args.wb_data = xlrd.open_workbook(input("Enter a file name (LongerTest.xlsx for testing purposes):  "))
    except IOError as e:
        warning("Problems reading file:", e)
        parser.print_help()
        return args, IO_ERROR

    return args, SUCCESS


def data_analysis(data_file):
    wb_data = xlrd.open_workbook(data_file)
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
    for x in range(3,c):


        #299 is the number of data points minus 2
        lambdas = sheet1.col_values(colx = 0,start_rowx = (xLimU - 299 ) - xLimL,  end_rowx = r) #x-vals (wavelength)
        abso = sheet1.col_values(colx = x,start_rowx = (xLimU - 299)-xLimL,end_rowx = r) #y-vals (absorbance)

        #400 is the lambda we start plotting at
        sID = sheet1.cell(0,x).value #name of each column
        lMax = abso.index(max(abso)) + 400 #find max lambda for a column
        Amax = max(abso) #get max Abs to norm against it

        absoNorm = [x/Amax for x in abso] #normalizes to Amax

        size = -0.02111514*(lMax**2.0) + 24.6*(lMax) - 7065.
        #J. Phys. Chem. C 2007, 111, 14664-14669

        #if lambdaMax outisde of this range then 1) particles aggregated and 2)outside of correlation
        if 518 < lMax < 570:
            data['Size (nm)'].append(int(size))

        else:
            data['Size (nm)'].append('>100')

        #added extracted/calculated items into dict 'data'
        data['Sample ID'].append(sID)
        data['lambdaMax (nm)'].append(lMax)
        data['Amax'].append( Amax )

        #plot each column (cycle in loop)
        plt.plot(lambdas, absoNorm ,linewidth=2,label= sheet1.cell(0,x).value)
        axes = plt.gca()
        box = axes.get_position()
        axes.set_position([box.x0, box.y0, box.width * 0.983, box.height])
        plt.xlabel('Wavelength (nm)')
        plt.ylabel('Absorbance (Normalized to Amax)')

    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fancybox=True, shadow=True)
    axes.set_xlim([400 , 700])
    axes.set_ylim([0 , 1.5])
    plt.show()



def plot_data(data_stats):
    pass


def main(argv=None):
    args, ret = parse_cmdline(argv)
    if ret != SUCCESS:
        return ret

    data_stats = data_analysis(args.workbook)

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
