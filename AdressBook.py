import re
from collections import UserDict
from datetime import datetime
from datetime import date
import pickle
import os.path


class Field:
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return f'{self.value}'


class Name(Field):
    pass


class MailExists(Exception):
    pass


class AdressExists(Exception):
    pass


class IncorrectEmailFormat(Exception):
    pass


class IncorrectAdressFormat(Exception):
    pass


class PhoneNumberError(Exception):
    pass


class Phone(Field):
    def __init__(self, value) -> None:
        super().__init__(value)
        self.__value = None
        self.value = value

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value) -> None:
        codes_operators = ["067", "068", "096", "097", "098", "050",
                           "066", "095", "099", "063", "073", "093"]
        new_value = (value.strip().
                     removeprefix('+').
                     replace("(", '').
                     replace(")", '').
                     replace("-", ''))
        if new_value[:2] == '38' and len(new_value) == 12 and new_value[2:5] in codes_operators:
            self.__value = new_value
        else:
            raise PhoneNumberError

    def get_phone(self) -> str:
        return self.value


class Birthday(Field):
    def __init__(self, value) -> None:
        super().__init__(value)
        self.__value = None
        self.value = value

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value) -> None:
        if value:
            try:
                datetime.strptime(value, "%d.%m.%Y")
            except ValueError:
                raise ValueError("Incorrect data format, should be DD.MM.YYYY")
        self.__value = value


class Mail(Field):
    def __init__(self, value) -> None:
        super().__init__(value)
        self.__value = None
        self.value = value

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value: str) -> None:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.match(regex, value):
            self.__value = value
        else:
            raise IncorrectEmailFormat

    def get_email(self) -> str:
        return self.value


class Adress(Field):
    def __init__(self, value) -> None:
        super().__init__(value)
        self.__value = None
        self.value = value

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value: str) -> None:
        regex = r'^([\w]([\.,]?)([\s]?)){1,60}$'
        if re.match(regex, value):
            self.__value = value
        else:
            raise IncorrectAdressFormat

    def get_adres(self) -> str:
        return self.value


class Record:
    def __init__(self, name: Name, phones=[], mails=[], adress=[], birthday: Birthday = None) -> None:
        self.name = name
        self.phone_list = phones
        self.birthday = birthday
        self.mails = mails
        self.adress = adress

    def __str__(self) -> str:
        return f'User {self.name} - Phones: {", ".join([phone.value for phone in self.phone_list])}' \
               f' - Birthday: {self.birthday} - Email: {", ".join([mail.value for mail in self.mails])}' \
               f' - Adress: {", ".join([adres.value for adres in self.adress])}'

    def add_phone(self, phone: Phone) -> None:
        self.phone_list.append(phone)


    def get_phones(self) -> str:
        if not self.phone_list:
            return 'No phones'
        return ', '.join([phone.get_phone() for phone in self.phone_list])

    def edit_phone(self, phone: Phone, new_phone: Phone) -> None:
        for el in self.phone_list:
            if el.get_phone() == phone.get_phone():
                self.phone_list.remove(el)
                self.phone_list.append(new_phone)
                return f"Email {phone} was changed to {new_phone}"

    def days_to_birthday(self):
        if self.birthday:
            start = date.today()
            birthday_date = datetime.strptime(str(self.birthday), '%d.%m.%Y')
            end = date(year=start.year, month=birthday_date.month,
                       day=birthday_date.day)
            count_days = (end - start).days
            if count_days < 0:
                count_days += 365
            return count_days
        else:
            return 'Unknown birthday'

    def add_email(self, mail: Mail):
        self.mails.append(mail)

    def get_emails(self) -> str:
        if not self.mails:
            return 'No emails'
        return ', '.join([mail.get_email() for mail in self.mails])

    def edit_email(self, mail: Mail, new_mail: Mail) -> str:
        for el in self.mails:
            if el.get_email() == mail.get_email():
                self.mails.remove(el)
                self.mails.append(new_mail)
                return f"Email {mail} was changed to {new_mail}"

    def add_adresses(self, adres: Adress):
        self.adress.append(adres)

    def get_adress(self) -> str:
        if not self.adress:
            return 'No adress'
        return ', '.join([adres.get_adres() for adres in self.adress])

    def edit_adres(self, adres: Adress, new_adres: Adress) -> str:
        for el in self.adress:
            if el.get_adres() == adres.get_adres():
                self.adress.remove(el)
                self.adress.append(new_adres)
                return f"Address {adres} was changed to {new_adres}"


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.n = None

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def iterator(self, n=2, days=0):
        self.n = n
        index = 1
        print_block = '-' * 50 + '\n'
        for record in self.data.values():
            if days == 0 or (record.birthday.value is not None and record.days_to_birthday(record.birthday) <= days):
                print_block += str(record) + '\n'
                if index < n:
                    index += 1
                else:
                    yield print_block
                    index, print_block = 1, '-' * 50 + '\n'
        yield print_block


