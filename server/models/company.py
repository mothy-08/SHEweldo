import hashlib

class Company:
    def __init__(self, name, size, industry, country):
        self.name = name
        self.size = size
        self.industry = industry
        self.country = country

    def generate_hash(self):
        hash_input = f"{self.name}{self.country}".encode()
        return hashlib.sha256(hash_input).hexdigest()