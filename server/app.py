from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Optional
from datetime import date

from models.enums import CompanySize, Department, ExperienceLevel, Gender, Industry
from models.entities import Company, SalaryRecord
from server.services import IService, SalaryService, CompanyService
from controllers.database import FilterParams, IDatabaseController

class AppAPI:
    def __init__(self,salary_service: IService, company_service: IService, db: IDatabaseController):
        self._salary_service = salary_service
        self._company_service = company_service
        self._db = db
        self._app = Flask(__name__)
        CORS(self._app, resources={r"/api/*": {"origins": "*"}}) 
        self._setup_routes()
        self._configure_error_handlers()

    def _setup_routes(self):
        @self._app.route("/api/salaries/submit", methods=["POST"])
        def submit_salary():
            try:
                data = request.get_json()
                response = self._salary_service.add(data)
                if response.get("error"):
                    return jsonify(response), 500
                return jsonify(response), 201
            except ValueError as e:
                return jsonify({"error": str(e)}), 400
            except Exception as e:
                return jsonify({"error": "Server error"}), 500
            
        @self._app.route("/api/companies/add", methods=["POST"])
        def add_company():
            try:
                data = request.get_json()
                response = self._company_service.add(data)
                if response.get("error"):
                    return jsonify(response), 500
                return jsonify(response), 201
            except ValueError as e:
                return jsonify({"error": str(e)}), 400
            except Exception as e:
                return jsonify({"error": "Server error"}), 500
            
        @self._app.route("/api/graphs", methods=["GET"])
        def get_graphs():
            try:
                filters = FilterParams()

                if 'company_hash' in request.args:
                    filters["company_hash"] = request.args.get("company_hash")

                if 'industry' in request.args:
                    filters["industry"] = Industry(request.args.get("industry").lower())

                if 'department' in request.args:
                    filters["department"] = Department(request.args.get("department").lower())

                if 'experience_level' in request.args:
                    filters["experience_level"] = ExperienceLevel(request.args.get("experience_level").lower())

                bargraph_data, piegraph_data = self._salary_service.fetch_filtered_records(filters, 1000)

                return jsonify({
                    "bar_graph": bargraph_data,
                    "pie_graph": piegraph_data
                }), 200

            except Exception as e:
                return jsonify({"error": str(e)}), 500

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

    def run(self, host: str = "0.0.0.0", port: int = 5000, debug: bool = False):
        self._app.run(host=host, port=port, debug=debug)

if __name__ == "__main__":
    from server.services import SalaryService, CompanyService
    from controllers.database import DatabaseController
    
    db = DatabaseController()
    salary_service = SalaryService(db)
    company_service = CompanyService(db)
    
    api = AppAPI(salary_service, company_service, db)
    api.run(debug=True)
