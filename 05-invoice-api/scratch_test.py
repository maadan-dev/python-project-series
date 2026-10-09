import os
from database import init_db, save_invoice, get_invoice
from models import Invoice, LineItem

if os.path.exists("invoices.db"):
    os.remove("invoices.db")

init_db()

test_invoice1 = Invoice(
    client_name="Acme Corp",
    items=[
        LineItem(description="Web Design", quantity=1, unit_price=500.0),
        LineItem(description="Hosting", quantity=12, unit_price=15.0),
    ],
)
test_invoice2 = Invoice(
    client_name="Bolu stores",
    items=[
        LineItem(description="chair", quantity=2, unit_price=500.0),
        LineItem(description="table", quantity=2, unit_price=15.0),
        LineItem(description="Stool", quantity=2, unit_price=10.0),
    ],
)

save_invoice(test_invoice1)
save_invoice(test_invoice2)

print("get_invoice(1):")
print(get_invoice(1))

print("-" * 40)

print("get_invoice(2):")
print(get_invoice(2))