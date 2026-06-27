import unittest

import os
import sys

#sys.path += [os.path.abspath(__file__ + "/..")]
sys.path += [os.path.abspath(__file__ + "/../..")]

from formatsGenerator import *
from asp.solve import *


class TestExecution(unittest.TestCase):
    def test_execution(self):
        #for filename in os.listdir('Input'):
            #if filename.endswith('merged_output.csv'):
                filename = "TestArticolo/Input/nuovi_dati/filtered_merged_test_predictions.csv"
                folder_list = [f for f in os.listdir('Input/nuovi_dati') if os.path.isdir(os.path.join('Input/nuovi_dati', f))]
                #houseFolder = filename[:filename.index('_Wh.csv')]
                #for folder in folder_list:
                folder = 'TestArticolo/Input/nuovi_dati'
                if not os.path.exists(f"{folder}/csv"):
                    os.makedirs(f"{folder}/csv")
                if not os.path.exists(f"{folder}/asp"):
                    os.makedirs(f"{folder}/asp")
                if not os.path.exists(f"{folder}/json"):
                    os.makedirs(f"{folder}/json")
                if not os.path.exists(f"{folder}/python"):
                    os.makedirs(f"{folder}/python")

                build_from_csv(f"{filename}", f"TestArticolo/Input/nuovi_dati/asp/k", split_data=SPLIT_DATA.DAY, format=FORMAT.ASP, unit="Wh",
                               noRound=False, csv_bounds_file=f"TestArticolo/Results/Compares/results.csv", what="timesnet-predprod")
                build_from_csv(f"{filename}", f"TestArticolo/Input/nuovi_dati/csv/k", split_data=SPLIT_DATA.DAY, format=FORMAT.CSV, unit="Wh",
                               noRound=False, csv_bounds_file=f"TestArticolo/Results/Compares/results.csv", what="timesnet-predprod")
                build_from_csv(f"{filename}", f"TestArticolo/Input/nuovi_dati/python/k", split_data=SPLIT_DATA.DAY, format=FORMAT.PYTHON, unit="Wh",
                               noRound=False, csv_bounds_file=f"TestArticolo/Results/Compares/results.csv", what="timesnet-predprod")

if __name__ == '__main__':
    unittest.main()