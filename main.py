from fastapi import FastAPI

from routers.system import router as system_router

app = FastAPI()

app.include_router(system_router)
