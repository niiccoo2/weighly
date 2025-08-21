from fastapi import FastAPI
from routers import weights
from database import createEmptyDB, db_file
import os

app = FastAPI()

if not os.path.exists(db_file):
    createEmptyDB(db_file)

app.include_router(weights.router)
