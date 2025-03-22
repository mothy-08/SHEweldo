import math
import os
from flask import Flask, make_response, request, jsonify, send_from_directory
from flask_cors import CORS
from typing import Optional
from datetime import date

from models.enums import CompanySize, Department, ExperienceLevel, Gender, Industry
from models.entities import Company, SalaryRecord
from server.services import Service, SalaryService, CompanyService
from controllers.database import FilterParams, IDatabaseController

class AppAPI:
    def __init__(self,salary_service: Service, company_service: Service):
        self._salary_service = salary_service
        self._company_service = company_service

        current_dir = os.path.dirname(os.path.abspath(__file__)) 
        project_dir = os.path.dirname(current_dir)
        client_dir = os.path.join(project_dir, 'client') 
        static_dir = os.path.join(client_dir, 'static')

        self._app = Flask(__name__)
        CORS(self._app, resources={r"/api/*": {"origins": "*"}}) 
        self._client_dir = client_dir
        self._setup_api_routes()
        self._setup_frontend_routes()
        self._configure_error_handlers()

    def _setup_api_routes(self):
        @self._app.route("/api/salaries/submit", methods=["POST"])
        def post_salary():
            try:
                data = request.get_json()
                response_data = self._salary_service.add(data)

                if response_data.get("error"):
                    return jsonify(response_data), 500

                salary_id = response_data.get('id')
                salary_amount = response_data.get('salary')

                response = make_response(jsonify(response_data), 201)

                response.set_cookie('salary_id', str(salary_id), max_age=315360000, path='/', samesite='None', secure=True)
                response.set_cookie('salary_amount', str(salary_amount), max_age=315360000, path='/', samesite='None', secure=True)

                return response
            
            except ValueError as e:
                return jsonify({"error": str(e)}), 400
            except Exception as e:
                return jsonify({"error": "Server error"}), 500
            
        @self._app.route("/api/companies/add", methods=["POST"])
        def post_company():
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
            
        @self._app.route("/api/graphs/employee", methods=["GET"])
        def get_graphs():
            try:
                filters: FilterParams = {}

                salary_id = request.cookies.get('salary_id')
                raw_salary = float(request.cookies.get('salary_amount'))

                range_steps = int(request.args.get("range_steps")) if request.args.get("range_steps") else 1000
                salary_amount = math.floor(raw_salary / range_steps) * range_steps

                if 'company_hash' in request.args:
                    filters["company_hash"] = request.args.get("company_hash")

                if 'department' in request.args:
                    filters["department"] = Department(request.args.get("department").lower())

                if 'experience_level' in request.args:
                    filters["experience_level"] = ExperienceLevel(request.args.get("experience_level").lower())

                if not filters:
                    bargraph_data, piegraph_data = self._salary_service.fetch_filtered_records(range_steps, salary_id)
                else:
                    bargraph_data, piegraph_data = self._salary_service.fetch_filtered_records(range_steps, filters)

                return jsonify({
                    "bar_graph": bargraph_data,
                    "pie_graph": piegraph_data,
                    "current": salary_amount
                }), 200

            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self._app.route("/api/companies", methods=["GET"])
        def get_companies():
            try:
                companies = self._company_service.get_all()
                return jsonify([{"name": name, "hash": hash} for name, hash in companies]), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self._app.route("/api/salaries/averages", methods=["GET"])
        def get_averages():
            pass

        @self._app.route("/api/companies/<string:company_hash>", methods=["GET"])
        def get_benchmark(company_hash: str):
            pass
            
    def _setup_frontend_routes(self):
        @self._app.route('/', defaults={'path': 'index.html'})  # TODO: Change this to index.html
        @self._app.route('/<path:path>')
        def serve_frontend(path):
            # the landing page make user choose to compare salary or compare company
            return send_from_directory(self._client_dir, path)

        @self._app.route("/salaries/submit", methods=["GET"])
        def submit_salary():
            return send_from_directory(self._client_dir, 'salary_form.html')

        @self._app.route("/companies/add", methods=["GET"])
        def add_company():
            return send_from_directory(self._client_dir, 'company_form.html')

        @self._app.route("/graph/employee", methods=["GET"])
        def serve_employee_graph():
            return send_from_directory(self._client_dir, 'employee_graph.html')

        @self._app.route("/graph/companies/<string:company_hash>")
        def serve_company_graph():
            return send_from_directory(self._client_dir, 'company_graph.html')

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
    
    salary_service = SalaryService()
    company_service = CompanyService()
    
    api = AppAPI(salary_service, company_service)
    api.run(debug=True)
