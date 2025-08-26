import sqlite3

conn = sqlite3.connect("weighly.db")
c = conn.cursor()

# Adding events:

c.execute("INSERT INTO events (name) VALUES (?)", ("Troop 30 Food Drive",))
c.execute("INSERT INTO events (name) VALUES (?)", ("WHS Coat Drive",))

# Adding entries:

# troop30 id: 0
c.execute("INSERT INTO weights (event_id, name, weight, type, time) VALUES (?, ?, ?, ?, ?)", (1, "Nico", 5, "scout", "2024-11-23 13:56:18.506589"))
c.execute("INSERT INTO weights (event_id, name, weight, type, time) VALUES (?, ?, ?, ?, ?)", (1, "Nico", 3, "scout", "2024-11-23 13:56:18.506589"))
c.execute("INSERT INTO weights (event_id, name, weight, type, time) VALUES (?, ?, ?, ?, ?)", (1, "Ben", 3, "cub", "2024-11-23 13:56:18.506589"))
c.execute("INSERT INTO weights (event_id, name, weight, type, time) VALUES (?, ?, ?, ?, ?)", (1, "Ben", 3, "scout", "2024-11-23 13:56:18.506589"))

# whs id: 1
c.execute("INSERT INTO weights (event_id, name, weight, type, time) VALUES (?, ?, ?, ?, ?)", (2, "Evan", 5, None, "2024-11-23 13:56:18.506589"))
c.execute("INSERT INTO weights (event_id, name, weight, type, time) VALUES (?, ?, ?, ?, ?)", (2, "Bob", 5, None, "2024-11-23 13:56:18.506589"))

conn.commit()
conn.close()