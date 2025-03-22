from abc import ABC, abstractmethod
from models.entities import SalaryRecord, Company
from models.enums import *
import aiosqlite
from typing import Any, Dict, List, Tuple, TypedDict, Optional

class FilterParams(TypedDict, total=False):
    company_hash: str
    industry: Industry
    department: Department
    experience: ExperienceLevel

class IDatabaseController(ABC):
    @abstractmethod
    async def get_company_record(self, hash_val: str) -> Optional[Company]:
        pass
    
    @abstractmethod
    async def get_all_companies(self) -> list[tuple[str, str]]:
        pass

    @abstractmethod
    async def insert_salary_record(self, record: SalaryRecord) -> bool:
        pass
    
    @abstractmethod
    async def insert_company(self, company: Company) -> bool:
        pass

    @abstractmethod
    async def get_salary_record(self, salary_id: str) -> Optional[SalaryRecord]:
        pass

    @abstractmethod
    async def get_average_salary(self, company_hash: str) -> float:
        pass

    @abstractmethod
    async def get_filtered_records(self, filters: FilterParams) -> list[SalaryRecord]:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass

class DatabaseController(IDatabaseController):
    def __init__(self, db_name="record.db"):
        self._db_name = db_name
        self._connection = None

    async def initialize(self):
        await self._connect()

    async def _connect(self):
        try:
            self._connection = await aiosqlite.connect(self._db_name)
            await self._create_tables()
            print("Database connection established successfully.")
        except Exception as e:
            print(f"Failed to connect to the database: {e}")
            raise

    async def _create_tables(self):
        cursor = await self._connection.cursor()
        await cursor.execute('''
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

        await cursor.execute('''
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

        await self._connection.commit()

    async def _build_where_clause_and_params(self, filters: FilterParams) -> tuple[str, List[Any]]:
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

    async def get_company_record(self, hash_val: str) -> Optional[Company]:
        if not isinstance(hash_val, str):
            raise ValueError("Invalid input: company hash must be a string")

        cursor = await self._connection.cursor()
        await cursor.execute("SELECT * FROM companies WHERE hash = ?", (hash_val,))
        row = await cursor.fetchone()
        return Company(*row) if row else None
    
    async def get_all_companies(self) -> list[tuple[str, str]]:
        cursor = await self._connection.cursor()
        await cursor.execute("SELECT name, hash FROM companies")
        return await cursor.fetchall()
    
    async def get_salary_record(self, salary_id: str) -> Optional[SalaryRecord]:
        if not isinstance(salary_id, str):
            raise ValueError("Invalid input: salary_id must be a string")
        
        cursor = await self._connection.cursor()
        await cursor.execute("SELECT * FROM salaries WHERE id = ?", (salary_id,))
        row = await cursor.fetchone()
        if row is not None:
            reordered_row = row[1:] + (row[0],)
            return SalaryRecord(*reordered_row)
        else:
            return None

    async def get_average_salary(self, company_hash: str) -> float:
        cursor = await self._connection.cursor()
        await cursor.execute('''
            SELECT AVG(salary_amount) 
            FROM salaries 
            WHERE company_hash = ?
        ''', (company_hash,))

        result = await cursor.fetchone()
        if result and result[0] is not None:
            return int(float(result[0]))
        else:
            return 0

    async def insert_salary_record(self, record: SalaryRecord) -> bool:
        try:
            cursor = await self._connection.cursor()
            await cursor.execute(
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
            await self._connection.commit()
            return True

        except aiosqlite.Error as e:
            print(f"SQLite Error: {e}")
            return False
    
    async def insert_company(self, company: Company) -> bool:
        try:
            cursor = await self._connection.cursor()
            await cursor.execute(
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
            await self._connection.commit()
            return True

        except aiosqlite.Error as e:
            print(f"SQLite Error: {e}")
            return False

    async def get_filtered_records(self, filters: FilterParams) -> List[SalaryRecord]:
        where_clause, params = await self._build_where_clause_and_params(filters)
        query = f"SELECT * FROM salaries {where_clause}"
        cursor = await self._connection.cursor()
        await cursor.execute(query, tuple(params))
        rows = await cursor.fetchall()
        return [SalaryRecord(*row) for row in rows]

    async def get_benchmark_data(self, filters: FilterParams, range_step: int) -> List[Dict[str, Any]]:
        where_clause, params = await self._build_where_clause_and_params(filters)
        
        query = f"""
            WITH company_avg_salaries AS (
                SELECT company_hash, AVG(salary_amount) AS avg_salary
                FROM salaries
                {where_clause}
                GROUP BY company_hash
            )
            SELECT FLOOR(avg_salary / ?) * ? AS range_start, COUNT(*) AS count
            FROM company_avg_salaries
            GROUP BY range_start
            ORDER BY range_start DESC
        """
        params = [range_step, range_step] + params
        cursor = await self._connection.cursor()

        await cursor.execute(query, tuple(params))

        results = await cursor.fetchall()
        return [{"range_start": row[0], "count": row[1]} for row in results]

    async def get_bar_graph_data(self, filters: FilterParams, range_step: int) -> list[dict]:
        where_clause, where_params = await self._build_where_clause_and_params(filters)
        query = f"""
            SELECT FLOOR(salary_amount / ?) * ? AS range_start, COUNT(*) AS count
            FROM salaries
            {where_clause}
            GROUP BY range_start
            ORDER BY range_start DESC
        """
        params = [range_step, range_step] + where_params
        cursor = await self._connection.cursor()
        await cursor.execute(query, tuple(params))
        rows = await cursor.fetchall()
        return [{"range_start": row[0], "count": row[1]} for row in rows]

    async def get_pie_graph_data(self, filters: FilterParams, id: str = None) -> List[Dict[str, Any]]:
        where_clause, where_params = await self._build_where_clause_and_params(filters)

        if id:
            where_clause += " AND company_hash = ?"
            where_params.append(id)
            
        query = f"""
            SELECT is_well_compensated, COUNT(*) AS count
            FROM salaries
            {where_clause}
            GROUP BY is_well_compensated
        """
        cursor = await self._connection.cursor()
        await cursor.execute(query, tuple(where_params))
        rows = await cursor.fetchall()
        return [{"is_well_compensated": row[0], "count": row[1]} for row in rows]

    async def close(self) -> None:
        if self._connection:
            await self._connection.close()