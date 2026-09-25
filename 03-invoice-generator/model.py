import datetime

class LineItem:
    def __init__(self, description, quantity, unit_price):
        self.description = description
        self.quantity = quantity
        self.unit_price = unit_price

    def total(self):
        return self.quantity * self.unit_price

    def to_dict(self):
        return {
            'description': self.description,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'total': self.total()
        }


class Invoice:
    def __init__(self, client_name, status, invoice_id=None):
        self.name = client_name
        self.items = []
        self.status = status
        self.date = datetime.date.today()
        self.invoice_id = invoice_id
        

    def add_item(self, item):
        self.items.append(item)

    def total(self):
        total = 0

        for item in self.items:
            total += item.total()

        return total

    def to_dict(self):
        return {
            'name': self.name,
            'items': [item.to_dict() for item in self.items],
            'status': self.status,
            'date': self.date.isoformat(),
            'invoice_id': self.invoice_id,
            'total': self.total()
        }