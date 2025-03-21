import os
from abc import ABC, abstractmethod
from pymongo import MongoClient
from dotenv import load_dotenv
from server.models.entities import SalaryRecord, Company
from server.models.enums import *
from typing import Any, Dict, List, TypedDict, Optional

load_dotenv()

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
    def __init__(self, db_name="record_db"):
        mongo_uri = os.getenv("MONGO_URI")  # Fetch from environment variables
        if not mongo_uri:
            raise ValueError("MongoDB URI not found in environment variables.")
        self._client = MongoClient(mongo_uri)
        self._db = self._client[db_name]

    def get_company_record(self, hash_val: str) -> Optional[Company]:
        result = self._db.companies.find_one({"hash": hash_val})
        return Company(**result) if result else None
    
    def get_all_companies(self) -> list[tuple[str, str]]:
        return [(company["name"], company["hash"]) for company in self._db.companies.find({}, {"name": 1, "hash": 1})]

    def insert_salary_record(self, record: SalaryRecord) -> bool:
        try:
            self._db.salaries.insert_one(record.__dict__)
            return True
        except Exception as e:
            print(f"MongoDB Error: {e}")
            return False
    
    def insert_company(self, company: Company) -> bool:
        try:
            self._db.companies.insert_one(company.__dict__)
            return True
        except Exception as e:
            print(f"MongoDB Error: {e}")
            return False

    def get_filtered_records(self, filters: FilterParams) -> List[SalaryRecord]:
        query = self._build_query(filters)
        results = self._db.salaries.find(query)
        return [SalaryRecord(**record) for record in results]

    def get_bar_graph_data(self, filters: FilterParams, range_step: int) -> list[dict]:
        query = self._build_query(filters)
        pipeline = [
            {"$match": query},
            {"$group": {"_id": {"$floor": {"$divide": ["$salary_amount", range_step]}}, "count": {"$sum": 1}}}
        ]
        results = self._db.salaries.aggregate(pipeline)
        return [{"range_start": doc["_id"] * range_step, "count": doc["count"]} for doc in results]

    def get_pie_graph_data(self, filters: FilterParams) -> List[Dict[str, Any]]:
        query = self._build_query(filters)
        pipeline = [
            {"$match": query},
            {"$group": {"_id": "$is_well_compensated", "count": {"$sum": 1}}}
        ]
        results = self._db.salaries.aggregate(pipeline)
        return [{"is_well_compensated": doc["_id"], "count": doc["count"]} for doc in results]

    def _build_query(self, filters: FilterParams) -> Dict[str, Any]:
        query = {}
        if "company_hash" in filters:
            query["company_hash"] = filters["company_hash"]
        if "industry" in filters:
            query["industry"] = filters["industry"].value
        if "department" in filters:
            query["department"] = filters["department"].value
        if "experience_level" in filters:
            query["experience_level"] = filters["experience_level"].value
        return query

    def close(self) -> None:
        self._client.close()
