from flask import jsonify, render_template
from controllers.base_controller import BaseController

class DashboardController(BaseController):
    def __init__(self, app, dashboard_service):
        self.service = dashboard_service
        self.rotas = [
            ("/dashboard", "dashboard_page", self.dashboard),
            ("/api/dashboard", "dashboard_api", self.api_dashboard),
        ]
        super().__init__(app)

    def dashboard(self):
        return render_template("dashboard.html")
    
    def api_dashboard(self):
        return jsonify(self.service.obter_dados())