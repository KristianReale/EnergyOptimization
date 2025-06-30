import unittest

import os
import sys

sys.path += [os.path.abspath(__file__ + "/..")]


import pandas as pd
class TestExecution(unittest.TestCase):
    def test_execution(self):
        # Leggi i due file CSV
        df1 = pd.read_csv("Input/cubo/load_results.csv")  # contiene Date, True, dLinear, TimesNet
        df2 = pd.read_csv("Input/cubo/pv_results_2023.csv")  # contiene Date, True, Pred

        # Converti esplicitamente la colonna 'Date' in datetime
        df1['Date'] = pd.to_datetime(df1['Date'])
        df2['Date'] = pd.to_datetime(df2['Date'])

        # Filtra i dati a partire dal 21 agosto  (incluso)
        start_date = pd.to_datetime("2023-08-21")  # metti l'anno corretto se serve
        df1 = df1[df1['Date'] >= start_date]
        df2 = df2[df2['Date'] >= start_date]

        # Escludi il 31 dicembre
        df1 = df1[~((df1['Date'].dt.month == 12) & (df1['Date'].dt.day == 31))]
        df2 = df2[~((df2['Date'].dt.month == 12) & (df2['Date'].dt.day == 31))]

        # Rinomina la colonna 'True' in entrambi per distinguerli
        df2 = df2.rename(columns={'True': 'True Prod'})

        # Merge (join) sui valori della colonna 'Date'
        merged_df = pd.merge(df1, df2, on='Date', how='outer')

        # Estrai solo la data (senza ora) per il raggruppamento
        merged_df['Day'] = merged_df['Date'].dt.date

        # Filtra per tenere solo le giornate dove c'è almeno un dato da file2
        filtered_df = merged_df.groupby('Day').filter(self.has_any_prediction)

        # Rimuovi la colonna ausiliaria 'Day'
        filtered_df = filtered_df.drop(columns=['Day'])

        # Ordina per data e salva
        filtered_df = filtered_df.sort_values(by='Date')

        # Sostituisci i NaN con 0
        filtered_df = filtered_df.fillna(0)

        # Rimuovi righe duplicate basate sulla colonna 'Date', mantieni la prima occorrenza
        filtered_df = filtered_df.drop_duplicates(subset=['Date'], keep='first')


        filtered_df.to_csv("Input/cubo/merged_output.csv", index=False)


    def has_any_prediction(self, group):
        return not group[['Pred']].isnull().all().all()
if __name__ == '__main__':
    unittest.main()