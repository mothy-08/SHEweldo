import hashlib, os
from abc import ABC, abstractmethod
from typing import Optional
from SHEweldo.models.enums import *

class BaseEntity(ABC):
    def __init__(self, entity_id: str):
        self._entity_id = entity_id

    @property
    def entity_id(self) -> str:
        return self._entity_id
    
    @abstractmethod
    def validate(self) -> bool:
        pass

class Company(BaseEntity):
    def __init__(self, name: str, size: CompanySize, industry: Industry, country: str):
        self._name = name.strip()
        self._size = size
        self._industry = industry
        self._country = country.strip()

        entity_id = self._generate_hash()
        super().__init__(entity_id)

    def validate(self) -> bool:
        return all([
            isinstance(self._size, CompanySize),
            len(self._name) > 0,
            isinstance(self._industry, Industry),
            len(self._country) > 0
        ])
    
    @property
    def id(self):
        return self._entity_id

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

    def _generate_hash(self) -> str:
        hash_input = f"{self.name.lower()}{self.country.lower()}".encode()
        return hashlib.sha256(hash_input).hexdigest()

class SalaryRecord(BaseEntity):
    def __init__(self, company_hash: str, experience_level: ExperienceLevel, salary_amount: float, gender: Gender,
                 submission_date: str, is_well_compensated: bool, 
                 department: Department, job_title: str, entity_id: Optional[str] = None):
        self._company_hash = company_hash
        self._experience_level = experience_level
        self._salary_amount = max(0.01, salary_amount)
        self._gender = gender
        self._submission_date = submission_date.strip()
        self._is_well_compensated = is_well_compensated
        self._department = department
        self._job_title = job_title.strip()

        entity_id = entity_id if entity_id is not None else self._generate_hash()
        super().__init__(entity_id)

    def validate(self) -> bool:
        return all([
            len(self._company_hash) > 0,
            isinstance(self.experience_level, ExperienceLevel),
            self._salary_amount > 0,
            isinstance(self._gender, Gender),
            isinstance(self._department, Department),
            len(self._job_title) > 0
        ])

    @property
    def id(self):
        return self._entity_id
    
    @property
    def company_hash(self):
        return self._company_hash

    @property
    def experience_level(self):
        return self._experience_level

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

    def _generate_hash(self) -> str:
        salt = os.urandom(16).hex()
        hash_input = f"{self.company_hash}{self.salary_amount}{self.submission_date}{salt}".encode()
        return hashlib.sha256(hash_input).hexdigest()
