# Invoice API

An invoice API built with FastAPI, Pydantic and SQLite. It saves invoices with line items, stores them in a database, and generates PDFs on demand.

## Project structure

- `main.py`: routes
- `models.py`: Pydantic models and validation rules
- `database.py`: SQLite schema, save and load logic
- `pdf_generator.py`: PDF generation

## How to run

1. `cd 05-invoice-api`
2. `python3 -m venv .venv`
3. Activate it: `source .venv/bin/activate` (Linux/macOS) or `.venv\Scripts\activate` (Windows)
4. `pip install -r requirements.txt`
5. `fastapi dev main.py`

The API runs at `http://127.0.0.1:8000`, with interactive docs at `/docs`.

## Endpoints

| Method | Path | Description | Responses |
| --- | --- | --- | --- |
| GET | `/` | Health check | 200 `{"status": "ok"}` |
| POST | `/invoices` | Create an invoice with line items | 201 `{"id": 1}` / 422 on invalid input |
| GET | `/invoices/{invoice_id}` | Get an invoice by id | 200 invoice JSON / 404 if missing |
| GET | `/invoices/{invoice_id}/pdf` | Download the invoice as a PDF | 200 PDF / 404 if missing |

## What I learned

- Pydantic validates request bodies and path parameters, and FastAPI returns 422 automatically.
- SQLite only enforces foreign keys when `PRAGMA foreign_keys = ON` runs on each connection.
- Transactions make multi-table writes all-or-nothing: commit once at the end, roll back on any error.
- In a one-to-many relationship, the foreign key lives on the "many" side.
- Test with data where ids don't line up, or a wrong query can pass by coincidence.
- Anchor file paths to `__file__` so they don't depend on where the server starts.

## What I struggled with

- Virtual environments: stale activations and running a project with the wrong interpreter.
- Querying line items by `id` instead of `invoice_id`, which returned plausible but wrong results.
- Writing the foreign key clause in SQL.
- Predicting what a crash leaves in the database.