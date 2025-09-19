import csv
import json
import re
from datetime import datetime
from collections import defaultdict
from enum import Enum
import os

import pandas as pd
from openpyxl.workbook import Workbook

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
    JSON = 3

def group_data(input_file, minute_granularity=60): #per media
    hourly_data = defaultdict(
        lambda: {'date': [], 'prod': [], 'cons': []})
    with open(input_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Legge l'intestazione

        for row in reader:
            #print(row)
            # Date,True_cons,dLinear,TimesNet,True Prod,Prod
            date, prod, cons = row
            #if true_cons == '' and dLinear == '' and TimesNet == '' and true_prod == '' and prod == '':
            #    continue
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


            hourly_data[key]['prod'].append(float(prod))
            hourly_data[key]['cons'].append(float(cons))

            #hourly_data[hour_key]['h1_w'].append(float(h1_w))
            #if chargeInitValue == None:
            #    chargeInitValue = float(state_of_charge)
    return hourly_data

def build_from_csv(input_file, output_dir, minute_granularity = 60, split_data = SPLIT_DATA.NO_SPLIT, format = FORMAT.ASP, unit ="W", what="real"):
    hourly_data = group_data(input_file, minute_granularity)

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
    currentDate = None
    initChargeStr = None
    for (date, time), values in hourly_data.items():
        if currentDate == None:
            currentDate = date
        elif currentDate != date:
            currentDate = date
            counterTime = 1

        #date, true_cons, dLinear, TimesNet, true_prod, prod

        prod = values['prod'][0]
        if unit == "KWh":
            prod = prod  # / 1000
            #prod = round(prod, 2)
        else:
            prod = round(prod, 1)
        cons = values['cons'][0]

        if unit == "KWh":
            cons = cons #/ 1000
            #cons = round(cons, 2)
        else:
            cons = round(cons, 1)

        production = prod
        consumption = cons

        state_of_charge = 80
        stringToWrite = ""
        minutes_seconds = "00:00"
        if (minute_granularity % 60) != 0:
            minutes_seconds = "00"
        if format == FORMAT.ASP:
            if counterTime == 1:
                if initChargeStr is None:
                    #stringToWrite += (
                    #    f"vE_SinitPercentage({round(state_of_charge)}).\n"
                    #)
                    initChargeStr = f"vE_SinitPercentage({round(state_of_charge)}).\n"
            if unit == "KWh":
                stringToWrite += (
                    f"time({counterTime}, \"{time}:{minutes_seconds}\").\n"                    
                    f"vP_PV(\"{date}\",\"{time}:{minutes_seconds}\",{production * 10000000:.00f}).\n"
                    f"vP_L(\"{date}\",\"{time}:{minutes_seconds}\",{consumption * 10000000:.00f}).\n"
                )
            else:
                stringToWrite += (
                    f"time({counterTime}, \"{time}:{minutes_seconds}\").\n"
                    f"vP_PV(\"{date}\",\"{time}:{minutes_seconds}\",{production * 10000000:.0f}).\n"
                    f"vP_L(\"{date}\",\"{time}:{minutes_seconds}\",{consumption * 10000000:.0f}).\n"
                )
        elif format == FORMAT.CSV:
            stringToWrite += f"{date} {time}:{minutes_seconds},{production},{consumption}\n"

        if split_data == SPLIT_DATA.DAY:
            if format == FORMAT.JSON:
                if date not in outputParts:
                    outputParts[date] = {
                        "production": [],
                        "consumption": []
                    }
                outputParts[date]["production"].append({
                    "time": f"{time}:{minutes_seconds}",
                    "value": production
                })
                outputParts[date]["consumption"].append({
                    "time": f"{time}:{minutes_seconds}",
                    "value": consumption
                })
            else:
                if date not in outputParts:
                    outputParts[date] = stringToWrite
                else:
                    outputParts[date] += stringToWrite
        counterTime += 1

    extension = ".asp"
    header = None
    if format == FORMAT.ASP:
        extension = ".asp"
        with open(output_dir + "/initCharge.asp", 'w') as initChargeFile:
            initChargeFile.write(initChargeStr)
    elif format == FORMAT.CSV:
        extension = ".csv"
        if unit == "KWh":
            header = "date,Production(KWh),Consumption(KWh)\n"
        else:
            header = "date,Production(W),Consumption(W)\n"
    elif format == FORMAT.JSON:
        extension = ".json"

    for key in outputParts:
        with open(output_dir + "/" + str(key) + "_" + unit + extension, 'w') as outfile:
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


def csv_to_json(file):
    data = pd.read_excel(file, 0)
    data = data["columns"]


def generate_final_excel(clingcon = False):
    resultsFolder = os.path.dirname(os.path.abspath(__file__)) + f"/ResultsClingcon"
    house_list = [f for f in os.listdir(resultsFolder) if os.path.isdir(os.path.join(resultsFolder, f))]

    for house in house_list:
        nextInitCharge = 36
        excel_file = resultsFolder + f"/{house}/analysis_{house}.xlsx"
        wb = Workbook()
        wb.remove(wb.active)
        file_list = sorted([f for f in os.listdir(os.path.dirname(os.path.abspath(__file__)) + f"/ResultsClingcon/{house}") if f.startswith("output") and not f.endswith("finalCharge.asp")])
        maxCharge = 36
        for file in file_list:
            date_file = re.search(r'(\d{4}-\d{2}-\d{2})', file).group(1)
            input_file_asp = os.path.dirname(
                os.path.abspath(__file__)) + "/ResultsClingcon" + f"/{house}/{file}"
            input_file_csv = os.path.dirname(
                os.path.abspath(__file__)) + "/Input" + f"/{house}/csv/{date_file}_KWh.csv"

            ws1 = wb.create_sheet(title=date_file)
            init_state_of_charge = 36
            with open(input_file_csv, 'r') as csvfile:
                reader = csv.reader(csvfile)
                header = next(reader)  # Legge l'intestazione
                ws1['A1'] = "Original Dataset"
                ws1['D1'] = "Analysis: " + house
                ws1['A2'] = "date"
                ws1['B2'] = "Discharge(KW)"
                ws1['C2'] = "Charge(KW)"
                ws1['D2'] = "Production(KW)"
                ws1['E2'] = "Consumption(KW)"
                ws1['F2'] = "Feed-in(KW)"
                ws1['G2'] = "From grid(KW)"
                ws1['H2'] = "State of Charge (%)"
                ws1['I2'] = "State of Charge (Value)"

                i = 3
                for row in reader:
                    #print(row)
                    #date, discharge, charge, production, consumption, feed_in, from_grid, state_of_charge = row
                    date, production, consumption = row
                    #if i == 3:
                    #    init_state_of_charge = state_of_charge
                    ws1[f"A{i}"] = date
                    #ws1[f"B{i}"] = float(discharge)
                    #ws1[f"C{i}"] = float(charge)
                    ws1[f"D{i}"] = float(production)
                    ws1[f"E{i}"] = float(consumption)
                    #ws1[f"F{i}"] = float(feed_in)
                    #ws1[f"G{i}"] = float(from_grid)
                    #ws1[f"H{i}"] = float(state_of_charge) / 100
                    #ws1[f"H{i}"].number_format = '0.00%'
                    #ws1[f"I{i}"] = ws1[f"H{i}"].value * 10
                    i+=1

            with open(input_file_asp, 'r') as in_f:
                lastString = in_f.read().split("Answer:")[-1]
                isOptimum = "OPTIMUM" in lastString
                numAns = lastString.split("%")[0]
                results = best_grid_transfer_results_parse(lastString, "kWh", clingcon= False)
                solving_time = "NA"

                match = re.search(r"Time:\s*([\d.]+)s", lastString.split("%")[0])
                if match:
                    secondi = float(match.group(1))
                    solving_time = secondi

                model_time = "NA"
                #pattern = r"Solving:\s*([\d.]+)s.*?1st Model:\s*([\d.]+)s"
                #match = re.search(pattern, lastString)
                #if match:
                #    solving_time = float(match.group(1))
                   # model_time = float(match.group(2))

                #ws1.title = date_file
                optStr = "NOT KNOWN"
                if isOptimum:
                    optStr = "YES"
                ws1['V6'] = "Is Optimal: "
                ws1['W6'] = optStr
                ws1['V7'] = "Last Answer Set Number: "
                ws1['W7'] = numAns
                ws1['V8'] = "Time Last Answer (seconds): "
                ws1['W8'] = solving_time
                ws1['V9'] = "Time Last Answer (minutes): "
                ws1['W9'] = "=W8/60"
                ws1['L1'] = "ASP Solution"
                ws1['L2'] = "date"
                ws1['M2'] = "Discharge(KW)"
                ws1['N2'] = "Charge(KW)"
                ws1['O2'] = "Production(KW)"
                ws1['P2'] = "Consumption(KW)"
                ws1['Q2'] = "Feed-in(KW)"
                ws1['R2'] = "From grid(KW)"
                ws1['S2'] = "State of Charge (%)"
                ws1['T2'] = "State of Charge (Value)"

                for cont in range(len(results["P_L"])):
                    i = cont + 3
                    date = results["P_L"][cont]["day"].replace("\"", "") + " " + results["P_L"][cont]["time"]
                    discharge = float(results["Discharge"][cont]["value"])
                    charge = float(results["Charge"][cont]["value"])
                    production = float(results["P_PV"][cont]["value"])
                    consumption = float(results["P_L"][cont]["value"])
                    feedin = float(results["Feed-in"][cont]["value"])
                    fromgrid = float(results["From grid"][cont]["value"])

                    if i == 3:
                        ws1['R1'] = "Init Charge (%):"
                        ws1['S1'] = float(init_state_of_charge) / maxCharge
                        #ws1['S1'] = 100
                        ws1['S1'].number_format = '0.00%'
                        #ws1['T1'] = ws1['S1'].value * 36
                        ws1['T1'] = init_state_of_charge
                        ws1['U1'] = "Max Charge:"
                        ws1['V1'] = maxCharge
                        ws1['W1'] = "Minimum storage Level"
                        ws1['X1'] = 0.1
                        ws1['X1'].number_format = '0.00%'
                        ws1['W2'] = "Maximum storage Level"
                        ws1['X2'] = 1
                        ws1['X2'].number_format = '0.00%'
                        ws1['W3'] = "Maximum Power (both Charge and Discharge)"
                        ws1['X3'] = "18kWh"


                    ws1[f"L{i}"] = date
                    ws1[f"M{i}"] = discharge
                    ws1[f"N{i}"] = charge
                    ws1[f"O{i}"] = production
                    ws1[f"P{i}"] = consumption
                    ws1[f"Q{i}"] = feedin
                    ws1[f"R{i}"] = fromgrid
                    ws1[f"S{i}"] = f"=T{i}/V$1"
                    ws1[f"S{i}"].number_format = '0.00%'
                    if (i == 3):
                        ws1["T3"] = "=T1-M3+N3"
                        ws1["T3"].number_format = '0.00'
                    else:
                        ws1[f"T{i}"] = f"=T{i-1}-M{i}+N{i}"
                        ws1[f"T{i}"].number_format = '0.00'
                    '''ws1[f"R{i}"] = float(state_of_charge) / 100
                    ws1[f"R{i}"].number_format = '0.00%'
                    ws1[f"S{i}"] = ws1['H1'].value * 10'''

            ws1['R1'] = "Init Charge (%):"
            ws1['S1'] = float(nextInitCharge) / maxCharge
            ws1['S1'].number_format = '0.00%'
            # ws1['T1'] = ws1['S1'].value * 36
            ws1['T1'] = float(nextInitCharge)

            if not clingcon:
                finalChargeFileName = input_file_asp.rsplit(".", 1)[0] + "_finalCharge.asp"
                #print("AAA " + finalChargeFileName)
                with open(finalChargeFileName, 'r') as in_fCharge:
                    result = in_fCharge.read().split("ANSWER")[-1]
                    pattern_initCharge = r'vFinalCharge\((.*?)\)'  # Adatta se il formato cambia
                    matches_initCharge = re.findall(pattern_initCharge, result)
                    for match in matches_initCharge:
                        nextInitCharge = float(match) / 100

        wb.save(excel_file)


