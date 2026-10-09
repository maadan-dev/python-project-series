from fastapi import FastAPI,status, HTTPException
from models import Invoice
from database import init_db, save_invoice, get_invoice

app = FastAPI()
init_db()

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/invoices", status_code=status.HTTP_201_CREATED)
def create_invoice(invoice: Invoice):
    id = save_invoice(invoice)
    return {"id": id}

@app.get("/invoices/{invoice_id}")
def read_invoice(invoice_id: int):
    invoice = get_invoice(invoice_id)
    if invoice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invoice with id {invoice_id} not found",
        )
    return invoice