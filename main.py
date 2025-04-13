import pickle
from address_book_pickle import load_data, AddressBook, parse_input, suggest_command, save_data, add_contact, add_all, remove_contact_info, edit_contact_info, remove_contact, show_phone,show_all, show_birthday, birthdays, search
from note_book import NoteBook, add_note, show_notes, delete_note, add_tag, find_by_tag


COMMANDS = [
    "hello",
    'help',
    "add",
    'add-note',
    "remove",
    "edit",
    "delete",
    "phone",
    "all",
    "show-birthday",
    "birthdays",
    "search",
    'show-all-notes',
    'delete-note',
    'add-tag',
    'find-tag',
    "exit",
    "close"
]

HELP = [
    "hello - <>",
    'help - <>',
    "add",
    'add-note',
    'remove',
    "edit",
    'delete',
    "phone [Name]",
    "all",
    "show-birthday [Name]",
    "birthdays [Days]",
    "search [Name|Phone|Birthday|Email|Address] [Value]",
    "exit",
    "close"
]


def main():
  filedata = load_data()
  book = filedata if filedata else AddressBook()
  filedata = load_data(filename="notebook.pkl")
  note_book = filedata if filedata else NoteBook()
  print("\nWelcome to the assistant bot!\nIf you need help, type 'help'.\n")
  while True:
    user_input = input("Enter a command: ")
    command, *args = parse_input(user_input)
    if command not in COMMANDS:
            suggestions = suggest_command(command, COMMANDS)
            if suggestions:
              for suggestion in suggestions:  
                choice = input(f"Did you mean '{suggestion}'? (Y/N): ").strip().lower()
                if choice == 'y':
                    command = suggestion
                    break
                elif choice == 'n':
                  continue
                else:
                    print("Invalid command. Please try again.")
                    break
              else:
                print("Invalid command. Please try again.")
              continue
            else:
              print("Invalid command. Please try again.")
              continue

            
    try:
      if command in ["close", "exit"]:
        save_data(book)
        save_data(note_book, filename="notebook.pkl")
        print("Good bye!\nSaving data...")
        break
      elif command == "hello":
        print("How can I help you?")
      elif command == "add":
        print(add_contact(book))
      elif command == "addall":
        print(add_all(book))
      elif command == "remove":
        print(remove_contact_info(book))
      elif command == "edit":
        print(edit_contact_info(book))    
      elif command == "delete":
        print(remove_contact(book))
      elif command == "phone":
        print(show_phone(args, book))
      elif command == "all":
        print(show_all(book))
      elif command == "show-birthday":
        print(show_birthday(args, book))
      elif command == "birthdays":
        print(birthdays(args, book))         
      elif command == 'search':
        print(search(args, book))
      elif command == "add-note":
        print(add_note(args, note_book))
      elif command == "show-all-notes":
        print(show_notes(note_book))  
      elif command == "delete-note":
        print(delete_note(args, note_book))  
      elif command == "add-tag":
        print(add_tag(args, note_book))  
      elif command == "find-tag":
        print(find_by_tag(args, note_book))
      elif command == 'help':
        print("Available commands:")
        for cmd in HELP:
          print(f"- {cmd}")
    except Exception as e:
      print(f'{e}')
          

if __name__ == "__main__":
  main()