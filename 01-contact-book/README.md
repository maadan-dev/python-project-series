# Contact Book CLI

A simple command-line contact management application built with Python.

This was the first project in my Python project series. The goal was to practice working with dictionaries, functions, modules, JSON persistence, validation, and basic CRUD operations.

## Features

* Add a contact
* Search contacts by name or phone number
* Delete contacts
* Validate Nigerian phone numbers
* Persist contacts to a JSON file
* Prevent duplicate contact names

## Project Structure

```text
01-contact-book/
├── actions.py       # Contact operations
├── main.py          # CLI and user interaction
├── model.py         # Contact validation
├── storage.py       # JSON file persistence
├── contacts.json    # Saved contacts
├── README.md
└── DESIGN_NOTES.md
```

## How It Works

The application stores contacts in a dictionary using the contact name as the key.

Example:

```json
{
  "Yekeen": {
    "phone": "+2348012345678"
  }
}
```

Contact operations are handled separately from the CLI.

`actions.py` contains functions for:

* Adding contacts
* Searching contacts
* Deleting contacts

`model.py` validates contact names and phone numbers.

`storage.py` handles loading and saving contacts using JSON.

`main.py` provides the command-line interface.

## Phone Validation

The application currently expects Nigerian phone numbers in this format:

```text
+234XXXXXXXXXX
```

The phone number must:

* Start with `+234`
* Contain 14 characters in total
* Contain only digits after `+234`

## Running the Project

Make sure Python is installed, then run:

```bash
python main.py
```

The application will create `contacts.json` when contacts are saved.

## Concepts Practiced

This project introduced/practiced:

* Dictionaries
* Lists and strings
* Functions
* Modules and imports
* Conditional statements
* Loops
* JSON
* File I/O
* Basic validation
* CRUD operations
* Separation of responsibilities
* Working with persistent data

## Example

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

## Project Status

This is an early learning project and intentionally remains simple.

Later projects in the series build on these concepts and introduce more advanced Python and software engineering concepts.
