from fastapi import FastAPI
import routers
from database import DB_FILE, DB
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://weighly.app", "https://api.weighly.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if not os.path.exists(DB_FILE):
    DB(DB_FILE)

app.include_router(routers.router)
