import hashlib

class Company:
    def __init__(self, name, size, industry, country):
        self.__name = name
        self.__size = size
        self.__industry = industry
        self.__country = country

    def generate_hash(self):
        hash_input = f"{self.name}{self.country}".encode()
        return hashlib.sha256(hash_input).hexdigest()