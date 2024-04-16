from .name import Name
from .phone import Phone
from .birthday import Birthday


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        name = f"Contact name: {self.name.value}" \
            if self.name is not None else ''
        phones = f", phone: {'; '.join(p.value for p in self.phones)}"
        birthday = f", birthday: {self.birthday.value.strftime('%d.%m.%Y')}" \
            if self.birthday is not None else ''

        return f"{name}{phones}{birthday}"

    def add_phone(self, phone):
        """
        :param phone:
        """
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        """
        :param birthday:
        """
        self.birthday = Birthday(birthday)

    def edit_phone(self, phone):
        """
        :param phone:
        """
        self.phones.pop(0)
        self.phones.append(Phone(phone))
