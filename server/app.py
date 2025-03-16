from flask import Flask, request, jsonify
from controllers.salary import SalaryService
from controllers.database import DatabaseController

class AppAPI:
    def __init__(self, service: SalaryService, db: DatabaseController):
        self.service = service
        self.db = db
        self.app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        @self.app.route("/submit", methods=["POST"])
        def submit_salary():
            data = request.json
            response = self.service.submit_salary(data)
            return jsonify(response)

        @self.app.route("/averages", methods=["GET"])
        def get_averages():
            response = self.service.get_averages()
            return jsonify(response)

        @self.app.route("/benchmark", methods=["GET"])
        def get_benchmark():
            response = self.service.get_benchmark()
            return jsonify(response)

        @self.app.route("/comparison", methods=["POST"])
        def get_comparison():
            data = request.json
            response = self.service.get_comparison(data)
            return jsonify(response)
        
        @self.app.route("/test", methods=["GET"])
        def test():
            response = self.service.test()
            return jsonify(response)

    def run(self, host="0.0.0.0", port=5000):
        self.app.run(host=host, port=port, debug=True)

if __name__ == "__main__":
    db_controller = DatabaseController()
    salary_controller = SalaryService(db_controller)
    api = AppAPI(salary_controller, db_controller)
    api.run()