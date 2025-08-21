import sqlite3

conn = sqlite3.connect("food_weights.db")
c = conn.cursor()

c.execute("SELECT * FROM weights")
rows = c.fetchall()

print(rows[1][1])

conn.close()
