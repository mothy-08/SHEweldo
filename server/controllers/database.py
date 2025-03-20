from abc import ABC, abstractmethod
from server.models.entities import SalaryRecord, Company
from server.models.enums import *
import sqlite3
from typing import TypedDict, Optional

class FilterParams(TypedDict, total=False):
    company_hash: str
    industry: Industry
    department: Department
    experience: ExperienceLevel

class IDatabaseController(ABC):
    @abstractmethod
    def get_company_record(self, hash_val: str) -> Optional[Company]:
        pass
    
    @abstractmethod
    def get_all_companies(self) -> list[tuple[str, str]]:
        pass

    @abstractmethod
    def insert_salary_record(self, record: SalaryRecord) -> bool:
        pass
    
    @abstractmethod
    def insert_company(self, company: Company) -> bool:
        pass

    @abstractmethod
    def get_filtered_records(self, filters: FilterParams) -> list[SalaryRecord]:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

class DatabaseController(IDatabaseController):
    def __init__(self, db_name="record.db"):
        self._db_name = db_name
        self._connection = None
        self._connect()

    def _connect(self):
        self._connection = sqlite3.connect(self._db_name, check_same_thread=False)
        self._create_tables()

    def _create_tables(self):
        cursor = self._connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY,
                hash TEXT UNIQUE,
                name TEXT NOT NULL,
                size TEXT CHECK(size IN ({sizes})),
                industry TEXT CHECK(industry IN ({industries})),
                country TEXT NOT NULL
            )
        '''.format(
            sizes=", ".join(f"'{size.value}'" for size in CompanySize),
            industries=", ".join(f"'{industry.value}'" for industry in Industry)
        ))

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS salaries (
                id TEXT PRIMARY KEY,
                company_hash TEXT NOT NULL,
                experience_level TEXT CHECK(experience_level IN ({experience_levels})),
                salary_amount REAL CHECK(salary_amount > 0),
                gender TEXT CHECK(gender IN ({genders})),
                submission_date TEXT NOT NULL,
                is_well_compensated BOOLEAN NOT NULL,
                department TEXT CHECK(department IN ({departments})),
                job_title TEXT NOT NULL,
                FOREIGN KEY(company_hash) REFERENCES companies(hash)
            )
        '''.format(
            experience_levels=", ".join(f"'{level.value}'" for level in ExperienceLevel),
            genders=", ".join(f"'{gender.value}'" for gender in Gender),
            departments=", ".join(f"'{department.value}'" for department in Department)
        ))

        self._connection.commit()


    def get_company_record(self, hash_val: str) -> Optional[Company]:
        if not isinstance(hash_val, str):
            raise ValueError("Invalid input: company hash must be a string")

        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM companies WHERE hash = ?", (hash_val,))
        row = cursor.fetchone()
        return Company(*row) if row else None
    
    def get_all_companies(self) -> list[tuple[str, str]]:
        cursor = self._connection.cursor()
        cursor.execute("SELECT name, hash FROM companies")
        return cursor.fetchall()

    def insert_salary_record(self, record: SalaryRecord) -> bool:
        cursor = self._connection.cursor()
        cursor.execute(
            """
            INSERT INTO salaries (
                id, company_hash, experience_level, salary_amount, gender, 
                submission_date, is_well_compensated, department, job_title
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.id,
                record.company_hash,
                record.experience_level.value,
                record.salary_amount,
                record.gender.value,
                record.submission_date,
                record.is_well_compensated,
                record.department.value,
                record.job_title,
            )
        )
        print("after")
        self._connection.commit()
        return True
    
    def insert_company(self, company: Company) -> bool:
        cursor = self._connection.cursor()
        cursor.execute(
            """
            INSERT INTO companies (
                hash, name, size, industry, country
            ) VALUES (?, ?, ?, ?, ?)
            """,
            (
                company.id,
                company.name,
                company.size.value,
                company.industry.value,
                company.country,
            )
        )
        self._connection.commit()
        return True

    def get_filtered_records(self, filters: FilterParams) -> list[SalaryRecord]:
        query = "SELECT * FROM salaries WHERE 1=1"
        params = []

        if "company_hash" in filters:
            query += " AND company_hash = ?"
            params.append(filters["company_hash"])

        if "industry" in filters:
            query += " AND company_hash IN (SELECT hash FROM companies WHERE industry = ?)"
            params.append(filters["industry"].value)

        if "department" in filters:
            query += " AND department = ?"
            params.append(filters["department"].value)

        if "experience_level" in filters:
            query += " AND experience_level = ?"
            params.append(filters["experience_level"].value)

        cursor = self._connection.cursor()
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        
        return [SalaryRecord(*row) for row in rows]

    def close(self) -> None:
        if self._connection:
            self._connection.close()
