from datetime import date, time
from typing import Optional

from pydantic import BaseModel


class EnergyUse(BaseModel):
    kwh: float
    start_time: time
    end_time: time
    date_of_record: date
    surplus: Optional[bool] = None
    consumed: Optional[bool] = None


class EnergyUses(BaseModel):
    results: list[EnergyUse]


class AggregateEnergyUse(BaseModel):
    surplus: Optional[bool] = None
    consumed: Optional[bool] = None
    kwh: float
    group_number: int
    grouped_by: str


class AggregateEnergyResponse(BaseModel):
    results: list[AggregateEnergyUse]
