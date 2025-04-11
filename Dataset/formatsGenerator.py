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

def group_data(input_file, minute_granularity=60): #per media
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
            key = None
            if minute_granularity == 60:
                key = (timestamp.date(), str(timestamp.hour))
            elif minute_granularity < 60:
                hourKey = timestamp.hour
                minuteKey = None
                if (timestamp.minute == 0) or (timestamp.minute % minute_granularity) == 0:
                    minuteKey = timestamp.minute
                else:
                    minuteKey = (((timestamp.minute + minute_granularity) // minute_granularity) * minute_granularity) % 60
                    if minuteKey == 0:
                        hourKey += 1
                key = (timestamp.date(), str(hourKey) + ":" + str(minuteKey))

            hourly_data[key]['discharge'].append(float(discharge))
            hourly_data[key]['charge'].append(float(charge))
            hourly_data[key]['production'].append(float(production))
            hourly_data[key]['consumption'].append(float(consumption))
            hourly_data[key]['feed_in'].append(float(feed_in))
            hourly_data[key]['from_grid'].append(float(from_grid))
            #hourly_data[hour_key]['state_of_charge'].append(float(state_of_charge))
            #hourly_data[hour_key]['h1_w'].append(float(h1_w))
            #if chargeInitValue == None:
            #    chargeInitValue = float(state_of_charge)
    return hourly_data

def build_from_csv(input_file, output_dir, minute_granularity = 60, split_data = SPLIT_DATA.NO_SPLIT, format = FORMAT.ASP, unit ="W"):
    hourly_data = None
    hourly_data = group_data(input_file, minute_granularity)
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

    counterTime = 1
    for (date, time), values in hourly_data.items():
        charge = sum(values['charge']) # / len(values['charge'])
        if unit == "KW":
            charge = charge / 1000
            charge = round(charge, 2)
        else:
            charge = round(charge, 1)
        discharge = sum(values['discharge']) #/ len(values['discharge'])
        if unit == "KW":
            discharge = discharge / 1000
            discharge = round(discharge, 2)
        else:
            discharge = round(discharge, 1)

        production = sum(values['production']) #/ len(values['production'])
        if unit == "KW":
            production = production / 1000
            production = round(production, 2)
        else:
            production = round(production, 1)
        consumption = sum(values['consumption']) #/ len(values['consumption'])
        if unit == "KW":
            consumption = consumption / 1000
            consumption = round(consumption, 2)
        else:
            consumption = round(consumption, 1)
        feed_in = sum(values['feed_in']) #/ len(values['feed_in'])
        if unit == "KW":
            feed_in = feed_in / 1000
            feed_in = round(feed_in, 2)
        else:
            feed_in = round(feed_in, 1)
        from_grid = sum(values['from_grid']) #/ len(values['from_grid'])
        if unit == "KW":
            from_grid = from_grid / 1000
            from_grid = round(from_grid, 2)
        else:
            from_grid = round(from_grid, 1)
        stringToWrite = ""
        minutes_seconds = "00:00"
        if (minute_granularity % 60) != 0:
            minutes_seconds = "00"
        if format == FORMAT.ASP:
            if unit == "KW":
                stringToWrite += (
                    f"time({counterTime}, \"{time}:{minutes_seconds}\").\n"                    
                    f"vP_PV(\"{date}\",\"{time}:{minutes_seconds}\",{production * 100:.00f}).\n"
                    f"vP_L(\"{date}\",\"{time}:{minutes_seconds}\",{consumption * 100:.00f}).\n"
                )
            else:
                stringToWrite += (
                    f"time({counterTime}, \"{time}:{minutes_seconds}\").\n"
                    f"vP_PV(\"{date}\",\"{time}:{minutes_seconds}\",{production * 10:.0f}).\n"
                    f"vP_L(\"{date}\",\"{time}:{minutes_seconds}\",{consumption * 10:.0f}).\n"
                )
        elif format == FORMAT.CSV:
            stringToWrite += f"{date} {time}:{minutes_seconds},{discharge},{charge},{production},{consumption},{feed_in},{from_grid}\n"

        if split_data == SPLIT_DATA.DAY:
            if date not in outputParts:
                outputParts[date] = stringToWrite
            else:
                outputParts[date] += stringToWrite
        counterTime += 1

    extension = ".asp"
    header = None
    if format == FORMAT.ASP:
        extension = ".asp"
    elif format == FORMAT.CSV:
        extension = ".csv"
        if unit == "KW":
            header = "date,Discharge(KW),Charge(KW),Production(KW),Consumption(KW),Feed-in(KW),From grid(KW)\n"
        else:
            header = "date,Discharge(W),Charge(W),Production(W),Consumption(W),Feed-in(W),From grid(W)\n"

    for key in outputParts:
        with open(output_dir + "/" + str(key) + extension, 'w') as outfile:
            if header is not None:
                outfile.write(header)
            outfile.write(outputParts[key])

def asp_to_cvs(input_file, output_file, unit ="W"):
    with open(input_file, 'r') as in_f, open(output_file, 'w') as out_f:
        #{"P_L": vP_L_results, "P_PV": vP_PV_results, "P_S": vP_S_results}
        results = best_grid_transfer_results_parse(in_f.read(), unit)
        if unit == "KW":
            out_f.write(
                "date,Discharge(KW),Charge(KW),Production(KW),Consumption(KW),Feed-in(KW),From grid(KW)\n")  # ,State of Charge( %)")
        else:
            out_f.write("date,Discharge(W),Charge(W),Production(W),Consumption(W),Feed-in(W),From grid(W)\n")#,State of Charge( %)")
        for cont in range(len(results["P_L"])):
            date = results["P_L"][cont]["day"].replace("\"", "") + " " + results["P_L"][cont]["time"]
            #discharge = float(results["P_S"][cont]["value"]) / 10 if float(results["P_S"][cont]["value"]) > 0 else 0
            #charge = float(results["P_S"][cont]["value"]) / 10 if float(results["P_S"][cont]["value"]) < 0 else 0
            charge = float(results["Charge"][cont]["value"]) #/ 10
            discharge = float(results["Discharge"][cont]["value"])# / 10
            production = float(results["P_PV"][cont]["value"]) #/ 10
            consumption = float(results["P_L"][cont]["value"])# / 10
            feedin = float(results["Feed-in"][cont]["value"])# / 10
            fromgrid = float(results["From grid"][cont]["value"])# / 10
            out_f.write(f"{date},{discharge},{charge},{production},{consumption},{feedin},{fromgrid}\n")


