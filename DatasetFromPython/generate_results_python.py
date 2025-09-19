import unittest

import os
import sys

import pandas as pd
import json


class TestExecution(unittest.TestCase):
    '''def test_execution(self):
        build_from_csv("DatasetDati/H1_W.csv", "FactsDataset/H1_W", SPLIT_DATA.DAY)
        filePath = os.path.dirname(os.path.abspath(__file__)) + "/FactsDataset/H1_W.asp"
        factsFiles = [filePath]
        solverResultsFilePath = os.path.dirname(os.path.abspath(__file__)) + "/Results/H1.txt"
        resultsFiles = os.path.dirname(os.path.abspath(__file__)) + "/Results/H1.csv"
        #results = calculate_best_grid_transfer(0, factsFiles, saveFilePath)
        asp_to_cvs(solverResultsFilePath, resultsFiles)'''


    '''def test_build_results(self):
        solverResultsFilePath = os.path.dirname(os.path.abspath(__file__)) + "/Results/H1_Wh_limit.txt"
        resultsFiles = os.path.dirname(os.path.abspath(__file__)) + "/Results/H1_Wh_limit.csv"
        #solverResultsFilePath = os.path.dirname(os.path.abspath(__file__)) + "/Results/H1_15min_Wh/H1_15min_Wh.txt"
        #resultsFiles = os.path.dirname(os.path.abspath(__file__)) + "/Results/H1_15min_Wh/H1_15min_Wh.csv"
        asp_to_cvs(solverResultsFilePath, resultsFiles, unit="KW")'''

    def test_build_excel_results(self):
        generate_final_excel()

def generate_final_excel():
    # Legge il JSON da file
    with open("pythonTest/output.json", "r") as f:
        data = json.load(f)

    # Converte le variabili in DataFrame
    df = pd.DataFrame(data["variables"])

    # Aggiunge una colonna con l’ora (1–24)
    df.insert(0, "Time (h)", range(1, len(df) + 1))

    # Metadati (tempo e funzione obiettivo)
    metadata = pd.DataFrame({
        "computation_time": [data["computation_time"]],
        "objective_function": [data["objective_function"]]
    })

    # Salva in Excel con due fogli
    output_path = "pythonTest/output.xlsx"
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Variables", index=False)
        metadata.to_excel(writer, sheet_name="Metadata", index=False)

    print(f"File Excel generato: {output_path}")

if __name__ == '__main__':
    unittest.main()