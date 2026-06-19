from dotenv import load_dotenv
from flask import Flask, session

from controllers.html_basico_controller import HTMLBasicoController
from controllers.login_controller import LoginController
from controllers.AdminUsuarioController import AdminUsuarioController
from controllers.dashboard_controller import DashboardController
from controllers.js_controller import JSController

from banco.BancoMySQL import BancoMySQL
from banco.criador_tabelas import CriadorTabelas
from banco.seeds import SeedsBanco
from banco.integridade import IntegridadeBanco

from repositories.usuario_repository import UsuarioRepository
from repositories.grupo_repository import GrupoRepository
from repositories.dashboard_repository import DashboardRepository

from services.usuario_service import UsuarioService
from services.grupo_service import GrupoService
from services.dashboard_service import DashboardService

import os
import mysql.connector

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

banco = BancoMySQL()

@app.teardown_appcontext
def fechar_conexao_banco(exception):
    banco.fechar_conexao(exception)

conexao = mysql.connector.connect(
    host = os.getenv("DB_HOST"),
    user = os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD"),
    database = os.getenv("DB_NAME"),
    autocommit = False
)

cursor = conexao.cursor(dictionary=True)

CriadorTabelas(cursor).criar_todas_as_tabelas()

SeedsBanco(cursor, conexao).executar()

IntegridadeBanco(cursor).executar_validacoes()

conexao.commit()
cursor.close()
conexao.close()

usuario_repo = UsuarioRepository(banco)
grupo_repo = GrupoRepository(banco)
dashboard_repo = DashboardRepository(banco)

usuario_service = UsuarioService(usuario_repo)
grupo_service = GrupoService(grupo_repo)

dashboard_service = DashboardService(usuario_repo, dashboard_repo)

LoginController(app)

HTMLBasicoController(app, dashboard_service)

AdminUsuarioController(app, usuario_service, grupo_service)

DashboardController(app, dashboard_service)

JSController(app)

if __name__ == "__main__":
    app.run(debug=True)