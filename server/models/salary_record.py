from models.company import Company

class SalaryRecord:
    def __init__(self, company: Company, years_at_company, total_experience, salary_amount, gender, submission_date, is_well_compensated, department, job_title):
        if not isinstance(company, Company):
            raise TypeError("company must be an instance of Company")

        self.__company = company
        self.__years_at_company = years_at_company
        self.__total_experience = total_experience
        self.__salary_amount = salary_amount
        self.__gender = gender
        self.__submission_date = submission_date
        self.__is_well_compensated = is_well_compensated
        self.__department = department
        self.__job_title = job_title

    @property
    def get_company(self):
        return self.__company

    @property
    def get_company_hash(self):
        return self.__company.generate_hash()

    @property
    def get_years_at_company(self):
        return self.__years_at_company

    @property
    def get_total_experience(self):
        return self.__total_experience

    @property
    def get_salary_amount(self):
        return self.__salary_amount

    @property
    def get_gender(self):
        return self.__gender

    @property
    def get_submission_date(self):
        return self.__submission_date

    @property
    def get_is_well_compensated(self):
        return self.__is_well_compensated

    @property
    def get_department(self):
        return self.__department

    @property
    def get_job_title(self):
        return self.__job_title
