from models import validate_contact

def add_contact(contacts, name, phone):
    is_valid = validate_contact(name, phone)
    message = ""

    if is_valid and name not in contacts:
        contacts[name] = {'phone': phone}
        message = "Contact added"
    elif is_valid and name in contacts:
        message = f"{name.capitalize()} already exists"
    else:
        message = "Enter a valid name and phone"

    return contacts, message


def delete_contact(contacts, name):
    message = f"{name} not found"
    if name in contacts:
        del contacts[name]
        message = f"{name} deleted"

    return contacts, message

def search_contact(contacts, query):
    matches = {}
    for name, data in contacts.items():
        if query.lower() in name.lower() or query in data["phone"]:
            matches[name] = data

    if not matches:
        return matches, "No contacts found"

    return matches, f"{len(matches)} contact(s) found"
        