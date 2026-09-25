from storage import load_contacts, save_contacts
import actions

contacts = load_contacts()


while True:
    print("1. Add contact")
    print("2. Search contact")
    print("3. Delete contact")
    print("4. Quit")

    choice = input("Choose: ")

    if choice == "1":
        # do add stuff
        name = input("Enter a name: ")
        phone = input("Enter phone: ")
        contacts, message = actions.add_contact(contacts, name, phone)
        save_contacts(contacts)
        print(message)
        
    elif choice == "2":
        # do search stuff
        query = input("Enter a name or phone: ")
        matches, message = actions.search_contact(contacts, query)
        print(message)
        print(matches)
    elif choice == "3":
        # do delete stuff
        name = input("Enter a name: ")
        contacts, message = actions.delete_contact(contacts, name)
        save_contacts(contacts)
        print(message)
        
    elif choice == "4":
        break
    else:
        print("Invalid choice")