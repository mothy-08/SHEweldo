from abc import ABC, abstractmethod
from enum import Enum
import hashlib

from models.company_size import CompanySize
from models.department import Department
from models.gender import Gender

class BaseEntity(ABC):
    def __init__(self, entity_id: str):
        self.__entity_id = entity_id
        
    @property
    def entity_id(self):
        return self.__entity_id
    
    @abstractmethod
    def validate(self) -> bool:
        pass

class Company(BaseEntity):
    def __init__(self, entity_id: str, name: str, size: CompanySize, industry: str, country: str):
        super().__init__(entity_id)
        self.__name = name
        self.__size = size
        self.__industry = industry
        self.__country = country

    def validate(self) -> bool:
        return all([
            isinstance(self.__size, CompanySize),
            len(self.__name.strip()) > 0,
            len(self.__industry.strip()) > 0,
            len(self.__country.strip()) > 0
        ])

    @property
    def name(self):
        return self.__name

    @property
    def country(self):
        return self.__country

    def generate_hash(self):
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
            
        self.__company = company
        self.__years_at_company = years_at_company
        self.__total_experience = total_experience
        self.__salary_amount = salary_amount
        self.__gender = gender
        self.__submission_date = submission_date
        self.__is_well_compensated = is_well_compensated
        self.__department = department
        self.__job_title = job_title

    def validate(self) -> bool:
        return all([
            self.__company.validate(),
            self.__years_at_company >= 0,
            self.__total_experience >= 0,
            self.__salary_amount > 0,
            isinstance(self.__gender, Gender),
            isinstance(self.__department, Department),
            len(self.__job_title.strip()) > 0
        ])

    @property
    def company(self):
        return self.__company

    @property
    def company_hash(self):
        return self.__company.generate_hash()

    @property
    def years_at_company(self):
        return self.__years_at_company

    @property
    def total_experience(self):
        return self.__total_experience

    @property
    def salary_amount(self):
        return self.__salary_amount

    @property
    def gender(self):
        return self.__gender

    @property
    def submission_date(self):
        return self.__submission_date

    @property
    def is_well_compensated(self):
        return self.__is_well_compensated

    @property
    def department(self):
        return self.__department

    @property
    def job_title(self):
        return self.__job_title