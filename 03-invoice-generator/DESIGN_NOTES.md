# Assumptions

These are things the application assumes will be true when it runs.

### User input

* The user enters a valid number when asked for the number of items.
* The user enters a valid integer for quantity.
* The user enters a valid number for unit price.
* The user enters `1` or `2` when selecting the invoice status.
* The user enters an existing invoice ID when viewing or generating an invoice PDF.
* Client names and item descriptions are provided as text.

### Invoice data

* Every invoice has at least the information required by the `Invoice` class: client name, status, invoice ID, date, and items.
* Quantity and unit price are numeric values.
* The JSON file contains valid invoice data in the structure expected by the application.
* Each stored invoice has an `invoice_id`.
* Each stored invoice has the expected keys such as `name`, `items`, `status`, `date`, and `total`.

### Storage

* `invoice.json` is accessible and writable when saving invoices.
* The application has permission to create the `invoices/` directory.
* The JSON file is stored in the current working directory.
* The application is used by one person/process at a time.

### Invoice IDs

* The number of existing invoices can be used to determine the next invoice number.
* Existing invoices are not manually removed or reordered in a way that causes the generated number to conflict with an existing invoice ID.

### PDF generation

* ReportLab is installed and available.
* The invoice contains a reasonable number of items that can fit on the PDF page.
* The text provided by the user can be rendered by the PDF's default Helvetica font.

# Promises

These are the things the application guarantees when its assumptions are satisfied.

### Invoice calculations

* A line item's total is always calculated as:

```text
quantity × unit price
```

* An invoice's total is calculated from the totals of its line items.
* The stored invoice total is generated from the invoice's actual items rather than being manually entered.

### Invoice IDs

* A newly created invoice receives an ID containing the current date and a sequential number.

For example:

```text
20260925-001
20260925-002
20260925-003
```

### Persistence

* Once an invoice is successfully saved, it is added to `invoice.json`.
* Previously saved invoices are loaded when the application starts or when invoice data is requested.
* Saving an invoice does not replace the existing invoices; the new invoice is appended to the collection.

### Invoice viewing

* If an invoice exists with the requested ID, the application displays its client, status, date, items, and total.
* If no invoice matches the requested ID, the application reports that the invoice was not found.

### PDF generation

* A PDF is generated using the stored invoice data.
* The generated PDF is saved using the invoice ID as part of its filename.

For example:

```text
invoices/INV-20260925-001.pdf
```

# Will Not Handle

These are situations the current version intentionally does not handle.

### Invalid input

The application does not currently handle:

* Non-numeric quantities.
* Non-numeric unit prices.
* Negative quantities.
* Negative prices.
* Empty required fields.
* Invalid menu choices.
* Invalid invoice status selections.

For example, entering:

```text
quantity: abc
```

will cause the current program to fail rather than asking the user to try again.

### Corrupted or invalid storage

The application does not currently handle:

* A corrupted `invoice.json`.
* Invalid JSON syntax.
* Missing keys inside an invoice.
* Manually modified invoice data with an unexpected structure.
* A read/write failure caused by filesystem permissions.

### Invoice management

The current version does not support:

* Editing an existing invoice.
* Deleting an invoice.
* Updating an invoice's payment status.
* Searching invoices by client name.
* Filtering invoices by status.
* Sorting invoices.
* Cancelling or voiding invoices.
* Duplicate invoice detection beyond the current ID-generation approach.

### Invoice IDs

The current ID generation does not guarantee globally unique IDs.

It relies on:

```python
len(invoices) + 1
```

Therefore, it assumes invoices are not removed or manipulated in a way that causes the same date/number combination to be generated again.

### PDF limitations

The PDF generator does not currently handle:

* Multiple PDF pages.
* Very long invoice descriptions.
* A large number of invoice items.
* Text wrapping.
* Automatic page breaks.
* Custom fonts.
* Tax calculations.
* Discounts.
* Currency conversion.
* Company logos or branding.
* Customer addresses or contact information.

### Data storage

The application does not currently provide:

* A database.
* Concurrent access from multiple users.
* Authentication or authorization.
* Cloud synchronization.
* Automatic backups.
* Encryption of stored invoice data.

### User interface

The application is currently a command-line application and does not handle:

* A graphical interface.
* A web interface.
* Mobile access.
* Remote invoice management.

# Scope of the Current Version

The purpose of this version is to provide a simple local invoice workflow:

```text
Create invoice
      ↓
Calculate totals
      ↓
Save invoice as JSON
      ↓
List / View invoice
      ↓
Generate PDF
```

The application deliberately keeps the scope small. More advanced validation, storage, invoice management, and PDF features can be added as the project evolves.
