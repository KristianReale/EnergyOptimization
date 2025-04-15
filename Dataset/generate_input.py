import unittest

import os
import sys

sys.path += [os.path.abspath(__file__ + "/../..")]

from formatsGenerator import *
from asp.solve import *


class TestExecution(unittest.TestCase):
    def test_execution(self):
        for filename in os.listdir('DatasetDati'):
            if filename.endswith('_Wh.csv'):
                houseFolder = filename[:filename.index('_Wh.csv')]
                if not os.path.exists(f"InputDataset/{houseFolder}_Wh"):
                    os.makedirs(f"InputDataset/{houseFolder}_Wh")
                if not os.path.exists(f"InputDataset/{houseFolder}_Wh/csv"):
                    os.makedirs(f"InputDataset/{houseFolder}_Wh/csv")
                if not os.path.exists(f"InputDataset/{houseFolder}_Wh/asp"):
                    os.makedirs(f"InputDataset/{houseFolder}_Wh/asp")
                build_from_csv(f"DatasetDati/{filename}", f"InputDataset/{houseFolder}_Wh/asp",split_data=SPLIT_DATA.DAY, format=FORMAT.ASP, unit="KW")
                build_from_csv(f"DatasetDati/{filename}", f"InputDataset/{houseFolder}_Wh/csv",split_data=SPLIT_DATA.DAY, format=FORMAT.CSV, unit="KW")

if __name__ == '__main__':
    unittest.main()