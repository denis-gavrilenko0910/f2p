import pickle
from collections import UserDict
from datetime import datetime, timedelta
import re
from prettytable import PrettyTable
from fuzzywuzzy import process


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


  def edit_name(self, new_name):
    if not new_name:
      raise ValueError('Name can not be empty') 
    if new_name == self.name.value:
      raise ValueError('new name is the same as current name')
    self.name = Name(new_name)
    

  def prettytable_for_search(self):
    table = PrettyTable()
    table.field_names = ["Name", "Phones", "Email", "Address", "Birthday"]
    birthday = self.birthday.value.strftime('%d.%m.%Y') if self.birthday else '-'
    email = self.email.value if self.email else '-'
    address = self.address.value if self.address else '-'
    phones = '\n'.join(str(p.value) for p in self.phones) if self.phones else '-'
    table.add_row([self.name.value, phones, email, address, birthday])
    return table
  

  def __str__(self):
    birthday = self.birthday.value.strftime('%d.%m.%Y') if self.birthday else '-'
    email = self.email.value if self.email else '-'
    address = self.address.value if self.address else '-'
    phones = '\n'.join(p.value for p in self.phones) if self.phones else '-'
    return f"Contact: {self.name.value}, Phones: {phones}, Email: {email}, Address: {address}, birthday: {birthday}"
  
  
class AddressBook(UserDict):
  def add_record(self, record: Record):
    self.data[record.name.value] = record

  def find(self, name) -> Record:
    if name in self.data:
      return self.data[name]

  def find_by_phone(self, phone) -> Record:
    for contact in self.data.values():
      if phone in [p.value for p in contact.phones]:
        return contact
    return None

  def find_by_brthd(self, birthday) -> Record:
    bday_with_year = (len(birthday.split('.')) == 3 and len(birthday.split('.')[0]) == 2 and len(birthday.split('.')[1]) == 2 and len(birthday.split('.')[2]) == 4)
    contacts = []
    for contact in self.data.values():
      if contact.birthday is not None and birthday == contact.birthday.value.strftime('%d.%m' + '%Y' * bday_with_year):
        contacts.append(contact)
    return contacts
    
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
    except ValueError as err:
      return str(err)
    except IndexError:
      return "\nGive me the name.\n"
    except KeyError:
      return "\nNo such contact.\n"
  return inner


def parse_input(user_input) -> tuple:
  user_input = user_input.strip()
  if not user_input:
    return 'empty', []
  cmd, *args = user_input.split()
  cmd = cmd.strip().lower()
  return cmd, *args


def suggestion_name(book: AddressBook):
  while True:  
    name = input(f'\nEnter the name: \n').strip()
    if not name:
      print(f'\nName cannot be empty\n')
      continue
    name = name.capitalize()
    break
  if name in book.data:
    return name
  contacts = list(book.data.keys())
  variants = process.extract(name, contacts, limit=None)
  variants = [v[0] for v in variants if v[1]>=60]
  for suggest_name in variants:
    choice = input(f'\nDid you mean {suggest_name}? [Y/N]. Or press Enter to add new contact: \n').strip().upper()
    if choice == 'Y':
      return suggest_name 
    elif choice == 'N':
      continue
    elif choice == '':
      return name      
  else:
    return name


@input_error
def remove_contact(book: AddressBook):
  name = input('\nWhich contact do you want to delete? \n').capitalize()
  record = book.find(name)
  if record:
    book.delete(name)
    return f'\nContact {name} deleted.\n'
  return '\nContact not exists\n'


