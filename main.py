from fastapi import FastAPI

from routers.data import router as data_router
from routers.system import router as system_router

app = FastAPI()

app.include_router(system_router)
app.include_router(data_router)
