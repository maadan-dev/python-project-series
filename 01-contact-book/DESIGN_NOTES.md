# Design Notes

This document describes the assumptions, promises, and current limitations of the Contact Book.

The purpose is to make the boundaries of the application explicit rather than assuming the code will handle situations it was not designed for.

## Assumptions

### Contact names

* A contact name is expected to be a non-empty string.
* Contact names are used as dictionary keys.
* Each contact name is expected to be unique.
* The application treats names with different capitalization as different keys.

For example:

```text
Yekeen
yekeen
YEKEEN
```

are technically different contact names.

### Phone numbers

* Phone numbers are expected to use the Nigerian `+234` format.
* The phone number must contain exactly 14 characters.
* The characters after `+234` must all be digits.
* The application assumes the phone number is provided as a string.

### Storage

* Contact data is stored in `contacts.json`.
* The JSON file is expected to contain a dictionary.
* The application has permission to read and write the file.
* The application is expected to run from the directory containing `contacts.json`.

### Search

* Search is performed against both contact names and phone numbers.
* Name searches are case-insensitive.
* Phone searches are not explicitly normalized before comparison.

## Promises

### Adding contacts

`add_contact()` promises that:

* A contact is only added when the name and phone number pass validation.
* A contact with an existing name will not be added again.
* The function returns the contacts dictionary and a message describing the result.

### Deleting contacts

`delete_contact()` promises that:

* An existing contact will be removed.
* Attempting to delete a contact that does not exist will leave the contact data unchanged.
* The function returns the contacts dictionary and a message describing the result.

### Searching contacts

`search_contact()` promises that:

* Matching contacts are returned as a dictionary.
* Name matching is case-insensitive.
* Phone numbers can be searched.
* If there are no matches, the function returns an empty dictionary and a message saying no contacts were found.

### Persistence

`load_contacts()` promises that:

* Existing contacts are loaded from `contacts.json`.
* If the file does not exist, an empty contact dictionary is returned.

`save_contacts()` promises that:

* The current contacts dictionary is serialized to JSON.
* Existing stored contact data is replaced with the current state.

## Will Not Handle

The current version does not handle:

### Input errors

* Empty input from the command line beyond the basic name validation.
* Invalid menu input beyond displaying `"Invalid choice"`.
* Unexpected input types passed directly to the functions.

### Phone number variations

The application does not currently handle:

```text
08012345678
+234 801 234 5678
+234-801-234-5678
```

It only accepts the specific `+234XXXXXXXXXX` format.

### Duplicate names

The application does not detect duplicate people who have different names but the same phone number.

For example:

```text
Yekeen → +2348012345678
Abdulyekeen → +2348012345678
```

Both can exist because uniqueness is based on the contact name.

### Name normalization

The application does not normalize names before storing them.

Therefore:

```text
Yekeen
yekeen
Yekeen 
```

may be treated differently.

### Storage failures

The application does not currently handle:

* Corrupted JSON.
* Invalid JSON structure.
* File permission errors.
* Disk/storage failures.
* Concurrent writes.

### Data management

The application does not currently support:

* Editing contacts.
* Updating phone numbers.
* Sorting contacts.
* Importing contacts from another file.
* Exporting contacts to another format.
* Contact groups.
* Multiple phone numbers per contact.
* Email addresses.
* Addresses or other contact information.

### User interface

The application is currently CLI-only.

It does not provide:

* A graphical interface.
* A web interface.
* Authentication.
* Multiple users.

## Design Decisions

### Dictionary for contacts

A dictionary was chosen because contact names can act as keys, making it straightforward to look up whether a name already exists.

```python
contacts[name] = {
    "phone": phone
}
```

### JSON for persistence

JSON was chosen because the data is small and structured, and it allows the dictionary to be saved and loaded without introducing a database.

### Separate modules

The application separates:

```text
main.py      → interaction
actions.py   → operations
model.py     → validation
storage.py   → persistence
```

This prevents `main.py` from containing all of the application's logic.

## Current Boundary

The project is intentionally small.

Its purpose is not to be a production contact-management system. It is the first step in a series of projects designed to progressively introduce more complex programming and engineering concepts.
