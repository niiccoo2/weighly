import sqlite3
from models import Weight

db_file = "food_weights.db"

def get_connection():
    return sqlite3.connect(db_file)

def createEmptyDB(name):
    conn = sqlite3.connect(name)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS weights (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_id TEXT NOT NULL,
        name TEXT NOT NULL,
        weight INTEGER NOT NULL,
        type TEXT,
        time TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def get_weights(group: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name, weight, type, time FROM weights WHERE group_id = ?", (group,))
    rows = c.fetchall()
    conn.close()
    return [Weight(id=row[0], name=row[1], weight=row[2], type=row[3], time=row[4]) for row in rows]