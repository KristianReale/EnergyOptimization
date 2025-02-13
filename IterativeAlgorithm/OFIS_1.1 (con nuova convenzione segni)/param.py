import os
current_path = os.path.abspath('')

import numpy as np

from datetime import date, datetime, timedelta

import pandas as pd

# importo i dati di input
df_input=pd.read_excel("data/OFIS_input.xlsx")

# importo i parametri
df_params=pd.read_excel("data/OFIS_params.xlsx")

# INPUT
Q = df_input['Q'].to_numpy()
P = df_input['P'].to_numpy()

D = P - Q
OVER_P = np.where(D<0, 0, D) #produzione in eccesso da immagazzinare o immettere in rete
print("Excess production = ", OVER_P )

UNDER_P = np.where(D>0, 0, D*-1) #produzione in difetto
print("Under production = ", UNDER_P )

PUN = df_input['PREZZO_ACQUISTO_ENERGIA'].to_numpy()
PZ = df_input['PREZZO_VENDITA_ENERGIA'].to_numpy()

DATES = df_input['DATE'].to_numpy()

# unità di misura
UNIT = df_params['UNIT'].to_numpy()[0]

# VARIABILI INIZIALI
SOC0_1 = df_params['SOC_1'].to_numpy()[0]

# numero di giorni a cui si riferiscono i dati di input (PARAMS)
NUMBER_OF_DAYS = df_params['NUMBER_OF_DAYS'].to_numpy()[0]

# risoluzione temporale dei dati di input (PARAMS)
TIME_RESOLUTION = df_params['TIME_RESOLUTION'].to_numpy()[0]

# fattore per ui moltipliccar eper trasformare i profili di potenza in energia
CONVERT_TO_ENERGY_FACTOR = int(60 / TIME_RESOLUTION)

# profili di energia
Q_E = Q / CONVERT_TO_ENERGY_FACTOR
P_E = P / CONVERT_TO_ENERGY_FACTOR

OVER_P_E = OVER_P / CONVERT_TO_ENERGY_FACTOR
UNDER_P_E = UNDER_P / CONVERT_TO_ENERGY_FACTOR

# calcolo il numero di slot in base al numero di giorni e alla risouzione temporale
SLOTS = int( ( 1440 / TIME_RESOLUTION ) * NUMBER_OF_DAYS )
print(SLOTS)

SLOTS_HOUR = 60 / TIME_RESOLUTION;

# parameters of the problem
# litio
COST_CHARGE_1 = df_params['COST_CHARGE_1'].to_numpy()[0]
COST_DISCHARGE_1 = df_params['COST_DISCHARGE_1'].to_numpy()[0]
E_MIN_1 = df_params['E_MIN_1'].to_numpy()[0]
E_MAX_1 = df_params['E_MAX_1'].to_numpy()[0]
CapTotMin_1 = df_params['CapTotMin_1'].to_numpy()[0]
CapTotMax_1 = df_params['CapTotMax_1'].to_numpy()[0]

# seasonal storage
PAP = df_input['PREZZO_ACQUISTO_ENERGIA'].to_numpy() * df_params['PAP'].to_numpy()[0] #nel periodo in cui si può accumulare (0.05)
PVP = df_input['PREZZO_VENDITA_ENERGIA'].to_numpy() * df_params['PVP'].to_numpy()[0] #nel periodo in cui non si può prelevare (10)

E_MIN_SEASONAL_1 = df_params['E_MIN_SEASONAL'].to_numpy()[0]
E_MAX_SEASONAL_1 = df_params['E_MAX_SEASONAL'].to_numpy()[0]
CapTotMin_SEASONAL_1 = df_params['CapTotMin_SEASONAL'].to_numpy()[0]
CapTotMax_SEASONAL_1 = df_params['CapTotMax_SEASONAL'].to_numpy()[0]
SOC_SEASONAL_1 = df_params['SOC_SEASONAL'].to_numpy()[0]

# MSD
CREG_PLUS = df_input['CREG_PLUS'].to_numpy()
CREG_MINUS = df_input['CREG_MINUS'].to_numpy()

CREG_PLUS_E = CREG_PLUS / CONVERT_TO_ENERGY_FACTOR
CREG_MINUS_E = CREG_MINUS / CONVERT_TO_ENERGY_FACTOR

POFF_PLUS = df_input['POFF_PLUS'].to_numpy()
POFF_MINUS = df_input['POFF_MINUS'].to_numpy()

Percentage_p_SEASONAL_1 = df_params['Percentage_p_SEASONAL'].to_numpy()[0]
Percentage_m_SEASONAL_1 = df_params['Percentage_m_SEASONAL'].to_numpy()[0]
