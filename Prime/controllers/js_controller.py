from flask import render_template, jsonify
from controllers.base_controller import BaseController
from banco.BancoMySQL import BancoMySQL
from repositories.dashboard_repository import DashboardRepository
from services.dashboard_service import DashboardService

class JSBascioController(BaseController):
    def __init__(self, app):
        self.rotas = [
            ('/js/dashboard', 'js_dashboard', self.proteger_rota(self.dashboard)),
            ('/js/graficos', 'js_graficos', self.proteger_rota(self.graficos)),
            ('/api/dashboard', 'api_dashboard', self.proteger_rota(self.api_dashboard)),
        ]
        super().__init__(app)

    def dashboard(self):
        return render_template("dashboard.html")
    
    def graficos(self):
        return render_template("graficos.html")
    
    def get_service(self):
        banco = BancoMySQL()
        repo = DashboardRepository(banco)
        return DashboardService(repo)
    
    def api_dashboard(self):
        service = self.get_service()
        dados = service.obter_dados_dashboard()
        return jsonify(dados)