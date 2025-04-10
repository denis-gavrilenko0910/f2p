from prettytable import PrettyTable
from collections import UserDict
from address_book_pickle import Field
from datetime import datetime
from address_book_pickle import load_data, save_data

class Note(Field):
  pass

class NoteRecord:
  def __init__(self, note):
    self.note = Note(note)
    self.tags = []
    self.ctreated = datetime.now()

  def __str__(self):
    return f"note: {self.note}"
  
  def edit_note(self, note):
    self.note = Note(note)


class NoteBook(UserDict):
  id = 1
  def add_note(self, note_record: NoteRecord):
    self.data[NoteBook.id] = note_record
    NoteBook.id += 1

  def find_note(self, id_):
    return self.data.get(id_, None)

  def delete_note(self, id_):
    return self.data.pop(id_, None)


def add_note(args, note_book: NoteBook):
  note_text = ' '.join(args)
  note = NoteRecord(note_text)
  note_book.add_note(note)

  return 'Note added successfully!'

def show_notes(note_book: NoteBook):
  table = PrettyTable()
  table.field_names = ['id', 'note text', 'added at']
  for id, note_record in note_book.items():
    table.add_row([id, note_record.note.value, note_record.ctreated.strftime('%d.%m.%Y %H:%M:%S')])
  return table

def delete_note(args, note_book: NoteBook):
  id = int(args[0])
  note = note_book.find_note(id)
  
  if note:
    note_book.delete_note(id)
    return 'Note deleted'
  return 'Note is not found'  

def parse_input(user_input) -> tuple:
  cmd, *args = user_input.split()
  cmd = cmd.strip().lower()
  return cmd, *args


def main():
  filedata = load_data(filename="notebook.pkl")
  note_book = filedata if filedata else NoteBook()
  print("Welcome to the assistant bot!")
  while True:
    user_input = input("Enter a command: ")
    command, *args = parse_input(user_input)
    if command in ["close", "exit"]:
      save_data(note_book, filename="notebook.pkl")
      print("Good bye!")
      break
    elif command == "hello":
      print("How can I help you?")
    elif command == "add-note":
      print(add_note(args, note_book))
    elif command == "all-notes":
      print(show_notes(note_book))  
    elif command == "delete-note":
      print(delete_note(args, note_book))  
    else:
      print("Invalid command.")
        

if __name__ == "__main__":
  main()