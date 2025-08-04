import json

from flask import Flask, jsonify, request
from flask_restx import Api, Resource
from pydantic import BaseModel

from asp.solve import *

app = Flask(__name__)
api = Api(app, version='1.0', title='My API', description='A simple demo API')
ns = api.namespace("", "api")


from dataclasses import dataclass, field


@dataclass
class TimeValue:
    time: str = "00:00"
    value: float = 0.0

@dataclass
class Results(BaseModel):
    date: str = "2020-01-01"
    unit: str = "kWh"
    discharge: list[TimeValue] = field(default_factory=list)
    charge: list[TimeValue] = field(default_factory=list)
    production: list[TimeValue] = field(default_factory=list)
    consumption: list[TimeValue] = field(default_factory=list)
    feed_in: list[TimeValue] = field(default_factory=list)
    from_grid: list[TimeValue] = field(default_factory=list)


'''@app.route('/best_energy_storage_python', methods=['POST'])
def best_energy_storage_python():
    data = request.get_json()

    P = data["P"]
    Q = data["Q"]
    PUN = data["PREZZO_ACQUISTO_ENERGIA"]
    PZ = data["PREZZO_VENDITA_ENERGIA"]
    CREG_PLUS = data["CREG_PLUS"]
    POFF_PLUS = data["POFF_PLUS"]
    CREG_MINUS = data["CREG_MINUS"]
    POFF_MINUS = data["POFF_MINUS"]



@app.route('/best_energy_storage', methods=['POST'])
def best_energy_storage_asp():
    data = request.get_json()
    method = request.args.get('method', default="asp", type=str)
    isStored = request.args.get('stored', default=False, type=bool)
    if method == 'asp':
        if isStored:
            return jsonify(best_storage_results_parse("time(23) date(\"2019-12-03\") vQ(\"2019-12-03\",23,84) vP(\"2019-12-03\",23,0) vPUN(\"2019-12-03\",23,2) vPZ(\"2019-12-03\",23,0) vCREG_PLUS(\"2019-12-03\",23,0) vPOFF_PLUS(\"2019-12-03\",23,0) vCREG_MINUS(\"2019-12-03\",23,0) vPOFF_MINUS(\"2019-12-03\",23,0) time(22) vQ(\"2019-12-03\",22,101) vP(\"2019-12-03\",22,0) vPUN(\"2019-12-03\",22,2) vPZ(\"2019-12-03\",22,0) vCREG_PLUS(\"2019-12-03\",22,0) vPOFF_PLUS(\"2019-12-03\",22,0) vCREG_MINUS(\"2019-12-03\",22,0) vPOFF_MINUS(\"2019-12-03\",22,0) time(21) vQ(\"2019-12-03\",21,92) vP(\"2019-12-03\",21,0) vPUN(\"2019-12-03\",21,2) vPZ(\"2019-12-03\",21,0) vCREG_PLUS(\"2019-12-03\",21,0) vPOFF_PLUS(\"2019-12-03\",21,0) vCREG_MINUS(\"2019-12-03\",21,0) vPOFF_MINUS(\"2019-12-03\",21,0) time(20) vQ(\"2019-12-03\",20,112) vP(\"2019-12-03\",20,0) vPUN(\"2019-12-03\",20,2) vPZ(\"2019-12-03\",20,0) vCREG_PLUS(\"2019-12-03\",20,0) vPOFF_PLUS(\"2019-12-03\",20,0) vCREG_MINUS(\"2019-12-03\",20,0) vPOFF_MINUS(\"2019-12-03\",20,0) time(19) vQ(\"2019-12-03\",19,50) vP(\"2019-12-03\",19,0) vPUN(\"2019-12-03\",19,2) vPZ(\"2019-12-03\",19,0) vCREG_PLUS(\"2019-12-03\",19,0) vPOFF_PLUS(\"2019-12-03\",19,0) vCREG_MINUS(\"2019-12-03\",19,0) vPOFF_MINUS(\"2019-12-03\",19,0) time(18) vQ(\"2019-12-03\",18,55) vP(\"2019-12-03\",18,0) vPUN(\"2019-12-03\",18,2) vPZ(\"2019-12-03\",18,0) vCREG_PLUS(\"2019-12-03\",18,0) vPOFF_PLUS(\"2019-12-03\",18,0) vCREG_MINUS(\"2019-12-03\",18,0) vPOFF_MINUS(\"2019-12-03\",18,0) time(17) vQ(\"2019-12-03\",17,79) vP(\"2019-12-03\",17,0) vPUN(\"2019-12-03\",17,2) vPZ(\"2019-12-03\",17,0) vCREG_PLUS(\"2019-12-03\",17,0) vPOFF_PLUS(\"2019-12-03\",17,0) vCREG_MINUS(\"2019-12-03\",17,0) vPOFF_MINUS(\"2019-12-03\",17,0) time(16) vQ(\"2019-12-03\",16,74) vP(\"2019-12-03\",16,0) vPUN(\"2019-12-03\",16,2) vPZ(\"2019-12-03\",16,0) vCREG_PLUS(\"2019-12-03\",16,0) vPOFF_PLUS(\"2019-12-03\",16,0) vCREG_MINUS(\"2019-12-03\",16,0) vPOFF_MINUS(\"2019-12-03\",16,0) time(15) vQ(\"2019-12-03\",15,58) vP(\"2019-12-03\",15,0) vPUN(\"2019-12-03\",15,2) vPZ(\"2019-12-03\",15,0) vCREG_PLUS(\"2019-12-03\",15,0) vPOFF_PLUS(\"2019-12-03\",15,0) vCREG_MINUS(\"2019-12-03\",15,0) vPOFF_MINUS(\"2019-12-03\",15,0) time(14) vQ(\"2019-12-03\",14,66) vP(\"2019-12-03\",14,0) vPUN(\"2019-12-03\",14,2) vPZ(\"2019-12-03\",14,0) vCREG_PLUS(\"2019-12-03\",14,0) vPOFF_PLUS(\"2019-12-03\",14,0) vCREG_MINUS(\"2019-12-03\",14,0) vPOFF_MINUS(\"2019-12-03\",14,0) time(13) vQ(\"2019-12-03\",13,66) vP(\"2019-12-03\",13,0) vPUN(\"2019-12-03\",13,2) vPZ(\"2019-12-03\",13,0) vCREG_PLUS(\"2019-12-03\",13,0) vPOFF_PLUS(\"2019-12-03\",13,0) vCREG_MINUS(\"2019-12-03\",13,0) vPOFF_MINUS(\"2019-12-03\",13,0) time(12) vQ(\"2019-12-03\",12,81) vP(\"2019-12-03\",12,0) vPUN(\"2019-12-03\",12,2) vPZ(\"2019-12-03\",12,0) vCREG_PLUS(\"2019-12-03\",12,0) vPOFF_PLUS(\"2019-12-03\",12,0) vCREG_MINUS(\"2019-12-03\",12,0) vPOFF_MINUS(\"2019-12-03\",12,0) time(11) vQ(\"2019-12-03\",11,80) vP(\"2019-12-03\",11,0) vPUN(\"2019-12-03\",11,2) vPZ(\"2019-12-03\",11,0) vCREG_PLUS(\"2019-12-03\",11,0) vPOFF_PLUS(\"2019-12-03\",11,0) vCREG_MINUS(\"2019-12-03\",11,0) vPOFF_MINUS(\"2019-12-03\",11,0) time(10) vQ(\"2019-12-03\",10,51) vP(\"2019-12-03\",10,0) vPUN(\"2019-12-03\",10,2) vPZ(\"2019-12-03\",10,0) vCREG_PLUS(\"2019-12-03\",10,0) vPOFF_PLUS(\"2019-12-03\",10,0) vCREG_MINUS(\"2019-12-03\",10,0) vPOFF_MINUS(\"2019-12-03\",10,0) time(9) vQ(\"2019-12-03\",9,59) vP(\"2019-12-03\",9,0) vPUN(\"2019-12-03\",9,2) vPZ(\"2019-12-03\",9,0) vCREG_PLUS(\"2019-12-03\",9,0) vPOFF_PLUS(\"2019-12-03\",9,0) vCREG_MINUS(\"2019-12-03\",9,0) vPOFF_MINUS(\"2019-12-03\",9,0) time(8) vQ(\"2019-12-03\",8,57) vP(\"2019-12-03\",8,0) vPUN(\"2019-12-03\",8,2) vPZ(\"2019-12-03\",8,0) vCREG_PLUS(\"2019-12-03\",8,0) vPOFF_PLUS(\"2019-12-03\",8,0) vCREG_MINUS(\"2019-12-03\",8,0) vPOFF_MINUS(\"2019-12-03\",8,0) time(7) vQ(\"2019-12-03\",7,67) vP(\"2019-12-03\",7,0) vPUN(\"2019-12-03\",7,2) vPZ(\"2019-12-03\",7,0) vCREG_PLUS(\"2019-12-03\",7,0) vPOFF_PLUS(\"2019-12-03\",7,0) vCREG_MINUS(\"2019-12-03\",7,0) vPOFF_MINUS(\"2019-12-03\",7,0) time(6) vQ(\"2019-12-03\",6,61) vP(\"2019-12-03\",6,0) vPUN(\"2019-12-03\",6,2) vPZ(\"2019-12-03\",6,0) vCREG_PLUS(\"2019-12-03\",6,0) vPOFF_PLUS(\"2019-12-03\",6,0) vCREG_MINUS(\"2019-12-03\",6,0) vPOFF_MINUS(\"2019-12-03\",6,0) time(5) vQ(\"2019-12-03\",5,66) vP(\"2019-12-03\",5,0) vPUN(\"2019-12-03\",5,2) vPZ(\"2019-12-03\",5,0) vCREG_PLUS(\"2019-12-03\",5,0) vPOFF_PLUS(\"2019-12-03\",5,0) vCREG_MINUS(\"2019-12-03\",5,0) vPOFF_MINUS(\"2019-12-03\",5,0) time(4) vQ(\"2019-12-03\",4,107) vP(\"2019-12-03\",4,0) vPUN(\"2019-12-03\",4,2) vPZ(\"2019-12-03\",4,0) vCREG_PLUS(\"2019-12-03\",4,0) vPOFF_PLUS(\"2019-12-03\",4,0) vCREG_MINUS(\"2019-12-03\",4,0) vPOFF_MINUS(\"2019-12-03\",4,0) time(3) vQ(\"2019-12-03\",3,213) vP(\"2019-12-03\",3,0) vPUN(\"2019-12-03\",3,2) vPZ(\"2019-12-03\",3,0) vCREG_PLUS(\"2019-12-03\",3,0) vPOFF_PLUS(\"2019-12-03\",3,0) vCREG_MINUS(\"2019-12-03\",3,0) vPOFF_MINUS(\"2019-12-03\",3,0) time(2) vQ(\"2019-12-03\",2,84) vP(\"2019-12-03\",2,0) vPUN(\"2019-12-03\",2,2) vPZ(\"2019-12-03\",2,0) vCREG_PLUS(\"2019-12-03\",2,0) vPOFF_PLUS(\"2019-12-03\",2,0) vCREG_MINUS(\"2019-12-03\",2,0) vPOFF_MINUS(\"2019-12-03\",2,0) time(1) vQ(\"2019-12-03\",1,110) vP(\"2019-12-03\",1,0) vPUN(\"2019-12-03\",1,2) vPZ(\"2019-12-03\",1,0) vCREG_PLUS(\"2019-12-03\",1,0) vPOFF_PLUS(\"2019-12-03\",1,0) vCREG_MINUS(\"2019-12-03\",1,0) vPOFF_MINUS(\"2019-12-03\",1,0) time(0) vQ(\"2019-12-03\",0,147) vP(\"2019-12-03\",0,0) vPUN(\"2019-12-03\",0,2) vPZ(\"2019-12-03\",0,0) vCREG_PLUS(\"2019-12-03\",0,0) vPOFF_PLUS(\"2019-12-03\",0,0) vCREG_MINUS(\"2019-12-03\",0,0) vPOFF_MINUS(\"2019-12-03\",0,0) vSOC(\"2019-12-03\",0,0) vSOC_S(\"2019-12-03\",0,0) vS_M1(\"2019-12-03\",23,14) vC_P(\"2019-12-03\",23,70) vS_P1(\"2019-12-03\",22,1) vS_M1(\"2019-12-03\",22,17) vC_P(\"2019-12-03\",22,85) vC_P(\"2019-12-03\",21,92) vS_P1(\"2019-12-03\",20,2) vS_M1(\"2019-12-03\",20,19) vC_P(\"2019-12-03\",20,95) vC_P(\"2019-12-03\",19,50) vC_P(\"2019-12-03\",18,55) vC_P(\"2019-12-03\",17,79) vC_P(\"2019-12-03\",16,74) vC_P(\"2019-12-03\",15,58) vS_M1(\"2019-12-03\",14,11) vC_P(\"2019-12-03\",14,55) vS_M1(\"2019-12-03\",13,11) vC_P(\"2019-12-03\",13,55) vC_P(\"2019-12-03\",12,81) vC_P(\"2019-12-03\",11,80) vC_P(\"2019-12-03\",10,51) vS_P1(\"2019-12-03\",9,1) vS_M1(\"2019-12-03\",9,10) vC_P(\"2019-12-03\",9,50) vC_P(\"2019-12-03\",8,57) vC_P(\"2019-12-03\",7,67) vC_P(\"2019-12-03\",6,61) vS_M1(\"2019-12-03\",5,11) vC_P(\"2019-12-03\",5,55) vS_P1(\"2019-12-03\",4,1) vS_M1(\"2019-12-03\",4,18) vC_P(\"2019-12-03\",4,90) vS_P1(\"2019-12-03\",3,3) vS_M1(\"2019-12-03\",3,36) vC_P(\"2019-12-03\",3,180) vS_M1(\"2019-12-03\",2,14) vC_P(\"2019-12-03\",2,70) vC_P(\"2019-12-03\",1,110) vS_P1(\"2019-12-03\",0,3) vS_M1(\"2019-12-03\",0,25) vC_P(\"2019-12-03\",0,125) vOVER_I(\"2019-12-03\",23,0) vOVER_I(\"2019-12-03\",22,0) vOVER_I(\"2019-12-03\",21,0) vOVER_I(\"2019-12-03\",20,0) vOVER_I(\"2019-12-03\",19,0) vOVER_I(\"2019-12-03\",18,0) vOVER_I(\"2019-12-03\",17,0) vOVER_I(\"2019-12-03\",16,0) vOVER_I(\"2019-12-03\",15,0) vOVER_I(\"2019-12-03\",14,0) vOVER_I(\"2019-12-03\",13,0) vOVER_I(\"2019-12-03\",12,0) vOVER_I(\"2019-12-03\",11,0) vOVER_I(\"2019-12-03\",10,0) vOVER_I(\"2019-12-03\",9,0) vOVER_I(\"2019-12-03\",8,0) vOVER_I(\"2019-12-03\",7,0) vOVER_I(\"2019-12-03\",6,0) vOVER_I(\"2019-12-03\",5,0) vOVER_I(\"2019-12-03\",4,0) vOVER_I(\"2019-12-03\",3,0) vOVER_I(\"2019-12-03\",2,0) vOVER_I(\"2019-12-03\",1,0) vOVER_I(\"2019-12-03\",0,0) vUNDER_I(\"2019-12-03\",23,84) vUNDER_I(\"2019-12-03\",22,101) vUNDER_I(\"2019-12-03\",21,92) vUNDER_I(\"2019-12-03\",20,112) vUNDER_I(\"2019-12-03\",19,50) vUNDER_I(\"2019-12-03\",18,55) vUNDER_I(\"2019-12-03\",17,79) vUNDER_I(\"2019-12-03\",16,74) vUNDER_I(\"2019-12-03\",15,58) vUNDER_I(\"2019-12-03\",14,66) vUNDER_I(\"2019-12-03\",13,66) vUNDER_I(\"2019-12-03\",12,81) vUNDER_I(\"2019-12-03\",11,80) vUNDER_I(\"2019-12-03\",10,51) vUNDER_I(\"2019-12-03\",9,59) vUNDER_I(\"2019-12-03\",8,57) vUNDER_I(\"2019-12-03\",7,67) vUNDER_I(\"2019-12-03\",6,61) vUNDER_I(\"2019-12-03\",5,66) vUNDER_I(\"2019-12-03\",4,107) vUNDER_I(\"2019-12-03\",3,213) vUNDER_I(\"2019-12-03\",2,84) vUNDER_I(\"2019-12-03\",1,110) vUNDER_I(\"2019-12-03\",0,147) vC_M(\"2019-12-03\",23,0) vC_M(\"2019-12-03\",22,0) vC_M(\"2019-12-03\",21,0) vC_M(\"2019-12-03\",20,0) vC_M(\"2019-12-03\",19,0) vC_M(\"2019-12-03\",18,0) vC_M(\"2019-12-03\",17,0) vC_M(\"2019-12-03\",16,0) vC_M(\"2019-12-03\",15,0) vC_M(\"2019-12-03\",14,0) vC_M(\"2019-12-03\",13,0) vC_M(\"2019-12-03\",12,0) vC_M(\"2019-12-03\",11,0) vC_M(\"2019-12-03\",10,0) vC_M(\"2019-12-03\",9,0) vC_M(\"2019-12-03\",8,0) vC_M(\"2019-12-03\",7,0) vC_M(\"2019-12-03\",6,0) vC_M(\"2019-12-03\",5,0) vC_M(\"2019-12-03\",4,0) vC_M(\"2019-12-03\",3,0) vC_M(\"2019-12-03\",2,0) vC_M(\"2019-12-03\",1,0) vC_M(\"2019-12-03\",0,0) vE_P1(\"2019-12-03\",23,0) vE_P1(\"2019-12-03\",22,0) vE_P1(\"2019-12-03\",21,0) vE_P1(\"2019-12-03\",20,0) vE_P1(\"2019-12-03\",19,0) vE_P1(\"2019-12-03\",18,0) vE_P1(\"2019-12-03\",17,0) vE_P1(\"2019-12-03\",16,0) vE_P1(\"2019-12-03\",15,0) vE_P1(\"2019-12-03\",14,0) vE_P1(\"2019-12-03\",13,0) vE_P1(\"2019-12-03\",12,0) vE_P1(\"2019-12-03\",11,0) vE_P1(\"2019-12-03\",10,0) vE_P1(\"2019-12-03\",9,0) vE_P1(\"2019-12-03\",8,0) vE_P1(\"2019-12-03\",7,0) vE_P1(\"2019-12-03\",6,0) vE_P1(\"2019-12-03\",5,0) vE_P1(\"2019-12-03\",4,0) vE_P1(\"2019-12-03\",3,0) vE_P1(\"2019-12-03\",2,0) vE_P1(\"2019-12-03\",1,0) vE_P1(\"2019-12-03\",0,0) vE_M1(\"2019-12-03\",23,0) vE_M1(\"2019-12-03\",22,0) vE_M1(\"2019-12-03\",21,0) vE_M1(\"2019-12-03\",20,0) vE_M1(\"2019-12-03\",19,0) vE_M1(\"2019-12-03\",18,0) vE_M1(\"2019-12-03\",17,0) vE_M1(\"2019-12-03\",16,0) vE_M1(\"2019-12-03\",15,0) vE_M1(\"2019-12-03\",14,0) vE_M1(\"2019-12-03\",13,0) vE_M1(\"2019-12-03\",12,0) vE_M1(\"2019-12-03\",11,0) vE_M1(\"2019-12-03\",10,0) vE_M1(\"2019-12-03\",9,0) vE_M1(\"2019-12-03\",8,0) vE_M1(\"2019-12-03\",7,0) vE_M1(\"2019-12-03\",6,0) vE_M1(\"2019-12-03\",5,0) vE_M1(\"2019-12-03\",4,0) vE_M1(\"2019-12-03\",3,0) vE_M1(\"2019-12-03\",2,0) vE_M1(\"2019-12-03\",1,0) vE_M1(\"2019-12-03\",0,0) vS_P1(\"2019-12-03\",23,0) vS_P1(\"2019-12-03\",21,0) vS_P1(\"2019-12-03\",19,0) vS_P1(\"2019-12-03\",18,0) vS_P1(\"2019-12-03\",17,0) vS_P1(\"2019-12-03\",16,0) vS_P1(\"2019-12-03\",15,0) vS_P1(\"2019-12-03\",14,0) vS_P1(\"2019-12-03\",13,0) vS_P1(\"2019-12-03\",12,0) vS_P1(\"2019-12-03\",11,0) vS_P1(\"2019-12-03\",10,0) vS_P1(\"2019-12-03\",8,0) vS_P1(\"2019-12-03\",7,0) vS_P1(\"2019-12-03\",6,0) vS_P1(\"2019-12-03\",5,0) vS_P1(\"2019-12-03\",2,0) vS_P1(\"2019-12-03\",1,0) vS_M1(\"2019-12-03\",21,0) vS_M1(\"2019-12-03\",19,0) vS_M1(\"2019-12-03\",18,0) vS_M1(\"2019-12-03\",17,0) vS_M1(\"2019-12-03\",16,0) vS_M1(\"2019-12-03\",15,0) vS_M1(\"2019-12-03\",12,0) vS_M1(\"2019-12-03\",11,0) vS_M1(\"2019-12-03\",10,0) vS_M1(\"2019-12-03\",8,0) vS_M1(\"2019-12-03\",7,0) vS_M1(\"2019-12-03\",6,0) vS_M1(\"2019-12-03\",1,0)"))
        else:
            ''''''P = data["P"]
            Q = data["Q"]
            PUN = data["PREZZO_ACQUISTO_ENERGIA"]
            PZ = data["PREZZO_VENDITA_ENERGIA"]
            CREG_PLUS = data["CREG_PLUS"]
            POFF_PLUS = data["POFF_PLUS"]
            CREG_MINUS = data["CREG_MINUS"]
            POFF_MINUS = data["POFF_MINUS"]

            #return jsonify(calculate_best_storage(P, Q, PUN, PZ, CREG_PLUS, POFF_PLUS, CREG_MINUS, POFF_MINUS))
    return ""
'''

