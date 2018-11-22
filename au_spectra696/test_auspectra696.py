
import unittest
import os
import auspectra696
#from auspectra696 import main
import xlrd
from auspectra696 import parse_cmdline
#from au_spectra696.auspectra696 import main
import logging



__author__ = 'salwan'

# logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
# DISABLE_REMOVE = logger.isEnabledFor(logging.DEBUG)

# Directories #

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
#SUB_DATA_DIR = os.path.join(DATA_DIR, 'col_stats')

# Input files #
EXCEL_INPUT = os.path.join(DATA_DIR, "LongerTest.xlsx")


x = 5
wb_data = xlrd.open_workbook(EXCEL_INPUT)
sheet1 = wb_data.sheet_by_index(0)
r = sheet1.nrows
c = sheet1.ncols
xLimLflt = sheet1.cell(1, 0).value  # must be less than 400
xLimL = int(xLimLflt)

# Upper limit
xLimUflt = sheet1.cell(r - 1, 0).value
xLimU = int(xLimUflt)
lambdas = sheet1.col_values(colx=0, start_rowx=(xLimU - 299) - xLimL, end_rowx=r)  # x-vals (wavelength)
abso = sheet1.col_values(colx=x, start_rowx=(xLimU - 299) - xLimL, end_rowx=r)  # y-vals (absorbance)

class Testauspectra696(unittest.TestCase):

    def test_norm(self):
        result = auspectra696.norm(abso, max(abso), x)
        resultF = max(result)
        self.assertEqual(resultF, 1)

    def test_data_analysis(self):
        result = auspectra696.data_analysis('data/LongerTest.xlsx')
        resultJ = result['Amax']
        self.assertEqual(resultJ, [0.01287, 0.20669, 0.21599, 0.21233, 0.20997,
                                  0.21041, 0.22364, 0.19213, 0.2101, 0.20578,
                                  0.18737, 0.20889, 0.19202])

class Test_parse_cmdline(unittest.TestCase):
    def testOneFileInput(self):
        test_input = ['-w', 'data/LongerTest.xlsx']
        foo = parse_cmdline(test_input)
        #vars(test_input)
        #cmdlineVars = vars(parse_cmdline(test_input))
        self.assertTrue(parse_cmdline(test_input)[0]['workbook'] == 'data/LongerTest.xlsx')

# if __name__ == '__main__':
#     unittest.main()
# DEF TEST NORM== ARE ALL LAMBDAMAXES ALL EQUAL TO 1