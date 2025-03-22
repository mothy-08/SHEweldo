from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Type

from server.models.entities import SalaryRecord, Company
from server.controllers.database import DatabaseController, FilterParams
from server.models.enums import *

class IService(ABC):
    """Base class for application services providing common utilities."""
    
    def __init__(self):
        self.db_controller = DatabaseController()

    def _str_to_enum(self, enum_cls: Type[StrEnum], value_str: Optional[str], default: StrEnum) -> StrEnum:
        """Converts a string to an enum member using case-insensitive comparison.
        
        Args:
            enum_cls: The Enum class to convert to
            value_str: Input string to match against enum members
            default: Default value if no match found
            
        Returns:
            Matched enum member or default value
        """
        if not value_str:
            return default
            
        normalized = value_str.strip().upper().replace(" ", "_")
        return next((e for e in enum_cls if e.name == normalized), default)
    
    def fetch_filtered_records(self, salary_range_step: int, filters: FilterParams = None, salary_id: str = None):
        if filters is None and salary_id is None:
            raise ValueError("Either 'filters' or 'salary_id' must be provided.")

        if salary_id:
            filters = FilterParams()
            salary_record = self.db_controller.get_salary_record(salary_id)
            filters["company_hash"] = salary_record.company_hash
            filters["department"] = Department(salary_record.department)
            filters["experience"] = ExperienceLevel(salary_record.experience_level)

        bargraph_data = self.db_controller.get_bar_graph_data(filters, salary_range_step)
        piegraph_data = self.db_controller.get_pie_graph_data(filters)

        return bargraph_data, piegraph_data

    @abstractmethod
    def add(self, data: Dict[str, Any]) -> tuple[Dict[str, Any], int]:
        pass

    @abstractmethod
    def get_all(self) -> list[tuple[str, str]]:
        pass

class SalaryService(IService):
    _EXP_THRESHOLDS = (
        (2, ExperienceLevel.ENTRY_LEVEL),
        (5, ExperienceLevel.JUNIOR),
        (9, ExperienceLevel.MID_LEVEL),
        (14, ExperienceLevel.SENIOR),
        (20, ExperienceLevel.EXPERT),
        (float('inf'), ExperienceLevel.LEGENDARY)
    )

    def __init__(self):
        super().__init__()

    def add(self, data: Dict[str, Any]) -> tuple[Dict[str, Any], int]:
        """Process and validate a new salary record submission."""
        try:
            if not (company_hash := data.get("company_hash")):
                return {"message": "Missing company identifier"}

            try:
                years_at_company = int(data["years_at_the_company"])
                total_experience = int(data["total_experience"])
            except (KeyError, ValueError) as e:
                return {"message": "Invalid experience data", "error": str(e)}

            salary_record = SalaryRecord(
                company_hash=company_hash,
                experience_level=self._merge_experience(years_at_company, total_experience),
                salary_amount=data.get("salary_amount", 0.0),
                gender=self._str_to_gender(data.get("gender")),
                submission_date=data.get("submission_date"),
                is_well_compensated=data.get("is_well_compensated", False),
                department=self._str_to_department(data.get("department")),
                job_title=data.get("job_title")
            )

            if not salary_record.validate():
                return {"message": "Invalid salary data", "data": data}
            
            if self.db_controller.insert_salary_record(salary_record):
                return {"message": "Salary submitted successfully", "id": salary_record.id, "salary": salary_record.salary_amount}
    
            return {"message": "Failed to save salary record"}

        except Exception as e:
            return {"message": "Processing failed", "error": str(e)}
        
    def get_all(self) -> list[tuple[str, str]]:
        pass

    def _merge_experience(self, years_at_company: int, total_experience: int) -> ExperienceLevel:
        """Determine experience level using weighted combination of experience metrics."""
        weighted = (years_at_company * 1.5) + total_experience
        for threshold, level in self._EXP_THRESHOLDS:
            if weighted < threshold:
                return level
        return ExperienceLevel.LEGENDARY

    def _str_to_gender(self, gender_str: Optional[str]) -> Gender:
        return self._str_to_enum(Gender, gender_str, Gender.OTHER)

    def _str_to_department(self, department_str: Optional[str]) -> Department:
        return self._str_to_enum(Department, department_str, Department.OTHER)

class CompanyService(IService):
    _SIZE_THRESHOLDS = (
        (50, CompanySize.SMALL),
        (200, CompanySize.MEDIUM),
        (400, CompanySize.LARGE),
        (float('inf'), CompanySize.ENTERPRISE)
    )

    def __init__(self):
        super().__init__()

    def add(self, data: Dict[str, Any]) -> tuple[Dict[str, Any], int]:
        try:
            if not (name := data.get("company_name")):
                return {"message": "Company name required"}
            try:
                size = self._int_to_company_size(int(data["company_size"]))
            except (KeyError, ValueError) as e:
                return {"message": "Invalid company size", "error": str(e)}

            company = Company(
                name=name,
                size=size,
                industry=self._str_to_industry(data.get("company_industry")),
                country=data.get("country")
            )

            if not company.validate():
                return {"message": "Invalid company data", "data": data}
            
            if self.db_controller.insert_company(company):
                return {"message": "Company registered successfully"}
            return {"message": "Failed to register company"}

        except Exception as e:
            return {"message": "Processing failed", "error": str(e)}
        
    def get_all(self) -> list[tuple[str, str]]:
        return self.db_controller.get_all_companies()


    def _str_to_industry(self, industry_str: Optional[str]) -> Industry:
        return self._str_to_enum(Industry, industry_str, Industry.OTHER)

    def _int_to_company_size(self, employee_count: int) -> CompanySize:
        for threshold, size in self._SIZE_THRESHOLDS:
            if employee_count <= threshold:
                return size
        return CompanySize.ENTERPRISE