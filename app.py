import json

from flask import Flask, jsonify, request
from asp.calculate import *

app = Flask(__name__)


@app.route('/best_energy_storage_python', methods=['POST'])
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



@app.route('/best_energy_storage_asp', methods=['POST'])
def best_energy_storage_asp():
    data = request.get_json()

    P = data["P"]
    Q = data["Q"]
    PUN = data["PREZZO_ACQUISTO_ENERGIA"]
    PZ = data["PREZZO_VENDITA_ENERGIA"]
    CREG_PLUS = data["CREG_PLUS"]
    POFF_PLUS = data["POFF_PLUS"]
    CREG_MINUS = data["CREG_MINUS"]
    POFF_MINUS = data["POFF_MINUS"]

    return jsonify(calculate_best_storage(P, Q, PUN, PZ, CREG_PLUS, POFF_PLUS, CREG_MINUS, POFF_MINUS))


@app.route('/best_grid_transfer', methods=['POST'])
def best_grid_transfer():
    data = request.get_json()
    esinit = data["ESInit"]
    return jsonify(calculate_best_grid_transfer(esinit))
    #return jsonify([{'day': 1, 'time':1, 'Pg': 10, 'PL': 5, 'PPV': 6, 'PS' : 4}, {'day': 1, 'time':1, 'Pg': 10, 'PL': 5, 'PPV': 6, 'PS' : 4}])



if __name__ == '__main__':
    app.run()
