import sqlite3

conn = sqlite3.connect("food_weights.db")
c = conn.cursor()

# troop30 id: 0
c.execute("INSERT INTO weights (event_id, name, weight, type, time) VALUES (?, ?, ?, ?, ?)", (0, "Nico", 5, "scout", "2024-11-23 13:56:18.506589"))
c.execute("INSERT INTO weights (event_id, name, weight, type, time) VALUES (?, ?, ?, ?, ?)", (0, "Nico", 3, "scout", "2024-11-23 13:56:18.506589"))
c.execute("INSERT INTO weights (event_id, name, weight, type, time) VALUES (?, ?, ?, ?, ?)", (0, "Ben", 3, "cub", "2024-11-23 13:56:18.506589"))
c.execute("INSERT INTO weights (event_id, name, weight, type, time) VALUES (?, ?, ?, ?, ?)", (0, "Ben", 3, "scout", "2024-11-23 13:56:18.506589"))

# whs id: 1
c.execute("INSERT INTO weights (event_id, name, weight, type, time) VALUES (?, ?, ?, ?, ?)", (1, "Evan", 5, "", "2024-11-23 13:56:18.506589"))
c.execute("INSERT INTO weights (event_id, name, weight, type, time) VALUES (?, ?, ?, ?, ?)", (1, "Bob", 5, "", "2024-11-23 13:56:18.506589"))

conn.commit()
conn.close()