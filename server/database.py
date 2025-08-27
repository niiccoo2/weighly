import sqlite3
from models import Weight, Summed_Weight, Event
from typing import Optional

DB_FILE = "weighly.db" # Do not put this in main.py, main needs it to make a new db
                       # on init so DON'T

class Database:
    def __init__(self, db_file: Optional[str] = None):
        if db_file is None:
            self.db_file = DB_FILE
        self.conn = sqlite3.connect(self.db_file)
        self.c = self.conn.cursor()
        self.c.execute("""
        CREATE TABLE IF NOT EXISTS weights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            weight REAL NOT NULL,
            type TEXT,
            time TEXT NOT NULL
        ) """)
        self.c.execute("""
        CREATE TABLE IF NOT EXISTS events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            custom_url TEXT,
            type_options TEXT
        ) """ )
        self.conn.commit()
        self.conn.close()

    def get_entries(self, event: str):
        self.conn = sqlite3.connect(self.db_file)
        self.c = self.conn.cursor()
        self.c.execute("SELECT id, name, weight, type, time FROM weights WHERE event_id = ?", (event,))
        rows =  self.c.fetchall()
        self.conn.close()

        if rows is None:
            return None

        return [Weight(id=row[0], name=row[1], weight=row[2], type=row[3], time=row[4]) for row in rows]

    def get_sums(self, event: str):
        self.conn = sqlite3.connect(self.db_file)
        self.c = self.conn.cursor()
        self.c.execute("""
            SELECT name, SUM(weight) AS weight, type
            FROM weights
            WHERE event_id = ?
            GROUP BY name, type
            ORDER BY weight DESC;
            """, (event,))
        
        rows = self.c.fetchall()
        self.conn.close()

        if rows is None:
            return None

        return [Summed_Weight(name=row[0], weight=row[1], type=row[2]) for row in rows]

    def get_event_info(self, event: str):
        self.conn = sqlite3.connect(self.db_file)
        self.c = self.conn.cursor()
        self.c.execute("""
            SELECT event_id, name, custom_url
            FROM events
            WHERE event_id = ?
            """, (event,))

        row = self.c.fetchone()
        self.conn.close()

        if row is None:
            return None

        return Event(event_id=row[0], name=row[1], custom_url=row[2])

    def get_total(self, event: str):
        self.conn = sqlite3.connect(self.db_file)
        self.c = self.conn.cursor()

        self.c.execute("""
            SELECT SUM(weight) AS total_weight
            FROM weights
            WHERE event_id = ?;
        """, (event,))
        
        row = self.c.fetchone()
        self.conn.close()

        # If there are no rows or SUM returns None
        if row is None or row[0] is None:
            return 0
        return row[0]


    def save_weight(self, event_id: int, weight: Weight):
        self.conn = sqlite3.connect(self.db_file)
        self.c = self.conn.cursor()

        self.c.execute("INSERT INTO weights (event_id, name, weight, type, time) VALUES (?, ?, ?, ?, ?)", (event_id, weight.name.capitalize(), weight.weight, weight.type.lower(), weight.time))

        self.conn.commit()
        self.conn.close()

    def remove_weight(self, weight_id: int):
        with sqlite3.connect(self.db_file) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM weights WHERE id = ?", (weight_id,))
            conn.commit()
            return c.rowcount