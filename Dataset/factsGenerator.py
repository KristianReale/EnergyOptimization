import csv
from datetime import datetime
from collections import defaultdict


def csv_to_asp(input_file, output_file=None):
    hourly_data = defaultdict(
        lambda: {'discharge': [], 'charge': [], 'production': [], 'consumption': [], 'state_of_charge': [], 'h1_w': []})

    chargeInitValue = None
    with open(input_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Legge l'intestazione

        for row in reader:
            #print(row)
            date, discharge, charge, production, consumption, state_of_charge, h1_w = row
            if discharge == '' and charge == '' and production == '' and consumption == '' and state_of_charge == '' and h1_w == '':
                continue
            timestamp = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            hour_key = (timestamp.date(), timestamp.hour)

            hourly_data[hour_key]['discharge'].append(float(discharge))
            hourly_data[hour_key]['charge'].append(float(charge))
            hourly_data[hour_key]['production'].append(float(production))
            hourly_data[hour_key]['consumption'].append(float(consumption))
            hourly_data[hour_key]['state_of_charge'].append(float(state_of_charge))
            hourly_data[hour_key]['h1_w'].append(float(h1_w))
            if chargeInitValue == None:
                chargeInitValue = float(state_of_charge)


    fact_str = ""
    '''for (date, hour), values in hourly_data.items():
        fact_str += (
            f"discharge(\"{date}\",{hour},{sum(values['discharge']) / len(values['discharge'])*10:.0f}).\n"
            f"charge(\"{date}\",{hour},{sum(values['charge']) / len(values['charge'])*10:.0f}).\n"
            f"production(\"{date}\",{hour},{sum(values['production']) / len(values['production'])*10:.0f}).\n"
            f"consumption(\"{date}\",{hour},{sum(values['consumption']) / len(values['consumption'])*10:.0f}).\n"
            f"state_of_charge(\"{date}\",{hour},{sum(values['state_of_charge']) / len(values['state_of_charge'])*10:.0f}).\n"
            f"h1_w(\"{date}\",{hour},{sum(values['h1_w']) / len(values['h1_w'])*10:.0f}).\n"
        )'''
    fact_str += f"vE_Sinit({chargeInitValue})\n"
    for (date, hour), values in hourly_data.items():
        fact_str += (
            f"vP_PV(\"{date}\",{hour},{sum(values['production']) / len(values['production'])*10:.0f}).\n"
            f"vP_L(\"{date}\",{hour},{sum(values['consumption']) / len(values['consumption'])*10:.0f}).\n"
        )

    if output_file:
        with open(output_file, 'w') as aspfile:
            aspfile.write(fact_str)
    else:
        print(fact_str, end='')


# Esempio di utilizzo
csv_to_asp("DatasetDati/H1_W.csv", "fatti.lp")
#csv_to_asp("test.csv", "fatti.lp")
