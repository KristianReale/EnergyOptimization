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
            if filename.endswith('merged_output.csv'):
                folder_list = [f for f in os.listdir('Input') if os.path.isdir(os.path.join('Input', f))]
                #houseFolder = filename[:filename.index('_Wh.csv')]
                for folder in folder_list:
                    if not os.path.exists(f"Input/{folder}"):
                        os.makedirs(f"Input/{folder}")
                    if not os.path.exists(f"Input/{folder}/csv"):
                        os.makedirs(f"Input/{folder}/csv")
                    if not os.path.exists(f"Input/{folder}/asp"):
                        os.makedirs(f"Input/{folder}/asp")
                    build_from_csv(f"Input/{filename}", f"Input/{folder}/asp",split_data=SPLIT_DATA.DAY, format=FORMAT.ASP, unit="KWh", what=folder)
                    build_from_csv(f"Input/{filename}", f"Input/{folder}/csv",split_data=SPLIT_DATA.DAY, format=FORMAT.CSV, unit="KWh", what=folder)

if __name__ == '__main__':
    unittest.main()