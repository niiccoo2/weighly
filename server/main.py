from fastapi import FastAPI
import routers
from database import createEmptyDB, db_file
import os

app = FastAPI()

if not os.path.exists(db_file):
    createEmptyDB(db_file)

app.include_router(routers.router)
