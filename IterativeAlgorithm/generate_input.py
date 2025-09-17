import unittest

import os
import sys

#sys.path += [os.path.abspath(__file__ + "/..")]
sys.path += [os.path.abspath(__file__ + "/../..")]

from formatsGenerator import *
from asp.solve import *


class TestExecution(unittest.TestCase):
    def test_execution(self):
        folder = "Input"
        build_from_csv("input.csv", folder ,split_data=SPLIT_DATA.DAY, format=FORMAT.ASP, unit="KWh", what=folder)
                    #build_from_csv(f"Input/{filename}", f"Input/{folder}/csv",split_data=SPLIT_DATA.DAY, format=FORMAT.CSV, unit="KWh", what=folder)
                    #build_from_csv(f"Input/{filename}", f"Input/{folder}/json", split_data=SPLIT_DATA.DAY, format=FORMAT.JSON, unit="KWh", what=folder)


if __name__ == '__main__':
    unittest.main()