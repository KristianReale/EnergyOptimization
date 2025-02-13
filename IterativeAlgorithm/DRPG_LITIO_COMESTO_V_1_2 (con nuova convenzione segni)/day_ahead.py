import os
current_path = os.path.abspath('')

import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta, timezone

from tools import append_list_as_row
from param import (
    SLOTS,
    STORAGES_LIST,
    RE_LIST,
    E_MIN_LIST,
    E_MAX_LIST,
    CAPTOTMIN_LIST,
    CAPTOTMAX_LIST,
    DATES,
    CHARGING_TOT,
    LOADS_arr,
    PRODUCTIONS_arr
)
from optimisation import solve_optim

from openpyxl import Workbook

if __name__ == "__main__":

    wb = Workbook()
    ws = wb.active

    dict_var = solve_optim(
        slots= SLOTS,
        storages_list= STORAGES_LIST,
        re_list= RE_LIST,
        e_min_list= E_MIN_LIST,
        e_max_list= E_MAX_LIST,
        captotmin_list= CAPTOTMIN_LIST,
        captotmax_list= CAPTOTMAX_LIST,
        charging_tot=CHARGING_TOT,
        loads=LOADS_arr,
        productions = PRODUCTIONS_arr
        )

    #print(dict_var)
    # array che contiene la traiettoria che dovrà seguire la batteria per perseguire l'ottimo (risultato della funzione di ottimizzazione)
    # litio
    RE_arr = []

    for j in range(len(STORAGES_LIST)):
        RE_arr.append( np.array([dict_var['battery_state_t_{storage}_{slot}'.format(storage=j+1, slot=k)] for k in range(0, SLOTS + 1)]) )

    for i in range(0, SLOTS):
        date = DATES[i]
        charging_tot = CHARGING_TOT[i]

        RE = []
        charging = []


        if i == 0:
            for j in range(len(STORAGES_LIST)):
                RE.append(RE_arr[j][i + 1])
                charging.append(RE_arr[j][i + 1] - RE_LIST[j])


        else:
            for j in range(len(STORAGES_LIST)):
                RE.append(RE_arr[j][i + 1])
                charging.append(RE_arr[j][i + 1] - RE_arr[j][i])

        # salvo il risultato in un file excel
        if i == 0:
            row_header = []
            row_header.append("DATE")

            for j in range(len(STORAGES_LIST)):
                row_header.append("RE_{storage}".format(storage=j+1))
                row_header.append("CHARGING_{storage}".format(storage=j+1))

            row_header.append("CHARGING_TOTAL")
            ws.append(row_header)

            row_content = []
            t = pd.to_datetime(str(date)) 
            timestring = t.strftime('%Y-%m-%d %H:%M')
            row_content.append(timestring)


            for j in range(len(STORAGES_LIST)):
                row_content.append(float(format(RE[j], '.3f') ))
                row_content.append(float(format(charging[j] * -1, '.3f') ))

            row_content.append(float(format(charging_tot * -1, '.3f')) )

            ws.append(row_content)
            
        else:
            row_content = []
            t = pd.to_datetime(str(date)) 
            timestring = t.strftime('%Y-%m-%d %H:%M')
            row_content.append(timestring)

            for j in range(len(STORAGES_LIST)):
                row_content.append(float(format(RE[j], '.3f') ))
                row_content.append(float(format(charging[j] * -1, '.3f') ))

            row_content.append(float(format(charging_tot * -1, '.3f')) )
            
            ws.append(row_content)

    wb.save("output/DRPG_DA_output.xlsx")

