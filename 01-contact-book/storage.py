import json
import os

FILE_PATH = "contacts.json"

def load_contacts():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as f:
            data = json.load(f)
    else:
        data = {}

    return data


def save_contacts(contacts):
    with open(FILE_PATH, "w") as f:
        json.dump(contacts, f, indent=2)