from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse

from database import get_invoice, init_db, save_invoice
from models import Invoice
from pdf_generator import generate_pdf, invoice_to_pdf_dict

app = FastAPI()
init_db()


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/invoices", status_code=status.HTTP_201_CREATED)
def create_invoice(invoice: Invoice):
    invoice_id = save_invoice(invoice)
    return {"id": invoice_id}


@app.get("/invoices/{invoice_id}")
def read_invoice(invoice_id: int):
    invoice = get_invoice(invoice_id)
    if invoice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invoice with id {invoice_id} not found",
        )
    return invoice


@app.get("/invoices/{invoice_id}/pdf")
def get_invoice_pdf(invoice_id: int):
    invoice = get_invoice(invoice_id)
    if invoice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invoice with id {invoice_id} not found",
        )

    pdf_dict = invoice_to_pdf_dict(invoice)
    pdf_path = generate_pdf(pdf_dict)

    return FileResponse(pdf_path, media_type="application/pdf")