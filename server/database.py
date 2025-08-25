import sqlite3
from models import Weight, Summed_Weight

db_file = "food_weights.db"

def get_connection():
    return sqlite3.connect(db_file)

def createEmptyDB(name):
    conn = sqlite3.connect(name)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS weights (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        weight REAL NOT NULL,
        type TEXT,
        time TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def get_entries(group: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name, weight, type, time FROM weights WHERE group_id = ?", (group,))
    rows = c.fetchall()
    conn.close()
    return [Weight(id=row[0], name=row[1], weight=row[2], type=row[3], time=row[4]) for row in rows]

def get_sums(event: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT name, SUM(weight) AS weight, type
        FROM weights
        WHERE event_id = ?
        GROUP BY name, type
        ORDER BY weight DESC;
        """, (event,))
    
    rows = c.fetchall()
    conn.close()
    return [Summed_Weight(name=row[0], weight=row[1], type=row[2]) for row in rows]