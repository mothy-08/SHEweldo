import hashlib

class Company:
    def __init__(self, name, size, industry, country):
        self.__name = name
        self.__size = size
        self.__industry = industry
        self.__country = country

    @property
    def get_name(self):
        return self.__name

    @property
    def get_country(self):
        return self.__country

    def generate_hash(self):
        hash_input = f"{self.get_name}{self.get_country}".encode()
        return hashlib.sha256(hash_input).hexdigest()
