class AppAPI:
    def __init__(self, salary_service, company_service):
        pass

    def _setup_api_routes(self):
        @self._app.route("/api/salaries/submit", methods=["POST"])
        async def post_salary():
            pass

        @self._app.route("/api/companies/add", methods=["POST"])
        async def post_company():
            pass

        @self._app.route("/api/graphs/employee", methods=["GET"])
        async def get_graphs():
            pass

        @self._app.route("/api/companies", methods=["GET"])
        async def get_companies():
            pass

        @self._app.route("/api/companies/<string:company_hash>", methods=["GET"])
        async def get_benchmark(company_hash):
            pass

    def _setup_frontend_routes(self):
        @self._app.route("/", defaults={"path": "landingPage.html"})
        @self._app.route("/<path:path>")
        async def serve_frontend(path):
            pass

        @self._app.route("/salaries/submit", methods=["GET"])
        async def submit_salary():
            pass

        @self._app.route("/companies/add", methods=["GET"])
        async def add_company():
            pass

        @self._app.route("/graph/employee", methods=["GET"])
        async def serve_employee_graph():
            pass

        @self._app.route("/graph/companies/", methods=["GET"])
        async def serve_company_graph():
            pass

    def _configure_error_handlers(self):
        @self._app.errorhandler(404)
        async def not_found(error):
            pass

        @self._app.errorhandler(405)
        async def method_not_allowed(error):
            pass

    def run(self, host="0.0.0.0", port=5000, debug=False):
        pass

async def main():
    pass

if __name__ == "__main__":
    async def run_app():
        pass

    run_app()
