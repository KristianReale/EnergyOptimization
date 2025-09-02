import json

from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields
from pydantic import BaseModel

from asp.solve import *

app = Flask(__name__)
description = """
Energy Efficiency Optimization Process for Smart Energy Management

The process of optimizing energy efficiency can be interpreted in three complementary ways:
- Reduction of the total amount of energy transferred to or drawn from the grid;
- Minimization of the costs associated with energy purchases;
- Maximization of self-consumption, thereby reducing dependence on the external grid.

The REST service operates as follows: given as input the energy production and consumption profiles (expressed in kWh) for each time interval of a specific day, the goal is to calculate the optimal amount of energy to be drawn from the battery, in order to minimize the energy purchased from the external grid and the energy fed back into the grid. In other words, the solution aims to maximize battery usage and recharge it using self-produced local energy. It is important to note that the production and consumption values can be derived from forecasts provided by a machine learning (ML) model.

The optimization results depend on the specific building of the University of Calabria being considered, which are:
- Experimental building Chiodo 2
- Office Buildings Cubo 18 B
- Office Buildings Cubo 31B
- Office Buildings Cubo 41B
- Office Buildings Cubo 44B
- Residential buildings Monaci121
- Residential buildings Monaci122
- Residential buildings Monaci123
- Residential buildings Monaci124
- Residential buildings Monaci223

Each building has internal parameters, already configured within the REST service, which may vary from building to building, including:
- The minimum and maximum capacity of the storage system (battery);
- The minimum and maximum amount of energy that can be drawn from the storage system.

Therefore, when invoking the REST service, it will be sufficient to specify the name of the building being considered.
"""
api = Api(app, version='1.0', title='Energy Efficiency Optimization Process', description=description)

app.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'
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

production_item_model = ns.model('ProductionItem', {
    'time': fields.String(required=True, description='Timestamp of the production measurement'),
    'value': fields.Float(required=True, description='Measured or predicted production value in kWh')
})
consumption_item_model = ns.model('ConsumptionItem', {
    'time': fields.String(required=True, description='Timestamp of the consumption measurement'),
    'value': fields.Float(required=True, description='Measured or predicted consumption value in kWh')
})
discharge_item_model = ns.model('DischargeItem', {
    'time': fields.String(required=True, description='Timestamp of the discharge value'),
    'value': fields.Float(required=True, description='Discharge value in kWh')
})
charge_item_model = ns.model('ChargeItem', {
    'time': fields.String(required=True, description='Timestamp of the charge value'),
    'value': fields.Float(required=True, description='Charge value in kWh')
})
feed_in_item_model = ns.model('FeedInItem', {
    'time': fields.String(required=True, description='Timestamp of the Feed-In value'),
    'value': fields.Float(required=True, description='Feed In Energy value in kWh')
})
from_grid_item_model = ns.model('FromGridItem', {
    'time': fields.String(required=True, description='Timestamp of the From-Grid value'),
    'value': fields.Float(required=True, description='Energy Taken from Grid in kWh')
})
best_grid_transfer_model = ns.model('best_grid_transfer', {
    'building': fields.String(required=True, description='The Building Name'),
    'date': fields.String(required=True, description='The day to be considered in the solution calculation.'),
    'init_charge_percentage': fields.Float(required=False, description='The initial charge percentage of the storage system.'),
    'production': fields.List(fields.Nested(production_item_model), required=True, description='Array of production values'),
    'consumption': fields.List(fields.Nested(consumption_item_model), required=True, description='Array of consumption values'),
    'time_execution_limit_secs': fields.Integer(required=False, description='The time execution limit in seconds.'),
    'schedule': fields.Boolean(required=False, description='Whether or not to schedule a production schedule.'),
})

get_best_grid_transfer_model = ns.model('get_best_grid_transfer_model', {
    'execution_id': fields.String(required=True, description='The Execution ID of an already launched computation'),
})
best_grid_transfer_output_data = ns.model('best_grid_transfer_output_data', {
    'date': fields.String(required=True, description='The day to be considered in the solution calculation.'),
    'discharge': fields.List(fields.Nested(discharge_item_model), description='Array of discharge values'),
    'charge': fields.List(fields.Nested(charge_item_model), description='Array of charge values'),
    'production': fields.List(fields.Nested(production_item_model), description='Array of production values'),
    'consumption': fields.List(fields.Nested(consumption_item_model), description='Array of consumption values'),
    'feed_in': fields.List(fields.Nested(feed_in_item_model), description='Array of feed-in values'),
    'from_grid': fields.List(fields.Nested(from_grid_item_model),  description='Array of from-grid values'),
})
api.schema_model('ResponseOneOf', {
    'oneOf': [
        {'$ref': '#/definitions/best_grid_transfer_output_data'},
        {'$ref': '#/definitions/get_best_grid_transfer_model'}
    ]
})

@ns.route('/best_grid_transfer')
class BestGridTransferFromInput(Resource):
    @ns.expect(best_grid_transfer_model)
    @ns.response(200, 'Successful Response', 'ResponseOneOf')
    def post(self):
        data = ns.payload
        building = data["building"]
        date = data["date"]
        init_charge_percentage = 100
        if "init_charge_percentage" in data:
            init_charge_percentage = data["init_charge_percentage"]

        production = data["production"]
        consumption = data["consumption"]
        time_execution_limit_secs = 1200
        if "time_execution_limit_secs" in data:
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
    @ns.expect(get_best_grid_transfer_model)
    @ns.response(200, 'Successful Response', 'best_grid_transfer_output_data')
    def post(self):
        data = ns.payload
        execution_id = data["execution_id"]
        return get_results_from_id(execution_id)

recommend_model = ns.model('recommend_model', {
    'building': fields.String(required=True, description='The Building Name'),
    'date': fields.String(required=True, description='The day to be considered in the solution calculation.'),
    'init_charge_percentage': fields.Float(required=False, description='The initial charge percentage of the storage system.'),
    'production_current': fields.Float(required=True, description='Measured or predicted production value in kWh'),
    'consumption:current': fields.Float(required=True, description='Measured or predicted consumption value in kWh'),
    'discharge': fields.List(fields.Nested(discharge_item_model), required=True, description='Array of discharge values'),
    'charge': fields.List(fields.Nested(charge_item_model), required=True, description='Array of charge values'),
    'production': fields.List(fields.Nested(production_item_model), required=True, description='Array of production values'),
    'consumption': fields.List(fields.Nested(consumption_item_model), required=True, description='Array of consumption values'),
    'feed_in': fields.List(fields.Nested(feed_in_item_model), required=True, description='Array of feed-in values'),
    'from_grid': fields.List(fields.Nested(from_grid_item_model), required=True, description='Array of from-grid values'),
})
recommend_best_discharge_model_output = ns.model('recommend_best_discharge_model_output', {
    'date': fields.String(description='The day to be considered in the solution calculation.'),
    'best_discharge': fields.Float(description='The best recommended discharge value in kWh.'),
})
@ns.route('/recommend')
class RecommendBestùGridTransferFromInput(Resource):
    @ns.expect(recommend_model)
    @ns.response(200, 'Successful Response', 'recommend_best_discharge_model_output')
    def post(self):
        data = ns.payload
        building = data["building"]
        date = data["date"]
        time = data["time"]
        init_charge_percentage = 0
        if "init_charge_percentage" in data:
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

        return recommend(building, date, time, init_charge_percentage, production_current, consumption_current,
                                                    discharge, charge, production, consumption, feed_in, from_grid, unit = "kWh")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
