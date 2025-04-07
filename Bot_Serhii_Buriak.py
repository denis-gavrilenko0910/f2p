import pickle
from collections import UserDict
from datetime import datetime, timedelta


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено
    

class Field:
    def __init__(self, value):
        self.value = value


    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) <= 9:
            raise ValueError("Phone number must be at least 10 characters long or contains letters")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            birthday = datetime.strptime(value, '%d.%m.%Y')
            super().__init__(birthday)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        

    def __str__(self):
        return self.value.strftime('%d.%m.%Y')


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None


    def add_phone(self, phone):
        if phone not in [p.value for p in self.phones]:
            self.phones.append(Phone(phone))


    def edit_phone(self, old_phone, new_phone):
        phones_list = [p.value for p in self.phones]
        if old_phone in phones_list:
            index = phones_list.index(old_phone)
            self.phones[index] = Phone(new_phone)
            return True
        return False


    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value
        return None


    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]


    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)


    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"


class AddressBook(UserDict):
        def add_record(self, record):
            self.data[record.name.value] = record


        def find(self, name):
            return self.data.get(name)


        def delete(self, name):
            if name in self.data:
                del self.data[name]


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Enter user name."
    return inner


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record is None:
        return f"Name {name} not found"
    if record.edit_phone(old_phone, new_phone):
        return "Contact updated."
    return 'Please provide a valid phone number.'


@input_error
def show_phone(args, book):
    name, = args
    record = book.find(name)
    if record is None:
        return f'There is no contact with this name: {name}'
    return f"{record}"


@input_error
def show_all(book):
    all_contacts = [f"{value}" for key, value in book.items()]
    return "\n".join(all_contacts)


@input_error
def add_birthday(args, book):
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        return f'There is no contact with name: {name}'
    try:
        record.add_birthday(birthday)
    except ValueError:
        return "Invalid date format. Use DD.MM.YYYY"
    return f'Successfully added birthday to the contact named: {name}'


@input_error
def show_birthday(args, book):
    name, = args
    record = book.find(name)
    if record is None or record.birthday is None:
        return f"No birthday for the contact with the name: {name}"
    return f"{name} birthday is {record.birthday}"


@input_error
def birthdays(args, book):
    today = datetime.today()
    next_week = today + timedelta(days=7)
    upcoming_birthdays = []
    val = book.values()
    for record in val:
        if record.birthday:
            birthday_this_year = record.birthday.value.replace(year=today.year)
            if today <= birthday_this_year <= next_week:
                upcoming_birthdays.append(f"{record.name.value}: {record.birthday}")
    return "\n".join(upcoming_birthdays)


def main():
    book = load_data()

    print(
    "\n"
    "\nWelcome to the assistant bot!\n"
    "\nAvailable commands: "
    "\n--------------------------------------------------------------------------------------------"
    "\nhello - greets the user"
    "\n--------------------------------------------------------------------------------------------"
    "\nadd [name] [phone(min 10 digits)] - adds a new contact"
    "\n--------------------------------------------------------------------------------------------"
    "\nchange [name] [old_phone(min 10 digits)] [new_phone(min 10 digits)] - changes a phone number"
    "\n--------------------------------------------------------------------------------------------"
    "\nphone [name] - shows the phone number of the contact"
    "\n--------------------------------------------------------------------------------------------"
    "\nall - shows all contacts"
    "\n--------------------------------------------------------------------------------------------"
    "\nadd-birthday [name] [birthday(DD.MM.YYYY)] - adds a birthday to the contact"
    "\n--------------------------------------------------------------------------------------------"
    "\nshow-birthday [name] - shows the birthday of the contact"
    "\n--------------------------------------------------------------------------------------------"
    "\nbirthdays - shows all contacts with birthdays in the next 7 days"
    "\n--------------------------------------------------------------------------------------------"
    "\n(close) or (exit) - closes the bot"
    "\n--------------------------------------------------------------------------------------------")

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
