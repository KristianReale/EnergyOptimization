import json

from flask import Flask, jsonify, request
from asp.calculate import *

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/best_energy_storage', methods=['POST'])
def best_energy_storage():
    data = request.get_json()
    #esinit = data["ESInit"]
    return jsonify(calculate_best_storage())

@app.route('/best_grid_transfer', methods=['POST'])
def best_grid_transfer():
    data = request.get_json()
    esinit = data["ESInit"]
    return jsonify(calculate_best_grid_transfer(esinit))
    #return jsonify([{'day': 1, 'time':1, 'Pg': 10, 'PL': 5, 'PPV': 6, 'PS' : 4}, {'day': 1, 'time':1, 'Pg': 10, 'PL': 5, 'PPV': 6, 'PS' : 4}])



if __name__ == '__main__':
    app.run()
