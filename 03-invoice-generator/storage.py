from pathlib import Path
import json
import datetime

FILE_PATH = Path("invoice.json")

def load_invoice():
    if FILE_PATH.is_file():
        with open(FILE_PATH, 'r') as f:
            invoices = json.load(f)
    else:
        invoices = []

    return invoices

def generate_invoice_id():
    invoices = load_invoice()
    next_num = len(invoices) + 1
    return datetime.date.today().strftime("%Y%m%d") + f"-{next_num:03d}"
# f"{next_num:03d}" formats the number with leading zeros — 001, 002, etc.



def save_invoice(invoice):
    invoices = load_invoice()
    invoices.append(invoice)
    with open(FILE_PATH, 'w') as f:
        json.dump(invoices, f, indent = 2)