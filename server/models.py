from enum import Enum

class CompanySize(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    ENTERPRISE = "enterprise"

def get_company_size(employee_count: int) -> CompanySize:
    """Returns the CompanySize enum based on the employee count."""
    if employee_count <= 50:
        return CompanySize.SMALL
    if employee_count <= 200:
        return CompanySize.MEDIUM
    if employee_count <= 400:
        return CompanySize.LARGE
    return CompanySize.ENTERPRISE
    
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

class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
    NONBINARY = "other"