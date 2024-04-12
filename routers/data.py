from fastapi import APIRouter, Depends, UploadFile
from dependencies.db_session_dep import DBSessionDep
from database import get_db_session, validate_db_connection
from models.responses.healthcheck import Check

router = APIRouter(prefix="/data", tags=["data"])


@router.post("/energy-csv")
def upload_energy_csv(file: UploadFile):
    return {"filename": file.filename}

