import pickle
from collections import UserDict
from datetime import datetime, timedelta
import re

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
      raise ValueError("Invalid email format")
    super().__init__(value)

class Record:
  def __init__(self, name):
    self.name = Name(name)
    self.phone = None
    self.birthday = None
    #Stenvar
    self.address = None
    self.email = None

  def add_email(self, email):
    self.email = Email(email)

  def add_address(self, address):
    self.address = Address(address)    

  def add_birthday(self, birthday):
    self.birthday = Birthday(birthday)

  def add_phone(self, phone):
    self.phone = (Phone(phone))
          
  def find_email(self):
    if self.email:
       return self.email
    return None

  def remove_email(self):
    rem_email=self.find_email()
    if rem_email:
       self.email = None
       return "Email removed"
    return "No email to remove"
  
  def find_address(self):
    if self.address:
       return self.address
    return None

  def remove_address(self):
    rem_address=self.find_address()
    if rem_address:
       self.address = None
       return "Address removed"
    return "No address to remove"
  
  def find_birthday(self):
    if self.birthday:
       return self.birthday
    return None

  def remove_birthday(self):
    rem_birthday=self.find_birthday()
    if rem_birthday:
       self.birthday = None
       return "Birthday removed"
    return "No birthday to remove"

  def find_phone(self, phone):
    if self.phone:
       return self.phone
    return None
      
  def remove_phone(self, phone):
    rem_phone = self.find_phone(phone)
    if rem_phone:
      self.phone = None
      return "Phone removed"
    return "No phone to remove"

  def edit_phone(self, new_phone):
     self.phone = Phone(new_phone)
    
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
        phone = self.phone.value if self.phone else '-'
        return f"Contact: {self.name.value}, Phones: {phone}, Email: {email}, Address: {address}, Birthday: {birthday}"

class AddressBook(UserDict):
  
  def add_record(self, record: Record):
    self.data[record.name.value] = record

  def find(self, name) -> Record:
    if name in self.data:
      return self.data[name]
    
  def get_upcoming_birthdays(self):
    result = []
    date_now = datetime.today().date()
    for name, record in self.data.items():
      if record.birthday:    
        user_brthday = record.birthday.value.date()
        user_brthday = user_brthday.replace(year=date_now.year)
        if user_brthday < date_now:
          user_brthday = user_brthday.replace(year=date_now.year + 1)

        if user_brthday >= date_now and user_brthday < date_now + timedelta(days=7):
          user_brthday = user_brthday.strftime('%d.%m.%Y')
          result.append({'name': name, 'congratulation_date':  user_brthday})
      
    return result  
  
  def delete(self, name):
    del_contact = self.find(name)
    if del_contact:
      self.data.pop(name, None)
      return 'Contact has been deleted'
    return 'No such contact'


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
       return "empty", []
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args
  
@input_error
def add_contact(args, book: AddressBook):
    name = input("Enter the name: ")  # Запитуємо ім'я
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
        return f"Contact {name} added."
    else:
        return "Contact already exists."

# видалення цілого контакту з книги
@input_error
def remove_contact(args, book: AddressBook):
   name = input('Which contact do you want to delete? ')
   rem_contact = book.delete(name)
   return rem_contact

@input_error
def change_contact(args, book: AddressBook) -> str:
  name, old_phone, new_phone = args
  result = 'No contact found'
  record: Record = book.find(name)
  if record:
    record.edit_phone(old_phone, new_phone)
    result = 'Contact updated.'    
  return result 

@input_error
def show_phone(args, book: AddressBook) -> str:
  name = args[0]
  record: Record = book.find(name)
  if record:
    result = f"phones: {'; '.join(p.value for p in record.phones)}"
  return result 

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
def birthdays(book: AddressBook):
  result = book.get_upcoming_birthdays()
  all_cont_brthds = ''
  for el in result:
    all_cont_brthds += f'name: {el["name"]}, congratulation date: {el["congratulation_date"]}'
  return all_cont_brthds
# Добавлення контакту одразу з усіма даними
@input_error 
def add_all(args, book: AddressBook):
    name = input("Give me the name: ")
    record = book.find(name)
    
    if record is None:
        record = Record(name)  # Створюємо контакт тільки з ім'ям
        book.add_record(record)
        print(f"Contact {name} added.")
        
        # Запитуємо телефон
        while True:
            phone = input("Enter phone number (or press Enter to skip): ")
            if phone == "":  # Якщо користувач натискає Enter без введення, пропускаємо цей етап
                break
            try:
                record.add_phone(phone)  # Якщо телефон невалідний, підніметься ValueError
                print(f"Phone {phone} added.")
                break
            except ValueError:
                print("Invalid phone number. Please enter a valid 10-digit phone number.")
        
        # Запитуємо email
        while True:
            email = input("Enter email address or press Enter to skip: ")
            if email == "":
               break  # Якщо користувач натискає Enter без введення, пропускаємо цей етап
            try:
                record.add_email(email)  # Якщо email невалідний, підніметься ValueError
                print(f"Email {email} added.")
                break
            except ValueError:
                print("Invalid email format. Please try again.")
        
        # Запитуємо адресу
        address = input("Enter address or press Enter to skip: ")
        if address != "":  # Якщо введено адресу
            record.add_address(address)
            print(f"Address {address} added.")
        
        # Запитуємо день народження
        birthday = input("Enter birthday (DD.MM.YYYY) or press Enter to skip: ")
        while True:
            if birthday == "":  # Якщо користувач натискає Enter без введення, пропускаємо цей етап
                break
            try:
                record.add_birthday(birthday)  # Якщо дата невалідна, підніметься ValueError
                print(f"Birthday {birthday} added.")
                break
            except ValueError:
                print("Invalid date format. Please use DD.MM.YYYY.")
        
        return f"Contact {name} updated with additional information."
    
    else:
        return "Contact already exists."
    
