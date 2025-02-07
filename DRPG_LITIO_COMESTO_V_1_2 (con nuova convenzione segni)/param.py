import os
current_path = os.path.abspath('')

import numpy as np

import pandas as pd

# importo i dati di input
df_input=pd.read_excel("data/DRPG_input.xlsx")

# importo i parametri
df_params=pd.read_excel("data/DRPG_params.xlsx")

# importo gli storage
df_storages=pd.read_excel("data/DRPG_storages.xlsx")


# traiettoria storage aggregato (INPUT)
CHARGING_TOT = df_input['CHARGING_TOT'].to_numpy()

# data e ora degli slot (INPUT)
DATES = df_input['DATE'].to_numpy()

# numero di giorni a cui si riferiscono i dati di input (PARAMS)
NUMBER_OF_DAYS = df_params['NUMBER_OF_DAYS'].to_numpy()[0]

# risoluzione temporale dei dati di input (PARAMS)
TIME_RESOLUTION = df_params['TIME_RESOLUTION'].to_numpy()[0]

# calcolo il numero di slot in base al numero di giorni e alla risouzione temporale
SLOTS = int( ( 1440 / TIME_RESOLUTION ) * NUMBER_OF_DAYS )

# Creo una lista di storage
STORAGES_LIST = df_storages['STORAGES'].to_numpy()

# Lista dei vari SOC
RE_LIST = df_storages['RE'].to_numpy()

# Lista dei vari E_MIN
E_MIN_LIST = df_storages['E_MIN'].to_numpy()

# Lista dei vari E_MAX
E_MAX_LIST = df_storages['E_MAX'].to_numpy()

# Lista dei vari CapTotMin
CAPTOTMIN_LIST = df_storages['CapTotMin'].to_numpy()

# Lista dei vari CapTotMax
CAPTOTMAX_LIST = df_storages['CapTotMax'].to_numpy()


###

# importo i profili di carico
df_loads=pd.read_excel("data/DRPG_loads.xlsx")
df_productions=pd.read_excel("data/DRPG_productions.xlsx")

LOADS_arr = []
for j in range(len(STORAGES_LIST)):
    LOADS_arr.append( df_loads[j + 1].to_numpy() )
#print(LOADS_arr)

PRODUCTIONS_arr = []
for j in range(len(STORAGES_LIST)):
    PRODUCTIONS_arr.append( df_productions[j + 1].to_numpy() )
#print(PRODUCTIONS_arr)

#print('TEST ', PRODUCTIONS_arr[0][10])






