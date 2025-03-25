import unittest

import os
import sys

sys.path += [os.path.abspath(__file__ + "/../..")]

from formatsGenerator import *
from asp.solve import *


class TestExecution(unittest.TestCase):
    def test_execution(self):
        build_from_csv("DatasetDati/H1_Wh.csv", "InputDataset/H1_Wh",split_data=SPLIT_DATA.DAY, format=FORMAT.ASP)
        build_from_csv("DatasetDati/H1_Wh.csv", "InputDataset/H1_Wh",split_data=SPLIT_DATA.DAY, format=FORMAT.CSV)
        #build_from_csv("DatasetDati/H1_Wh.csv", "InputDataset/H1_15min_Wh", minute_granularity=15, split_data=SPLIT_DATA.DAY, format=FORMAT.ASP)
        #build_from_csv("DatasetDati/H1_Wh.csv", "InputDataset/H1_15min_Wh", minute_granularity=15, split_data=SPLIT_DATA.DAY, format=FORMAT.CSV)

if __name__ == '__main__':
    unittest.main()