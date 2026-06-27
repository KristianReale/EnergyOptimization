import unittest

import os
import sys

#sys.path += [os.path.abspath(__file__ + "/..")]
sys.path += [os.path.abspath(__file__ + "/../..")]

from formatsGenerator import *
from asp.solve import *


class TestExecution(unittest.TestCase):
    def test_execution(self):
        filename = "Input/nuovi_dati/filtered_merged_test_predictions.csv"
        folder_list = [f for f in os.listdir('Input/nuovi_dati') if os.path.isdir(os.path.join('Input/nuovi_dati', f))]
        # houseFolder = filename[:filename.index('_Wh.csv')]
        # for folder in folder_list:
        folder = 'Input/nuovi_dati'

        #folder_list = [f for f in os.listdir('Input') if os.path.isdir(os.path.join('TestArticolo/Input', f))]
        #houseFolder = filename[:filename.index('_Wh.csv')]

        if not os.path.exists(f"Input/csv/k"):
            os.makedirs(f"Input/csv/k")
        if not os.path.exists(f"Input/asp/k"):
            os.makedirs(f"Input/asp/k")
        if not os.path.exists(f"Input/json/k"):
            os.makedirs(f"Input/json/k")
        if not os.path.exists(f"Input/python/k"):
            os.makedirs(f"Input/python/k")
        if not os.path.exists(f"Input/greedy/k"):
            os.makedirs(f"Input/greedy/k")
        build_from_csv(f"{filename}", f"Input/asp/k",split_data=SPLIT_DATA.DAY, format=FORMAT.ASP, unit="KWh", noRound=False, csv_bounds_file=f"Results/Compares/results.csv")
        build_from_csv(f"{filename}", f"Input/csv/k",split_data=SPLIT_DATA.DAY, format=FORMAT.CSV, unit="KWh", noRound=False, csv_bounds_file=f"Results/Compares/results.csv")
        build_from_csv(f"{filename}", f"Input/python/k", split_data=SPLIT_DATA.DAY, format=FORMAT.PYTHON, unit="KWh", noRound=False, csv_bounds_file=f"Results/Compares/results.csv")
        build_from_csv(f"{filename}", f"Input/greedy/k", split_data=SPLIT_DATA.DAY, format=FORMAT.GREEDY,
                       unit="KWh", noRound=False, csv_bounds_file=f"Results/Compares/results.csv")
        #build_from_csv(f"Input/{filename}", f"Input/{folder}/json", split_data=SPLIT_DATA.DAY, format=FORMAT.JSON, unit="KWh", what=folder, noRound=True)


if __name__ == '__main__':
    unittest.main()