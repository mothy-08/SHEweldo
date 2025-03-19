from enum import Enum
import string

class CompanySize(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    ENTERPRISE = "enterprise"
 
class Department(Enum):
    EXECUTIVE_LEADERSHIP = "executive"
    OPERATIONS = "operations"
    FINANCE_ACCOUNTING = "finance"
    HUMAN_RESOURCES = "hr"
    LEGAL_COMPUANCE = "legal"
    MARKETING_SALES = "marketing"
    CUSTOMER_SERVICE_SUPPORT = "customer_support"
    TECHNOLOGY_IT = "it"
    PRODUCT_RD = "product_rd"
    SUPPLY_CHAIN_LOGISTICS = "supply"
    OTHER = "other"

class Industry(Enum):
    TECHNOLOGY = "technology"
    FINANCE = "finance"
    HEALTHCARE = "healthcare"
    MANUFACTURING = "manufacturing"
    RETAIL = "retail"
    EDUCATION = "education"
    TRANSPORTATION = "transportation"
    ENERGY = "energy"
    ENTERTAINMENT = "entertainment"
    TELECOMMUNICATIONS = "telecommunications"
    CONSTRUCTION = "construction"
    HOSPITALITY = "hospitality"
    REAL_ESTATE = "real_estate"
    AGRICULTURE = "agriculture"
    PHARMACEUTICALS = "pharmaceuticals"
    OTHER = "other"

class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
    NONBINARY = "other"

class EnumConverter:
    def __str_to_enum(self, enum_cls: type[Enum], value_str: str, default: Enum) -> Enum:
        """
        Helper method to convert a string to an enum member.
        """
        normalized_str = value_str.lower().replace(" ", "_")
        for enum_member in enum_cls:
            if enum_member.value == normalized_str:
                return enum_member
        return default

    @staticmethod
    def int_to_company_size(employee_count: int) -> CompanySize:
        """
        Convert an employee count to a CompanySize enum.
        """
        if employee_count <= 50:
            return CompanySize.SMALL
        if employee_count <= 200:
            return CompanySize.MEDIUM
        if employee_count <= 400:
            return CompanySize.LARGE
        return CompanySize.ENTERPRISE

    def str_to_industry(self, industry_str: str) -> Industry:
        """
        Convert a string to an Industry enum.
        """
        return self.__str_to_enum(Industry, industry_str, Industry.OTHER)

    def str_to_gender(self, gender_str: str) -> Gender:
        """
        Convert a string to a Gender enum.
        """
        return self.__str_to_enum(Gender, gender_str, Gender.OTHER)

    def str_to_department(self, department_str: str) -> Department:
        """
        Convert a string to a Department enum.
        """
        return self.__str_to_enum(Department, department_str, Department.OTHER)