@input_error
def show_all(book: AddressBook) -> str:
  if not book.data:
    return "\nNo contacts found :(\n"
  table = PrettyTable()
  table.title = "CONTACTS"
  table.field_names = ['NAME', 'PHONES', 'EMAIL', 'ADDRESS', 'BIRTHDAY']
  table.align = 'c'
  table.hrules = 1

  for record in book.data.values():
    birthday = record.birthday.value.strftime('%d.%m.%Y') if record.birthday else '-'
    email = record.email.value if record.email else '-'
    address = record.address.value if record.address else '-'
    phones = '\n'.join(str(p.value) for p in record.phones) if record.phones else '-'

    table.add_row([record.name.value, phones, email, address, birthday])
  return '\n' + str(table) + '\n'


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
  name = suggestion_name(book)
  record = book.find(name)
  
  if record is None:
    record = Record(name)
    book.add_record(record)
    print(f'\nContact {name} added.\n')
  else:
    print(f'\nContact {name} already exist. Go add rest info.')
    print(record.prettytable_for_search())
    print()


  def add_phone():
    if len(record.phones) == 2:
      return f'\nMax 2 phones for contact.\n'
    
    while True:
      validation = f'Enter' + (' EXTENSION' if len(record.phones) >= 1 else "") + f' phone number or press Enter to skip: \n'
      phone = input(validation)
      if phone == '':
        break
      try:
        record.add_phone(phone)
        print(f'\nPhone {phone} added.\n')
        if len(record.phones) == 2:
          return f'\nMax 2 phones for contact.\n'
      except ValueError:
        print(f'\nInvalid phone number. Please enter a valid 10-digit number.\n')


  def add_email():
    if record.email:
      return
    while True:
      email = input(f'Enter the valid email or press Enter to skip:: \n')
      if email == '':
        break
      try:
        record.add_email(email)
        print(f'\nEmail {email} added.\n')
        break
      except ValueError:
        print(f'\nInvalid email format. Please enter a valid email: \n')


  def add_address():
    if record.address:
      return
    address = input(f'Enter address or press Enter to skip: \n')
    if address != '':
      record.add_address(address)
      print(f'\nAddress {address} added.\n')


  def add_birthday():
    if record.birthday:
      return
    while True:
      birthday = input(f'Enter bitrhday DD.MM.YYYY or press Enter to skip: \n')
      if birthday == '':
        break
      try:
        record.add_birthday(birthday)
        print(f'\nBirthday {birthday} added.\n')
        break
      except ValueError:
        print(f'\nInvalid date format. Please use DD.MM.YYYY.\n')
      

  add_phone()
  add_email()
  add_address()
  add_birthday()
  print(record.prettytable_for_search())
  return f'Contact {name} with information succesfully added.\n'
          

@input_error
def remove_contact_info(book: AddressBook):
  name = suggestion_name(book)
  record = book.find(name)
  if record:
    print()
    print(record.prettytable_for_search())
    while True: 
      info_type = input('\nWhat do you want to remove? (phone, email, address, birthday): \n').lower()
      try:
        if info_type == 'phone':
          if not record.phones:
            return f'\nContact {name} has no phone.\n'
          elif len(record.phones) == 1:
            phone_to_remove = record.phones[0].value
            record.remove_phone(phone_to_remove)
            print()
            print(record.prettytable_for_search()) 
            return f'Phone {phone_to_remove} removed from {name}\n'
          elif len(record.phones) > 1:
            for phone in record.phones:
              print(phone.value)
            phone = input('\nEnter the phone number you want to remove: \n')
            record.remove_phone(phone)
            print()
            print(record.prettytable_for_search()) 
            return f'Phone {phone} removed from {name}\n'

        elif info_type == 'email':
          if record.email:
            record.remove_email()
            print()
            print(record.prettytable_for_search()) 
            return f'Email removed from {name}.\n'
          else:
            return f'\nContact {name} has no email.\n'

        elif info_type == 'address':
          if record.address:
            record.remove_address()
            print()
            print(record.prettytable_for_search()) 
            return f'Address removed from {name}.\n'
          else:
            return f'\nContact {name} has no address.\n'

        elif info_type == 'birthday':
          if record.birthday:
            record.remove_birthday()
            print()
            print(record.prettytable_for_search()) 
            return f'Birthday removed from {name}.\n'
          else:
            return f'\nContact {name} has no birthday.\n'
          
        else:
          print('\nUse only:  phone  email  address  birthday\n')
          continue

      except Exception as e:
        print(f"\nInvalid {e}.\n")
    
  return "\nNo such contact.\n"


