import sqlite3

conn = sqlite3.connect("invoices.db")
conn.execute("PRAGMA foreign_keys = ON")
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_name TEXT NOT NULL
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS line_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_id INTEGER NOT NULL,
        description TEXT NOT NULL,
        quantity INTEGER NOT NULL CHECK (quantity >= 1),
        unit_price REAL NOT NULL CHECK (unit_price > 0),
        FOREIGN KEY (invoice_id) REFERENCES invoices(id)
    )
""")

conn.commit()
conn.close()