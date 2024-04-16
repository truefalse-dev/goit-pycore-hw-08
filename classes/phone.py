from .field import Field


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if not (value.isdigit() and len(value) == 10):
            raise ValueError('The phone number is invalid')
