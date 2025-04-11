import pickle
from collections import UserDict
from datetime import datetime, timedelta
import re
from prettytable import PrettyTable
from fuzzywuzzy import process


COMMANDS = [
    "hello",
    'help',
    "add",
    "addall",
    "remove",
    "edit",
    "delete",
    "phone",
    "all",
    "show-birthday",
    "birthdays",
    "search",
    "exit",
    "close"
]

HELP = [
    "hello",
    'help',
    "add",
    'addall',
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


class Field:
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return str(self.value)
  

class Name(Field):
  pass


class Phone(Field):
  def __init__(self, value: str):
    if value.isdigit() and len(value) == 10:
      super().__init__(value)
    else:
      raise ValueError('Incorrect phone number')
    

class Birthday(Field):
  def __init__(self, value):
    try:
      brth_date = datetime.strptime(value, '%d.%m.%Y')
      super().__init__(brth_date)
    except ValueError:
      raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Address(Field):
  pass

class Email(Field):
  def __init__(self, value):
    if not re.match(r'\w+@\w+\.\w+', value):
      raise ValueError('Invalid email format')
    super().__init__(value)

class Address(Field):
  pass


class Email(Field):
  pass


class Record:
  def __init__(self, name):
    self.name = Name(name)
    self.phones = []
    self.birthday = None
    self.email = None
    self.address = None
  

  def add_birthday(self, birthday):
    self.birthday = Birthday(birthday)


  def add_phone(self, phone):
    if not any(p.value == phone for p in self.phones):
      self.phones.append(Phone(phone))
    else:
      raise ValueError('This phone is already added')  

  def add_email(self, email):
    self.email = Email(email)

  def add_address(self, address):
    self.address = Address(address)

  def find_email(self):
    if self.email:
      return self.email
    return 'Contact do not have email'

  def remove_email(self):
    rem_email = self.find_email
    if rem_email:
      self.email = None
      return 'Email removed'
    return 'No email to remove'

  def find_address(self):
    if self.address:
      return self.address
    return 'Contact do not have address'
  
  def remove_address(self):
    rem_address = self.find_address
    if rem_address:
      self.address = None
      return 'Address removed'
    return 'No address to remove'
  
  def find_birthday(self):
    if self.birthday:
      return self.birthday
    return 'Contact does not have birthday'
  
  def remove_birthday(self):
    rem_birthday = self.find_birthday
    if rem_birthday:
      self.birthday = None
      return 'Birthday removed'
    return 'No birthday to remove'
  

  def find_phone(self, phone):
    for phone_obj in self.phones:
      if phone_obj.value == phone:
        return phone_obj
    return 'Contact do not have phones'
      

  def remove_phone(self, phone):
    rem_phone = self.find_phone(phone)
    if rem_phone:
      self.phones.remove(rem_phone)
      return 'Phone removed'
    return 'No phone to remove'  


  def edit_phone(self, old_phone, new_phone):
    phone_obj = self.find_phone(old_phone)
    if phone_obj:
      phone_obj.value = Phone(new_phone)

  def edit_email(self, new_email):
    self.email = Email(new_email)

  def edit_address(self, new_address):
    self.address = Address(new_address)

  def edit_birthday(self, new_birthday):
    self.birthday = Birthday(new_birthday)     


  def __str__(self):
    birthday = self.birthday.value.strftime('%d.%m.%Y') if self.birthday else '-'
    email = self.email.value if self.email else '-'
    address = self.address.value if self.address else '-'
    phones = ';'.join(p.value for p in self.phones) if self.phones else '-'
    return f"Contact: {self.name.value}, Phones: {phones}, Email: {email}, Address: {address}, birthday: {birthday}"
  
  
class AddressBook(UserDict):
  def add_record(self, record: Record):
    self.data[record.name.value] = record


  def find(self, name) -> Record:
    if name in self.data:
      return self.data[name]


  def find_by_ph(self, phone) -> Record:
    for contact in self.data.values():
      if phone in [p.value for p in contact.phones]:
        return contact
    return None


  def find_by_brthd(self, birthday) -> Record:
    for contact in self.data.values():
      if contact.birthday is not None and Birthday(birthday).value == contact.birthday.value:
        yield contact
    return (None,)
    

  def find_by_mail(self, email) -> Record:
    for contact in self.data.values():
        if contact.email is not None and email == contact.email.value:
          return contact
    return None


  def find_by_addr(self, address) -> Record:
    for contact in self.data.values():
      if contact.address is not None and address == contact.address.value:
        return contact
    return None


  def get_upcoming_birthdays(self, days):
        today = datetime.today().date()
        end_date = today + timedelta(days=days)
        list_of_birthdays = []

        for record in self.data.values():
            if record.birthday:
                birthday = record.birthday.value.date()
                birthday_this_year = birthday.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                if today <= birthday_this_year <= end_date:
                    list_of_birthdays.append({
                        "name": record.name.value,
                        "birthday": birthday_this_year.strftime("%Y-%m-%d")
                    })

        return list_of_birthdays


  def delete(self, name):
    del_contact = self.find(name)
    if del_contact:
      self.data.pop(name, None)


def input_error(func):
  def inner(*args, **kwargs):
    try:
      return func(*args, **kwargs)
    except ValueError:
      return "Give me name and phone please."
    except IndexError:
      return "Give me the name."
    except KeyError:
      return "No such contact."
  return inner


def parse_input(user_input) -> tuple:
  user_input = user_input.strip()
  if not user_input:
    return 'empty', []
  cmd, *args = user_input.split()
  cmd = cmd.strip().lower()
  return cmd, *args


@input_error
def add_contact(book: AddressBook):
  name = input('Enter the name: ')
  record = book.find(name)
  if record is None:
    record = Record(name)
    book.add_record(record)
    return f'Contact {name} added.'
  return "Contact alreade exists"


@input_error
def remove_contact(book: AddressBook):
  name = input('Which contact do you want to delete? ')
  record = book.find(name)
  if record:
    book.delete(name)
    return f'Contact {name} deleted.'
  return 'Contact not exists'


@input_error
def show_phone(args, book: AddressBook) -> str:
  name = args[0]
  record: Record = book.find(name)
  if record:
    result = f"phones: {'; '.join(p.value for p in record.phones)}"
    return result 
  return 'No contact with this phone number.'


@input_error
def show_all(book: AddressBook) -> str:
  result = ''
  for name, record in book.data.items():
    result += f'{record}\n'
  if not result:
    return 'no contacts :('
  return result


@input_error
def show_birthday(args, book: AddressBook) -> str:
  name = args[0]
  record: Record = book.find(name)
  if record:
    birthday = record.birthday.value.strftime('%d.%m.%Y') if record.birthday else '-'
    return birthday
  return 'The contact is not found'


@input_error
def birthdays(args, book):
    if len(args) != 1:
        raise KeyError
    days = int(args[0])
    upcoming_birthdays = book.get_upcoming_birthdays(days)
    if not upcoming_birthdays:
        return f"No birthdays in the next {days} days."
     
    table = PrettyTable()
    table.field_names = ["Name", "Birthday", "Days Left"]

    
    for entry in upcoming_birthdays:
        name = entry["name"]
        birthday = entry["birthday"]
        days_left = (datetime.strptime(birthday, "%Y-%m-%d").date() - datetime.today().date()).days
        table.add_row([name, birthday, days_left])

    return table

@input_error
def add_all(book: AddressBook):
  name = input('Enter the name where you want add informations: ').capitalize()
  record = book.find(name)
  if record is None:
    record = Record(name)
    book.add_record(record)
    print(f'Contact {name} added.')

    while True:
      phone = input('Enter valid phone number or press Enter to skip: ')
      if phone == '':
        break
      try:
        record.add_phone(phone)
        print(f'Phone {phone} added.')
      except ValueError:
        print('Invalid phone number. Please enter a valid 10-digit number ')

    while True:
      email = input('Enter valid email or press Enter to skip: ')
      if email == '':
        break
      try:
        record.add_email(email)
        print(f'Email {email} added')
        break
      except ValueError:
        print('Invalid email format. Please enter a valid email: ')

    address = input('Enter address or press Enter to skip: ')
    if address != '':
      record.add_address(address)
      print(f'Address {address} added.')

    birthday = input('Enter bitrhday DD.MM.YYYY or press Enter to skip: ')
    while True:
      if birthday == '':
        break
      try:
        record.add_birthday(birthday)
        print(f'Birthday {birthday} added.')
        break
      except ValueError:
        print('Invalid date format. Please use DD.MM.YYYY .')
  else:
    return 'Contact already exists.'      

@input_error
def remove_contact_info(book: AddressBook):
  name = input('Which contact do you want to edit? ').capitalize()
  record = book.find(name)
  if record:
    info_type = input('What do you want to remove? (phone, email, address, birthday)').lower()
    
    if info_type == 'phone':
      if len(record.phones) == 1:
        record.remove_phone(record.phones[0].value)
        return f'Phone {record.phones[0].value} removed from {name}'
      elif len(record.phones) > 1:
        for phone in record.phones:
          print(phone.value)
        phone = input('Enter the phone number you want to remove: ')
        return record.remove_phone(phone)
      else:
        return f'Contact {name} has no phone.'

    elif info_type == 'email':
      if record.email:
        record.remove_email()
        return f'Email removed from {name}.'
      else:
        return f'Contact {name} has no email.'

    elif info_type == 'address':
      if record.address:
        record.remove_address()
        return f'Address removed from {name}.'
      else:
        return f'Contact {name} has no address.'

    elif info_type == 'birthday':
      if record.birthday:
        record.remove_birthday()
        return f'Birthday removed from {name}.'
      else:
        return f'Contact {name} has no birthday.'

    else:
      return "Invalid option. Please choose from: phone, email, address, birthday"
    
  return "No such contact."

@input_error
def edit_contact_info(book: AddressBook):
  name = input('Enter the contact name: ').capitalize()
  record = book.find(name)
  if record:
    info_type = input('What do you want to edit? (phone, email, address, birthday)').lower()

    if info_type == 'phone':
      if record.phones:
        print(f'{name} phone numders:')
        for phone in record.phones:
          print(f'- {phone.value}')
        choice = input('Do you want to add or change? (add/change): ').lower()
        if choice == "add":
          while True:
            new_phone = input('Enter phone number: ')
            try:
              record.add_phone(new_phone)
              return f'Phone {new_phone} added to {name}'
            except ValueError:
              print('Invalid phone number. Please use 10-digit phone')
        elif choice == 'change':
          while True:
            old_phone = input('Enter phone number you want to change: ')
            new_phone = input('Enter the new phone number: ')
            try:
              record.edit_phone(old_phone, new_phone)
              return f"{old_phone} changed to {new_phone}"
            except ValueError:  
              print('Invalid phone number. Please use 10-digit phone')
            except AttributeError:
              print('No such phone number')
      else:
        while True:
          new_phone = input('Enter phone number: ') 
          try:
            record.add_phone(new_phone)
            return f'Phone {new_phone} added to {name}.'
          except ValueError:  
                print('Invalid phone number. Please use 10-digit phone')
    
    elif info_type == 'email':
      choice = input('Do you want add or change? (add/change): ').lower()
      if choice == 'add':
        if not record.email:
          while True:
            new_email = input('Enter valid email: ')
            try:
              record.add_email(new_email)
              return f'{new_email} added to {name}'
            except ValueError:
              print('Ivalid email format.')
        else:
          return f'{name} have email'
      elif choice == 'change':
        if record.email:
          while True:
            new_email = input('Enter valid email: ')
            try:
              record.edit_email(new_email)
              return f'{new_email} changed to {name}'
            except ValueError:
              print('Ivalid email format.')
        else:
          return f'{name} have not email'
        
    elif info_type == 'birthday':
      choice = input('Do you want add or change? (add/change): ').lower()
      if choice == 'add':
        if not record.birthday:
          while True:
            new_birthday = input('Enter birthday format DD.MM.YYYY: ')
            try:
              record.add_birthday(new_birthday)
              return f'{new_birthday} added to {name}'
            except ValueError:
              print('Ivalid birthday format. Please use DD.MM.YYYY')
        else:
          return f'{name} have birthday'
      elif choice == 'change':
        if record.birthday:
          while True:
            new_birthday = input('Enter birthday format DD.MM.YYYY: ')
            try:
              record.edit_birthday(new_birthday)
              return f'{new_birthday} changed to {name}'
            except ValueError:
              print('Ivalid birthday format. Please use DD.MM.YYYY')
        else:
          return f'{name} have not email' 

    elif info_type == 'address':
      choice = input('Do you want add or change? (add/change): ').lower()
      if choice == 'add':
        if not record.address:
          new_address = input('Enter address: ')
          record.add_address(new_address)
          return f'{new_address} added to {name}.'
        else:
          print(f'{name} have address')
      elif choice == 'change':
        if record.address:
          new_address = input('Enter address: ')
          record.edit_address(new_address)
          return f'{new_address} changed to {name}.'
        else:
          print(f'{name} have not address')

  else:
    return 'No such contact'        
             

def search_by_name(name: str, book) -> str:
  record: Record = book.find(name.capitalize())
  if record:
    return record
  return 'No such contact.'


def search_by_phone(phone: str, book) -> str:
  record: Record = book.find_by_ph(phone)
  if record:
    return record
  return f'No contact with this Phone: {phone}.'


def search_by_birthday(birthday: str, book) -> str:
  records = book.find_by_brthd(birthday)
  if records == (None,):
    return f'No contact with this Birthday: {birthday}.'
  answer = ""
  for record in records:
    answer += record.__str__() + "\n"
  return answer


def search_by_email(email: str, book) -> str:
  record: Record = book.find_by_mail(email)
  if record:
    return record
  return f'No contact with this Email: {email}.'


def search_by_address(address: str, book) -> str: 
  record: Record = book.find_by_addr(address)
  if record:
    return record
  return f'No contact with this Address: {address}.'


@input_error
def search(args, book: AddressBook) -> str:
  comms = {'name': search_by_name, 'phone': search_by_phone, 'birthday': search_by_birthday, 'email': search_by_email, 'address': search_by_address}
  return comms[args[0]](args[1], book)


def suggest_command(user_input, commands):
    best_match = process.extractOne(user_input, commands)
    if best_match and best_match[1] > 60:  # Если схожесть больше 60%
        return best_match[0]


def save_data(book, filename="addressbook.pkl"):
  with open(filename, "wb") as f:
    pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
  try:
    with open(filename, "rb") as f:
      return pickle.load(f)
  except FileNotFoundError:
    return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено
  

def main():
  filedata = load_data() 
  book = filedata if filedata else AddressBook()
  print("\nWelcome to the assistant bot!\nIf you need help, type 'help'.\n")
  while True:
    user_input = input("Enter a command: ")
    command, *args = parse_input(user_input)
    if command not in COMMANDS:
            suggestion = suggest_command(command, COMMANDS)
            if suggestion:
                
                choice = input(f"Did you mean '{suggestion}'? (Y/N): ").strip().lower()
                if choice == 'y':
                    command = suggestion
                else:
                    print("Invalid command. Please try again.")
                    continue
            else:
                print("Invalid command. Please try again.")
                continue
            

    if command in ["close", "exit"]:
      save_data(book)
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
    elif command == 'help':
      print("Available commands:")
      for cmd in HELP:
        print(f"- {cmd}")
    else:
      print("Invalid command.")
        

if __name__ == "__main__":
  main()