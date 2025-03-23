from enum import StrEnum, auto

class CompanySize(StrEnum):
    SMALL = auto()
    MEDIUM = auto()
    LARGE = auto()
    ENTERPRISE = auto()

class Department(StrEnum):
    EXECUTIVE_LEADERSHIP = auto()
    OPERATIONS = auto()
    FINANCE_ACCOUNTING = auto()
    HUMAN_RESOURCES = auto()
    LEGAL_COMPLIANCE = auto()
    MARKETING_SALES = auto()
    CUSTOMER_SERVICE_SUPPORT = auto()
    TECHNOLOGY_IT = auto()
    PRODUCT_RD = auto()
    SUPPLY_CHAIN_LOGISTICS = auto()
    OTHER = auto()

class Industry(StrEnum):
    TECHNOLOGY = auto()
    FINANCE = auto()
    HEALTHCARE = auto()
    MANUFACTURING = auto()
    RETAIL = auto()
    EDUCATION = auto()
    TRANSPORTATION = auto()
    ENERGY = auto()
    ENTERTAINMENT = auto()
    TELECOMMUNICATIONS = auto()
    CONSTRUCTION = auto()
    HOSPITALITY = auto()
    REAL_ESTATE = auto()
    AGRICULTURE = auto()
    PHARMACEUTICALS = auto()
    OTHER = auto()

class Gender(StrEnum):
    MALE = auto()
    FEMALE = auto()
    NONBINARY = auto()
    OTHER = auto()

class ExperienceLevel(StrEnum):
    ENTRY_LEVEL = auto()
    JUNIOR = auto()
    MID_LEVEL = auto()
    SENIOR = auto()
    EXPERT = auto()
    LEGENDARY = auto()