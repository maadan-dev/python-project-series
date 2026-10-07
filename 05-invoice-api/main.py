from fastapi import FastAPI
from model import Invoice, LineItem

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/invoices")
def create_invoice(invoice: Invoice):
    return invoice
