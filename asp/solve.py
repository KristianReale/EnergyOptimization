import configparser
import subprocess
import re
import os
import tempfile
import json
import threading
import uuid
from collections import OrderedDict
from datetime import datetime
from pathlib import Path

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DLV_PATH = ROOT_PATH + "/../solver/DLV/macosx/dlv-2.1.2-arm64"
ASP_PROGRAM_PATH = ROOT_PATH + "/../asp_encodings/simplified/encoding_article.asp"
ASP_RECOMMENDATION_PATH = ROOT_PATH + "/../asp_encodings/recommendation/recommend.asp"
ASP_RECOMMENDATION_BATTERY_PATH = ROOT_PATH + "/../asp_encodings/recommendation/recommendation_battery.asp"
ASP_FINAL_CHARGE_PATH = ROOT_PATH + "/../asp_encodings/simplified/final_charge.asp"
#ASP_PROGRAM_PATH = "asp_encodings/simplified/encoding.asp"
ASP_PARAMS_PATH = ROOT_PATH + "/../asp_encodings/simplified/params_per_building/"
ASP_MAXCHARGE_PATH = ROOT_PATH + "/../asp_encodings/simplified/maxChargeKwh.asp"

scheduledExecIds = []

def calculate_best_storage(building, esinit, date, saveResultsFile = None):
    command = [DLV_PATH, ASP_PROGRAM_PATH, ASP_PARAMS_PATH, "--silent"]
    response = subprocess.run(command, capture_output=True, text=True)
    return best_storage_results_parse(response.stdout)
    #print(P, Q, PUN, PZ, CREG_PLUS, POFF_PLUS, CREG_MINUS, POFF_MINUS)

