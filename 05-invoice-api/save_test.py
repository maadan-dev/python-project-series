import sqlite3

conn = sqlite3.connect("invoices.db")
conn.execute("PRAGMA foreign_keys = ON")
cur = conn.cursor()

try:
    # 1. Insert the invoice
    cur.execute(
        "INSERT INTO invoices (client_name) VALUES (?)",
        ("Acme Ltd",),
    )

    new_id = cur.lastrowid
    print(f"The auto-generated ID is: {new_id}")

    items = [
        (new_id, "logo design", 1, 150.0),
        (new_id, "hosting", 12, 10.0),
        (new_id, "domain", 1, 15.0),
    ]

    cur.executemany(
        "INSERT INTO line_items (invoice_id, description, quantity, unit_price) VALUES (?, ?, ?, ?)",
        items,
    )

    conn.commit()

except Exception:
    conn.rollback()
    raise
finally:
    conn.close()