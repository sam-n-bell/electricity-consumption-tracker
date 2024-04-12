import csv
import shutil
from datetime import datetime
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, UploadFile

from database.pg_models import EnergyStats
from dependencies.db_session_dep import DBSessionDep

router = APIRouter(prefix="/data", tags=["data"])


@router.post("/energy-csv")
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
                EnergyStats(
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

    return {"filename": file.content_type}
