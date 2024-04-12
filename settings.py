import os

from dotenv import load_dotenv

load_dotenv()

PG_DIALECT = os.getenv("POSTGRES_DIALECT")
PG_HOST = os.getenv("POSTGRES_HOST")
PG_DB = os.getenv("POSTGRES_DB")
PG_USER = os.getenv("POSTGRES_USER")
PG_PWD = os.getenv("POSTGRES_PASSWORD")
PG_PORT = os.getenv("POSTGRES_PORT")
