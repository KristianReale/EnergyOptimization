import re
import sys
from datetime import datetime


def finalcharge_results_parse(file):
    #result = "{vP_L(1,1,0), vP_L(1,2,0), vP_L(1,3,0), vP_L(1,4,0), vP_L(1,5,0), vP_L(1,6,0), vP_L(1,7,0), vP_L(1,8,0), vP_L(1,9,0), vP_L(1,10,0), vP_L(1,11,0), vP_L(1,12,0), vP_L(1,13,0), vP_L(1,14,0), vP_L(1,15,0), vP_L(1,16,0), vP_L(1,17,0), vP_L(1,18,0), vP_L(1,19,0), vP_L(1,20,0), vP_L(1,21,0), vP_L(1,22,0), vP_L(1,23,0), vP_S(1,1,999), vP_S(1,2,999), vP_S(1,3,999), vP_S(1,4,999), vP_S(1,5,999), vP_S(1,6,999), vP_S(1,7,999), vP_S(1,8,999), vP_S(1,9,999), vP_S(1,10,999), vP_S(1,11,999), vP_S(1,12,999), vP_S(1,13,999), vP_S(1,14,999), vP_S(1,15,999), vP_S(1,16,999), vP_S(1,17,999), vP_S(1,18,999), vP_S(1,19,999), vP_S(1,20,999), vP_S(1,21,999), vP_S(1,22,999), vP_S(1,23,999), vP_PV(1,1,998), vP_PV(1,2,998), vP_PV(1,3,998), vP_PV(1,4,998), vP_PV(1,5,998), vP_PV(1,6,998), vP_PV(1,7,998), vP_PV(1,8,998), vP_PV(1,9,998), vP_PV(1,10,998), vP_PV(1,11,998), vP_PV(1,12,998), vP_PV(1,13,998), vP_PV(1,14,998), vP_PV(1,15,998), vP_PV(1,16,998), vP_PV(1,17,998), vP_PV(1,18,998), vP_PV(1,19,998), vP_PV(1,20,998), vP_PV(1,21,998), vP_PV(1,22,998), vP_PV(1,23,998)} COST 11442569@1"
    #print(result)
    with open(file, "r") as file:
        result = file.read()
        pattern_vE_Sinit = r'vE_Sinit\((.*?)\)'  # Adatta se il formato cambia
        pattern_maxCharge = r'maxChargeKWh\((.*?)\)'  # Adatta se il formato cambia
        #pattern_xP_S = r'xP_S\("([^"]+)",\s*([\d.]+),\s*"([^"]+)",\s*"([-+]?\d+(?:\.\d+)?)"\)'
        pattern_xP_S = r'xP_S\("([^"]+)",\s*([\d.]+),\s*"([^"]+)"\)\s*=\s*([-+]?\d+(?:\.\d+)?)'


        matches_maxCharge = re.findall(pattern_maxCharge, result)
        matches_vE_Sinit = re.findall(pattern_vE_Sinit, result)
        matches_xP_S = re.findall(pattern_xP_S, result)

        initCharge = 0
        for match in matches_vE_Sinit:
            initCharge = float(match.replace("\"", ""))

        maxCharge = 0
        for match in matches_maxCharge:
            maxCharge = float(match.replace("\"", ""))


        charge_results = []
        discharge_results = []

        for match in matches_xP_S:
            date, timeI, time, value = match
            value = float(value.replace("\"", ""))

            if value >= 0:
                charge_results.append({"day": date, "time": time, "value": float(value)})
                discharge_results.append({"day": date, "time": time, "value": float(0)})
            else:
                charge_results.append({"day": date, "time": time, "value": float(0)})
                discharge_results.append({"day": date, "time": time, "value": float(value) * -1})

        charge_results = sorted(charge_results, key=lambda k: (k["day"], datetime.strptime(k["time"].replace("24:00:00", "23:59:59"), "%H:%M:%S")))
        discharge_results = sorted(discharge_results, key=lambda k: (k["day"], datetime.strptime(k["time"].replace("24:00:00", "23:59:59"), "%H:%M:%S")))

        finalChargeValue = initCharge
        for item in charge_results:
            finalChargeValue += float(item["value"])

        for item in discharge_results:
            finalChargeValue -= float(item["value"])

        return finalChargeValue# / maxCharge * 100

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(f"vE_Sinit(\"{finalcharge_results_parse(sys.argv[1])}\").\n")
