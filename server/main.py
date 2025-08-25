from fastapi import FastAPI
import routers
from database import createEmptyDB
import os

DB_FILE = "weighly.db"
app = FastAPI()

if not os.path.exists(DB_FILE):
    createEmptyDB(DB_FILE)

app.include_router(routers.router)