#Stenvar добавляємо або змінюємо певні дані 
@input_error
def edit_contact_info(args, book: AddressBook):
    name = input("Enter the contact name: ")
    record = book.find(name)
    if record:
        # Запитуємо, яку інформацію додавати або змінювати
        info_type = input("What do you want to add? (phone, email, address, birthday): ")

        if info_type == "phone":
            while True:
                new_phone = input("Enter phone number: ")
                try:
                    if not record.phone:
                        record.add_phone(new_phone)
                        return f"Phone number added to {name}."
                    else:
                       record.edit_phone(new_phone)
                       return f"Phone number added to {name}."
                except ValueError:
                   print("Invalid phone number. Please enter a valid 10-digit phone number.")

        elif info_type == "email":
                while True:
                    new_email = input('Enter email: ')
                    try:
                        if not record.email:
                            record.add_email(new_email)
                            return f"Email added to {name}."
                        else:
                            record.edit_email(new_email)
                            return f'Email changed to {name}'
                    except ValueError:
                        print("Invalid email format. Please try again.")

        elif info_type == "address":
            if not record.address:
                address = input("Enter address to add: ")
                record.add_address(address)
                return f"Address added to {name}."
            else:
                new_address = input("Enter new address to change old: ")
                record.edit_address(new_address)
                return f"Address change to {name}."
            
        elif info_type == "birthday":
                while True:
                    new_birthday = input("Enter birthday (DD.MM.YYYY): ")
                    try:
                        if not record.birthday:
                            record.add_birthday(new_birthday)
                            return f"Birthday added to {name}."
                        else:
                            record.edit_birthday(new_birthday)
                            return f"Birthday changed to {name}."
                    except ValueError:
                        print("Invalid date format. Please use DD.MM.YYYY.")
        else:
            return "Invalid option. Please choose from phone, email, address, or birthday."
    return "No such contact"

#Stenvar Видалення даних з контакту 
@input_error
def remove_contact_info(args, book: AddressBook):
    name = input("Which contact do you want to edit? ")  # Запитуємо ім'я контакту
    record = book.find(name)
    
    if record:
        # Запитуємо, яку інформацію видалити
        info_type = input("What do you want to remove? (phone, email, address, birthday): ").lower()
        
        if info_type == "phone":
            if len(record.phones) == 1:
               return record.remove_phone(phone)
            elif len(record.phones) > 1:
                phone = input("Enter the phone number to remove: ")
                return record.remove_phone(phone)
            else:
               return "Contact have no phone"
        
        elif info_type == "email":
            if record.email:
                return record.remove_email()
            else:
               return f"{name} have no email"
        
        elif info_type == "address":
            if record.address:
                return record.remove_address()
            else:
                return f"{name} have no address"
        
        elif info_type == "birthday":
            if record.birthday:
                return record.remove_birthday()
            else:
                return f"{name} have no birthday"
        
        else:
            return "Invalid option. Please choose from phone, email, address, or birthday."
    
    return "No such contact."

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
  book = load_data()
  print("Welcome to the assistant bot!")
  while True:
    user_input = input("Enter a command: ")
    command, *args = parse_input(user_input)
    if command == "empty":
       print("Enter some command: ")
       continue

    if command in ["close", "exit"]:
      save_data(book)
      print("Good bye!")
      break
    elif command == "hello":
      print("How can I help you?")
    elif command == "add":#stenvar
      print(add_contact(args, book))
    elif command == "add-all":#stenvar
      print(add_all(args, book))  
    elif command == "edit":#stenvar
      print(edit_contact_info(args, book))
    elif command == "remove-contact":#stenvar
      print(remove_contact(args, book))
    elif command == "remove":#stenvar
      print(remove_contact_info(args, book))                           
    elif command == "change":
      print(change_contact(args, book))
    elif command == "phone":
      print(show_phone(args, book))
    elif command == "all":
      print(show_all(book))
    elif command == "show-birthday":
      print(show_birthday(args, book))
    elif command == "birthdays":
      print(birthdays(book))         
    else:
      print("Invalid command.")
        

if __name__ == "__main__":
  main()