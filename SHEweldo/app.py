import math

from quart import Quart, jsonify, request, render_template

from models.enums import Department, ExperienceLevel, Industry
from services import Service, SalaryService, CompanyService
from controllers.database import FilterParams


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

        @self._app.route("/api/salaries/submit", methods=["POST"])
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
            
        @self._app.route("/api/companies/add", methods=["POST"])
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
        async def get_graphs():
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

                if "company_hash" in request.args:
                    filters["company_hash"] = request.args.get("company_hash")

                if "department" in request.args:
                    filters["department"] = Department(request.args.get("department").lower())

                if "experience_level" in request.args:
                    filters["experience_level"] = ExperienceLevel(
                        request.args.get("experience_level").lower()
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

                if "department" in request.args:
                    filters["department"] = Department(request.args.get("department").lower())

                if "industry" in request.args:
                    filters["industry"] = Industry(request.args.get("industry").lower())

                if "experience_level" in request.args:
                    filters["experience_level"] = ExperienceLevel(
                        request.args.get("experience_level").lower()
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

        @self._app.route("/salaries/submit", methods=["GET"])
        async def submit_salary():
            return await render_template("salary-form.html")

        @self._app.route("/companies/add", methods=["GET"])
        async def add_company():
            return await render_template("companies.html")

        @self._app.route("/graph/employee", methods=["GET"])
        async def serve_employee_graph():
            return await render_template("employee-charts.html")

        @self._app.route("/graph/companies/", methods=["GET"])
        async def serve_company_graph():
            return await render_template("company-charts.html")

    def _configure_error_handlers(self):
        @self._app.errorhandler(404)
        async def not_found(error):
            return jsonify({"error": "Resource not found"}), 404

        @self._app.errorhandler(405)
        async def method_not_allowed(error):
            return jsonify({"error": "Method not allowed"}), 405

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
    import asyncio
    from hypercorn.asyncio import serve
    from hypercorn.config import Config

    async def run_app():
        salary_service = SalaryService()
        company_service = CompanyService()

        await salary_service.initialize()
        await company_service.initialize()

        api = AppAPI(salary_service, company_service)

        config = Config()
        config.bind = ["0.0.0.0:5000"]
        config.use_reloader = False

        await serve(api._app, config)

    asyncio.run(run_app())