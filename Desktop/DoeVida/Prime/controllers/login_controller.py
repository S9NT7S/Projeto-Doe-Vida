from flask import render_template, request, redirect, url_for, session, flash
from controllers.base_controller import BaseController
from banco.BancoMySQL import BancoMySQL
from repositories.usuario_repository import UsuarioRepository
from repositories.login_repositories import LoginRepository
from services.usuario_service import UsuarioService
from services.login_service import LoginService
import requests

class LoginController(BaseController):
    def __init__(self, app, login_service):
        self.rotas = [
            ('/login', 'login', self.login),
            ('/entrar', 'entrar', self.entrar, ['POST']),
            ('/logout', 'logout', self.logout),
            ('/cadastro', 'cadastro', self.cadastro),
            ('/registrar', 'registrar', self.registrar, ['GET', 'POST']),
            ('/minha_area', 'minha_area', self.minha_area, ['GET', 'POST']),
            ('/gerar_usuarios', 'gerar_usuarios', self.gerar_usuarios_api, ['GET', 'POST']),
            ('/salvar_data', 'salvar_data', self.salvar_data, ['GET', 'POST']),
        ]
        super().__init__(app)

        self.login_service = login_service
        self.db = BancoMySQL()

    def login(self):
        if session.get("usuario_logado"):
            return redirect(url_for("home"))
        return render_template("login.html")

    def entrar(self):
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        if not usuario or not senha:
            erro = "Preencha usuário e senha"
            return render_template("login.html", erro=erro)
        
        if self.db.validar_credenciais(usuario, senha):
            session["usuario_logado"] = usuario

            query = "SELECT id, perfil FROM usuarios WHERE usuario = %s"
            self.db.cursor.execute(query, (usuario,))
            resultado = self.db.cursor.fetchone()

            session["usuario_id"] = resultado[0]
            session["perfil_logado"] = resultado[1]

            try:
                login_repo = LoginRepository(self.db)
                login_service = LoginService(login_repo)
                login_service.registrar_login(resultado[0])
            except Exception as erro:
                print(f"Erro ao registrar login login_controller: {erro}")

            return redirect(url_for("home"))
        else:
            erro = "Usuário ou senha incorretos"
            return render_template("login.html", erro=erro)
        
    def logout(self):
        session.clear()
        return render_template("login.html")
    
    def cadastro(self):
        return render_template("cadastro.html")
    
    def registrar(self):
        if request.method == 'POST':
            nome = request.form.get("nome")
            email = request.form.get("email")
            senha = request.form.get("senha")
            perfil = request.form.get("perfil")
            sexo = request.form.get("sexo")
            sangue = request.form.get("sangue")
            idade = request.form.get("idade")
        
        if not nome or not email or not senha or not idade:
            erro = "Todos os campos devem ser preenchidos"
            return render_template("cadastro.html", erro=erro)
        
        try:
            self.db.salvar_usuario(nome, email, senha, perfil, sexo, sangue, idade)
            sucesso = "Cadastro realizado com sucesso"
            return render_template("login.html", sucesso=sucesso)
        except ValueError as e:
            return render_template("cadastro.html", erro=str(e))
        except Exception as e:
            return render_template("cadastro.html", erro=f"Erro ao cadastrar usuário: {str(e)}")
        
    def salvar_data(self):
        if request.method == 'POST':
            hemocentro = request.form.get("hemocentro")
            usuario_id = request.form.get("usuario_id")
            data = request.form.get("data")
            horario = request.form.get("horario")

        try:
            self.login_service.registrar_horario(hemocentro, usuario_id, data, horario)
        except ValueError as e:
            return render_template("agendamento.html", erro=str(e))
    
    def minha_area(self):
        # tipoSangue = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-', 'Não tenho certeza']
        # sangue = request.form.get("sangue")
        return render_template("minha_area.html")
    
    def gerar_usuarios_api(self):
        if request.method == "POST":
            qtd = int(request.form.get("qtd", 5))

            try:
                response = requests.post(
                "http://localhost:5001/gerar_usuarios",
                json = {"qtd": qtd},
                timeout=200
                )
                data = response.json()
                usuarios_gerados = data.get("usuarios", [])

                user_repo = UsuarioRepository(self.db)
                user_service = UsuarioService(user_repo)

                for i in usuarios_gerados:
                    print(i)
                    user_service.cadastrar_usuario(
                        nome=i['nome'],
                        email=i.get('email', i['usuario']+"@fake.com"),
                        senha=i['senha'],
                        perfil=i['perfil'],
                        sexo=i['sexo'],
                        sangue=i['sangue'],
                        idade=i['idade']
                    )

                return render_template("cadastro.html", sucesso=f"{len(usuarios_gerados)} usuários gerados e salvos com sucesso")
        
            except Exception as e:
                return render_template("cadastro.html", erro=f"Erro ao chamar API: {str(e)}")
        
        return render_template("cadastro.html")
    
