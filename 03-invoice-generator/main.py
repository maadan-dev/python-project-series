from storage import load_invoice, save_invoice, generate_invoice_id
from model import LineItem, Invoice
from generator import generate_pdf

while True:
    print("1. Create invoice")
    print("2. List invoices")
    print("3. View invoice")
    print("4. Generate Invoice PDF")

    choice = input("Enter a number: ").strip()

    if choice == '1':
        
        name = input("Enter client name: ").strip()
        print("1. Paid")
        print("2. Unpaid")

        status_choice = input()
        status = "paid" if status_choice == '1' else "unpaid"

        invoice_id = generate_invoice_id()

        num_of_items = input("Enter the number of Items: ").strip()
        new_invoice = Invoice(name, status, invoice_id)


        for i in range(int(num_of_items)):
            description = input("Enter description ").strip()
            quantity = input("Enter Number of quantity: ").strip()
            quantity = int(quantity)
            unit_price = input("Enter unit price: ")
            unit_price = float(unit_price)
            new_invoice.add_item(LineItem(description, quantity, unit_price))
        save_invoice(new_invoice.to_dict())
        generate_pdf(new_invoice.to_dict())

        

    elif choice == '2':
        invoices = load_invoice()
        if not invoices:
            print("No invoices found.")
        else:
            for i, invoice in enumerate(invoices, 1):
                id = invoice['invoice_id']
                name = invoice['name']
                total = invoice['total']
                status = invoice['status']
                print(f"{i}. INV-{id} | {name} | ${total} | {status}")

    elif choice == '3':
        id = input("Enter invoice ID: ").strip()
        invoices = load_invoice()
        result = next((inv for inv in invoices if inv['invoice_id'] == id), None)
        

        if not result:
            print("Invoice not found")
        else:
            name = result['name']
            items = result['items']
            status = result['status']
            date = result['date']
            total = result['total']
            invoice_id = result['invoice_id']

            length = 34

            # Header
            print("=" * length)
            print("INVOICE".center(length, "="))
            print("=" * length)

            print(f"{'Date: ' + date:>{length}}")
            print(f"{'Invoice ID: ' + invoice_id:>{length}}\n")

            print(f"Customer: {name.capitalize()}")
            print(f"Status:   {status}")
            print("-" * length)

            print(f"{'DESCRIPTION':<24}{'UNIT PRICE':>10}")
            print("-" * length)

            for item in items:
                description = item['description']
                quantity = item['quantity']
                total_a = item['total']
                print(f"{description:<18} X {quantity} {total_a:>10.2f}")

            print("=" * length)

            print(f"{'TOTAL:':<24}${total:>9.2f}")
            print("=" * length)
    elif choice == '4':
        id = input("Enter invoice ID: ").strip()
        invoices = load_invoice()
        invoice = next((inv for inv in invoices if inv['invoice_id'] == id), None)
        if not invoice:
            print(f"No invoice with ID {id}")
        else:
            generate_pdf(invoice)
            print("Generated Invoice pdf succesfully!")