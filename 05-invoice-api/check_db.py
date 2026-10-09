import sqlite3

conn = sqlite3.connect("invoices.db")
cur = conn.cursor()

cur.execute("SELECT * FROM invoices")
print("invoices:", cur.fetchall())

cur.execute("SELECT * FROM line_items")
print("line_items:", cur.fetchall())

conn.close()