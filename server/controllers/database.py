import sqlite3

class DatabaseController:
    def __init__(self, db_name="record.db"):
        self.db_name = db_name
        self.connection = None
        self.connect()

    def connect(self):
        self.connection = sqlite3.connect(self.db_name, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hash TEXT UNIQUE,
                name TEXT,
                size TEXT,
                industry TEXT,
                country TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS salaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_hash TEXT,
                years_at_company INTEGER,
                total_experience INTEGER,
                salary_amount REAL,
                gender TEXT,
                submission_date TEXT,
                is_well_compensated BOOLEAN,
                department TEXT,
                job_title TEXT,
                FOREIGN KEY(company_hash) REFERENCES companies(hash)
            )
        ''')
        self.connection.commit()

    def get_company(self, hash: str):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM companies WHERE hash = ?", (hash,))
        return cursor.fetchone()

    def insert_record(self, record):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO salaries (company_hash, years_at_company, total_experience, salary_amount, gender, submission_date, is_well_compensated, department, job_title) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (record.company.generate_hash(), record.years_at_company, record.total_experience, record.salary_amount, record.gender, record.submission_date, record.is_well_compensated, record.department, record.job_title))
        self.connection.commit()
        return True

    def get_records(self, filters):
        query = "SELECT * FROM salaries WHERE 1=1"
        params = []
        
        if "company_hash" in filters:
            query += " AND company_hash = ?"
            params.append(filters["company_hash"])
        if "position" in filters:
            query += " AND job_title = ?"
            params.append(filters["position"])
        
        cursor = self.connection.cursor()
        cursor.execute(query, tuple(params))
        return cursor.fetchall()

    def close(self):
        if self.connection:
            self.connection.close()