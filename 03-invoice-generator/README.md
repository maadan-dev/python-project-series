# Invoice Generator CLI

Command-line invoice manager built with Python. Create invoices, store them as JSON, view them in the terminal, and export PDFs with ReportLab. Project 3 of my [Python project series](../README.md).

## Features

- Create invoices with multiple line items
- Automatic item and invoice totals
- Generated invoice IDs
- Track status (`paid` / `unpaid`)
- Store invoices in JSON
- List and view saved invoices
- Generate PDFs from stored data, any time after creation

## Run it

Requires Python 3.10+.

```bash
git clone https://github.com/maadan-dev/python-project-series.git
cd python-project-series/03-invoice-generator
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install reportlab
python main.py
```

`invoice.json` and the `invoices/` folder are created automatically.

```text
1. Create invoice
2. List invoices
3. View invoice
4. Generate Invoice PDF
```

Creating an invoice asks for the client name, payment status and number of items, then for each item:

```text
Enter description: Laptop
Enter Number of quantity: 2
Enter unit price: 450000
```

Viewing it:

```text
==================================
=============INVOICE==============
==================================
             Date: 2026-09-25
       Invoice ID: 20260925-001

Customer: Acme
Status:   unpaid
----------------------------------
DESCRIPTION             UNIT PRICE
----------------------------------
Laptop             X 2   900000.00
Mouse              X 2    30000.00
Keyboard           X 1    25000.00
==================================
TOTAL:                   $955000.00
==================================
```

## Structure

```text
03-invoice-generator/
├── main.py         # CLI and user interaction
├── model.py        # Invoice and LineItem classes
├── storage.py      # JSON storage and invoice ID generation
├── generator.py    # PDF generation (ReportLab)
└── README.md
```

## How it works

```text
User input → Invoice / LineItem objects → to_dict() → JSON storage
          → load_invoice() → CLI display / PDF generation
```

- `model.py`: `LineItem` calculates its own total (`quantity * unit_price`). `Invoice` holds its items and calculates the invoice total. Both have `to_dict()` for JSON.
- `storage.py`: `load_invoice()`, `save_invoice()`, and `generate_invoice_id()` (format `YYYYMMDD-NNN`).
- `generator.py`: builds the PDF and saves it to `invoices/`.

Model, storage, PDF and UI don't depend on each other's internals.

## What I learned

- Classes that own their own state and behavior (`Invoice.add_item()`, `LineItem.total`)
- Turning objects into dicts for JSON and back
- Using `pathlib` and `datetime`
- Working with an external library (ReportLab)

## What broke, and what fixed it

- **PDF generated before the invoice was finished.** I called `generate_pdf()` before the item loop ended, so the PDF was empty. Fix: understand execution order and add all items first.
- **Managing object state outside the object.** I kept a separate `items` list instead of using `Invoice.add_item()`. The object should own the state that belongs to it.
- **Wrong variable for `status`.** I compared `status == '1'` when I meant `status_choice`.
- **`range(num_of_items + 1)` on a string.** `input()` returns a string, so it needed `int()`. The `+ 1` also caused an extra iteration.
- **Trailing and missing commas.** Recurring syntax mistakes, again.

Most of these bugs came down to three questions: who owns the state, what type a value actually is, and when something runs.

## Known limitations

- No input validation or error handling
- Can't edit or delete invoices, or change payment status
- Invoice IDs depend on how many invoices are stored
- No tests

## Next

Project 4: [Sudoku](../04-sudoku-game).