@input_error
def edit_contact_info(book: AddressBook):
  name = suggestion_name(book)
  record = book.find(name)

  if record:
    print()
    print(record.prettytable_for_search())
    while True: 
      info_type = input('\nWhat do you want to edit? (name, phone, email, address, birthday): \n').lower()
      try:
        if info_type == 'phone':
          if record.phones:
            print(f'\n{name} phone numders:')
            for phone in record.phones:
              print(phone.value)
            while True:
                old_phone = input('\nEnter phone number you want to change: \n')
                new_phone = input('\nEnter the new phone number: \n')
                try:
                  record.edit_phone(old_phone, new_phone)
                  print()
                  print(record.prettytable_for_search()) 
                  return f"Phone {old_phone} changed to phone {new_phone}\n"
                except ValueError:  
                  print('\nInvalid phone number. Please use 10-digit phone\n')
                except AttributeError:
                  print('\nNo such phone number\n')
        
        elif info_type == 'email':
            if record.email:
              print()
              print(record.prettytable_for_search()) 
              while True:
                new_email = input('\nEnter valid email: \n')
                try:
                  record.edit_email(new_email)
                  print()
                  print(record.prettytable_for_search()) 
                  return f'Email {new_email} changed to {name}\n'
                except ValueError:
                  print('\nIvalid email format.\n')
            else:
              return f'\n{name} has no email.\n'
            
        elif info_type == 'birthday':
            if record.birthday:
              print()
              print(record.prettytable_for_search()) 
              while True:
                new_birthday = input('\nEnter birthday format DD.MM.YYYY: \n')
                try:
                  record.edit_birthday(new_birthday)
                  print()
                  print(record.prettytable_for_search()) 
                  return f'Birthday {new_birthday} changed to {name}\n'
                except ValueError:
                  print('\nIvalid birthday format. Please use DD.MM.YYYY.\n')
            else:
              return f'\n{name} have not birthday.\n' 

        elif info_type == 'address':
            if record.address:
              print()
              print(record.prettytable_for_search()) 
              new_address = input('\nEnter address: \n')
              record.edit_address(new_address)
              print()
              print(record.prettytable_for_search()) 
              return f'Address {new_address} changed to {name}.\n'
            else:
              print(f'\n{name} have not address\n')
        elif info_type == 'name':
            print()
            print(record.prettytable_for_search())
            while True:
              new_name = input('\nEnter new name: \n').strip().capitalize()
              try:
                record.edit_name(new_name)
                book.delete(name)
                book.add_record(record)
                print()
                print(record.prettytable_for_search())
                return f'Name {name} changed to name {new_name}\n'
              except ValueError as e:
                print(f'{e}')
                continue
        else:
            print('\nUse only:  name  phone  email  address  birthday\n')
            continue

      except Exception as e:
        print(f"\nInvalid {e}.\n")     
  else:
    return '\nNo such contact\n'        
             

def search_by_name(name: str, book) -> str:
  record: Record = book.find(name.capitalize())
  if record:
    return record.prettytable_for_search()
  return 'No such contact.'


def search_by_phone(phone: str, book) -> str:
  record: Record = book.find_by_phone(phone)
  if record:
    return record.prettytable_for_search()
  return f'No contact with this Phone: {phone}.'


def prettytable_for_search_birthday(records):
  table = PrettyTable()
  table.field_names = ["Name", "Birthday"]
  for cont in records:
    name = cont.name.value
    birthday = cont.birthday.value.strftime('%d.%m.%Y') if cont.birthday else '-'
    table.add_row([name, birthday])
  return table


def search_by_birthday(birthday: str, book) -> str:
  records = book.find_by_brthd(birthday)
  if len(records) == 0:
    return f'No contact with this Birthday: {birthday}.'
  return prettytable_for_search_birthday(records)


def search_by_email(email: str, book) -> str:
  record: Record = book.find_by_mail(email)
  if record:
    return record.prettytable_for_search()
  return f'No contact with this Email: {email}.'


def search_by_address(address: str, book) -> str: 
  record: Record = book.find_by_addr(address)
  if record:
    return record.prettytable_for_search()
  return f'No contact with this Address: {address}.'


@input_error
def search(args, book: AddressBook) -> str:
  comms = {'name': search_by_name, 'phone': search_by_phone, 'birthday': search_by_birthday, 'email': search_by_email, 'address': search_by_address}
  return comms[args[0]](args[1], book)


def suggest_command(user_input, commands):
    best_match = process.extract(user_input, commands)
    best_match = [match[0] for match in best_match if match[1] > 60]
    return best_match


def save_data(book, filename="addressbook.pkl"):
  with open(filename, "wb") as f:
    pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
  try:
    with open(filename, "rb") as f:
      return pickle.load(f)
  except FileNotFoundError:
    return None
