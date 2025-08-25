from fastapi import FastAPI
import routers
from database import createEmptyDB, DB_FILE
import os

app = FastAPI()

if not os.path.exists(DB_FILE):
    createEmptyDB(DB_FILE)

app.include_router(routers.router)
