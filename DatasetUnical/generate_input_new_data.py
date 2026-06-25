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
                filename = "Input/nuovi_dati/filtered_merged_test_predictions.csv"
                folder_list = [f for f in os.listdir('Input/nuovi_dati') if os.path.isdir(os.path.join('Input/nuovi_dati', f))]
                #houseFolder = filename[:filename.index('_Wh.csv')]
                #for folder in folder_list:
                folder = 'Input/nuovi_dati'
                if not os.path.exists(f"{folder}"):
                    os.makedirs(f"{folder}")
                if not os.path.exists(f"{folder}/csv"):
                    os.makedirs(f"{folder}/csv")
                if not os.path.exists(f"{folder}/asp"):
                    os.makedirs(f"{folder}/asp")
                if not os.path.exists(f"{folder}/json"):
                    os.makedirs(f"{folder}/json")
                if not os.path.exists(f"{folder}/python"):
                    os.makedirs(f"{folder}/python")
                #build_from_csv(f"{filename}", f"{folder}/asp",split_data=SPLIT_DATA.DAY, format=FORMAT.ASP, unit="Wh", what="timesnet-predprod", noRound=False)
                #build_from_csv(f"{filename}", f"{folder}/csv",split_data=SPLIT_DATA.DAY, format=FORMAT.CSV, unit="Wh", what="timesnet-predprod", noRound=False)
                #build_from_csv(f"{filename}", f"{folder}/json", split_data=SPLIT_DATA.DAY, format=FORMAT.JSON, unit="Wh", what="timesnet-predprod", noRound=False)
                build_from_csv(f"{filename}", f"{folder}/python",split_data=SPLIT_DATA.DAY, format=FORMAT.PYTHON, unit="Wh", what="timesnet-predprod", noRound=False)

if __name__ == '__main__':
    unittest.main()