from models.salary_record import SalaryRecord
from server.controllers.database import DatabaseController
from models.company import Company

class SalaryController:
    def __init__(self, db_controller: DatabaseController):
        self.db_controller = db_controller

    def submit_salary(self, data):
        try:
            company = Company(
                name=data.get("company"),
                size=data.get("company_size"),
                industry=data.get("industry"),
                country=data.get("country")
            )

            salary_record = SalaryRecord(
                company=company,
                years_at_company=data.get("years_at_company"),
                total_experience=data.get("total_experience"),
                salary_amount=data.get("salary_amount"),
                gender=data.get("gender"),
                submission_date=data.get("submission_date"),
                is_well_compensated=data.get("is_well_compensated"),
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


    def get_averages(self):
        # TODO: Logic for retrieving salary averages
        return {"average_salary": 75000}

    def get_benchmark(self):
        # TODO: Logic for benchmarking salaries
        return {"benchmark": "Above average"}

    def get_comparison(self, data):
        # TODO: Logic for comparing salaries
        return {"comparison": "Your salary is in the 80th percentile"}
    
    def test(self):
        return {"isSuccessful": "Success"}