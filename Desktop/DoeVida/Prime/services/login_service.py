from repositories.login_repositories import LoginRepository

class LoginService:
    def __init__(self, login_repo : LoginRepository):
        self.login_repo = login_repo

    def registrar_login(self, usuario_id):
        self.login_repo.registrar_login(usuario_id)

    def obter_logins(self):
        return self.login_repo.listar_logins()
    
    def registrar_horario(self, hemocentro, usuario_id, data, hora):
        return self.login_repo.saveDate(hemocentro, usuario_id, data, hora)