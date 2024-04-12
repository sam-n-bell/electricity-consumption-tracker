from fastapi import APIRouter

from database import validate_db_connection
from dependencies.db_session_dep import DBSessionDep
from models.responses.healthcheck import Check

router = APIRouter(prefix="/system", tags=["system"])


@router.get("/db", response_model=Check, response_model_exclude_unset=True)
def check_postgres_connection(db: DBSessionDep):
    return Check(available=validate_db_connection(db_session=db))


@router.get("/", response_model=Check, response_model_exclude_unset=True)
def check_api_up():
    return Check(status="I'm up!")
