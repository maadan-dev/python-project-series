from reportlab.pdfgen import canvas
from pathlib import Path

invoice_dir = Path("invoices")
invoice_dir.mkdir(exist_ok=True)



def generate_pdf(invoice_dict):
    name = invoice_dict['name']
    items = [item for item in invoice_dict['items']]
    status = invoice_dict['status']
    date = invoice_dict['date']
    id = invoice_dict['invoice_id']
    total = invoice_dict['total']

    FILE_PATH = str(invoice_dir / f"INV-{id}.pdf")
    c = canvas.Canvas(FILE_PATH, pagesize=(595.27, 841.89))
    bold = "Helvetica-Bold"
    normal = "Helvetica"
    c.setFont(bold, 14)

    # HEADER

    text_width = c.stringWidth("INVOICE", bold, 14)
    x = (595.27 - text_width) / 2
    y = 800
    c.drawString(x, y, "INVOICE")

    y -= 20
    x = 50
    c.setFont(normal, 11)

    c.drawString(420, y, f"Date: {date}")
    y -= 20
    c.drawString(420, y, f"Invoice ID: INV-{id}")

    y -= 50
    x = 50

    c.drawString(x, y, f"Customer: {name}")
    y -= 20
    c.drawString(x, y, f"Status: {status}")
    y -= 20

    c.setFont(bold, 12)
    c.drawString(x, y, "DESCRIPTION")
    c.drawString(450, y, "UNIT PRICE")

    c.setFont(normal, 11)

    y -= 50
    for item in items:
        description = item['description']
        quantity = item['quantity']
        item_total = item['total']
        c.drawString(x, y, f"{description}      X{quantity}")
        c.drawString(450, y, f"${item_total:.2f}")
        y -= 20

    y -= 30
    c.setFont(bold, 12)
    c.drawString(x, y, "TOTAL")
    c.drawString(450, y, f"${total}")

    c.showPage()
    c.save()