class InputError:
    def __init__(self, func) -> None:
        self.func = func

    def __call__(self, contacts, *args):
        try:
            return self.func(contacts, *args)
        except IndexError:
            return 'Input formatting is not correct, make sure to check -help-!'
        except KeyError:
            return 'Sorry,user not found, try again!'
        except ValueError:
            return 'Sorry,incorrect argument,try again!'
        except MailExists:
            return "This e-mail already exists in the adress book"
        except AdressExists:
            return 'This adress already exists in the adress book'
        except IncorrectEmailFormat:
            return "Email must contain latin letters, @ and domain after . (Example: 'email@.com)"
        except IncorrectAdressFormat:
            return 'Incorrect adress! May be (Example: Kyiv,Pr.Dnipro,12'
        except PhoneNumberError:
            return "Phone number must be 12 digits, and start with 380"


def greeting(*args):
    return 'Hello! Can I help you?'


@InputError
def add(contacts, *args):
    name = Name(args[0])
    phone = Phone(args[1])
    try:
        birthday = Birthday(args[2])
    except IndexError:
        birthday = None
    if name.value in contacts:
        contacts[name.value].add_phone(phone)
        writing_db(contacts)
        return f'Add phone number: {phone} for {name}'
    else:
        contacts[name.value] = Record(name, [phone], [], [], birthday)
        writing_db(contacts)
        return f'Add {name}: {phone}'


@InputError
def add_mail(contacts, *args):
    name = Name(args[0])
    mail = Mail(args[1])
    try:
        birthday = Birthday(args[2])
    except IndexError:
        birthday = None
    if name.value in contacts:
        if mail.value in contacts[name.value].mails:
            raise MailExists
        else:
            contacts[name.value].add_email(mail)
    else:
        contacts[name.value] = Record(name, [], [mail], [], birthday)
    writing_db(contacts)
    return f'Added {mail} to user {name}'


@InputError
def add_adress(contacts, *args):
    name = Name(args[0])
    adres = Adress(args[1])
    try:
        birthday = Birthday(args[2])
    except IndexError:
        birthday = None
    if name.value in contacts:
        if adres.value in contacts[name.value].adress:
            raise AdressExists
        else:
            contacts[name.value].add_adresses(adres)
    else:
        contacts[name.value] = Record(name, [], [], [adres], birthday)
    writing_db(contacts)
    return f'Added {adres} to user {name}'


@InputError
def change_phone(contacts, *args):
    name, phone, new_phone = args[0], args[1], args[2]
    contacts[name].edit_phone(Phone(phone), Phone(new_phone))
    writing_db(contacts)
    return f'{name} your old phone number: {phone} was changed to {new_phone}'


@InputError
def change_email(contacts, *args):
    name = args[0]
    mail = args[1]
    new_mail = args[2]
    contacts[name].edit_email(Mail(mail), Mail(new_mail))
    writing_db(contacts)
    return f'Email {mail} changed to {new_mail} for {name}'


