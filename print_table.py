import sqlite3, pprint
conn = sqlite3.connect("questions.db")
cur = conn.execute("PRAGMA table_info(questions)")
pprint.pp(cur.fetchall())
conn.close()
