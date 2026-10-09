import os
import sqlite3
from database import DB_PATH, init_db

# 1. Remove old database so schema gets recreated
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

# 2. Run init_db to create fresh tables
init_db()

# 3. Verify columns with PRAGMA
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.execute("PRAGMA table_info(invoices)")
print(cur.fetchall())
conn.close()