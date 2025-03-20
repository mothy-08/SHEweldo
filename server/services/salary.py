from abc import ABC, abstractmethod
from typing import Dict, Any

from server.models.entities import SalaryRecord, Company
from server.controllers.database import DatabaseController
from server.models.enums import *

class ISalaryService(ABC):
    @abstractmethod
    def submit_salary(self, data: Dict[str, Any]):
        pass

    @abstractmethod
    def add_company(self, data: Dict[str, Any]):
        pass

    @abstractmethod
    def calculate_averages(self, department: Department) -> Dict[str, float]:
        pass
    
    @abstractmethod
    def get_salary_distribution(self) -> Dict[str, float]:
        pass
    
    @abstractmethod
    def generate_benchmark(self, company: Company) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def generate_comparison(self, user_record: SalaryRecord) -> Dict[str, Any]:
        pass

class SalaryService(ISalaryService):
    def __init__(self, db_controller: DatabaseController):
        self.db_controller = db_controller

    def submit_salary(self, data: Dict[str, Any]):
        try:
            salary_record = SalaryRecord(
                company_hash=data.get("company_hash"),
                experience_level=self.merge_experience(data.get("years_at_the_company"), data.get("total_experience")),
                salary_amount=data.get("salary_amount", 0.0),
                gender=self.str_to_gender(data.get("gender", "Not specified")),
                submission_date=data.get("submission_date"),
                is_well_compensated=data.get("is_well_compensated", False),
                department=self.str_to_department(data.get("department")),
                job_title=data.get("job_title")
            )

            if not salary_record.validate():
                return {"message": "Data might be malform", "data": data}
            
            success = self.db_controller.insert_salary_record(salary_record)
            
            if success:
                return {"message": "Salary submitted successfully", "data": data}
            else:
                return {"message": "Failed to submit salary", "error": "Database insertion failed"}, 500
        except Exception as e:
            return {"message": "An error occurred", "error": str(e)}, 500
        
    def add_company(self, data: Dict[str, Any]):
        try:
            company = Company(
                name=data.get("company_name"),
                size=self.int_to_company_size(int(data.get("company_size"))),
                industry=self.str_to_industry(data.get("company_industry")),
                country=data.get("country")
            )

            if not company.validate():
                return {"message": "Company data might be malform", "data": data}
            
            success = self.db_controller.insert_company(company)

            if success:
                return {"message": "Company added successfully", "data": data}
            else:
                return {"message": "Failed to add company", "error": "Database insertion failed"}, 500
            
        except Exception as e:
            return {"message": "An error occurred", "error": str(e)}, 500
        
    def _str_to_enum(self, enum_cls: type[StrEnum], value_str: str, default: StrEnum) -> StrEnum:
        """Converts a string to an enum value, with a fallback default."""
        normalized_str = value_str.strip().upper().replace(" ", "_")
        return next((e for e in enum_cls if e.name == normalized_str), default)


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
    
    @staticmethod
    def merge_experience(years_at_company: int, total_experience: int) -> ExperienceLevel:
        """Calculates weighted experience and returns an ExperienceLevel enum."""
        weighted_experience = (years_at_company * 1.5) + total_experience
        if weighted_experience < 2:
            return ExperienceLevel.ENTRY_LEVEL
        elif weighted_experience < 5:
            return ExperienceLevel.JUNIOR
        elif weighted_experience < 9:
            return ExperienceLevel.MID_LEVEL
        elif weighted_experience < 14:
            return ExperienceLevel.SENIOR
        elif weighted_experience < 20:
            return ExperienceLevel.EXPERT
        else:
            return ExperienceLevel.LEGENDARY

    def str_to_industry(self, industry_str: str) -> Industry:
        return self._str_to_enum(Industry, industry_str, Industry.OTHER)

    def str_to_gender(self, gender_str: str) -> Gender:
        return self._str_to_enum(Gender, gender_str, Gender.OTHER)

    def str_to_department(self, department_str: str) -> Department:
        return self._str_to_enum(Department, department_str, Department.OTHER)

    def calculate_averages(self, department: Department) -> Dict[str, float]:
        # TODO: Implement database query to get salary averages by department
        return {"average_salary": 75000.0}

    def get_salary_distribution(self) -> Dict[str, float]:
        # TODO: Implement logic to calculate salary distribution
        return {"median_salary": 65000.0, "percentile_90": 120000.0}

    def generate_benchmark(self, company: Company) -> Dict[str, Any]:
        # TODO: Implement logic to benchmark salaries within a company
        return {"benchmark": "Above average", "company": company.name}

    def generate_comparison(self, user_record: SalaryRecord) -> Dict[str, Any]:
        # TODO: Implement logic to compare a user's salary with the dataset
        return {
            "comparison": "Your salary is in the 80th percentile",
            "user_salary": user_record.get_salary_amount(),
        }

    def test(self) -> Dict[str, str]:
        return {"isSuccessful": "Success"}
