from collections import UserDict


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

class Field:
    def __init__(self, name):
        self.value = name

class Name(Field):
    pass

class Phone(Field):
    pass

class Record:
    def __init__(self, name, phone):
        self.name = Name(name)
        self.phones = [Phone(phone)]

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def delete_phone(self, phone):
        for item in self.phones:
            if item.value == phone:
                self.phones.remove(item)

    def change_phone(self, old_phone, new_phone):
        self.delete_phone(old_phone)
        self.add_phone(new_phone)


contacts = AddressBook()


def parser(command_input):
    parsed_input = command_input.lower().strip().split()
    return parsed_input


def input_error(func):
    def inner(data):
        try:
            return func(data)
        except ValueError as exception:
            return exception.args[0]
        except KeyError as exception:
            return exception.args[0]
        except IndexError:
            return 'With this command you should enter contact name and phone number or contact name.'
    return inner


def hello():
    return 'How can I help you?'

@input_error
def add(data):
    if data[0].isnumeric():
        raise ValueError('Name should be a string.')
    if not data[1].isnumeric():
        raise ValueError('Phone should be a number.')
    if data[0] in contacts:
        record = contacts.data[data[0]]
        record.add_phone(data[1])
        message = f'Phone {data[1]} was successfully added to contact {data[0].title()}.'
        return message
    else:
        record = Record(data[0], data[1])
        contacts.add_record(record)
        message = f'Contact {data[0].title()} with phone {data[1]} was successfully added.'
        return message

@input_error
def delete(data):
    if data[0].isnumeric():
        raise ValueError('Name should be a string.')
    if not data[1].isnumeric():
        raise ValueError('Phone should be a number.')
    if data[0] in contacts:
        record = contacts.data[data[0]]
        record.delete_phone(data[1])
        message = f'Phone {data[1]} was successfully deleted from contact {data[0].title()}.'
        return message
    else:
        raise KeyError('There is no such contact.')

@input_error
def change(data):
    if data[0].isnumeric():
        raise ValueError('Name should be a string.')
    if data[0] not in contacts:
        raise KeyError('There is no such contact.')
    if not data[1].isnumeric() or not data[2].isnumeric():
        raise ValueError('Phone should be a number.')
    record = contacts.data[data[0]]
    record.change_phone(data[1], data[2])
    message = f'Contact {data[0].title()} phone {data[1]} was successfully updated with phone {data[2]}.'
    return message

@input_error
def phone(data):
    if data[0].isnumeric():
        raise ValueError('Name should be a string.')
    if data[0] not in contacts:
        raise KeyError('There is no such contact.')
    for name, record in contacts.items():
        if name == data[0]:
            phones_list = []
            for phone in record.phones:
                phones_list.append(phone.value)
            phones_str = ', '.join(phones_list)
            contact_data = f"{name.title()}: {phones_str}\n"
            return contact_data

def show():
    if len(contacts):
        contacts_data = []
        for name, record in contacts.items():
            phones_list = []
            for phone in record.phones:
                phones_list.append(phone.value)
            phones_str = ', '.join(phones_list)
            contact_data = f"{name.title()}: {phones_str}\n"
            contacts_data.append(contact_data)
        return ''.join(contacts_data)
    else:
        return 'There are no any contacts.'

def close():
    return 'Good bye!'


commands = {
    'hello': hello,
    'add': add,
    'delete': delete,
    'change': change,
    'phone': phone,
    'show all': show,
    'close': close
}


def main():
    while True:
        command_input = input("Enter command and data: ")

        if command_input in ('hello', 'show all'):
            print(commands.get(command_input)())
            continue

        if command_input in ('good bye', 'close', 'exit'):
            print(commands.get('close')())
            break

        parsed_input = parser(command_input)
        command = parsed_input[0]

        if command not in commands.keys():
            print('There is no such command.')
            continue

        data = parsed_input[1:]
        method = commands.get(command)
        print(method(data))


if __name__ == '__main__':
    main()
