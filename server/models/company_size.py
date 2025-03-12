from enum import Enum

class CompanySize(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    ENTERPRISE = "enterprise"

def get_company_size(employee_count: int) -> CompanySize:
    if employee_count <= 50:
        return CompanySize.SMALL
    elif 51 <= employee_count <= 200:
        return CompanySize.MEDIUM
    elif 201 <= employee_count <= 400:
        return CompanySize.LARGE
    else:
        return CompanySize.ENTERPRISE