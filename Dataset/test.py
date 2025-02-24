import unittest

import os
import sys

sys.path += [os.path.abspath(__file__ + "/../..")]

from formatsGenerator import *
from asp.solve import *


class TestExecution(unittest.TestCase):
    '''def test_execution(self):
        build_from_csv("DatasetDati/H1_W.csv", "FactsDataset/H1_W", SPLIT_DATA.DAY)
        filePath = os.path.dirname(os.path.abspath(__file__)) + "/FactsDataset/H1_W.asp"
        factsFiles = [filePath]
        solverResultsFilePath = os.path.dirname(os.path.abspath(__file__)) + "/Results/H1.txt"
        resultsFiles = os.path.dirname(os.path.abspath(__file__)) + "/Results/H1.csv"
        #results = calculate_best_grid_transfer(0, factsFiles, saveFilePath)
        asp_to_cvs(solverResultsFilePath, resultsFiles)'''

    def test_build_results(self):
        solverResultsFilePath = os.path.dirname(os.path.abspath(__file__)) + "/Results/H1.txt"
        resultsFiles = os.path.dirname(os.path.abspath(__file__)) + "/Results/H1.csv"
        asp_to_cvs(solverResultsFilePath, resultsFiles)

if __name__ == '__main__':
    unittest.main()