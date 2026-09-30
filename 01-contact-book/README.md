# Contact Book CLI

Command-line contact manager built with Python. Project 1 of my [Python project series](../README.md).

Goal: practice dictionaries, functions, modules, JSON persistence, validation and basic CRUD.

## Features

- Add a contact
- Search contacts by name or phone number
- Delete contacts
- Validate Nigerian phone numbers
- Persist contacts to a JSON file
- Prevent duplicate contact names

## Run it

```bash
git clone https://github.com/maadan-dev/python-project-series.git
cd python-project-series/01-contact-book
python main.py
```

`contacts.json` is created when the first contact is saved.

```text
1. Add contact
2. Search contact
3. Delete contact
4. Quit

Choose: 1
Enter a name: Yekeen
Enter phone: +2348012345678

Contact added
```

## Structure

```text
01-contact-book/
├── actions.py        # add, search, delete
├── main.py           # CLI and user interaction
├── model.py          # name and phone validation
├── storage.py        # JSON load/save
├── README.md
└── DESIGN_NOTES.md
```

Contacts are stored in a dictionary keyed by name:

```json
{
  "Yekeen": {
    "phone": "+2348012345678"
  }
}
```

Phone numbers must start with `+234`, be 14 characters long, and contain only digits after `+234`.

## What I learned

- Structuring a project across files, one responsibility per file
- Validating data and acting on data are different jobs and shouldn't live in the same place
- Reading and writing JSON to persist data between runs
- A unique-name constraint makes a dict of dicts a better fit than a list of dicts, because lookups by name become direct
- Writing ASSUMES / PROMISES / WILL NOT HANDLE before each function. This became the basis of my [engineering notes](https://maadan.dev/writing)

## What broke, and what fixed it

- **`load_contacts` missing parentheses.** I assigned the function instead of calling it, which caused a `TypeError`. Fix: `contacts = load_contacts()`. Lesson: referencing a function is not calling it.
- **`f.write()` with a dictionary.** `write()` expects a string. Fixed with `json.dump()`.
- **`contact.json` vs `contacts.json`.** One part of the program wrote to one file, another read from a different one. No error, just a second file, so persistence looked broken. Some bugs don't crash. The program does exactly what it was told, and the instructions disagree.

## Next

Project 2: [Study Planner Agent](../02-study-planner).
