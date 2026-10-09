import sqlite3

from models import Invoice, LineItem

def init_db():
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

def save_invoice(invoice: Invoice) -> int:
    conn = sqlite3.connect("invoices.db")
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO invoices (client_name) VALUES (?)",
            (invoice.client_name,),
        )

        new_id = cur.lastrowid

        items = [
            (new_id, item.description, item.quantity, item.unit_price)
            for item in invoice.items
        ]

        cur.executemany(
            "INSERT INTO line_items (invoice_id, description, quantity, unit_price) VALUES (?, ?, ?, ?)",
            items,
        )

        conn.commit()
        return new_id

    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def get_invoice(invoice_id: int) -> Invoice | None:
    conn = sqlite3.connect("invoices.db")
    cur = conn.cursor()

    try:
        cur.execute("SELECT client_name FROM invoices WHERE id = ?", (invoice_id,))
        invoice_row = cur.fetchone()
        if invoice_row is None:
            return None

        client_name = invoice_row[0]

        cur.execute(
            "SELECT description, quantity, unit_price FROM line_items WHERE invoice_id = ?", 
            (invoice_id,)
        )
        items_row = cur.fetchall()

        items = [
            LineItem(description=row[0], quantity=row[1], unit_price=row[2])
            for row in items_row
        ]

        return Invoice(client_name=client_name, items=items)
    finally:
        conn.close()
