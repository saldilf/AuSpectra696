
import unittest
import os
import auspectra696
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


class Testauspectra696(unittest.TestCase):

    def test_data_analysis(self):
        result = auspectra696.data_analysis(EXCEL_INPUT)
        self.assertEqual(result, [0.01287, 0.20669, 0.21599, 0.21233, 0.20997,
                                  0.21041, 0.22364, 0.19213, 0.2101, 0.20578,
                                  0.18737, 0.20889, 0.19202])

   # DEF TEST NORM== ARE ALL LAMBDAMAXES ALL EQUAL TO 1