from abc import ABC, abstractmethod
from typing import Dict, Any

from server.models.entities import SalaryRecord, Company
from server.controllers.database import DatabaseController
from server.models.enums import Department

class ISalaryService(ABC):
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
            company = Company(
                name=data.get("company"),
                size=data.get("company_size"),
                industry=data.get("industry"),
                country=data.get("country")
            )

            salary_record = SalaryRecord(
                company=company,
                years_at_company=data.get("years_at_company", 0),
                total_experience=data.get("total_experience", 0),
                salary_amount=data.get("salary_amount", 0.0),
                gender=data.get("gender", "Not specified"),
                submission_date=data.get("submission_date"),
                is_well_compensated=data.get("is_well_compensated", False),
                department=data.get("department"),
                job_title=data.get("job_title")
            )

            success = self.db_controller.insert_record(salary_record)
            
            if success:
                return {"message": "Salary submitted successfully", "data": data}
            else:
                return {"message": "Failed to submit salary", "error": "Database insertion failed"}, 500
        except Exception as e:
            return {"message": "An error occurred", "error": str(e)}, 500

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
