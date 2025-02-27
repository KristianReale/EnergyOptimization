import csv
from datetime import datetime
from collections import defaultdict
from enum import Enum
import os

from asp.solve import best_grid_transfer_results_parse


class SPLIT_DATA(Enum):
    YEAR = 1
    MONTH = 2
    WEEK = 3
    DAY = 4
    NO_SPLIT = 10

class FORMAT(Enum):
    ASP = 1
    CSV = 2

def group_data(input_file): #per media
    hourly_data = defaultdict(
        lambda: {'discharge': [], 'charge': [], 'production': [], 'consumption': [], 'feed_in': [], 'from_grid': [], 'state_of_charge': [], 'h1_w': []})
    with open(input_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Legge l'intestazione

        for row in reader:
            #print(row)
            #date, discharge, charge, production, consumption, state_of_charge, h1_w = row
            date, discharge, charge, production, consumption, feed_in, from_grid, state_of_charge = row
            if discharge == '' and charge == '' and production == '' and consumption == '' and feed_in == '' and from_grid == '': # and state_of_charge == '' and h1_w == '':
                continue
            timestamp = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            hour_key = (timestamp.date(), timestamp.hour)

            hourly_data[hour_key]['discharge'].append(float(discharge))
            hourly_data[hour_key]['charge'].append(float(charge))
            hourly_data[hour_key]['production'].append(float(production))
            hourly_data[hour_key]['consumption'].append(float(consumption))
            hourly_data[hour_key]['feed_in'].append(float(feed_in))
            hourly_data[hour_key]['from_grid'].append(float(from_grid))
            #hourly_data[hour_key]['state_of_charge'].append(float(state_of_charge))
            #hourly_data[hour_key]['h1_w'].append(float(h1_w))
            #if chargeInitValue == None:
            #    chargeInitValue = float(state_of_charge)
    return hourly_data

def build_from_csv(input_file, output_dir, split_data = SPLIT_DATA.NO_SPLIT, format = FORMAT.ASP):
    hourly_data = group_data(input_file)
    chargeInitValue = 0 #cambiare


    '''for (date, hour), values in hourly_data.items():
        fact_str += (
            f"discharge(\"{date}\",{hour},{sum(values['discharge']) / len(values['discharge'])*10:.0f}).\n"
            f"charge(\"{date}\",{hour},{sum(values['charge']) / len(values['charge'])*10:.0f}).\n"
            f"production(\"{date}\",{hour},{sum(values['production']) / len(values['production'])*10:.0f}).\n"
            f"consumption(\"{date}\",{hour},{sum(values['consumption']) / len(values['consumption'])*10:.0f}).\n"
            f"state_of_charge(\"{date}\",{hour},{sum(values['state_of_charge']) / len(values['state_of_charge'])*10:.0f}).\n"
            f"h1_w(\"{date}\",{hour},{sum(values['h1_w']) / len(values['h1_w'])*10:.0f}).\n"
        )'''
    #fact_str += f"vE_Sinit({chargeInitValue*10:.0f}).\n"
    os.makedirs(output_dir, exist_ok=True)
    outputParts = {}

    for (date, hour), values in hourly_data.items():
        charge = sum(values['charge']) / len(values['charge'])
        charge = round(charge, 1)
        discharge = sum(values['discharge']) / len(values['discharge'])
        discharge = round(discharge, 1)
        production = sum(values['production']) / len(values['production'])
        production = round(production, 1)
        consumption = sum(values['consumption']) / len(values['consumption'])
        consumption = round(consumption, 1)
        feed_in = sum(values['feed_in']) / len(values['feed_in'])
        feed_in = round(feed_in, 1)
        from_grid = sum(values['from_grid']) / len(values['from_grid'])
        from_grid = round(from_grid, 1)
        stringToWrite = ""
        if format == FORMAT.ASP:
            '''if charge != 0:
                stringToWrite += (
                    f"vP_S(\"{date}\",{hour},{charge * 10:.0f}).\n"
                )
            if discharge != 0:
                stringToWrite += (
                    f"vP_S(\"{date}\",{hour},{discharge * -10:.0f}).\n"
                )'''
            stringToWrite += (
                f"vP_PV(\"{date}\",{hour},{production * 10:.0f}).\n"
                f"vP_L(\"{date}\",{hour},{consumption * 10:.0f}).\n"
            )
        elif format == FORMAT.CSV:
            stringToWrite += f"{date} {hour}:00:00,{discharge},{charge},{production},{consumption},{feed_in},{from_grid}\n"

        if split_data == SPLIT_DATA.DAY:
            if date not in outputParts:
                outputParts[date] = stringToWrite
            else:
                outputParts[date] += stringToWrite

    extension = ".asp"
    header = None
    if format == FORMAT.ASP:
        extension = ".asp"
    elif format == FORMAT.CSV:
        extension = ".csv"
        header = "date,Discharge(W),Charge(W),Production(W),Consumption(W),Feed-in(W),From grid(W)\n"

    for key in outputParts:
        with open(output_dir + "/" + str(key) + extension, 'w') as outfile:
            if header is not None:
                outfile.write(header)
            outfile.write(outputParts[key])

def asp_to_cvs(input_file, output_file):
    with open(input_file, 'r') as in_f, open(output_file, 'w') as out_f:
        #{"P_L": vP_L_results, "P_PV": vP_PV_results, "P_S": vP_S_results}
        results = best_grid_transfer_results_parse(in_f.read())
        out_f.write("date,Discharge(W),Charge(W),Production(W),Consumption(W),Feed-in(W),From grid(W)\n")#,State of Charge( %)")
        for cont in range(len(results["P_L"])):
            date = results["P_L"][cont]["day"].replace("\"", "") + " " + results["P_L"][cont]["time"] + ":00:00"
            #discharge = float(results["P_S"][cont]["value"]) / 10 if float(results["P_S"][cont]["value"]) > 0 else 0
            #charge = float(results["P_S"][cont]["value"]) / 10 if float(results["P_S"][cont]["value"]) < 0 else 0
            charge = float(results["Charge"][cont]["value"]) / 10
            discharge = float(results["Discharge"][cont]["value"]) / 10
            production = float(results["P_PV"][cont]["value"]) / 10
            consumption = float(results["P_L"][cont]["value"]) / 10
            feedin = float(results["Feed-in"][cont]["value"]) / 10
            fromgrid = float(results["From grid"][cont]["value"]) / 10
            out_f.write(f"{date},{discharge},{charge},{production},{consumption},{feedin},{fromgrid}\n")


