import functools
import os
import re
import datetime
import sys
from classes.addressbook import AddressBook
from classes.record import Record
from collections import defaultdict
from pathlib import Path
import pickle


def input_error(func):
    """
    :param func:
    :return:
    """

    @functools.wraps(func)
    def inner(*args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError) as er:
            return er

    return inner


def parse_input(command: str):
    """
    :param command:
    :return:
    """
    cmd, *args = re.split(r"\s+", command)
    cmd = cmd.lower()

    return cmd, args


@input_error
def add_contact(args, book: AddressBook) -> str:
    """
    :param args:
    :param book:
    :return:
    """
    try:
        name, phone, *_ = args
    except ValueError:
        raise ValueError('Input name and phone number')

    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        message = "Contact added."
    else:
        record.add_phone(phone)
    return message


def show_all(book: AddressBook) -> str:
    """
    :param book:
    :return:
    """
    result = ""
    for name, record in book.data.items():
        result += f"\n{record}"

    return result


@input_error
def change_contact(args, book: AddressBook) -> str:
    """
    :param args:
    :param book:
    :return:
    """
    try:
        name, phone, *_ = args
    except ValueError:
        raise ValueError('Input name and phone number')

    record = book.find(name)
    record.edit_phone(phone)
    return 'Contact changed.'


@input_error
def show_contact(args, book: AddressBook) -> str:
    """
    :param args:
    :param book:
    :return:
    """
    try:
        name, *_ = args
    except ValueError:
        raise ValueError('Input name')

    record = book.find(name)
    return record


@input_error
def add_birthday(args, book) -> str:
    """
    :param args:
    :param book:
    """
    try:
        name, birthday, *_ = args
    except ValueError:
        raise ValueError('Input name and birthday')

    record = book.find(name)
    message = "Contact not found."
    if isinstance(record, Record):
        record.add_birthday(birthday)
        message = "Birthday added."
    return message


@input_error
def show_birthday(args, book) -> str:
    """
    :param args:
    :param book:
    :return:
    """
    try:
        name, *_ = args
    except ValueError:
        raise ValueError('Input name')

    record = book.find(name)
    message = "Contact not found."
    if isinstance(record, Record):
        message = record.birthday.value.strftime("%d.%m.%Y") \
            if record.birthday is not None \
            else f"{name} birthday not found."
    return message


def next_monday(_datetime) -> datetime:
    """
    :param _datetime:
    :return:
    """
    days_ahead = 0 - _datetime.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return _datetime + datetime.timedelta(days_ahead)


def birthdays(book: AddressBook):
    """
    :param book:
    :return:
    """
    result = ""
    for date, records in get_upcoming_birthdays(book).items():
        result += f"\n{date}"
        for record in records:
            result += f"\n{record}"

    return result


def get_upcoming_birthdays(book: AddressBook):
    """
    :param book:
    :return:
    """
    current_year = datetime.datetime.now().year
    today_date = datetime.datetime.today().date()
    weekdays = [today_date + datetime.timedelta(days=x) for x in range(0, 7)]

    result = defaultdict(list)
    for name, record in book.data.items():
        date_birthday = record.birthday.value.replace(year=current_year) if record.birthday is not None else None

        if date_birthday in weekdays:
            if date_birthday.weekday() in (5, 6):
                date_birthday = next_monday(date_birthday)

            result[date_birthday.strftime('%d.%m.%Y')].append(record)

    return result


STORAGE_PATH = './storage/addressbook.pkl'


def save_data(book: AddressBook) -> str:
    """
    :param book:
    :return:
    """
    with open(Path(STORAGE_PATH), 'wb') as f:
        pickle.dump(book, f)
    return "Contacts saved!"


def load_data() -> AddressBook:
    """
    :return:
    """
    try:
        with open(Path(STORAGE_PATH), 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return AddressBook()


def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        try:
            user_input = input("Enter a command: ")
            command, args = parse_input(user_input)

            if command in ["close", "exit"]:
                save_data(book)
                print("Good bye!")
                break

            elif command == "hello":
                result = "How can I help you?"

            elif command == "add":
                result = add_contact(args, book)

            elif command == "change":
                result = change_contact(args, book)

            elif command == "phone":
                result = show_contact(args, book)

            elif command == "all":
                result = show_all(book)

            elif command == "add-birthday":
                result = add_birthday(args, book)

            elif command == "show-birthday":
                result = show_birthday(args, book)

            elif command == "birthdays":
                result = birthdays(book)

            else:
                result = "Invalid command."

            print(result)

        except KeyboardInterrupt:
            save_data(book)
            print("Good bye!")
            break


def test():
    book = load_data()
    print(add_contact(['Tim', '0961296501'], book))
    print(add_contact(['Mike', '0971456509'], book))
    print(add_contact(['Mike', '0501111111'], book))
    print(add_contact(['Lisa', '096129650'], book))
    print(add_contact(['Peter', '0380031234'], book))
    print(add_contact(['Janet', '0730231771'], book))
    print(add_contact(['Victor', '0115567948'], book))
    print(show_birthday(['Ken'], book))
    print(show_birthday(['Tim'], book))
    print(show_birthday([], book))
    print(show_contact(['Lisa'], book))
    print(show_contact(['Mike'], book))
    print(add_contact(['Kenny'], book))
    print(show_all(book))
    print(change_contact(['Tim', '0505555555'], book))
    print(add_birthday(['Tim', '21.11.1982'], book))
    print(add_birthday(['Mike', '09.04.1981'], book))
    print(add_birthday(['Mike', '09.04.198'], book))
    print(add_birthday(['Janet', '07.04.1999'], book))
    print(add_birthday(['John'], book))
    print(show_birthday(['Mike'], book))
    print(add_contact(['Jonny', '0389912345'], book))
    print(add_contact(['Miriam', '0385912111'], book))
    print(add_birthday(['Miriam', '11.04.2009'], book))
    print(add_birthday(['Peter', '13.04.2001'], book))
    print(add_birthday(['Victor', '13.04.2001'], book))
    print(show_all(book))
    print(birthdays(book))

    save_data(book)


def show():
    if load_data():
        print(show_all(load_data()))
    else:
        print('No data saved!')


def clear():
    try:
        os.remove(Path(STORAGE_PATH))
        print("File removed!")
    except OSError as error:
        print(error)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        main()
    else:
        if sys.argv[1] == 'test':
            test()
        elif sys.argv[1] == 'clear':
            clear()
        elif sys.argv[1] == 'show':
            show()
        else:
            print("Invalid parameter.")
