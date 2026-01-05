import pandas as pd
import numpy as np

# === 1️⃣ Carica il dataset ===
# Sostituisci "file.xlsx" con il nome del tuo file Excel
df = pd.read_excel("analysis_picco.xlsx")

import time

start = time.time()  # tempo iniziale

maxCharge = 100
minCharge = 20
initChargePercentage = 60
maxDischargeTimes = 7
countDischargeTimes = 0

# === 2️⃣ Assicurati che la colonna 'date' sia di tipo datetime ===
df['date'] = pd.to_datetime(df['date'])
df["MaxCharge"] = None
df[maxCharge] = None
df["MinCharge"] = None
df[minCharge] = None
df["InitChargePercentage"] = None
df[initChargePercentage] = None

# === 3️⃣ Itera sulle righe e calcola i valori mancanti ===
soc_value = maxCharge * initChargePercentage / 100
print(soc_value)

lookahead = 1  # numero di ore da guardare avanti

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

    deficit = consumption - production

    if deficit > 0:
        # Guarda avanti e scarica solo se strettamente necessario
        future_deficit = any(
            df.loc[min(i + j, len(df) - 1), 'Consumption(KW)'] > df.loc[min(i + j, len(df) - 1), 'Production(KW)']
            for j in range(1, lookahead + 1)
        )

        if not future_deficit:
            # Scarica solo se soc_value lo permette
            discharge = min(deficit, soc_value - minCharge)
            from_grid = max(0, deficit - discharge)
        else:
            from_grid = deficit
    else:
        # Produzione maggiore del consumo → carica batteria
        charge = min(-deficit, maxCharge - soc_value)
        feed_in = max(0, -deficit - charge)

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
df.to_excel("file_completato_greedy.xlsx", index=False)
end = time.time()  # tempo finale

print("Tempo di esecuzione:", end - start, "secondi")
print("Calcolo dei valori mancanti completato.")
