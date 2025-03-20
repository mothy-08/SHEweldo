from abc import ABC, abstractmethod
import hashlib
from server.models.enums import *

class BaseEntity(ABC):
    def __init__(self, entity_id: str):
        self._entity_id = entity_id

    @property
    def entity_id(self):
        return self._entity_id
    
    @abstractmethod
    def validate(self) -> bool:
        pass

class Company(BaseEntity):
    def __init__(self, entity_id: str, name: str, size: CompanySize, industry: Industry, country: str):
        super().__init__(entity_id)
        self._name = name.strip()
        self._size = size
        self._industry = industry
        self._country = country.strip()

    def validate(self) -> bool:
        return all([
            isinstance(self._size, CompanySize),
            len(self._name) > 0,
            isinstance(self._industry, Industry),
            len(self._country) > 0
        ])

    @property
    def name(self):
        return self._name

    @property
    def country(self):
        return self._country

    @property
    def size(self):
        return self._size

    @property
    def industry(self):
        return self._industry

    def generate_hash(self) -> str:
        hash_input = f"{self.name}{self.country}".encode()
        return hashlib.sha256(hash_input).hexdigest()

class SalaryRecord(BaseEntity):
    def __init__(self, entity_id: str, company: Company, years_at_company: int, 
                 total_experience: int, salary_amount: float, gender: Gender,
                 submission_date: str, is_well_compensated: bool, 
                 department: Department, job_title: str):
        super().__init__(entity_id)

        if not isinstance(company, Company):
            raise TypeError("company must be an instance of Company")

        self._company = company
        self._years_at_company = max(0, years_at_company)
        self._total_experience = max(0, total_experience)
        self._salary_amount = max(0.01, salary_amount)
        self._gender = gender
        self._submission_date = submission_date.strip()
        self._is_well_compensated = is_well_compensated
        self._department = department
        self._job_title = job_title.strip()

    def validate(self) -> bool:
        return all([
            self._company.validate(),
            self._years_at_company >= 0,
            self._total_experience >= 0,
            self._salary_amount > 0,
            isinstance(self._gender, Gender),
            isinstance(self._department, Department),
            len(self._job_title) > 0
        ])

    @property
    def company(self):
        return self._company

    @property
    def company_hash(self):
        return self._company.generate_hash()

    @property
    def years_at_company(self):
        return self._years_at_company

    @property
    def total_experience(self):
        return self._total_experience

    @property
    def salary_amount(self):
        return self._salary_amount

    @property
    def gender(self):
        return self._gender

    @property
    def submission_date(self):
        return self._submission_date

    @property
    def is_well_compensated(self):
        return self._is_well_compensated

    @property
    def department(self):
        return self._department

    @property
    def job_title(self):
        return self._job_title
