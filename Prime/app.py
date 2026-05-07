from flask import Flask, session
from controllers.html_basico_controller import HTMLBasicoController
from controllers.login_controller import LoginController
from controllers.AdminUsuarioController import AdminUsuarioController
from banco.BancoMySQL import BancoMySQL
from repositories.usuario_repository import UsuarioRepository
from repositories.grupo_repository import GrupoRepository
from services.usuario_service import UsuarioService
from services.grupo_service import GrupoService
import os

app = Flask(__name__)
app.secret_key = os.urandom(100)

banco = BancoMySQL()

usuario_repo = UsuarioRepository(banco)
grupo_repo = GrupoRepository(banco)

usuario_service = UsuarioService(usuario_repo)
grupo_service = GrupoService(grupo_repo)

LoginController(app)
HTMLBasicoController(app)
AdminUsuarioController(app, usuario_service, grupo_service)

if __name__ == "__main__":
    app.run(debug=True)