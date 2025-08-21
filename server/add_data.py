import sqlite3

conn = sqlite3.connect("food_weights.db")
c = conn.cursor()

c.execute("INSERT INTO weights (group_id, name, weight) VALUES (?, ?)", ("troop30", "Nico", 5))
c.execute("INSERT INTO weights (group_id, name, weight) VALUES (?, ?)", ("troop30", "Ben", 7))
c.execute("INSERT INTO weights (group_id, name, weight) VALUES (?, ?)", ("whs", "Bob", 12))
c.execute("INSERT INTO weights (group_id, name, weight) VALUES (?, ?)", ("whs", "Mary", 12))

conn.commit()
conn.close()