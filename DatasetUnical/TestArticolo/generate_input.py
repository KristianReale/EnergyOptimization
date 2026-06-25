import unittest

import os
import sys

#sys.path += [os.path.abspath(__file__ + "/..")]
sys.path += [os.path.abspath(__file__ + "/../..")]

from formatsGenerator import *
from asp.solve import *


class TestExecution(unittest.TestCase):
    def test_execution(self):
        for filename in os.listdir('Input'):
            print(filename)
            if filename.endswith('input.csv'):
                #folder_list = [f for f in os.listdir('Input') if os.path.isdir(os.path.join('TestArticolo/Input', f))]
                #houseFolder = filename[:filename.index('_Wh.csv')]

                if not os.path.exists(f"Input/csv"):
                    os.makedirs(f"Input/csv")
                if not os.path.exists(f"Input/asp"):
                    os.makedirs(f"Input/asp")
                if not os.path.exists(f"Input/json"):
                    os.makedirs(f"Input/json")
                if not os.path.exists(f"Input/python"):
                    os.makedirs(f"Input/python")
                if not os.path.exists(f"Input/greedy"):
                    os.makedirs(f"Input/greedy")
                #build_from_csv(f"Input/{filename}", f"Input/asp",split_data=SPLIT_DATA.DAY, format=FORMAT.ASP, unit="KWh", noRound=False)
                #build_from_csv(f"Input/{filename}", f"Input/csv",split_data=SPLIT_DATA.DAY, format=FORMAT.CSV, unit="KWh", noRound=False)
                #build_from_csv(f"Input/{filename}", f"Input/python", split_data=SPLIT_DATA.DAY, format=FORMAT.PYTHON, unit="KWh", noRound=False)
                build_from_csv(f"Input/{filename}", f"Input/greedy", split_data=SPLIT_DATA.DAY, format=FORMAT.GREEDY,
                               unit="KWh", noRound=False)
                #build_from_csv(f"Input/{filename}", f"Input/{folder}/json", split_data=SPLIT_DATA.DAY, format=FORMAT.JSON, unit="KWh", what=folder, noRound=True)


if __name__ == '__main__':
    unittest.main()