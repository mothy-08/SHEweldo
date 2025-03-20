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

class EnumConverter:
    def _str_to_enum(self, enum_cls: type[StrEnum], value_str: str, default: StrEnum) -> StrEnum:
        """Converts a string to an enum value, with a fallback default."""
        normalized_str = value_str.upper().replace(" ", "_")
        return next((e for e in enum_cls if e.value == normalized_str), default)

    @staticmethod
    def int_to_company_size(employee_count: int) -> CompanySize:
        """Converts an employee count to a CompanySize enum."""
        if employee_count <= 50:
            return CompanySize.SMALL
        if employee_count <= 200:
            return CompanySize.MEDIUM
        if employee_count <= 400:
            return CompanySize.LARGE
        return CompanySize.ENTERPRISE

    def str_to_industry(self, industry_str: str) -> Industry:
        return self._str_to_enum(Industry, industry_str, Industry.OTHER)

    def str_to_gender(self, gender_str: str) -> Gender:
        return self._str_to_enum(Gender, gender_str, Gender.OTHER)

    def str_to_department(self, department_str: str) -> Department:
        return self._str_to_enum(Department, department_str, Department.OTHER)