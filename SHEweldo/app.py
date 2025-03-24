import asyncio
import math
import sys
import logging


sys.path.append(".")

from quart import Quart, jsonify, request, render_template

from SHEweldo.models.enums import Department, ExperienceLevel, Gender, Industry
from SHEweldo.services import Service, SalaryService, CompanyService
from SHEweldo.controllers.database import FilterParams


class AppAPI:
    def __init__(self, salary_service: Service, company_service: Service):
        self._salary_service = salary_service
        self._company_service = company_service

        self._app = Quart(__name__)
        self._app.debug = True

        self._setup_api_routes()
        self._setup_frontend_routes()
        self._configure_error_handlers()

    def _setup_api_routes(self):

        @self._app.route("/api/employee/submit", methods=["POST"])
        async def post_salary():
            try:
                data = await request.get_json()
                if not data:
                    return jsonify({"error": "No data provided"}), 400

                response_data = await self._salary_service.add(data)

                if response_data.get("error"):
                    return jsonify(response_data), 500

                salary_id = response_data.get("id")
                salary_amount = response_data.get("salary")

                response = jsonify(response_data)
                response.status_code = 201

                response.set_cookie(
                    "salary_id",
                    str(salary_id),
                    max_age=315360000,
                    path="/",
                    samesite="None",
                    secure=True,
                )
                response.set_cookie(
                    "salary_amount",
                    str(salary_amount),
                    max_age=315360000,
                    path="/",
                    samesite="None",
                    secure=True,
                )

                return response

            except ValueError as e:
                return jsonify({"error": str(e)}), 400
            except Exception as e:
                return jsonify({"error": "Server error"}), 500
            
        @self._app.route("/api/company/submit", methods=["POST"])
        async def post_company():
            try:
                data = await request.get_json()
                response = await self._company_service.add(data)
                if response.get("error"):
                    return jsonify(response), 500
                return jsonify(response), 201
            except ValueError as e:
                return jsonify({"error": str(e)}), 400
            except Exception as e:
                return jsonify({"error": "Server error"}), 500

        @self._app.route("/api/graphs/employee", methods=["GET"])
        async def get_comparison_graphs():
            try:
                filters: FilterParams = {}

                salary_id = request.cookies.get("salary_id")
                raw_salary = float(request.cookies.get("salary_amount"))

                range_steps = (
                    int(request.args.get("range_steps"))
                    if request.args.get("range_steps")
                    else 1000
                )
                salary_amount = math.floor(raw_salary / range_steps) * range_steps

                filters = self._salary_service._build_filters(
                    request.args,
                    [
                        ("company_hash", None),
                        ("industry", Industry),
                        ("department", Department),
                        ("experience_level", ExperienceLevel),
                        ("gender", Gender)
                    ]
                )

                if not filters:
                    bargraph_data, piegraph_data = await self._salary_service.fetch_filtered_records(
                        range_steps, salary_id
                    )
                else:
                    bargraph_data, piegraph_data = await self._salary_service.fetch_filtered_records(
                        range_steps, filters
                    )

                return jsonify(
                    {
                        "bar_graph": bargraph_data,
                        "pie_graph": piegraph_data,
                        "current": salary_amount,
                    }
                ), 200

            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self._app.route("/api/companies", methods=["GET"])
        async def get_companies():
            try:
                companies = await self._company_service.get_all()
                return jsonify([{"name": name, "hash": hash} for name, hash in companies]), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self._app.route("/api/companies/<string:company_hash>", methods=["GET"])
        async def get_benchmark(company_hash: str):
            try:
                filters: FilterParams = {}

                range_steps = (
                    int(request.args.get("range_steps"))
                    if request.args.get("range_steps")
                    else 1000
                )

                filters = self._company_service._build_filters(
                    request.args,
                    [
                        ("industry", Industry),
                        ("department", Department),
                        ("experience_level", ExperienceLevel),
                        ("gender", Gender)
                    ]
                )

                if not filters:
                    bargraph_data, current_average, piegraph_data = await self._company_service.fetch_filtered_records(
                        salary_range_step=range_steps, id=company_hash
                    )
                else:
                    bargraph_data, current_average, piegraph_data = await self._company_service.fetch_filtered_records(
                        salary_range_step=range_steps, filters=filters, id=company_hash
                    )

                return jsonify(
                    {
                        "bar_graph": bargraph_data,
                        "current_avg": current_average,
                        "pie_graph": piegraph_data,
                    }
                ), 200

            except Exception as e:
                return jsonify({"error": str(e)}), 500

    def _setup_frontend_routes(self):
        @self._app.route("/")
        async def serve_frontend():
            return await render_template("index.html")

        @self._app.route("/employee/submit", methods=["GET"])
        async def submit_salary():
            return await render_template("salary-form.html")

        @self._app.route("/company/submit", methods=["GET"])
        async def add_company():
            return await render_template("company-form.html")

        @self._app.route("/employee/graph", methods=["GET"])
        async def serve_employee_graph():
            return await render_template("employee-charts.html")

        @self._app.route("/company/graph", methods=["GET"])
        async def serve_company_graph():
            return await render_template("company-charts.html")

    def _configure_error_handlers(self):
        @self._app.errorhandler(404)
        async def not_found(error):
            return await render_template(
                "error.html",
                error_code="404",
                error_message="Oops! The page you're looking for doesn't exist."
            ), 404

        @self._app.errorhandler(500)
        async def internal_server_error(error):
            return await render_template(
                "error.html",
                error_code="500",
                error_message="Something went wrong on our end. Please try again later."
            ), 500

        @self._app.errorhandler(405)
        async def method_not_allowed(error):
            return await render_template(
                "error.html",
                error_code="405",
                error_message="This method is not allowed for the requested resource."
            ), 405

    def run(self, host: str = "0.0.0.0", port: int = 5000, debug: bool = False):
        self._app.run(host=host, port=port, debug=debug)


async def main():
    salary_service = SalaryService()
    company_service = CompanyService()

    await salary_service.initialize()
    await company_service.initialize()

    api = AppAPI(salary_service, company_service)

    api.run(debug=True)


if __name__ == "__main__":
    import logging
    import os
    import asyncio
    from hypercorn.config import Config
    from hypercorn.asyncio import serve

    log_file = os.path.abspath("app.log")
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)
    logger.info("===== Application Starting =====")

    async def setup_app():
        from SHEweldo.services import SalaryService, CompanyService
        
        salary_service = SalaryService()
        company_service = CompanyService()
        await salary_service.initialize()
        await company_service.initialize()
        
        from SHEweldo.app import AppAPI
        api = AppAPI(salary_service, company_service)
        return api._app

    config = Config()
    config.bind = ["0.0.0.0:5000"]
    config.use_reloader = True
    config.loglevel = "info"
    config.logconfig = None

    certfile_path = os.path.join("SHEweldo", "localhost.pem")
    keyfile_path = os.path.join("SHEweldo", "localhost-key.pem")

    if os.path.exists(certfile_path) and os.path.exists(keyfile_path):
        config.certfile = certfile_path
        config.keyfile = keyfile_path
        logger.info("SSL/TLS certificates found. Enabling HTTPS.")
    else:
        logger.warning("SSL/TLS certificates not found. Running in HTTP mode.")

    try:
        logger.info(f"Log file location: {log_file}")
        app = asyncio.run(setup_app())
        asyncio.run(serve(app, config))
    except Exception as e:
        logger.exception("Server failed to start")
        raise