# Invoice Generator CLI

A simple command-line invoice management system built with Python.

The application lets you create invoices, store them as JSON, view and list saved invoices, and generate professional PDF invoices from the stored data.

## Features

* Create invoices from the command line
* Add multiple line items to an invoice
* Automatically calculate item totals and invoice totals
* Generate unique invoice IDs
* Track invoice status (`paid` / `unpaid`)
* Store invoices locally in JSON
* List all saved invoices
* View individual invoices in the terminal
* Generate PDF invoices using ReportLab
* Reuse stored invoice data to generate PDFs later

## Project Structure

```text
invoice-generator/
│
├── main.py          # CLI application and user interaction
├── model.py         # Invoice and LineItem classes
├── storage.py       # JSON storage and invoice ID generation
├── generator.py     # PDF invoice generation
├── invoice.json     # Stored invoice data
├── invoices/        # Generated PDF invoices
└── README.md
```

## How It Works

The project is split into a few small modules, each responsible for a specific part of the application.

### `model.py`

Contains the core data models:

* `LineItem` represents an individual item on an invoice.
* `Invoice` represents a complete invoice.

A `LineItem` calculates its own total:

```python
quantity * unit_price
```

The `Invoice` class stores its line items and calculates the overall invoice total.

Both classes also provide `to_dict()` methods so their data can be converted into dictionaries before being stored as JSON.

### `storage.py`

Handles persistent invoice storage using Python's `json` module.

It provides:

* `load_invoice()` — loads existing invoices from `invoice.json`
* `save_invoice()` — adds and saves a new invoice
* `generate_invoice_id()` — generates IDs such as:

```text
20260925-001
20260925-002
20260925-003
```

### `generator.py`

Uses [ReportLab](https://www.reportlab.com/) to generate PDF invoices.

Generated PDFs are stored inside the `invoices/` directory using the invoice ID:

```text
invoices/INV-20260925-001.pdf
```

### `main.py`

Provides the command-line interface.

The user can:

```text
1. Create invoice
2. List invoices
3. View invoice
4. Generate Invoice PDF
```

## Example

When creating an invoice, the program asks for the client name, payment status, and number of items.

For each item:

```text
Enter description: Laptop
Enter Number of quantity: 2
Enter unit price: 450000
```

The application calculates the line-item total automatically.

An invoice can then be viewed from the CLI:

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

The same invoice can also be exported as a PDF.

## Requirements

* Python 3.10+
* ReportLab

## Installation

Clone the repository:

```bash
git clone <https://github.com/maadan-dev/invoice_generator.git>
cd invoice-generator
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Linux/macOS:

```bash
source .venv/bin/activate
```

Install the dependency:

```bash
pip install reportlab
```

## Running the Application

Run:

```bash
python main.py
```

Then choose an option from the CLI menu.

The application automatically creates `invoice.json` when the first invoice is saved and creates the `invoices/` directory for generated PDFs.

## Concepts Practiced

This project was built as a hands-on Python project and covers several concepts:

* Object-oriented programming
* Classes and objects
* Instance methods
* Lists and dictionaries
* Loops
* Conditional statements
* Functions
* Modules and imports
* JSON serialization/deserialization
* File handling
* `pathlib`
* Date handling with `datetime`
* String formatting
* List comprehensions
* Generator expressions
* `next()` with a default value
* Exception-free input flow
* Working with external libraries
* PDF generation with ReportLab

## Data Flow

The application follows this basic flow:

```text
User Input
    ↓
Invoice / LineItem objects
    ↓
to_dict()
    ↓
JSON storage
    ↓
load_invoice()
    ↓
CLI display / PDF generation
```

This separation keeps the invoice data model, storage logic, PDF generation, and user interface independent from each other.

## Future Improvements

Possible improvements include:

* Input validation and error handling
* Editing existing invoices
* Deleting invoices
* Updating invoice payment status
* Searching invoices
* Better PDF styling
* Customer contact information
* Tax and discount support
* Invoice due dates
* Database storage instead of JSON
* Proper CLI argument parsing with Typer
* Rich terminal output
* Automated tests
* Better invoice ID generation that doesn't depend on the number of stored invoices

## License

This project is for learning and experimentation.
