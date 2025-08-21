from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
import sqlite3

app = FastAPI()

class Weight(BaseModel):
    id: int
    name: str
    weight: float

@app.get("/weights", response_model=List[Weight])
def read_weights():
    conn = sqlite3.connect("food_weights.db")
    c = conn.cursor()

    c.execute("SELECT * FROM weights")
    rows = c.fetchall()

    conn.close()

    return [Weight(id=row[0], name=row[1], weight=row[2]) for row in rows]
