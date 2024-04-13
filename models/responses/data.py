from datetime import time, date
from pydantic import BaseModel


class EnergyUse(BaseModel):
    kwh: float
    start_time: time
    end_time: time
    date_of_record: date
    is_surplus: bool


class EnergyUses(BaseModel):
    results: list[EnergyUse]