@ns.route('/best_grid_transfer')
class BestGridTransferFromInput(Resource):
    def post(self):
        data = request.get_json()
        building = data["building"]
        date = data["date"]
        init_charge_percentage = data["init_charge_percentage"]
        production = data["production"]
        consumption = data["consumption"]
        time_execution_limit_secs = data["time_execution_limit_secs"]
        isSchedule = False
        if "schedule" in data:
            isSchedule = bool(data["schedule"])

        #return json.dumps(calculate_best_grid_transfer(building, date, init_charge_percentage,
        #                                               "kWh", production, consumption, time_execution_limit_secs))
        return calculate_best_grid_transfer(building, date, init_charge_percentage,
                                                       "kWh", production, consumption, time_execution_limit_secs, isSchedule)

@ns.route('/get_best_grid_transfer')
class GetBestGridTransfer(Resource):
    def post(self):
        data = request.get_json()
        execution_id = data["execution_id"]
        return get_results_from_id(execution_id)

@ns.route('/recommend_best_discharge')
class RecommendBestGridTransferFromInput(Resource):
    def post(self):
        data = request.get_json()
        building = data["building"]
        date = data["date"]
        init_charge_percentage = data["init_charge_percentage"]
        production_current = data["production_current"]
        consumption_current = data["consumption_current"]
        discharge = data["discharge"]
        charge = data["charge"]
        production = data["production"]
        consumption = data["consumption"]
        feed_in = data["feed_in"]
        from_grid = data["from_grid"]
        #time_execution_limit_secs = data["time_execution_limit_secs"]
        #isSchedule = False
        #if "schedule" in data:
        #    isSchedule = bool(data["schedule"])

        return recommend_best_discharge(building, date, init_charge_percentage, production_current, consumption_current,
                                                    discharge, charge, production, consumption, feed_in, from_grid, unit = "kWh")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
