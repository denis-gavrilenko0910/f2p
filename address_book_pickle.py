import pickle
from collections import UserDict
from datetime import datetime, timedelta
import re
from prettytable import PrettyTable
from fuzzywuzzy import process
table = PrettyTable()


COMMANDS = [
    "hello",
    'help',
    "add",
    "change",
    "phone",
    "all",
    "add-birthday",
    "show-birthday",
    "birthdays",
    "search",
    "exit",
    "close"
]

COMMANDS_HELP = [
    "hello",
    'help',
    "add [Name] [Phone]",
    "change [Name] [Old Phone] [New Phone]",
    "phone [Name]",
    "all",
    "add-birthday [Name] [Birthday]",
    "show-birthday [Name]",
    "birthdays",
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
    if phone not in [p.value for p in self.phones]:
      self.phones.append(Phone(phone))

  def add_email(self, email):
    if self.is_valid_email(email):
        self.email = email
    else:
      raise ValueError('Invalid email format. Please use "example@domain.com".')
    
  def is_valid_email(self, email):
    email_regex = r'(\w+)@(\w+\.\w+)'
    return re.match(email_regex, email) is not None


  def find_phone(self, phone):
    for phone_obj in self.phones:
      if phone_obj.value == phone:
        return phone_obj
      

  def remove_phone(self, phone):
    rem_phone = self.find_phone(phone)
    if rem_phone:
      self.phones.remove(rem_phone)


  def edit_phone(self, old_phone, new_phone):
    phone_obj = self.find_phone(old_phone)
    if phone_obj:
      phone_obj.value = new_phone


  def __str__(self):
    birthday = self.birthday.value.strftime('%d.%m.%Y') if self.birthday else '-'
    return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {birthday}, email: {self.email.value if self.email else '-'}, address: {self.address.value if self.address else '-'}"


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
  cmd, *args = user_input.split()
  cmd = cmd.strip().lower()
  return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
  name, phone, email, *_ = args
  record = book.find(name)
  message = "Contact updated."
  if not phone.isdigit() or len(phone) != 10:
    return 'Phone number must be 10 digits'
  
  if not re.match(r'(\w+)@(\w+\.\w+)', email):
    return 'Invalid email format. Please use "example@domain.com".'
  
  if record is None:
    record = Record(name)
    book.add_record(record)
    message = "Contact added."

  if phone:
    try:
      record.add_phone(phone)
    except ValueError:
      return 'Invalid phone number. it must be 10 digits.'
    
  if email:
    try:
      record.add_email(email)
    except ValueError:
      return 'Invalid email format. Please use "example@domain.com".'
  return message


@input_error
def change_contact(args, book: AddressBook) -> str:
  name, old_phone, new_phone = args
  result = 'Сontact not found'
  record: Record = book.find(name)
  if record:
    if not new_phone.isdigit() or len(new_phone) != 10:
      return 'Phone number must be 10 digits.'
    
    try:
      record.edit_phone(old_phone, new_phone)
      result = 'Contact updated.'
    except ValueError as e:
      result = str(e)
  return result

@input_error
def change_email(args, book: AddressBook) -> str:
  name, new_email = args
  record: Record = book.find(name)
  if not re.match(r'(\w+)@(\w+\.\w+)', new_email):
    return 'Invalid email format. Please use "example@domain.com".'
  
  if record:
    try:
      record.add_email(new_email)
      return 'Email updated successfully.'
    except ValueError:
      return 'Invalid email format. Please use "example@domain.com".'
  return 'Contact not found'



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
def add_birthday(args, book: AddressBook) -> str:
  name, birthday = args
  record: Record = book.find(name)
  if record:
    record.add_birthday(birthday)
    return 'Contact`s birthday added'
  return 'no contact'


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


def search_by_name(name: str, book) -> str:
  record: Record = book.find(name)
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
      print(add_contact(args, book))
    elif command == "change":
      print(change_contact(args, book))
    elif command == "change-email":
      print(change_email(args, book))
    elif command == "phone":
      print(show_phone(args, book))
    elif command == "all":
      print(show_all(book))
    elif command == "add-birthday":
      print(add_birthday(args, book))
    elif command == "show-birthday":
      print(show_birthday(args, book))
    elif command == "birthdays":
      print(birthdays(book))         
    elif command == 'search':
      print(search(args, book))
    elif command == 'help':
      print("Available commands:")
      for cmd in COMMANDS_HELP:
        print(f"- {cmd}")
    else:
      print("Invalid command.")
        

if __name__ == "__main__":
  main()