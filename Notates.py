import re
from collections import UserList
import pickle
import os.path


class Record:
    def __init__(self, notate = None, tag = []) -> None:
        self.notate = notate
        self.tag = tag

    def __str__(self) -> str:
        return f" {self.notate} \n    Tag(s): {self.tag} "

    def add_tag(self, tag) -> None:
        self.tag.append(tag)

    def del_tag(self, tag) -> None:
        self.tag.remove(tag)


class NotateBook(UserList):
    def __init__(self):
        super().__init__()

    def add_record(self, record: Record) -> None:
        self.data.append(record)

    def __repr__(self):
        count = 0
        for i in self.data: # notates_list:
            count +=1
            print(f"{count}. {i}\n")
        return f'End of notates'

    def find_notate(self, symbol) -> str:
        count = 0
        ind = 0
        for record in self.data:
            ind += 1
            if record.notate.find(symbol) != -1:
                count += 1
                print(f"{ind}. {record}")
        if count == 0:
            return 'Notate not found'
        else:
            return 'Search complete'

    def find_tag(self, symbol) -> str:
        count = 0
        ind = 0
        for rec in self.data:
            ind += 1
            n = 0
            for i in range(len(symbol)):
                if symbol[i] in rec.tag:
                    n +=1
                    if n == len(symbol):
                        count +=1
                        print(f"{ind}. {rec}")
        if count == 0:
            return 'Tag not found'
        else:
            return 'Search complete'


class InputError:
    def __init__(self, func) -> None:
        self.func = func

    def __call__(self, *args):
        try:
            return self.func(*args)
        except IndexError:
            return 'Sorry,such a note does not exist'
        except KeyError:
            return 'Sorry,user not found, try again!'
        except ValueError:
            return 'Sorry,phone number not found,try again!'


@InputError
def add(notates_list, *args):
    #notates_list.append(Record(data, []))
    notates_list.append(Record(' '.join(args), []))
    writing_db(notates_list)
    return f'Your note is added under number {len(notates_list)}'


@InputError
def del_notate(notates_list, *args):
    numb_notate = args[0]
    notates_list.pop(int(numb_notate)-1)
    writing_db(notates_list)
    return f'Notate deleted'


@InputError
def del_tag(notates_list, *args):
    numb_notate = args[0]
    notates_list[int(numb_notate)-1].tag.clear()
    writing_db(notates_list)
    return f'Tags deleted'


@InputError
def change_notate(notates_list, *args):
    numb_notate = args[0]
    new_line = ''
    for i in range(1, len(args)):
        new_line += args[i] + ' '
    notates_list[int(numb_notate) - 1].notate = new_line.strip()
    writing_db(notates_list)
    return f'Notate changed'


@InputError
def find_symb(notates_list, *args):
    new_line = ''
    for i in range(len(args)):
        new_line += args[i] + ' '
    symbol = new_line.strip()
    return notates_list.find_notate(symbol)


@InputError
def find_tags(notates_list, *args):
    new_line = ''
    for i in range(len(args)):
        new_line += args[i] + ' '
    symbol = new_line.strip().split(', ')
    return notates_list.find_tag(symbol)


@InputError
def add_tag(notates_list, *args):  # 1 tag1, tag2, tag3
    numb_notate = args[0]
    new_line = ''
    for i in range(1, len(args)):
        new_line += args[i] + ' '
    tags = new_line.strip().split(', ')
    for i in tags:
        if i in notates_list[int(numb_notate)-1].tag:
            print(f'Tag {i} already exists')
        else:
            notates_list[int(numb_notate)-1].tag.append(i)
            print(f'Tag {i} added')
    writing_db(notates_list)
    return f'Tag(s) added successfully'


@InputError
def clear(notates_list, *args):
    notates_list.clear()
    writing_db(notates_list)
    return 'All notates deleted'


def show_notates(notates_list, *args):
    if len(notates_list) == 0:
        return 'No notes yet'
    else:
        return notates_list


def backing_notates(notates_list, *args):
    return 'Good bye!'


def unknown_command(notates_list, *args):
    return 'Unknown command! Enter again!'


def greeting(*args):
    return 'Hello! Can I help you?'


def help(*args):
    return """Commands format - Command meaning
    Command: "help" - returns a list of available commands with formatting
    Command: "hello" - returns a greeting
    Command: "add" Enter: note - adds a note to a NotateBook
    Command: "tag" Enter: number of note and tags in format 'tag1, tag2, ...'
    Command: "del notate" Enter: the number of the note you want to delete
    Command: "del tag" Enter: the number of the note whose tags you want to delete
    Command: "change" Enter: the number of the note you want to change and new note
    Command: "find notate" Enter: the text that the notes should contain
    Command: "find tag" Enter: the tag(s) that the note's tags should contain
    Command: "show"  print a book of notes
    Command: "clear"  delete a book of notes
    Command: "back" returns to the selection of work branches
    """




file_name_notates = 'Notatebook.bin'


def reading_db_notate(file_name_notates):
    check_file = os.path.exists('Notatebook.bin')
    if check_file == True and os.path.getsize('Notatebook.bin') !=0:
        with open(file_name_notates, "rb") as fh:
            unpacked = pickle.load(fh)
    else:
        with open(file_name_notates, "wb") as fh:
            unpacked = NotateBook()
    return unpacked


def writing_db(notates_list):
    with open(file_name_notates, "wb") as fh:
        pickle.dump(notates_list, fh)


COMMANDS = {greeting: ['hello'], add: ['add'], backing_notates: ['back'],
            show_notates: ['show'], add_tag: ['tag'], del_notate : ['del notate'],
            del_tag : ['del tag'], change_notate: ['change'],  help: ['help'],
            find_symb: ['find notate'], clear: ['clear'], find_tags: ['find tag']}


def new_func():
    return str, list


def command_parser_not(user_command: str) -> new_func():
    for key, list_value in COMMANDS.items():
        for value in list_value:
            if user_command.lower().startswith(value):
                data = user_command[len(value)+1:].split(' ')
                return key, data
    else:
        return unknown_command, []