def best_storage_results_parse(result):
    #result = "vQ(\"2019-12-03\",23,84) vP(\"2019-12-03\",23,0) vPUN(\"2019-12-03\",23,2) vPZ(\"2019-12-03\",23,0) vCREG_PLUS(\"2019-12-03\",23,0) vPOFF_PLUS(\"2019-12-03\",23,0) vCREG_MINUS(\"2019-12-03\",23,0) vPOFF_MINUS(\"2019-12-03\",23,0) time(22) vQ(\"2019-12-03\",22,101) vP(\"2019-12-03\",22,0) vPUN(\"2019-12-03\",22,2) vPZ(\"2019-12-03\",22,0) vCREG_PLUS(\"2019-12-03\",22,0) vPOFF_PLUS(\"2019-12-03\",22,0) vCREG_MINUS(\"2019-12-03\",22,0) vPOFF_MINUS(\"2019-12-03\",22,0) time(21) vQ(\"2019-12-03\",21,92) vP(\"2019-12-03\",21,0) vPUN(\"2019-12-03\",21,2) vPZ(\"2019-12-03\",21,0) vCREG_PLUS(\"2019-12-03\",21,0) vPOFF_PLUS(\"2019-12-03\",21,0) vCREG_MINUS(\"2019-12-03\",21,0) vPOFF_MINUS(\"2019-12-03\",21,0) time(20) vQ(\"2019-12-03\",20,112) vP(\"2019-12-03\",20,0) vPUN(\"2019-12-03\",20,2) vPZ(\"2019-12-03\",20,0) vCREG_PLUS(\"2019-12-03\",20,0) vPOFF_PLUS(\"2019-12-03\",20,0) vCREG_MINUS(\"2019-12-03\",20,0) vPOFF_MINUS(\"2019-12-03\",20,0) time(19) vQ(\"2019-12-03\",19,50) vP(\"2019-12-03\",19,0) vPUN(\"2019-12-03\",19,2) vPZ(\"2019-12-03\",19,0) vCREG_PLUS(\"2019-12-03\",19,0) vPOFF_PLUS(\"2019-12-03\",19,0) vCREG_MINUS(\"2019-12-03\",19,0) vPOFF_MINUS(\"2019-12-03\",19,0) time(18) vQ(\"2019-12-03\",18,55) vP(\"2019-12-03\",18,0) vPUN(\"2019-12-03\",18,2) vPZ(\"2019-12-03\",18,0) vCREG_PLUS(\"2019-12-03\",18,0) vPOFF_PLUS(\"2019-12-03\",18,0) vCREG_MINUS(\"2019-12-03\",18,0) vPOFF_MINUS(\"2019-12-03\",18,0) time(17) vQ(\"2019-12-03\",17,79) vP(\"2019-12-03\",17,0) vPUN(\"2019-12-03\",17,2) vPZ(\"2019-12-03\",17,0) vCREG_PLUS(\"2019-12-03\",17,0) vPOFF_PLUS(\"2019-12-03\",17,0) vCREG_MINUS(\"2019-12-03\",17,0) vPOFF_MINUS(\"2019-12-03\",17,0) time(16) vQ(\"2019-12-03\",16,74) vP(\"2019-12-03\",16,0) vPUN(\"2019-12-03\",16,2) vPZ(\"2019-12-03\",16,0) vCREG_PLUS(\"2019-12-03\",16,0) vPOFF_PLUS(\"2019-12-03\",16,0) vCREG_MINUS(\"2019-12-03\",16,0) vPOFF_MINUS(\"2019-12-03\",16,0) time(15) vQ(\"2019-12-03\",15,58) vP(\"2019-12-03\",15,0) vPUN(\"2019-12-03\",15,2) vPZ(\"2019-12-03\",15,0) vCREG_PLUS(\"2019-12-03\",15,0) vPOFF_PLUS(\"2019-12-03\",15,0) vCREG_MINUS(\"2019-12-03\",15,0) vPOFF_MINUS(\"2019-12-03\",15,0) time(14) vQ(\"2019-12-03\",14,66) vP(\"2019-12-03\",14,0) vPUN(\"2019-12-03\",14,2) vPZ(\"2019-12-03\",14,0) vCREG_PLUS(\"2019-12-03\",14,0) vPOFF_PLUS(\"2019-12-03\",14,0) vCREG_MINUS(\"2019-12-03\",14,0) vPOFF_MINUS(\"2019-12-03\",14,0) time(13) vQ(\"2019-12-03\",13,66) vP(\"2019-12-03\",13,0) vPUN(\"2019-12-03\",13,2) vPZ(\"2019-12-03\",13,0) vCREG_PLUS(\"2019-12-03\",13,0) vPOFF_PLUS(\"2019-12-03\",13,0) vCREG_MINUS(\"2019-12-03\",13,0) vPOFF_MINUS(\"2019-12-03\",13,0) time(12) vQ(\"2019-12-03\",12,81) vP(\"2019-12-03\",12,0) vPUN(\"2019-12-03\",12,2) vPZ(\"2019-12-03\",12,0) vCREG_PLUS(\"2019-12-03\",12,0) vPOFF_PLUS(\"2019-12-03\",12,0) vCREG_MINUS(\"2019-12-03\",12,0) vPOFF_MINUS(\"2019-12-03\",12,0) time(11) vQ(\"2019-12-03\",11,80) vP(\"2019-12-03\",11,0) vPUN(\"2019-12-03\",11,2) vPZ(\"2019-12-03\",11,0) vCREG_PLUS(\"2019-12-03\",11,0) vPOFF_PLUS(\"2019-12-03\",11,0) vCREG_MINUS(\"2019-12-03\",11,0) vPOFF_MINUS(\"2019-12-03\",11,0) time(10) vQ(\"2019-12-03\",10,51) vP(\"2019-12-03\",10,0) vPUN(\"2019-12-03\",10,2) vPZ(\"2019-12-03\",10,0) vCREG_PLUS(\"2019-12-03\",10,0) vPOFF_PLUS(\"2019-12-03\",10,0) vCREG_MINUS(\"2019-12-03\",10,0) vPOFF_MINUS(\"2019-12-03\",10,0) time(9) vQ(\"2019-12-03\",9,59) vP(\"2019-12-03\",9,0) vPUN(\"2019-12-03\",9,2) vPZ(\"2019-12-03\",9,0) vCREG_PLUS(\"2019-12-03\",9,0) vPOFF_PLUS(\"2019-12-03\",9,0) vCREG_MINUS(\"2019-12-03\",9,0) vPOFF_MINUS(\"2019-12-03\",9,0) time(8) vQ(\"2019-12-03\",8,57) vP(\"2019-12-03\",8,0) vPUN(\"2019-12-03\",8,2) vPZ(\"2019-12-03\",8,0) vCREG_PLUS(\"2019-12-03\",8,0) vPOFF_PLUS(\"2019-12-03\",8,0) vCREG_MINUS(\"2019-12-03\",8,0) vPOFF_MINUS(\"2019-12-03\",8,0) time(7) vQ(\"2019-12-03\",7,67) vP(\"2019-12-03\",7,0) vPUN(\"2019-12-03\",7,2) vPZ(\"2019-12-03\",7,0) vCREG_PLUS(\"2019-12-03\",7,0) vPOFF_PLUS(\"2019-12-03\",7,0) vCREG_MINUS(\"2019-12-03\",7,0) vPOFF_MINUS(\"2019-12-03\",7,0) time(6) vQ(\"2019-12-03\",6,61) vP(\"2019-12-03\",6,0) vPUN(\"2019-12-03\",6,2) vPZ(\"2019-12-03\",6,0) vCREG_PLUS(\"2019-12-03\",6,0) vPOFF_PLUS(\"2019-12-03\",6,0) vCREG_MINUS(\"2019-12-03\",6,0) vPOFF_MINUS(\"2019-12-03\",6,0) time(5) vQ(\"2019-12-03\",5,66) vP(\"2019-12-03\",5,0) vPUN(\"2019-12-03\",5,2) vPZ(\"2019-12-03\",5,0) vCREG_PLUS(\"2019-12-03\",5,0) vPOFF_PLUS(\"2019-12-03\",5,0) vCREG_MINUS(\"2019-12-03\",5,0) vPOFF_MINUS(\"2019-12-03\",5,0) time(4) vQ(\"2019-12-03\",4,107) vP(\"2019-12-03\",4,0) vPUN(\"2019-12-03\",4,2) vPZ(\"2019-12-03\",4,0) vCREG_PLUS(\"2019-12-03\",4,0) vPOFF_PLUS(\"2019-12-03\",4,0) vCREG_MINUS(\"2019-12-03\",4,0) vPOFF_MINUS(\"2019-12-03\",4,0) time(3) vQ(\"2019-12-03\",3,213) vP(\"2019-12-03\",3,0) vPUN(\"2019-12-03\",3,2) vPZ(\"2019-12-03\",3,0) vCREG_PLUS(\"2019-12-03\",3,0) vPOFF_PLUS(\"2019-12-03\",3,0) vCREG_MINUS(\"2019-12-03\",3,0) vPOFF_MINUS(\"2019-12-03\",3,0) time(2) vQ(\"2019-12-03\",2,84) vP(\"2019-12-03\",2,0) vPUN(\"2019-12-03\",2,2) vPZ(\"2019-12-03\",2,0) vCREG_PLUS(\"2019-12-03\",2,0) vPOFF_PLUS(\"2019-12-03\",2,0) vCREG_MINUS(\"2019-12-03\",2,0) vPOFF_MINUS(\"2019-12-03\",2,0) time(1) vQ(\"2019-12-03\",1,110) vP(\"2019-12-03\",1,0) vPUN(\"2019-12-03\",1,2) vPZ(\"2019-12-03\",1,0) vCREG_PLUS(\"2019-12-03\",1,0) vPOFF_PLUS(\"2019-12-03\",1,0) vCREG_MINUS(\"2019-12-03\",1,0) vPOFF_MINUS(\"2019-12-03\",1,0) time(0) vQ(\"2019-12-03\",0,147) vP(\"2019-12-03\",0,0) vPUN(\"2019-12-03\",0,2) vPZ(\"2019-12-03\",0,0) vCREG_PLUS(\"2019-12-03\",0,0) vPOFF_PLUS(\"2019-12-03\",0,0) vCREG_MINUS(\"2019-12-03\",0,0) vPOFF_MINUS(\"2019-12-03\",0,0) vSOC(\"2019-12-03\",0,0) vSOC_S(\"2019-12-03\", 0,0) vS_M1(\"2019-12-03\",23,14) vC_P(\"2019-12-03\",23,70) vS_P1(\"2019-12-03\",22,1) vS_M1(\"2019-12-03\",22,17) vC_P(\"2019-12-03\",22,85) vC_P(\"2019-12-03\",21,92) vS_P1(\"2019-12-03\",20,2) vS_M1(\"2019-12-03\",20,19) vC_P(\"2019-12-03\",20,95) vC_P(\"2019-12-03\",19,50) vC_P(\"2019-12-03\",18,55) vC_P(\"2019-12-03\",17,79) vC_P(\"2019-12-03\",16,74) vC_P(\"2019-12-03\",15,58) vS_M1(\"2019-12-03\",14,11) vC_P(\"2019-12-03\",14,55) vS_M1(\"2019-12-03\",13,11) vC_P(\"2019-12-03\",13,55) vC_P(\"2019-12-03\",12,81) vC_P(\"2019-12-03\",11,80) vC_P(\"2019-12-03\",10,51) vS_P1(\"2019-12-03\",9,1) vS_M1(\"2019-12-03\",9,10) vC_P(\"2019-12-03\",9,50) vC_P(\"2019-12-03\",8,57) vC_P(\"2019-12-03\",7,67) vC_P(\"2019-12-03\",6,61) vS_M1(\"2019-12-03\",5,11) vC_P(\"2019-12-03\",5,55) vS_P1(\"2019-12-03\",4,1) vS_M1(\"2019-12-03\",4,18) vC_P(\"2019-12-03\",4,90) vS_P1(\"2019-12-03\",3,3) vS_M1(\"2019-12-03\",3,36) vC_P(\"2019-12-03\",3,180) vS_M1(\"2019-12-03\",2,14) vC_P(\"2019-12-03\",2,70) vC_P(\"2019-12-03\",1,110) vS_P1(\"2019-12-03\",0,3) vS_M1(\"2019-12-03\",0,25) vC_P(\"2019-12-03\",0,125) vOVER_I(\"2019-12-03\",23,0) vOVER_I(\"2019-12-03\",22,0) vOVER_I(\"2019-12-03\",21,0) vOVER_I(\"2019-12-03\",20,0) vOVER_I(\"2019-12-03\",19,0) vOVER_I(\"2019-12-03\",18,0) vOVER_I(\"2019-12-03\",17,0) vOVER_I(\"2019-12-03\",16,0) vOVER_I(\"2019-12-03\",15,0) vOVER_I(\"2019-12-03\",14,0) vOVER_I(\"2019-12-03\",13,0) vOVER_I(\"2019-12-03\",12,0) vOVER_I(\"2019-12-03\",11,0) vOVER_I(\"2019-12-03\",10,0) vOVER_I(\"2019-12-03\",9,0) vOVER_I(\"2019-12-03\",8,0) vOVER_I(\"2019-12-03\",7,0) vOVER_I(\"2019-12-03\",6,0) vOVER_I(\"2019-12-03\",5,0) vOVER_I(\"2019-12-03\",4,0) vOVER_I(\"2019-12-03\",3,0) vOVER_I(\"2019-12-03\",2,0) vOVER_I(\"2019-12-03\",1,0) vOVER_I(\"2019-12-03\",0,0) vUNDER_I(\"2019-12-03\",23,84) vUNDER_I(\"2019-12-03\",22,101) vUNDER_I(\"2019-12-03\",21,92) vUNDER_I(\"2019-12-03\",20,112) vUNDER_I(\"2019-12-03\",19,50) vUNDER_I(\"2019-12-03\",18,55) vUNDER_I(\"2019-12-03\",17,79) vUNDER_I(\"2019-12-03\",16,74) vUNDER_I(\"2019-12-03\",15,58) vUNDER_I(\"2019-12-03\",14,66) vUNDER_I(\"2019-12-03\",13,66) vUNDER_I(\"2019-12-03\",12,81) vUNDER_I(\"2019-12-03\",11,80) vUNDER_I(\"2019-12-03\",10,51) vUNDER_I(\"2019-12-03\",9,59) vUNDER_I(\"2019-12-03\",8,57) vUNDER_I(\"2019-12-03\",7,67) vUNDER_I(\"2019-12-03\",6,61) vUNDER_I(\"2019-12-03\",5,66) vUNDER_I(\"2019-12-03\",4,107) vUNDER_I(\"2019-12-03\",3,213) vUNDER_I(\"2019-12-03\",2,84) vUNDER_I(\"2019-12-03\",1,110) vUNDER_I(\"2019-12-03\",0,147) vC_M(\"2019-12-03\",23,0) vC_M(\"2019-12-03\",22,0) vC_M(\"2019-12-03\",21,0) vC_M(\"2019-12-03\",20,0) vC_M(\"2019-12-03\",19,0) vC_M(\"2019-12-03\",18,0) vC_M(\"2019-12-03\",17,0) vC_M(\"2019-12-03\",16,0) vC_M(\"2019-12-03\",15,0) vC_M(\"2019-12-03\",14,0) vC_M(\"2019-12-03\",13,0) vC_M(\"2019-12-03\",12,0) vC_M(\"2019-12-03\",11,0) vC_M(\"2019-12-03\",10,0) vC_M(\"2019-12-03\",9,0) vC_M(\"2019-12-03\",8,0) vC_M(\"2019-12-03\",7,0) vC_M(\"2019-12-03\",6,0) vC_M(\"2019-12-03\",5,0) vC_M(\"2019-12-03\",4,0) vC_M(\"2019-12-03\",3,0) vC_M(\"2019-12-03\",2,0) vC_M(\"2019-12-03\",1,0) vC_M(\"2019-12-03\",0,0) vE_P1(\"2019-12-03\",23,0) vE_P1(\"2019-12-03\",22,0) vE_P1(\"2019-12-03\",21,0) vE_P1(\"2019-12-03\",20,0) vE_P1(\"2019-12-03\",19,0) vE_P1(\"2019-12-03\",18,0) vE_P1(\"2019-12-03\",17,0) vE_P1(\"2019-12-03\",16,0) vE_P1(\"2019-12-03\",15,0) vE_P1(\"2019-12-03\",14,0) vE_P1(\"2019-12-03\",13,0) vE_P1(\"2019-12-03\",12,0) vE_P1(\"2019-12-03\",11,0) vE_P1(\"2019-12-03\",10,0) vE_P1(\"2019-12-03\",9,0) vE_P1(\"2019-12-03\",8,0) vE_P1(\"2019-12-03\",7,0) vE_P1(\"2019-12-03\",6,0) vE_P1(\"2019-12-03\",5,0) vE_P1(\"2019-12-03\",4,0) vE_P1(\"2019-12-03\",3,0) vE_P1(\"2019-12-03\",2,0) vE_P1(\"2019-12-03\",1,0) vE_P1(\"2019-12-03\",0,0) vE_M1(\"2019-12-03\",23,0) vE_M1(\"2019-12-03\",22,0) vE_M1(\"2019-12-03\",21,0) vE_M1(\"2019-12-03\",20,0) vE_M1(\"2019-12-03\",19,0) vE_M1(\"2019-12-03\",18,0) vE_M1(\"2019-12-03\",17,0) vE_M1(\"2019-12-03\",16,0) vE_M1(\"2019-12-03\",15,0) vE_M1(\"2019-12-03\",14,0) vE_M1(\"2019-12-03\",13,0) vE_M1(\"2019-12-03\",12,0) vE_M1(\"2019-12-03\",11,0) vE_M1(\"2019-12-03\",10,0) vE_M1(\"2019-12-03\",9,0) vE_M1(\"2019-12-03\",8,0) vE_M1(\"2019-12-03\",7,0) vE_M1(\"2019-12-03\",6,0) vE_M1(\"2019-12-03\",5,0) vE_M1(\"2019-12-03\",4,0) vE_M1(\"2019-12-03\",3,0) vE_M1(\"2019-12-03\",2,0) vE_M1(\"2019-12-03\",1,0) vE_M1(\"2019-12-03\",0,0) vS_P1(\"2019-12-03\",23,0) vS_P1(\"2019-12-03\",21,0) vS_P1(\"2019-12-03\",19,0) vS_P1(\"2019-12-03\",18,0) vS_P1(\"2019-12-03\",17,0) vS_P1(\"2019-12-03\",16,0) vS_P1(\"2019-12-03\",15,0) vS_P1(\"2019-12-03\",14,0) vS_P1(\"2019-12-03\",13,0) vS_P1(\"2019-12-03\",12,0) vS_P1(\"2019-12-03\",11,0) vS_P1(\"2019-12-03\",10,0) vS_P1(\"2019-12-03\",8,0) vS_P1(\"2019-12-03\",7,0) vS_P1(\"2019-12-03\",6,0) vS_P1(\"2019-12-03\",5,0) vS_P1(\"2019-12-03\",2,0) vS_P1(\"2019-12-03\",1,0) vS_M1(\"2019-12-03\",21,0) vS_M1(\"2019-12-03\",19,0) vS_M1(\"2019-12-03\",18,0) vS_M1(\"2019-12-03\",17,0) vS_M1(\"2019-12-03\",16,0) vS_M1(\"2019-12-03\",15,0) vS_M1(\"2019-12-03\",12,0) vS_M1(\"2019-12-03\",11,0) vS_M1(\"2019-12-03\",10,0) vS_M1(\"2019-12-03\",8,0) vS_M1(\"2019-12-03\",7,0) vS_M1(\"2019-12-03\",6,0) vS_M1(\"2019-12-03\",1,0)"

    # vOVER_I(\"2019-12-03\",23,0)
    pattern_vOVER_I = r'vOVER_I\((.*?)\)'  # Adatta se il formato cambia
    matches_vOVER_I = re.findall(pattern_vOVER_I, result)
    vOVER_I_results = []
    for match in matches_vOVER_I:
        # Suddividere il contenuto in massimo 3 parti
        valori = match.split(",")  # Cambia il delimitatore se necessario
        valori = [v.strip() for v in valori]  # Rimuove spazi extra

        # Riempire con stringhe vuote se ci sono meno di 3 valori
        #while len(valori) < 3:
        #    valori.append("")

        # Creare un oggetto VP_PV con i valori estratti
        vOVER_I_results.append({"date": valori[0].replace("\"", ""), "time": valori[1].replace("\"", ""), "value": float(valori[2])})
    vOVER_I_results = sorted(vOVER_I_results, key=lambda k: (k["date"], datetime.strptime((k["time"] + ":00").replace("24:0", "23:59"), "%H:%M")))

    # vUNDER_I(\"2019-12-03\",23,84)
    pattern_vUNDER_I = r'vUNDER_I\((.*?)\)'  # Adatta se il formato cambia
    matches_vUNDER_I = re.findall(pattern_vUNDER_I, result)
    vUNDER_I_results = []
    for match in matches_vUNDER_I:
        # Suddividere il contenuto in massimo 3 parti
        valori = match.split(",")  # Cambia il delimitatore se necessario
        valori = [v.strip() for v in valori]  # Rimuove spazi extra

        # Riempire con stringhe vuote se ci sono meno di 3 valori
        # while len(valori) < 3:
        #    valori.append("")

        # Creare un oggetto VP_PV con i valori estratti
        vUNDER_I_results.append({"date": valori[0].replace("\"", ""), "time": valori[1].replace("\"", ""), "value": float(valori[2])})
    vUNDER_I_results = sorted(vUNDER_I_results,
                             key=lambda k: (k["date"], datetime.strptime((k["time"] + ":00").replace("24:0", "23:59"), "%H:%M")))

    pattern_vC_P = r'vC_P\((.*?)\)'  # Adatta se il formato cambia
    matches_vC_P = re.findall(pattern_vC_P, result)
    vC_P_results = []
    for match in matches_vC_P:
        # Suddividere il contenuto in massimo 3 parti
        valori = match.split(",")  # Cambia il delimitatore se necessario
        valori = [v.strip() for v in valori]  # Rimuove spazi extra

        # Riempire con stringhe vuote se ci sono meno di 3 valori
        # while len(valori) < 3:
        #    valori.append("")
        vC_P_results.append({"date": valori[0].replace("\"", ""), "time": valori[1].replace("\"", ""), "value": float(valori[2])})
    vC_P_results = sorted(vC_P_results,
                              key=lambda k: (k["date"], datetime.strptime((k["time"] + ":00").replace("24:0", "23:59"), "%H:%M")))

    pattern_vC_M = r'vC_M\((.*?)\)'  # Adatta se il formato cambia
    matches_vC_M = re.findall(pattern_vC_M, result)
    vC_M_results = []
    for match in matches_vC_M:
        # Suddividere il contenuto in massimo 3 parti
        valori = match.split(",")  # Cambia il delimitatore se necessario
        valori = [v.strip() for v in valori]  # Rimuove spazi extra

        # Riempire con stringhe vuote se ci sono meno di 3 valori
        # while len(valori) < 3:
        #    valori.append("")
        vC_M_results.append({"date": valori[0].replace("\"", ""), "time": valori[1].replace("\"", ""), "value": float(valori[2])})
    vC_M_results = sorted(vC_M_results,
                          key=lambda k: (k["date"], datetime.strptime((k["time"] + ":00").replace("24:0", "23:59"), "%H:%M")))

    # To be calculated iteratively
    # vE_P1(\"2019-12-03\",23,14)
    # vE_M1(\"2019-12-03\",23,14)
    # vSOC_S(0, 0)
    # vSOC_Si+1 = vSOC_i + E_P_i - E_M_i
    pattern_vSOC_S0 = r'vSOC_S\((.*?)\)'  # Adatta se il formato cambia
    matches_vSOC_S0 = re.findall(pattern_vSOC_S0, result)
    vSOC_S_results = []
    currentSOCSValue = 0
    for match in matches_vSOC_S0:
        # Suddividere il contenuto in massimo 3 parti
        valori = match.split(",")  # Cambia il delimitatore se necessario
        valori = [v.strip() for v in valori]  # Rimuove spazi extra

        # Riempire con stringhe vuote se ci sono meno di 3 valori
        #while len(valori) < 3:
        #    valori.append("")
        vSOC_S_results.append({"date": valori[0].replace("\"", ""), "time": valori[1].replace("\"", ""), "value": float(valori[2])})
        currentSOCSValue = valori[2]
    vSOC_S_results = sorted(vSOC_S_results,
                          key=lambda k: (k["date"], datetime.strptime((k["time"] + ":00").replace("24:0", "23:59"), "%H:%M")))

    pattern_vE_P1 = r'vE_P1\((.*?)\)'  # Adatta se il formato cambia
    matches_vE_P1 = re.findall(pattern_vE_P1, result)
    vE_P1_results = []
    for match in matches_vE_P1:
        # Suddividere il contenuto in massimo 3 parti
        valori = match.split(",")  # Cambia il delimitatore se necessario
        valori = [v.strip() for v in valori]  # Rimuove spazi extra

        # Riempire con stringhe vuote se ci sono meno di 3 valori
        # while len(valori) < 3:
        #    valori.append("")
        vE_P1_results.append({"date": valori[0].replace("\"", ""), "time": valori[1].replace("\"", ""), "value": float(valori[2])})
    vE_P1_results = sorted(vE_P1_results,
                            key=lambda k: (k["date"], datetime.strptime((k["time"] + ":00").replace("24:0", "23:59"), "%H:%M")))

    pattern_vE_M1 = r'vE_M1\((.*?)\)'  # Adatta se il formato cambia
    matches_vE_M1 = re.findall(pattern_vE_M1, result)
    vE_M1_results = []
    for match in matches_vE_M1:
        # Suddividere il contenuto in massimo 3 parti
        valori = match.split(",")  # Cambia il delimitatore se necessario
        valori = [v.strip() for v in valori]  # Rimuove spazi extra

        # Riempire con stringhe vuote se ci sono meno di 3 valori
        # while len(valori) < 3:
        #    valori.append("")
        vE_M1_results.append({"date": valori[0].replace("\"", ""), "time": valori[1].replace("\"", ""), "value": float(valori[2])})
    vE_M1_results = sorted(vE_M1_results,
                           key=lambda k: (k["date"], datetime.strptime((k["time"] + ":00").replace("24:0", "23:59"), "%H:%M")))

    # for vvS_P1 in vS_P1_results:
    for vvE_P1 in vE_P1_results:
        #vvE_P1 = [v for v in vE_P1_results if v["time"] == i][0]
        vE_M1_value = [v for v in vE_M1_results if v["date"] == vvE_P1["date"] and v["time"] == vvE_P1["time"]][0]["value"]
        vSOC_S_results.append({"date": vvE_P1["date"], "time": vvE_P1["time"], "value": currentSOCSValue})
        currentSOCSValue = int(currentSOCSValue) + int(vvE_P1["value"]) - int(vE_M1_value)



    # To be calculated iteratively
    # vS_P1(\"2019-12-03\",23,14)
    # vS_M1(\"2019-12-03\",23,14)
    # vSOC(0, 0)
    # vSOC_i+1 = vSOC_i + S_P_i - S_M_iù
    pattern_vSOC_0 = r'vSOC\((.*?)\)'  # Adatta se il formato cambia
    matches_vSOC_0 = re.findall(pattern_vSOC_0, result)
    vSOC_results = []
    currentSOCValue = 0
    for match in matches_vSOC_0:
        # Suddividere il contenuto in massimo 3 parti
        valori = match.split(",")  # Cambia il delimitatore se necessario
        valori = [v.strip() for v in valori]  # Rimuove spazi extra

        # Riempire con stringhe vuote se ci sono meno di 3 valori
        # while len(valori) < 3:
        #    valori.append("")
        vSOC_results.append({"date": valori[0].replace("\"", ""), "time": valori[1].replace("\"", ""), "value": int(valori[2])})
        currentSOCValue = valori[2]

    pattern_vS_P1 = r'vS_P1\((.*?)\)'  # Adatta se il formato cambia
    matches_vS_P1 = re.findall(pattern_vS_P1, result)
    vS_P1_results = []
    for match in matches_vS_P1:
        # Suddividere il contenuto in massimo 3 parti
        valori = match.split(",")  # Cambia il delimitatore se necessario
        valori = [v.strip() for v in valori]  # Rimuove spazi extra

        # Riempire con stringhe vuote se ci sono meno di 3 valori
        # while len(valori) < 3:
        #    valori.append("")
        vS_P1_results.append({"date": valori[0].replace("\"", ""), "time": valori[1].replace("\"", ""), "value": int(valori[2])})
    vS_P1_results = sorted(vS_P1_results,
                           key=lambda k: (
                           k["date"], datetime.strptime((k["time"] + ":00").replace("24:0", "23:59"), "%H:%M")))

    pattern_vS_M1 = r'vS_M1\((.*?)\)'  # Adatta se il formato cambia
    matches_vS_M1 = re.findall(pattern_vS_M1, result)
    vS_M1_results = []
    for match in matches_vS_M1:
        # Suddividere il contenuto in massimo 3 parti
        valori = match.split(",")  # Cambia il delimitatore se necessario
        valori = [v.strip() for v in valori]  # Rimuove spazi extra

        # Riempire con stringhe vuote se ci sono meno di 3 valori
        # while len(valori) < 3:
        #    valori.append("")
        vS_M1_results.append({"date": valori[0].replace("\"", ""), "time": valori[1].replace("\"", ""), "value": int(valori[2])})
    vS_M1_results = sorted(vS_M1_results,
                           key=lambda k: (
                               k["date"], datetime.strptime((k["time"] + ":00").replace("24:0", "23:59"), "%H:%M")))

    for vvS_P1 in vS_P1_results:
    #for i in range(24):
        #vvS_P1 = [v for v in vS_P1_results if v["time"] == i][0]
        vS_M1_value = [v for v in vS_M1_results if v["date"] == vvS_P1["date"] and v["time"] == vvS_P1["time"]][0][
            "value"]
        vSOC_results.append({"date": vvS_P1["date"], "time": vvS_P1["time"], "value": currentSOCValue})
        currentSOCValue = int(currentSOCValue) + int(vvS_P1["value"]) - int(vS_M1_value)



    #object_result = {"OVER": vOVER_I_results, "UNDER": vUNDER_I_results, "SOC": vSOC_results, "SP_1": vS_P1_results, "SM_1": vS_M1_results}
    object_result = {"OVER": vOVER_I_results, "UNDER": vUNDER_I_results, "C_P": vC_P_results, "C_M": vC_M_results, "SOC": vSOC_results, "SOC_S": vSOC_S_results}
    return object_result

