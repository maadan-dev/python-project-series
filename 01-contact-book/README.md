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


## What I Learned

* How to structure a Python project across multiple files, with each file having a single responsibility.
* The difference between **validating data** and **acting on data**, and why those responsibilities shouldn't live in the same place.
* How to read and write JSON files to persist data between program sessions.
* How a unique-name constraint can influence the choice of data structure: using a dictionary of dictionaries instead of a list of dictionaries makes direct name-based lookups more straightforward.
* How to apply the **ASSUMES / PROMISES / WILL NOT HANDLE** framework before writing functions. This became the foundation for the approach I later wrote about in my engineering notes.


## What I Struggled With and How I Fixed It

### 1. `load_contacts` was missing parentheses

I accidentally assigned the function itself instead of calling it. This meant I was working with a function reference rather than the contacts it was supposed to return, which eventually caused a `TypeError`.

**Fix:** I added `()` to actually execute the function:

```python
contacts = load_contacts()
```

The important lesson was understanding the difference between **referencing a function** and **calling a function**.

### 2. Using `f.write()` with a dictionary

I initially tried to use `f.write()` to save the contacts dictionary directly to a file. That doesn't work because `write()` expects a string, not a Python dictionary.

**Fix:** I switched to `json.dump()`, which converts the Python dictionary into JSON and writes it to the file.

### 3. `contact.json` vs `contacts.json`

I had a filename typo where one part of the program used `contact.json` while another used `contacts.json`.

The program didn't immediately fail — it simply created a second file. That made it look like persistence wasn't working because I was writing to one file and reading from another.

**Fix:** I made sure both loading and saving used the same filename.

The bigger lesson was that some bugs don't produce an obvious error. Sometimes the program behaves exactly as instructed — the instructions are just inconsistent.
