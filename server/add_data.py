import sqlite3

conn = sqlite3.connect("food_weights.db")
c = conn.cursor()

c.execute("INSERT INTO weights (group_id, name, weight, type, time) VALUES (?, ?, ?, ?, ?)", ("troop30", "Nico", 5, "scout", "2024-11-23 13:56:18.506589"))
c.execute("INSERT INTO weights (group_id, name, weight, type, time) VALUES (?, ?, ?, ?, ?)", ("troop30", "Ben", 3, "cub", "2024-11-23 13:56:18.506589"))
c.execute("INSERT INTO weights (group_id, name, weight, type, time) VALUES (?, ?, ?, ?, ?)", ("whs", "Evan", 5, "", "2024-11-23 13:56:18.506589"))
c.execute("INSERT INTO weights (group_id, name, weight, type, time) VALUES (?, ?, ?, ?, ?)", ("whs", "Bob", 5, "", "2024-11-23 13:56:18.506589"))

conn.commit()
conn.close()