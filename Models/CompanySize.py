from enum import Enum

class CompanySize(Enum):
    SMALL_1_50_EMPLOYEES = "small"
    MEDIUM_51_100_EMPLOYEES = "medium"
    LARGE_101_400_EMPLOYEES = "large"
    ENTERPRISE_401_PLUS_EMPLOYEES = "enterprise"