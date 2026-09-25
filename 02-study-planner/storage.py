# storage.py

import json
import os

FILE_PATH = "history.json"

def save_history(data):
    with open(FILE_PATH, 'w') as f:
        json.dump(data, f, indent=4)

def load_history():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r') as f:
            data = json.load(f)
            return data
    return []