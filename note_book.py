from prettytable import PrettyTable
from collections import UserDict
from address_book_pickle import Field
from datetime import datetime
from address_book_pickle import input_error

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

  def add_tag(self, tag):
    self.tags.append(tag)
  

class NoteBook(UserDict):
  def add_note(self, note_record: NoteRecord):
    id = len(self.data) + 1
    self.data[id] = note_record
    return id

  def find_note(self, id_):
    return self.data.get(id_, None)

  def delete_note(self, id_):
    return self.data.pop(id_, None)

@input_error
def add_note(args, note_book: NoteBook):
  if not args:
    raise ValueError('Please enter note text!')
  note_text = ' '.join(args)
  note = NoteRecord(note_text)
  id = note_book.add_note(note)
  return f'Note {id} added successfully!'

@input_error
def add_tag(args, note_book: NoteBook):
  if len(args) < 2:
    raise ValueError('Please enter note ID and tag(s)')
  id, *tags = args
  if not id.isdigit():
    raise ValueError('Tag ID must be a number')
  note_record: NoteRecord = note_book.find_note(int(id))

  if note_record:
    for tag in tags:
      note_record.add_tag(tag)
    return f'Tags successfully added for {id} note'
  return 'Note not found'


def show_notes(note_book: NoteBook):
  table = PrettyTable()
  table.field_names = ['id', 'note text', 'added at', 'tags']
  for id, note_record in note_book.items():
    tags_text = '\n'.join(note_record.tags)
    table.add_row([id, note_record.note.value, note_record.ctreated.strftime('%d.%m.%Y %H:%M:%S'), tags_text])
  return table

@input_error
def find_by_tag(args, note_book):
    if len(args) < 1:
      raise ValueError('Please enter tag!')
    tag = args[0]
    table = PrettyTable()
    table.field_names = ['id', 'note text', 'added at', 'tags']
    for id, note_record in note_book.items():
      if tag in note_record.tags:
        tags_text = '\n'.join(note_record.tags)
        table.add_row([id, note_record.note.value, note_record.ctreated.strftime('%d.%m.%Y %H:%M:%S'), tags_text])
    return table

@input_error
def delete_note(args, note_book: NoteBook):
  if len(args) < 1:
    raise ValueError('Please enter note ID!')
  id = args[0]
  if not id.isdigit():
    raise ValueError('Tag ID must be a number')
  note = note_book.find_note(int(id))
  
  if note:
    note_book.delete_note(id)
    return 'Note deleted'
  return 'Note is not found'  

def parse_input(user_input) -> tuple:
  cmd, *args = user_input.split()
  cmd = cmd.strip().lower()
  return cmd, *args
