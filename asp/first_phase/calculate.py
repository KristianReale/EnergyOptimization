import subprocess
import re

DLV_PATH = "solver/DLV/macosx/dlv-2.1.2-arm64"
ASP_PROGRAM_PATH = "asp_encodings/simplified/encoding.asp"
ASP_PARAMS_PATH = "asp_encodings/simplified/params.asp"

def calculate_best_grid_transfer(esinit):
    command = [DLV_PATH, ASP_PROGRAM_PATH, ASP_PARAMS_PATH, "--silent", "--stdin"]

    # response = subprocess.run(command, capture_output=True, text=True)
    # return response.stdout

    result = "{vP_L(1,1,0), vP_L(1,2,0), vP_L(1,3,0), vP_L(1,4,0), vP_L(1,5,0), vP_L(1,6,0), vP_L(1,7,0), vP_L(1,8,0), vP_L(1,9,0), vP_L(1,10,0), vP_L(1,11,0), vP_L(1,12,0), vP_L(1,13,0), vP_L(1,14,0), vP_L(1,15,0), vP_L(1,16,0), vP_L(1,17,0), vP_L(1,18,0), vP_L(1,19,0), vP_L(1,20,0), vP_L(1,21,0), vP_L(1,22,0), vP_L(1,23,0), vP_S(1,1,999), vP_S(1,2,999), vP_S(1,3,999), vP_S(1,4,999), vP_S(1,5,999), vP_S(1,6,999), vP_S(1,7,999), vP_S(1,8,999), vP_S(1,9,999), vP_S(1,10,999), vP_S(1,11,999), vP_S(1,12,999), vP_S(1,13,999), vP_S(1,14,999), vP_S(1,15,999), vP_S(1,16,999), vP_S(1,17,999), vP_S(1,18,999), vP_S(1,19,999), vP_S(1,20,999), vP_S(1,21,999), vP_S(1,22,999), vP_S(1,23,999), vP_PV(1,1,998), vP_PV(1,2,998), vP_PV(1,3,998), vP_PV(1,4,998), vP_PV(1,5,998), vP_PV(1,6,998), vP_PV(1,7,998), vP_PV(1,8,998), vP_PV(1,9,998), vP_PV(1,10,998), vP_PV(1,11,998), vP_PV(1,12,998), vP_PV(1,13,998), vP_PV(1,14,998), vP_PV(1,15,998), vP_PV(1,16,998), vP_PV(1,17,998), vP_PV(1,18,998), vP_PV(1,19,998), vP_PV(1,20,998), vP_PV(1,21,998), vP_PV(1,22,998), vP_PV(1,23,998)} COST 11442569@1"
    vP_L = []
    vP_PV = []
    vP_S = []

    pattern_vP_L = r'vP_L\((.*?)\)'  # Adatta se il formato cambia
    pattern_vP_PV = r'vP_PV\((.*?)\)'  # Adatta se il formato cambia
    pattern_vP_S = r'vP_S\((.*?)\)'  # Adatta se il formato cambia

    matches_vP_L = re.findall(pattern_vP_L, result)
    matches_vP_PV = re.findall(pattern_vP_PV, result)
    matches_vP_S = re.findall(pattern_vP_S, result)

    vP_L_results = []
    for match in matches_vP_L:
        # Suddividere il contenuto in massimo 3 parti
        valori = match.split(",")  # Cambia il delimitatore se necessario
        valori = [v.strip() for v in valori]  # Rimuove spazi extra

        # Riempire con stringhe vuote se ci sono meno di 3 valori
        while len(valori) < 3:
            valori.append("")

        # Creare un oggetto VP_PV con i valori estratti
        vP_L_results.append({"day" : valori[0], "time" : valori[1], "value" : valori[2]})

    vP_PV_results = []
    for match in matches_vP_PV:
        # Suddividere il contenuto in massimo 3 parti
        valori = match.split(",")  # Cambia il delimitatore se necessario
        valori = [v.strip() for v in valori]  # Rimuove spazi extra

        # Riempire con stringhe vuote se ci sono meno di 3 valori
        while len(valori) < 3:
            valori.append("")

        # Creare un oggetto VP_PV con i valori estratti
        vP_PV_results.append({"day": valori[0], "time": valori[1], "value": valori[2]})

    vP_S_results = []
    for match in matches_vP_S:
        # Suddividere il contenuto in massimo 3 parti
        valori = match.split(",")  # Cambia il delimitatore se necessario
        valori = [v.strip() for v in valori]  # Rimuove spazi extra

        # Riempire con stringhe vuote se ci sono meno di 3 valori
        while len(valori) < 3:
            valori.append("")

        # Creare un oggetto VP_PV con i valori estratti
        vP_S_results.append({"day": valori[0], "time": valori[1], "value": valori[2]})
    object_result = {"P_L": vP_L_results, "P_PV": vP_PV_results, "P_S": vP_S_results}
    return object_result
