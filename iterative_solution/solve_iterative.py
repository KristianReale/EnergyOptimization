import pandas as pd
import numpy as np

# === 1️⃣ Carica il dataset ===
# Sostituisci "file.xlsx" con il nome del tuo file Excel
df = pd.read_excel("analysis_H1_15_min.xlsx")
maxCharge = 10000
initChargePercentage = 100

# === 2️⃣ Assicurati che la colonna 'date' sia di tipo datetime ===
df['date'] = pd.to_datetime(df['date'])
df["MaxCharge"] = None
df[maxCharge] = None
df["InitChargePercentage"] = None
df[initChargePercentage] = None

# === 3️⃣ Itera sulle righe e calcola i valori mancanti ===
soc_value = maxCharge * initChargePercentage / 100
for i in range(len(df)):
    row = df.loc[i]

    # Esempio: ottieni i valori noti della riga
    date = row['date']
    discharge = row['Discharge(KW)']
    charge = row['Charge(KW)']
    production = row['Production(KW)']
    consumption = row['Consumption(KW)']
    feed_in = row['Feed-in(KW)']
    from_grid = row['From grid(KW)']
    soc_percent = row['State of Charge (%)']


    # === 4️⃣ Se un valore è mancante (NaN), calcolalo con la tua formula ===

    discharge = 0
    charge = 0
    feed_in = 0
    from_grid = 0

    if production < consumption:
        discharge = consumption - production
        if discharge > soc_value:
            discharge = soc_value
        from_grid = consumption - production - discharge
    else:
        charge = production - consumption
        if charge + soc_value > maxCharge:
            charge = maxCharge - soc_value
        feed_in = production - consumption - charge

    soc_value = soc_value - discharge + charge

    soc_percent = soc_value / maxCharge * 100

    # === 5️⃣ Aggiorna la riga nel DataFrame ===
    df.loc[i, 'Discharge(KW)'] = discharge
    df.loc[i, 'Charge(KW)'] = charge
    df.loc[i, 'Feed-in(KW)'] = feed_in
    df.loc[i, 'From grid(KW)'] = from_grid
    df.loc[i, 'State of Charge (%)'] = soc_percent
    df.loc[i, 'State of Charge (Value)'] = soc_value



# === 6️⃣ (Facoltativo) Salva il risultato ===
df.to_excel("file_completato.xlsx", index=False)

print("Calcolo dei valori mancanti completato.")
