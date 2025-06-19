import bentoml


from app import TimeValue, Results
from asp.solve import *

@bentoml.service(

)
class Optimization:
    @bentoml.api()
    def best_grid_transfer_from_prediction(self, building: str, date: str, init_charge_percentage: float, unit: str, production: list[TimeValue], consumption: list[TimeValue], time_execution_limit_secs: int = 1200) -> Results:
        res = Results()
        resObj = calculate_best_grid_transfer(building, date, init_charge_percentage, unit, production, consumption, time_execution_limit_secs)
        res.date = resObj["date"]
        res.unit = resObj["unit"]
        res.discharge = resObj["discharge"]
        res.charge = resObj["charge"]
        res.production = resObj["production"]
        res.consumption = resObj["consumption"]
        res.feed_in = resObj["feed_in"]
        res.from_grid = resObj["from_grid"]

        return res