@InputError
def change_adres(contacts, *args):
    name = args[0]
    adres = args[1]
    new_adres = args[2]
    contacts[name].edit_adres(Adress(adres), Adress(new_adres))
    writing_db(contacts)
    return f'Address {adres} changed to {new_adres} for {name}'


def del_contact(contacts, *args):
    name = args[0]
    del contacts[name]
    writing_db(contacts)
    return f'Deleted user {name}'


def show_all(contacts, *args):
    if not contacts:
        return 'Address book is empty'
    result = 'Users: \n'
    print_list = contacts.iterator()
    for item in print_list:
        result += f'{item}'
    return result


def birthday(contacts, *args):
    if args:
        name = args[0]
        return f'{contacts[name].birthday}'


def show_birthday_x_days(contacts, *args):
    x = int(args[0])
    result = f'List of users with birthday in {x} days:'
    for key in contacts:
        if contacts[key].days_to_birthday() <= x:
            result += f'\n{contacts[key]}'
    return result


def backing(*args):
    return 'Good bye CommandBot!'


def unknown_command(*args):
    return 'Unknown command! Enter again!'


def help(*args):
    return """Commands format - Command meaning
    Command: "help" - returns a list of available commands with formatting
    Command: "hello" - returns a greeting
    Command: "add" Enter: name phone (birthday) - adds a phone to a contact, adds a birthday (optional)
    Command: "new phone" Enter: name phone new phone - changes a phone number to a new one
    Command: "show all" - displays all contacts
    Command: "birthday" Enter: name - finds a birthday for name
    Command: "soon birthday" Enter: {days} - gives a list of users who have birthday within the next {days}, where days = number of your choosing
    Command: "find" Enter: [any strings} - finds matches in the address book and returns the findings
    Command: "email" Enter: name email - adds an email for a user
    Command: "new email" Enter: name old email new email - changes old email to new email
    Command: "new adress" Enter: name old address new address - changes old address to the new address
    Command: "adress" Enter: name address - adds and address for a user, address format city,street,number
    Command: "remove contact" Enter:  name - deletes the user and all his data from the contact book
    Command: "back" - returns to the selection of work branches
    """


file_name = 'AddressBook.bin'


def reading_db(file_name):
    check_file = os.path.exists('AddressBook.bin')
    if check_file == True and os.path.getsize('AddressBook.bin') !=0 :
        with open(file_name, "rb") as fh:
            unpacked = pickle.load(fh)
    else:
        with open(file_name, "wb") as fh:
            unpacked = AddressBook()
    return unpacked


def writing_db(contacts):
    with open(file_name, "wb") as fh:
        pickle.dump(contacts, fh)



@InputError
def find(contacts, *args):
    substring = args[0]
    if contacts:
        # [phone.value for phone in self.phones]
        for name, data in contacts.items():
            if substring.lower() in name.lower():
                return f'{data}'
            for phone in data.phone_list:
                if substring in str(phone):
                    return f"The phone is {phone} and belongs to {name}"
            for mail in data.mails:
                if substring in str(mail):
                    return f"The email is {mail} and belongs to {name}"
            for adres in data.adress:
                if substring in str(adres):
                    return f"The address is {adres} and belongs to {name}"
    else:
        return "Address Book is empty"


COMMANDS = {greeting: ['hello'], add: ['add '], change_phone: ['new phone'],
            show_all: ['show all'], backing: ['back'],
            birthday: ['birthday '], show_birthday_x_days: ['soon birthday'],
            find: ['find', 'check'], add_mail: ['email'], add_adress: ['adress'],
            change_email: ["new email"], change_adres: ['new address', 'new adress'],
            del_contact: ['remove contact'], help: ['help']}


def new_func():
    return str, list


def command_parser(user_command: str) -> new_func():
    for key, list_value in COMMANDS.items():
        for value in list_value:
            if user_command.lower().startswith(value):
                args = user_command[len(value):].split()
                return key, args
    else:
        return unknown_command, []



