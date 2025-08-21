from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
import sqlite3
import os

app = FastAPI()
db_file = "food_weights.db"

class Weight(BaseModel):
    id: int
    name: str
    weight: float

def createEmptyDB(name):
    conn = sqlite3.connect(name)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS weights (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_id TEXT NOT NULL,
        name TEXT NOT NULL,
        weight INTEGER NOT NULL
    )
    """)

    conn.commit()
    conn.close()

try: # Testing to see if there is a db, if there is not it will make one
    if not os.path.exists(db_file):
        createEmptyDB(db_file)
        # raise FileNotFoundError("Database file does not exist.")
    conn = sqlite3.connect(db_file)
except (sqlite3.OperationalError, FileNotFoundError) as e:
    print(f"Error: {e}")


@app.get("/weights", response_model=List[Weight])
def read_weights(group: str):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("SELECT id, name, weight FROM weights WHERE group_id = ?", (group,))
    rows = c.fetchall()
    conn.close()
    return [Weight(id=row[0], name=row[1], weight=row[2]) for row in rows]
