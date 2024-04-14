import csv
import shutil
from datetime import date, datetime
from enum import Enum
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, UploadFile

from database.data import get_aggregate_energy
from database.data import get_energy as db_get_energy
from database.pg_models import EnergyStat
from dependencies.db_session_dep import DBSessionDep
from models.responses.data import (
    AggregateEnergyResponse,
    AggregateEnergyUse,
    EnergyUse,
    EnergyUses,
)

router = APIRouter(prefix="/data", tags=["data"])


class EnergyClassification(str, Enum):
    both = "both"
    surplus = "surplus"
    consumption = "consumption"


class AggregateDateBy(str, Enum):
    day = "day"
    week = "week"
    month = "month"


@router.get("/energy", response_model_exclude_none=True)
async def get_energy(
    db: DBSessionDep,
    energyClassification: EnergyClassification,
    start_date: date = None,
    end_date: date = None,
) -> EnergyUses:
    results: list[EnergyStat] = await db_get_energy(
        db_session=db,
        classification=energyClassification,
        start_date=start_date,
        end_date=end_date,
    )
    models = [
        EnergyUse(
            kwh=r.kwh,
            start_time=r.start_time,
            end_time=r.end_time,
            date_of_record=r.use_date,
            surplus=True if r.surplus else None,
            consumed=False if not r.surplus else None,
        )
        for r in results
    ]
    return EnergyUses(results=models)


@router.get("/energy/aggregates", response_model_exclude_none=True)
async def get_energy_aggregates(
    db: DBSessionDep,
    aggregateDateBy: AggregateDateBy,
    start_date: date = None,
    end_date: date = None,
) -> AggregateEnergyResponse:
    data = await get_aggregate_energy(
        db_session=db,
        group_date_by=aggregateDateBy,
        start_date=start_date,
        end_date=end_date,
    )
    results = []
    for group, is_surplus, kwh in data:
        results.append(
            AggregateEnergyUse(
                surplus=True if is_surplus else None,
                consumed=True if not is_surplus else None,
                kwh=kwh,
                group_number=group,
                grouped_by=aggregateDateBy,
            )
        )
    return AggregateEnergyResponse(results=results)


@router.post("/energy-csv", status_code=201)
async def upload_energy_csv(
    db: DBSessionDep, file: UploadFile, containsHeaders: bool = True
):
    with NamedTemporaryFile(delete=False) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    stats = []
    with open(tmp_path, newline="") as csv_file:
        reader = csv.reader(csv_file)
        if containsHeaders:
            next(reader, None)
        for (
            _,
            date_recorded,
            _,
            start_time,
            end_time,
            kwh,
            _,
            consump_or_surplus,
        ) in reader:
            stats.append(
                EnergyStat(
                    use_date=datetime.strptime(
                        date_recorded.strip(), "%m/%d/%Y"
                    ).date(),
                    start_time=datetime.strptime(start_time.strip(), "%H:%M").time(),
                    end_time=datetime.strptime(end_time.strip(), "%H:%M").time(),
                    kwh=float(kwh.strip()),
                    surplus=True if "surplus" in consump_or_surplus.lower() else False,
                )
            )
        db.add_all(stats)
        await db.commit()
    return
