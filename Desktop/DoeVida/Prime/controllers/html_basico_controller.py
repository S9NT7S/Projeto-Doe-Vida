from flask import render_template
from controllers.base_controller import BaseController

class HTMLBasicoController(BaseController):
    def __init__(self, app, dashboard_service):
        self.dashboard_service = dashboard_service
        self.rotas = [
            ('/', 'home', self.proteger_rota(self.pagina_inicial)),
            ('/cbasico1', 'cbasico1', self.cbasico1),
            ('/impedimentos_temp', 'impedimentos_temp', self.impedimentos_temp),
            ('/impedimentos_def', 'impedimentos_def', self.impedimentos_def),
            ('/testeModal', 'testeModal', self.testeModal),
            ('/agendamento', 'agendamento', self.agendamento),
            ('/agendaHemorgs', 'agendaHemorgs', self.hemorgs),
            ('/agendaHemopasso', 'agendaHemopasso', self.hemopasso),
            ('/agendaHemopel', 'agendaHemopel', self.hemopel),
            ('/agendaHemosm', 'agendaHemosm', self.hemosm),
            ('/agendaHemocruz', 'agendaHemocruz', self.hemocruz),
            ('/news', 'news', self.news)
        ]
        super().__init__(app)

    def pagina_inicial(self):
        return render_template("pagina_inicial.html")
    
    def cbasico1(self):
        return render_template("cbasico1.html")
    
    def impedimentos_temp(self):
        return render_template("impedimentos_temp.html")
    
    def impedimentos_def(self):
        return render_template("impedimentos_def.html")
    
    def testeModal(self):
        return render_template("testeModal.html")
    
    def agendamento(self):
        return render_template("agendamento.html")
    
    def hemorgs(self):
        return render_template("agendaHemorgs.html")
    
    def hemopasso(self):
        return render_template("agendaHemopasso.html")
    
    def hemopel(self):
        return render_template("agendaHemopel.html")
    
    def hemosm(self):
        return render_template("agendaHemosm.html")
    
    def hemocruz(self):
        return render_template("agendaHemocruz.html")
    
    def news(self):
        return render_template("news.html")