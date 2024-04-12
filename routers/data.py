import shutil
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, Depends, UploadFile

from database.pg_models import EnergyStats
from dependencies.db_session_dep import DBSessionDep
from database import get_db_session, validate_db_connection
from models.responses.healthcheck import Check
from datetime import datetime
import csv

router = APIRouter(prefix="/data", tags=["data"])


@router.post("/energy-csv")
async def upload_energy_csv(db: DBSessionDep, file: UploadFile):
    with NamedTemporaryFile(delete=False) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    stats = []
    with open(tmp_path, newline='') as csv_file:
        reader = csv.reader(csv_file)
        for _, date, _, start_time, end_time, kwh, _, consum_surplus  in reader:
            consum_surplus = consum_surplus.lower()
            stats.append(
                EnergyStats(
                    use_date=datetime.strptime(date, '%m/%d/%Y').date(),
                    start_time=datetime.strptime(start_time, '%H:%M').time(),
                    end_time=datetime.strptime(end_time, '%H:%M').time(),
                    kwh=float(kwh),
                    surplus=True if "surplus" in consum_surplus else False
                )
            )
        db.add_all(stats)
        await db.commit()

    return {"filename": file.content_type}

