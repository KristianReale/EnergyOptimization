import unittest

import os
import sys

sys.path += [os.path.abspath(__file__ + "/..")]

from formatsGenerator import *
#from asp.solve import *


class TestExecution(unittest.TestCase):
    def test_execution(self):
        for filename in os.listdir('Input/cubo'):
            if filename.endswith('all.csv'):
                #houseFolder = filename[:filename.index('_Wh.csv')]
                houseFolder = "cubo"
                if not os.path.exists(f"Input/{houseFolder}"):
                    os.makedirs(f"Input/{houseFolder}")
                if not os.path.exists(f"Input/{houseFolder}/csv"):
                    os.makedirs(f"Input/{houseFolder}/csv")
                if not os.path.exists(f"Input/{houseFolder}/asp"):
                    os.makedirs(f"Input/{houseFolder}/asp")
                build_from_csv(f"Input/{houseFolder}/{filename}", f"Input/{houseFolder}/asp",split_data=SPLIT_DATA.DAY, format=FORMAT.ASP, unit="KWh", what="real")
                build_from_csv(f"Input/{houseFolder}/{filename}", f"Input/{houseFolder}/csv",split_data=SPLIT_DATA.DAY, format=FORMAT.CSV, unit="KWh", what="real")

if __name__ == '__main__':
    unittest.main()