import sqlite3

conn = sqlite3.connect("food_weights.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS weights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    weight INTEGER NOT NULL
)
""")

conn.commit()
conn.close()
