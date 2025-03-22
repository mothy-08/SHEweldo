from abc import ABC, abstractmethod
from server.models.entities import SalaryRecord, Company
from server.models.enums import *
import sqlite3
from typing import Any, Dict, List, TypedDict, Optional

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
    def get_salary_record(self, salary_id: str) -> Optional[SalaryRecord]:
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

    

    def _build_where_clause_and_params(self, filters: FilterParams) -> tuple[str, List[Any]]:
        where_clause = "WHERE 1=1"
        params = []
        if "company_hash" in filters:
            where_clause += " AND company_hash = ?"
            params.append(filters["company_hash"])
        if "industry" in filters:
            where_clause += " AND company_hash IN (SELECT hash FROM companies WHERE industry = ?)"
            params.append(filters["industry"].value)
        if "department" in filters:
            where_clause += " AND department = ?"
            params.append(filters["department"].value)
        if "experience_level" in filters:
            where_clause += " AND experience_level = ?"
            params.append(filters["experience_level"].value)
        return where_clause, params


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
    
    def get_salary_record(self, salary_id: str) -> Optional[SalaryRecord]:
        if not isinstance(salary_id, str):
            raise ValueError("Invalid input: salary_id must be a string")
        
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM salaries WHERE id = ?", (salary_id,))
        row = cursor.fetchone()
        if row is not None:
            reordered_row = row[1:] + (row[0],)
            return SalaryRecord(*reordered_row)
        else:
            return None

    def insert_salary_record(self, record: SalaryRecord) -> bool:
        try:
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
            self._connection.commit()
            return True

        except sqlite3.Error as e:
            print(f"SQLite Error: {e}")
            return False
    
    def insert_company(self, company: Company) -> bool:
        try:
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

        except sqlite3.Error as e:
            print(f"SQLite Error: {e}")
            return False

    def get_filtered_records(self, filters: FilterParams) -> List[SalaryRecord]:
        where_clause, params = self._build_where_clause_and_params(filters)
        query = f"SELECT * FROM salaries {where_clause}"
        cursor = self._connection.cursor()
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        return [SalaryRecord(*row) for row in rows]

    def get_bar_graph_data(self, filters: FilterParams, range_step: int) -> list[dict]:
        where_clause, where_params = self._build_where_clause_and_params(filters)
        query = f"""
            SELECT FLOOR(salary_amount / ?) * ? AS range_start, COUNT(*) AS count
            FROM salaries
            {where_clause}
            GROUP BY range_start
            ORDER BY range_start DESC
        """
        params = [range_step, range_step] + where_params
        cursor = self._connection.cursor()
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        return [{"range_start": row[0], "count": row[1]} for row in rows]

    def get_pie_graph_data(self, filters: FilterParams) -> List[Dict[str, Any]]:
        where_clause, where_params = self._build_where_clause_and_params(filters)
        query = f"""
            SELECT is_well_compensated, COUNT(*) AS count
            FROM salaries
            {where_clause}
            GROUP BY is_well_compensated
        """
        cursor = self._connection.cursor()
        cursor.execute(query, tuple(where_params))
        rows = cursor.fetchall()
        return [{"is_well_compensated": row[0], "count": row[1]} for row in rows]

    def close(self) -> None:
        if self._connection:
            self._connection.close()