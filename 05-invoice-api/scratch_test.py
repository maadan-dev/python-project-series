from database import get_invoice
from pdf_generator import generate_pdf, invoice_to_pdf_dict

invoice = get_invoice(1)
if invoice:
    pdf_dict = invoice_to_pdf_dict(invoice)
    generate_pdf(pdf_dict)
    print("Date shown:", pdf_dict["date"])
    print("Total shown:", pdf_dict["total"])