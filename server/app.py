from flask import Flask, request, jsonify
from typing import Optional
from datetime import date

from models.enums import CompanySize, Department, Gender
from models.entities import Company, SalaryRecord
from services.salary import ISalaryService
from controllers.database import IDatabaseController

class AppAPI:
    def __init__(self, service: ISalaryService, db: IDatabaseController):
        self._service = service
        self._db = db
        self._app = Flask(__name__)
        self._setup_routes()
        self._configure_error_handlers()

    def _setup_routes(self):
        @self._app.route("/api/salaries", methods=["POST"])
        def submit_salary():
            try:
                data = request.get_json()
                response = self._service.submit_salary(data)
                if response.get("error"):
                    return jsonify(response), 500
                return jsonify(response), 201
            except ValueError as e:
                return jsonify({"error": str(e)}), 400
            except Exception as e:
                return jsonify({"error": "Server error"}), 500

        @self._app.route("/api/salaries/averages", methods=["GET"])
        def get_averages():
            try:
                dept = request.args.get("department")
                if not dept:
                    return jsonify({"error": "Missing department parameter"}), 400
                department = Department[dept.upper()]
                averages = self._service.calculate_averages(department)
                return jsonify(averages), 200
            except KeyError:
                return jsonify({"error": "Invalid department"}), 400
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self._app.route("/api/companies/<string:company_hash>/benchmark", methods=["GET"])
        def get_benchmark(company_hash: str):
            try:
                company = self._db.get_company(company_hash)
                if not company:
                    return jsonify({"error": "Company not found"}), 404
                benchmark = self._service.generate_benchmark(company)
                return jsonify(benchmark), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self._app.route("/api/salaries/comparison", methods=["POST"])
        def get_comparison():
            try:
                data = request.get_json()
                record_id = data.get("id")
                records = self._db.get_records({"id": record_id})
                if not records:
                    return jsonify({"error": "Record not found"}), 404
                comparison = self._service.generate_comparison(records[0])
                return jsonify(comparison), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500

    def _configure_error_handlers(self):
        @self._app.errorhandler(404)
        def not_found(error):
            return jsonify({"error": "Resource not found"}), 404

        @self._app.errorhandler(405)
        def method_not_allowed(error):
            return jsonify({"error": "Method not allowed"}), 405

    def _create_company(self, data: dict) -> Company:
        try:
            return Company(
                entity_id=data.get("id"),
                name=data["name"],
                size=CompanySize[data["size"].upper()],
                industry=data["industry"],
                country=data["country"]
            )
        except KeyError as e:
            raise ValueError(f"Missing required field: {e}")

    def _create_salary_record(self, data: dict, company: Company) -> SalaryRecord:
        try:
            return SalaryRecord(
                entity_id=data.get("id"),
                company=company,
                years_at_company=int(data["years_at_company"]),
                total_experience=int(data["total_experience"]),
                salary_amount=float(data["salary_amount"]),
                gender=Gender[data["gender"].upper()],
                submission_date=date.fromisoformat(data["submission_date"]),
                is_well_compensated=bool(data["is_well_compensated"]),
                department=Department[data["department"].upper()],
                job_title=data["job_title"]
            )
        except (KeyError, ValueError) as e:
            raise ValueError(f"Invalid data format: {e}")

    def run(self, host: str = "0.0.0.0", port: int = 5000, debug: bool = False):
        self._app.run(host=host, port=port, debug=debug)

if __name__ == "__main__":
    from services.salary import SalaryService
    from controllers.database import DatabaseController
    
    db = DatabaseController()
    service = SalaryService(db)
    
    api = AppAPI(service, db)
    api.run(debug=True)
