import sqlite3

conn = sqlite3.connect("food_weights.db")
c = conn.cursor()

c.execute("INSERT INTO weights (name, weight) VALUES (?, ?)", ("Nico", 5))
c.execute("INSERT INTO weights (name, weight) VALUES (?, ?)", ("Ben", 7))

conn.commit()
conn.close()
