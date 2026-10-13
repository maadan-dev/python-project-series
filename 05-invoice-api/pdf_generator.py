from pathlib import Path
from reportlab.lib import colors
from reportlab.pdfgen import canvas

from models import InvoiceOut

invoice_dir = Path(__file__).parent / "invoices"
invoice_dir.mkdir(exist_ok=True)


def invoice_to_pdf_dict(invoice: InvoiceOut) -> dict:
    items = [
        {
            "description": item.description,
            "quantity": item.quantity,
            "total": item.quantity * item.unit_price,
        }
        for item in invoice.items
    ]

    grand_total = sum(item["total"] for item in items)
    date_only = invoice.created_at.split(" ")[0]

    return {
        "invoice_id": invoice.id,
        "name": invoice.client_name,
        "date": date_only,
        "status": invoice.status,
        "items": items,
        "total": grand_total,
    }


def generate_pdf(invoice_dict: dict) -> Path:
    name = invoice_dict["name"]
    items = invoice_dict["items"]
    status = str(invoice_dict["status"]).upper()
    date = invoice_dict["date"]
    inv_id = invoice_dict["invoice_id"]
    grand_total = invoice_dict["total"]

    file_path = invoice_dir / f"INV-{inv_id}.pdf"

    width, height = 595.27, 841.89
    c = canvas.Canvas(str(file_path), pagesize=(width, height))

    PRIMARY_COLOR = colors.HexColor("#1E293B")  # Deep Slate
    ACCENT_COLOR = colors.HexColor("#2563EB")   # Royal Blue
    TEXT_DARK = colors.HexColor("#0F172A")      # Dark Gray Text
    TEXT_MUTED = colors.HexColor("#64748B")     # Muted Slate
    BG_LIGHT = colors.HexColor("#F8FAFC")       # Soft Table Header Gray
    LINE_COLOR = colors.HexColor("#E2E8F0")     # Light Border Gray

    bold = "Helvetica-Bold"
    normal = "Helvetica"

    c.setFillColor(ACCENT_COLOR)
    c.rect(0, height - 6, width, 6, stroke=0, fill=1)

    c.setFillColor(PRIMARY_COLOR)
    c.setFont(bold, 22)
    c.drawString(50, height - 50, "INVOICE")

    c.setFillColor(TEXT_MUTED)
    c.setFont(normal, 10)
    c.drawString(50, height - 65, f"Invoice #: INV-{inv_id}")

    c.drawRightString(width - 50, height - 50, f"Date: {date}")

    is_paid = status == "PAID"
    badge_bg = colors.HexColor("#DCFCE7") if is_paid else colors.HexColor("#FEF3C7")
    badge_text = colors.HexColor("#166534") if is_paid else colors.HexColor("#92400E")

    c.setFillColor(badge_bg)
    c.roundRect(width - 115, height - 78, 65, 18, 4, stroke=0, fill=1)
    c.setFillColor(badge_text)
    c.setFont(bold, 8)
    c.drawCentredString(width - 82.5, height - 72, status)

    y = height - 105
    c.setStrokeColor(LINE_COLOR)
    c.setLineWidth(1)
    c.line(50, y, width - 50, y)

    y -= 25
    c.setFillColor(TEXT_MUTED)
    c.setFont(bold, 8)
    c.drawString(50, y, "BILLED TO")

    y -= 18
    c.setFillColor(TEXT_DARK)
    c.setFont(bold, 12)
    c.drawString(50, y, name)

    y -= 35
    c.setFillColor(BG_LIGHT)
    c.roundRect(50, y - 5, width - 100, 24, 3, stroke=0, fill=1)

    c.setFillColor(TEXT_MUTED)
    c.setFont(bold, 9)
    c.drawString(60, y + 2, "DESCRIPTION")
    c.drawCentredString(360, y + 2, "QTY")
    c.drawRightString(width - 60, y + 2, "TOTAL")

    c.setFont(normal, 10)
    c.setFillColor(TEXT_DARK)

    y -= 25
    for item in items:
        description = item["description"]
        quantity = item["quantity"]
        item_total = item["total"]

        c.drawString(60, y, str(description))
        c.drawCentredString(360, y, str(quantity))
        c.drawRightString(width - 60, y, f"${item_total:.2f}")

        # Row divider line
        c.setStrokeColor(LINE_COLOR)
        c.setLineWidth(0.5)
        c.line(50, y - 8, width - 50, y - 8)

        y -= 25

    # --- GRAND TOTAL SECTION ---
    y -= 10
    c.setStrokeColor(PRIMARY_COLOR)
    c.setLineWidth(1)
    c.line(width - 200, y, width - 50, y)

    y -= 20
    c.setFillColor(TEXT_MUTED)
    c.setFont(bold, 10)
    c.drawString(width - 200, y, "Grand Total:")

    c.setFillColor(ACCENT_COLOR)
    c.setFont(bold, 14)
    c.drawRightString(width - 60, y, f"${grand_total:.2f}")

    # --- FOOTER ---
    c.setFillColor(TEXT_MUTED)
    c.setFont(normal, 9)
    c.drawCentredString(width / 2, 35, "Thank you for your business!")

    c.showPage()
    c.save()

    return file_path