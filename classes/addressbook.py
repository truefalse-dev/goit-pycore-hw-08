from collections import UserDict


class AddressBook(UserDict):
    def add_record(self, record):
        """
        :param record:
        """
        self.update({record.name.value: record})

    def find(self, name):
        """
        :param name:
        :return:
        """
        return self.get(name)

    def delete(self, name):
        """
        :param name:
        """
        self.pop(name, None)