# SIMPLIFIED PHASE
def generate_execution_id():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    short_uuid = uuid.uuid4().hex[:8]
    return f"{timestamp}_{short_uuid}"


def recommend(building, date, time, init_charge_percentage, production_current, consumption_current,
                                                       discharge, charge, production, consumption, feed_in, from_grid, unit = "kWh"):

    buildingName = building.replace(" ", "_")

    config = configparser.ConfigParser()
    config.read('asp_encodings/simplified/params_per_building/param_files.properties')
    if buildingName not in config['default']:
        return {"ERROR": f"Building '{building}' not found."}
    print("Building: " + config["default"][buildingName])
    max_charge_paramFileName = "max_charge_" + config["default"][buildingName]
    paramFileName = config["default"][buildingName]

    with tempfile.NamedTemporaryFile(mode='w+t', delete=False) as tmp:
        factsFile = tmp.name
        tmp.write(f"vE_SinitPercentage({init_charge_percentage * 100:.00f}).\n")
        tmp.write(f"vE_Sinit(X):- X = P * M / 10000, maxChargeKWh(M), vE_SinitPercentage(P).\n")
        tmp.write(f"date(\"{date}\").\n")
        tmp.write(f"timeTarget(\"{time}:00\").\n")
        season = ["winter", "spring", "summer", "autumu"][(int(date.split("-")[1]) % 12) // 3]
        print(season)
        tmp.write(f"season({season}).\n")
        counterTime = 1
        for prod in production:
            # print(prod)
            time_value = prod['time']
            prod_value = prod['value']
            cons_value = next((item['value'] for item in consumption if item['time'] == time_value), None)
            discharge_value = next((item['value'] for item in discharge if item['time'] == time_value), None)
            charge_value = next((item['value'] for item in charge if item['time'] == time_value), None)
            feed_in_value = next((item['value'] for item in feed_in if item['time'] == time_value), None)
            from_grid_value = next((item['value'] for item in from_grid if item['time'] == time_value), None)
            tmp.write(f"time({counterTime}, \"{time_value}:00\").\n")
            tmp.write(f"vP_PV(\"{date}\",\"{time_value}:00\",{prod_value * 100:.00f}).\n")
            tmp.write(f"vP_L(\"{date}\",\"{time_value}:00\",{cons_value * 100:.00f}).\n")
            tmp.write(f"vDischarge(\"{date}\",\"{time_value}:00\",{discharge_value * 100:.00f}).\n")
            tmp.write(f"vCharge(\"{date}\",\"{time_value}:00\",{charge_value * 100:.00f}).\n")
            tmp.write(f"vFeed_in(\"{date}\",\"{time_value}:00\",{feed_in_value * 100:.00f}).\n")
            tmp.write(f"vFrom_grid(\"{date}\",\"{time_value}:00\",{from_grid_value * 100:.00f}).\n")
            counterTime += 1
        tmp.write(f"time({counterTime}, \"{time}:00\").\n")
        tmp.write(f"vP_PV(\"{date}\",\"{time}:00\",{production_current * 100:.00f}).\n")
        tmp.write(f"vP_L(\"{date}\",\"{time}:00\",{consumption_current * 100:.00f}).\n")

    command = ["clingo", ASP_RECOMMENDATION_PATH, factsFile, ASP_PARAMS_PATH + max_charge_paramFileName, ASP_PARAMS_PATH + paramFileName, "--quiet=1", "--outf=1"]
    print(*command)

    result = subprocess.run(command, capture_output=True, text=True)

    print(result.stdout)
    results = []
    results.append(recommendation_results_parse(result.stdout))

    #moreProgram = result.stdout
    #moreProgram = moreProgram.replace("ANSWER", "%ANSWER")
    #prod = [{"time": "23:59", "value": production_current}]
    #cons = [{"time": "23:59", "value": consumption_current}]
    #res = calculate_best_grid_transfer(building, date, None,
     #                            unit, prod, cons, None, isSchedule=False, more_program=moreProgram)
    #results.append("{discharge: " + res)

    #if not res:
    #    return {"date": date, "best_discharge": 0}
    return {"date": date, "time": time, "recommendation": results}


def calculate_best_grid_transfer(building, date, init_charge_percentage, unit, production, consumption, time_limit, isSchedule = False,
                                 more_program = None):

    if time_limit is None:
        time_limit = 100000
    buildingName = building.replace(" ", "_")
    paramFileName = None

    config = configparser.ConfigParser()
    config.read('asp_encodings/simplified/params_per_building/param_files.properties')
    if buildingName not in config['default']:
        return {"ERROR": f"Building '{building}' not found."}
    print("Building: " + config["default"][buildingName])
    paramFileName = config["default"][buildingName]


    with tempfile.NamedTemporaryFile(mode='w+t', delete=False) as tmp:
        print(tmp.name)
        factsFile = tmp.name
        if init_charge_percentage is not None:
            tmp.write(f"vE_SinitPercentage({init_charge_percentage * 100:.00f}).\n")
        if unit == "kWh":
            counterTime = 1
            print(production)
            for prod in production:
                time_value = prod['time']
                prod_value = prod['value']
                cons_value = next((item['value'] for item in consumption if item['time'] == time_value), None)
                tmp.write(f"time({counterTime}, \"{time_value}:00\").\n")
                tmp.write(f"vP_PV(\"{date}\",\"{time_value}:00\",{prod_value * 100:.00f}).\n")
                tmp.write(f"vP_L(\"{date}\",\"{time_value}:00\",{cons_value * 100:.00f}).\n")
                counterTime += 1
        if more_program is not None:
            tmp.write(more_program)

    #command = ["clingo", ASP_PROGRAM_PATH, factsFile, ASP_PARAMS_PATH, ASP_MAXCHARGE_PATH, "--quiet=1", "--outf=1",
    #           f"--time-limit={time_limit}"]
    command = ["clingo", ASP_PROGRAM_PATH, factsFile, ASP_PARAMS_PATH + paramFileName,
               ASP_PARAMS_PATH + "max_charge_" + paramFileName, "--quiet=1", "--outf=1",
               f"--time-limit={time_limit}"]
    print(*command)
    if not isSchedule:
        response = subprocess.run(command, capture_output=True, text=True)
        print(response.stdout)
        return asp_to_json(response.stdout)
    else:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        execution_id = generate_execution_id()
        scheduledExecIds.append(execution_id)
        results_filename = f"serviceOutput/solver_output_{execution_id}.txt"
        def monitor():
            stdout, stderr = process.communicate()
            with open(results_filename, "w+") as f:
                if stderr:
                    print("Errori:", stderr)
                    f.write(stderr)
                f.write(stdout)
                print("Risultato:", stdout)
            print(f"Esecuzione con id {execution_id} terminata.")


        # Avvia monitoraggio in background
        threading.Thread(target=monitor, daemon=True).start()
        return {"execution_id": execution_id}

def get_results_from_id(execution_id):
    results_filename = f"serviceOutput/solver_output_{execution_id}.txt"
    file = Path(results_filename)
    if file.exists():
        with open(results_filename, "r") as f:
            return asp_to_json(f.read())
    else:
        if execution_id in scheduledExecIds:
            return {"status": "RUNNING"}
        else:
            return {"status": "NOT_SCHEDULED"}





def recommendation_results_parse(result):
    pattern_recommend = r'recommend\((.*?)\)'  # Adatta se il formato cambia
    matches_recommend = re.findall(pattern_recommend, result)
    results = []
    for match in matches_recommend:
        # Suddividere il contenuto in massimo 3 parti
        valori = match.split(",")  # Cambia il delimitatore se necessario
        valori = [v.strip() for v in valori]  # Rimuove spazi extra

        results.append(valori[2].replace("\"", ""))

    return results

def best_grid_transfer_results_parse(result, unit="W", decimal_digits=2, clingcon = False):
    #result = "{vP_L(1,1,0), vP_L(1,2,0), vP_L(1,3,0), vP_L(1,4,0), vP_L(1,5,0), vP_L(1,6,0), vP_L(1,7,0), vP_L(1,8,0), vP_L(1,9,0), vP_L(1,10,0), vP_L(1,11,0), vP_L(1,12,0), vP_L(1,13,0), vP_L(1,14,0), vP_L(1,15,0), vP_L(1,16,0), vP_L(1,17,0), vP_L(1,18,0), vP_L(1,19,0), vP_L(1,20,0), vP_L(1,21,0), vP_L(1,22,0), vP_L(1,23,0), vP_S(1,1,999), vP_S(1,2,999), vP_S(1,3,999), vP_S(1,4,999), vP_S(1,5,999), vP_S(1,6,999), vP_S(1,7,999), vP_S(1,8,999), vP_S(1,9,999), vP_S(1,10,999), vP_S(1,11,999), vP_S(1,12,999), vP_S(1,13,999), vP_S(1,14,999), vP_S(1,15,999), vP_S(1,16,999), vP_S(1,17,999), vP_S(1,18,999), vP_S(1,19,999), vP_S(1,20,999), vP_S(1,21,999), vP_S(1,22,999), vP_S(1,23,999), vP_PV(1,1,998), vP_PV(1,2,998), vP_PV(1,3,998), vP_PV(1,4,998), vP_PV(1,5,998), vP_PV(1,6,998), vP_PV(1,7,998), vP_PV(1,8,998), vP_PV(1,9,998), vP_PV(1,10,998), vP_PV(1,11,998), vP_PV(1,12,998), vP_PV(1,13,998), vP_PV(1,14,998), vP_PV(1,15,998), vP_PV(1,16,998), vP_PV(1,17,998), vP_PV(1,18,998), vP_PV(1,19,998), vP_PV(1,20,998), vP_PV(1,21,998), vP_PV(1,22,998), vP_PV(1,23,998)} COST 11442569@1"
    #print(result)

    pattern_vP_L = r'vP_L\((.*?)\)'  # Adatta se il formato cambia
    pattern_vP_PV = r'vP_PV\((.*?)\)'  # Adatta se il formato cambia
    pattern_vP_S = r'vP_S\((.*?)\)'  # Adatta se il formato cambia
    pattern_charge = r'vCharge\((.*?)\)'  # Adatta se il formato cambia
    pattern_discharge = r'vDischarge\((.*?)\)'  # Adatta se il formato cambia
    pattern_feed_in = r'vFeed_in\((.*?)\)'  # Adatta se il formato cambia
    pattern_from_grid = r'vFrom_grid\((.*?)\)'  # Adatta se il formato cambia
    
    matches_vP_L = re.findall(pattern_vP_L, result)
    matches_vP_PV = re.findall(pattern_vP_PV, result)
    matches_vP_S = re.findall(pattern_vP_S, result)
    matches_charge = re.findall(pattern_charge, result)
    matches_discharge = re.findall(pattern_discharge, result)
    matches_feed_in = re.findall(pattern_feed_in, result)
    matches_from_grid = re.findall(pattern_from_grid, result)

    vP_L_results = []
    decimalDigitDivide = 1
    for i in range(0, decimal_digits):
        decimalDigitDivide *=10

    for match in matches_vP_L:
        # Suddividere il contenuto in massimo 3 parti
        valori = match.split(",")  # Cambia il delimitatore se necessario
        valori = [v.strip() for v in valori]  # Rimuove spazi extra

        # Riempire con stringhe vuote se ci sono meno di 3 valori
        #while len(valori) < 3:
        #    valori.append("")

        # Creare un oggetto VP_PV con i valori estratti
        vP_L_results.append({"day" : valori[0].replace("\"", ""), "time" : valori[1].replace("\"", ""), "value" : float(valori[2].replace("\"", ""))/ decimalDigitDivide})
    vP_L_results = sorted(vP_L_results, key=lambda k: (k["day"], datetime.strptime(k["time"].replace("24:00:00", "23:59:59"), "%H:%M:%S")))

    vP_PV_results = []
    for match in matches_vP_PV:
        # Suddividere il contenuto in massimo 3 parti
        valori = match.split(",")  # Cambia il delimitatore se necessario
        valori = [v.strip() for v in valori]  # Rimuove spazi extra

        # Riempire con stringhe vuote se ci sono meno di 3 valori
        while len(valori) < 3:
            valori.append("")

        # Creare un oggetto VP_PV con i valori estratti
        vP_PV_results.append({"day": valori[0].replace("\"", ""), "time": valori[1].replace("\"", ""), "value": float(valori[2].replace("\"", ""))/ decimalDigitDivide})
    vP_PV_results = sorted(vP_PV_results, key=lambda k: (k["day"], datetime.strptime(k["time"].replace("24:00:00", "23:59:59"), "%H:%M:%S")))

    charge_results = []
    discharge_results = []
    feed_in_results = []
    from_grid_results = []

    if clingcon:
        for match in matches_vP_S:
            # Suddividere il contenuto in massimo 3 parti
            valori = match.split(",")  # Cambia il delimitatore se necessario
            valori = [v.strip() for v in valori]  # Rimuove spazi extra

            # Riempire con stringhe vuote se ci sono meno di 3 valori
            while len(valori) < 3:
                valori.append("")
            date = valori[0].replace('"', '')
            time = valori[1].replace('"', '')
            value = float(valori[2].replace('"', ''))
            if value >= 0:
                charge_results.append({"day": date, "time": time, "value": float(value) / decimalDigitDivide})
                discharge_results.append({"day": date, "time": time, "value": float(0)})
            else:
                charge_results.append({"day": date, "time": time, "value": float(0)})
                discharge_results.append({"day": date, "time": time, "value": float(value) * -1 / decimalDigitDivide})

            feed_in_results.append({"day": date, "time": time, "value": float(0)})
            from_grid_results.append({"day": date, "time": time, "value": float(0)})
            # Creare un oggetto VP_PV con i valori estratti
    else:
        for match in matches_charge:
            if clingcon:
                date = match[0].replace('"', '')
                time = match[1].replace('"', '')
                value = match[2].replace('"', '')
                print(f"Data: {date}, Ora: {time}, Valore: {value}")
                charge_results.append({"day": date, "time": time, "value": float(value) / decimalDigitDivide})
            else:
                # Suddividere il contenuto in massimo 3 parti
                valori = match.split(",")  # Cambia il delimitatore se necessario
                valori = [v.strip() for v in valori]  # Rimuove spazi extra

                # Riempire con stringhe vuote se ci sono meno di 3 valori
                while len(valori) < 3:
                    valori.append("")

                charge_results.append({"day": valori[0].replace("\"", ""), "time": valori[1].replace("\"", ""), "value": float(valori[2].replace("\"", ""))/ decimalDigitDivide})

        for match in matches_discharge:
            if clingcon:
                date = match[0].replace('"', '')
                time = match[1].replace('"', '')
                value = match[2].replace('"', '')
                print(f"Data: {date}, Ora: {time}, Valore: {value}")
                discharge_results.append({"day": date, "time": time, "value": float(value) / decimalDigitDivide})
            else:
                # Suddividere il contenuto in massimo 3 parti
                valori = match.split(",")  # Cambia il delimitatore se necessario
                valori = [v.strip() for v in valori]  # Rimuove spazi extra

                # Riempire con stringhe vuote se ci sono meno di 3 valori
                while len(valori) < 3:
                    valori.append("")

                # Creare un oggetto VP_PV con i valori estratti
                discharge_results.append({"day": valori[0].replace("\"", ""), "time": valori[1].replace("\"", ""), "value": float(valori[2].replace("\"", ""))/ decimalDigitDivide})


        for match in matches_feed_in:
            if clingcon:
                date = match[0].replace('"', '')
                time = match[1].replace('"', '')
                value = match[2].replace('"', '')
                print(f"Data: {date}, Ora: {time}, Valore: {value}")
                feed_in_results.append({"day": date, "time": time, "value": float(value) / decimalDigitDivide})
            else:
                # Suddividere il contenuto in massimo 3 parti
                valori = match.split(",")  # Cambia il delimitatore se necessario
                valori = [v.strip() for v in valori]  # Rimuove spazi extra

                # Riempire con stringhe vuote se ci sono meno di 3 valori
                while len(valori) < 3:
                    valori.append("")

                # Creare un oggetto VP_PV con i valori estratti
                feed_in_results.append({"day": valori[0].replace("\"", ""), "time": valori[1].replace("\"", ""), "value": float(valori[2].replace("\"", ""))/ decimalDigitDivide})

        for match in matches_from_grid:
            if clingcon:
                date = match[0].replace('"', '')
                time = match[1].replace('"', '')
                value = match[2].replace('"', '')
                print(f"Data: {date}, Ora: {time}, Valore: {value}")
                from_grid_results.append({"day": date, "time": time, "value": float(value) / decimalDigitDivide})
            else:
                # Suddividere il contenuto in massimo 3 parti
                valori = match.split(",")  # Cambia il delimitatore se necessario
                valori = [v.strip() for v in valori]  # Rimuove spazi extra

                # Riempire con stringhe vuote se ci sono meno di 3 valori
                while len(valori) < 3:
                    valori.append("")

                # Creare un oggetto VP_PV con i valori estratti
                from_grid_results.append({"day": valori[0].replace("\"", ""), "time": valori[1].replace("\"", ""), "value": float(valori[2].replace("\"", ""))/ decimalDigitDivide})

    charge_results = sorted(charge_results, key=lambda k: (k["day"], datetime.strptime(k["time"].replace("24:00:00", "23:59:59"), "%H:%M:%S")))
    discharge_results = sorted(discharge_results, key=lambda k: (k["day"], datetime.strptime(k["time"].replace("24:00:00", "23:59:59"), "%H:%M:%S")))
    feed_in_results = sorted(feed_in_results, key=lambda k: (k["day"], datetime.strptime(k["time"].replace("24:00:00", "23:59:59"), "%H:%M:%S")))
    from_grid_results = sorted(from_grid_results, key=lambda k: (k["day"], datetime.strptime(k["time"].replace("24:00:00", "23:59:59"), "%H:%M:%S")))
    object_result = {"P_L": vP_L_results, "P_PV": vP_PV_results,  "Charge": charge_results,
                     "Discharge": discharge_results, "Feed-in" : feed_in_results, "From grid": from_grid_results}
    #print(object_result)
    return object_result

def asp_to_json(solver_results, unit="kWh"):
    if "ANSWER" not in solver_results:
        return []
    results = best_grid_transfer_results_parse(solver_results, unit)
    toReturn = OrderedDict()
    toReturn["date"] = ""
    #toReturn["unit"] = "kWh"
    toReturn["discharge"] = []
    toReturn["charge"] = []
    toReturn["production"] = []
    toReturn["consumption"] = []
    toReturn["feed_in"] = []
    toReturn["from_grid"] = []
    for cont in range(len(results["P_L"])):
        date = results["P_L"][cont]["day"].replace("\"", "")
        toReturn["date"] = date
        time = results["P_L"][cont]["time"][:-3]
        charge = float(results["Charge"][cont]["value"])
        discharge = float(results["Discharge"][cont]["value"])
        production = float(results["P_PV"][cont]["value"])
        consumption = float(results["P_L"][cont]["value"])
        feedin = float(results["Feed-in"][cont]["value"])
        fromgrid = float(results["From grid"][cont]["value"])
        toReturn["charge"].append({"time": time, "value": charge})
        toReturn["discharge"].append({"time": time, "value": discharge})
        toReturn["production"].append({"time": time, "value": production})
        toReturn["consumption"].append({"time": time, "value": consumption})
        toReturn["feed_in"].append({"time": time, "value": feedin})
        toReturn["from_grid"].append({"time": time, "value": fromgrid})


    return toReturn
