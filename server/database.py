import sqlite3
from models import Weight, Summed_Weight, Event

DB_FILE = "weighly.db" # Do not put this in main.py, main needs it to make a new db
                       # on init so DON'T

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
    ) """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS events (
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        custom_url TEXT
    ) """ )
    conn.commit()
    conn.close()

def get_entries(event: str):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, name, weight, type, time FROM weights WHERE event_id = ?", (event,))
    rows = c.fetchall()
    conn.close()

    if rows is None:
        return None

    return [Weight(id=row[0], name=row[1], weight=row[2], type=row[3], time=row[4]) for row in rows]

def get_sums(event: str):
    conn = sqlite3.connect(DB_FILE)
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

    if rows is None:
        return None

    return [Summed_Weight(name=row[0], weight=row[1], type=row[2]) for row in rows]

def get_event_info(event: str):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("""
        SELECT event_id, name, custom_url
        FROM events
        WHERE event_id = ?
        """, (event,))

    row = c.fetchone()
    conn.close()

    if row is None:
        return None

    return Event(event_id=row[0], name=row[1], custom_url=row[2])

def save_weight(event_id: int, weight: Weight):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("INSERT INTO weights (event_id, name, weight, type, time) VALUES (?, ?, ?, ?, ?)", (event_id, weight.name, weight.weight, weight.type, weight.time))

    conn.commit()
    conn.close()