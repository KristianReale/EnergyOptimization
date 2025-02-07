import os
current_path = os.path.abspath('')

import pandas as pd
import numpy as np

from tools import append_list_as_row
from param import (
    SLOTS,
    SLOTS_HOUR,
    SOC0_1,
    COST_CHARGE_1,
    COST_DISCHARGE_1,
    E_MIN_1,
    E_MAX_1,
    CapTotMin_1,
    CapTotMax_1,
    DATES,
    Q,
    P,
    OVER_P,
    UNDER_P,
    PUN,
    PZ,
    CREG_PLUS,
    CREG_MINUS,
    CREG_PLUS_E,
    CREG_MINUS_E,
    POFF_PLUS,
    POFF_MINUS,
    PAP,
    PVP,
    SOC_SEASONAL_1,
    E_MIN_SEASONAL_1,
    E_MAX_SEASONAL_1,
    CapTotMin_SEASONAL_1,
    CapTotMax_SEASONAL_1,
    Percentage_p_SEASONAL_1,
    Percentage_m_SEASONAL_1,
    Q_E,
    P_E,
    UNIT,
    OVER_P_E,
    UNDER_P_E,
)
from optimisation import solve_optim

from openpyxl import Workbook

if __name__ == "__main__":

    wb = Workbook()
    ws = wb.active

    dict_var = solve_optim(
        slots= SLOTS,
        p=P_E,
        q=Q_E,
        over_p=OVER_P_E,
        under_p=UNDER_P_E,
        cost_charge_1=COST_CHARGE_1,
        cost_discharge_1=COST_DISCHARGE_1,
        e_min_1=E_MIN_1,
        e_max_1=E_MAX_1,
        cap_tot_min_1=CapTotMin_1,
        cap_tot_max_1=CapTotMax_1,
        soc0_1=SOC0_1,
        pun=PUN,
        pz=PZ,
        pap=PAP,
        pvp=PVP,
        creg_plus=CREG_PLUS_E,
        creg_minus=CREG_MINUS_E,
        poff_plus=POFF_PLUS,
        poff_minus=POFF_MINUS,
        e_min_seasonal_1=E_MIN_SEASONAL_1,
        e_max_seasonal_1=E_MAX_SEASONAL_1,
        cap_tot_min_seasonal_1=CapTotMin_SEASONAL_1,
        cap_tot_max_seasonal_1=CapTotMax_SEASONAL_1,
        soc0_seasonal_1=SOC_SEASONAL_1,
        percentage_p_SEASONAL_1=Percentage_p_SEASONAL_1,
        percentage_m_SEASONAL_1=Percentage_m_SEASONAL_1

        )


    # array che contiene la traiettoria che dovrà seguire la batteria per perseguire l'ottimo (risultato della funzione di ottimizzazione)
    # litio
    SOC_arr_1 = np.array([dict_var['battery_state_1_' + str(k)] for k in range(0, SLOTS + 1)])

    # idrogeno (seasonal)
    SOC_arr_seasonal_1 = np.array([dict_var['battery_state_seasonal_1_' + str(k)] for k in range(0, SLOTS + 1)])


    for i in range(0, SLOTS):
        date = DATES[i]
        t = pd.to_datetime(str(date)) 
        timestring = t.strftime('%Y-%m-%d %H:%M')

        generation = P_E[i]
        load = Q_E[i]
        over_p = OVER_P_E[i]
        under_p = UNDER_P_E[i]

        generation_profile = P[i]
        load_profile = Q[i]

        over_p_profile = OVER_P[i]
        under_p_profile = UNDER_P[i]

        pun = PUN[i]
        pz = PZ[i]

        creg_plus = CREG_PLUS[i]
        creg_minus = CREG_MINUS[i]
        poff_plus = POFF_PLUS[i]
        poff_minus = POFF_MINUS[i]

        if i == 0:
            SOC_1 = SOC_arr_1[i + 1]
            charging_1 = SOC_arr_1[i + 1] - SOC0_1

            SOC_seasonal_1 = SOC_arr_seasonal_1[i + 1]
            charging_seasonal_1 = SOC_arr_seasonal_1[i + 1] - SOC_SEASONAL_1

        else:
            SOC_1 = SOC_arr_1[i + 1]
            charging_1 = SOC_arr_1[i + 1] - SOC_arr_1[i]

            SOC_seasonal_1 = SOC_arr_seasonal_1[i + 1]
            charging_seasonal_1 = SOC_arr_seasonal_1[i + 1] - SOC_arr_seasonal_1[i]

        imported = charging_1 + charging_seasonal_1 + (load - generation)
        balance = imported + generation - load - charging_1 - charging_seasonal_1


        # salvo il risultato in un file csv
        if i == 0:
            row_header = ["DATE", "GENERATION (" + UNIT + ")", "LOAD (" + UNIT + ")", "OVER_P (" + UNIT + ")", "UNDER_P (" + UNIT + ")",  "GENERATION (" + UNIT + "h)", "LOAD (" + UNIT + "h)", "SOC_TOT (" + UNIT + "h)", "CHARGING_TOT (" + UNIT + ")", "SOC_SEASONAL_TOT (" + UNIT + "h)", "CHARGING_SEASONAL_TOT (" + UNIT + ")", "IMPORTED", "BALANCE", "PREZZO_ACQUISTO_ENERGIA", "PREZZO_VENDITA_ENERGIA", "CREG_PLUS", "POFF_PLUS", "CREG_MINUS", "POFF_MINUS"]
            ws.append(row_header)

            row_content = [timestring, float(format(generation_profile, '.6f')), float(format(load_profile, '.6f')), float(format(over_p_profile, '.6f')), float(format(under_p_profile, '.6f')), float(format(generation, '.6f')), float(format(load, '.6f')), float(format(SOC_1, '.6f')), float(format(charging_1 * SLOTS_HOUR * -1, '.6f')), float(format(SOC_seasonal_1, '.6f')), float(format(charging_seasonal_1 * SLOTS_HOUR * -1, '.6f')), float(format(imported * SLOTS_HOUR * -1, '.6f')), float(format(balance, '.6f')), float(format(pun, '.6f')), float(format(pz, '.6f')), float(format(creg_plus, '.6f')), float(format(poff_plus, '.6f')), float(format(creg_minus, '.6f')), float(format(poff_minus, '.6f'))]
            ws.append(row_content)
        else:
            row_content = [timestring, float(format(generation_profile, '.6f')), float(format(load_profile, '.6f')), float(format(over_p_profile, '.6f')), float(format(under_p_profile, '.6f')), float(format(generation, '.6f')), float(format(load, '.6f')),   float(format(SOC_1, '.6f')), float(format(charging_1 * SLOTS_HOUR * -1, '.6f')), float(format(SOC_seasonal_1, '.6f')), float(format(charging_seasonal_1 * SLOTS_HOUR * -1, '.6f')), float(format(imported * SLOTS_HOUR * -1, '.6f')), float(format(balance, '.6f')), float(format(pun, '.6f')), float(format(pz, '.6f')), float(format(creg_plus, '.6f')), float(format(poff_plus, '.6f')), float(format(creg_minus, '.6f')), float(format(poff_minus, '.6f'))]
            ws.append(row_content)

    wb.save("output/OFIS_DA_output.xlsx")