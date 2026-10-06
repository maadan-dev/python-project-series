from fastapi import FastAPI
from model import Invoice, LineItem

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/line-items")
def create_line_item(item: LineItem):
    return item

@app.post("/invoices")
def create_invoice(invoice: Invoice):
    return invoice
