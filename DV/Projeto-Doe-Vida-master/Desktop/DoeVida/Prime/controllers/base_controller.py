from flask import session, redirect, url_for
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("usuario_logado"):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

class BaseController:
    def __init__(self, app):
        self.app = app
        if hasattr(self, 'rotas'):
            self.registrar_rotas()

    def registrar_rotas(self):
        for rota in self.rotas:
            if len(rota) == 3:
                endereco_url, nome_rota, funcao_resposta = rota
                self.app.add_url_rule(endereco_url, nome_rota, funcao_resposta)
            elif len(rota) == 4:
                endereco_url, nome_rota, funcao_resposta, metodos = rota
                self.app.add_url_rule(endereco_url, nome_rota, funcao_resposta, methods=metodos)

    def proteger_rota(self, funcao):
        return login_required(funcao)