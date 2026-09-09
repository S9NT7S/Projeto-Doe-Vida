from repositories.usuario_repository import UsuarioRepository
import bcrypt
from bcrypt import gensalt

class UsuarioService:
    def __init__(self, usuario_repository: UsuarioRepository):
        self.usuario_repository = usuario_repository

    def validar_senha(self, senha):
        if len(senha) < 8:
            return False, "A senha deve conter pelo menos 8 caracteres."
        if not any(c.isupper() for c in senha):
            return False, "A senha deve conter pelo menos uma letra maiúscula."
        if not any(c.isdigit() for c in senha):
            return False, "A senha deve conter pelo menos um número."
        caracteres_especiais = "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?`~"
        if not any(c in caracteres_especiais for c in senha):
            return False, "A senha deve conter pelo menos um caractere especial."
        return True, "Senha válida."

    def cadastrar_usuario(self, nome, email, senha, perfil, sangue, sexo, idade):
        try:
            if not isinstance(email, str) or "@" not in email:
                raise ValueError("Email inválido.")
            senha_valida, mensagem = self.validar_senha(senha)
            if not senha_valida:
                raise ValueError(mensagem)
            
            self.usuario_repository.salvar(nome, email, senha, perfil, sangue, sexo, idade)
        except Exception as e:
            return e
        
    def login_usuario(self, email, senha):
        return self.usuario_repository.validar_login(email, senha)

    def atualizar_usuario(self, usuario_id: int, novo_nome, nova_senha, novo_perfil, novo_sangue, novo_sexo, nova_idade):
        senha_hash = None
        if nova_senha:
            senha_valida, mensagem = self.validar_senha(nova_senha)
            if not senha_valida:
                raise ValueError(mensagem)
            senha_hash = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        try:
            self.usuario_repository.update_nome(novo_nome)
            self.usuario_repository.update_senha(nova_senha)
            
            #self.usuario_repository.atualizar(usuario_id, novo_nome=novo_nome, nova_senha=senha_hash, novo_perfil=novo_perfil, novo_sangue=novo_sangue, novo_sexo=novo_sexo, nova_idade=nova_idade)
        except Exception:
            print("Erro no usuario_service")

    def att_user(self, usuario_id, nome, senha, perfil, sexo, sangue, idade):
        senha_hash = None
        senha_valida = self.validar_senha(senha)
        if not senha_valida:
            raise ValueError
        senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode("utf-8")
        
        try:
            self.usuario_repository.update_nome(usuario_id, nome)
            self.usuario_repository.update_senha(usuario_id, senha_hash)
            self.usuario_repository.update_perfil(usuario_id, perfil)
            self.usuario_repository.update_sexo(usuario_id, sexo)
            self.usuario_repository.update_sangue(usuario_id, sangue)
            self.usuario_repository.update_idade(usuario_id, idade)

        except Exception:
            print("usuario service")

    def excluir_usuario(self, usuario_id):
        usuario = self.usuario_repository.buscar_por_id(usuario_id)
        
        if not usuario:
            raise ValueError("Usuário não encontrado.")

        try:            
            self.usuario_repository.excluir(usuario_id)
        
        except Exception as e:
            print("usuario_service")

    def obter_todos_usuarios(self):
        return self.usuario_repository.listar_todos()
    
    def obter_usuario_por_id(self, usuario_id: tuple):
        return self.usuario_repository.buscar_por_id(usuario_id)
    
    def obter_nome_do_usuario(self, nome):
        return self.usuario_repository.buscar_por_nome(nome)

    def obter_grupos(self, usuario_id: int):
        return self.usuario_repository.listar_grupos_do_usuario(usuario_id)
    
    def valida_admin(self, usuario_id):
        return self.usuario_repository.valida_admin(usuario_id)
    
    def salva_sangue(self, sangue):
        return self.salva_sangue(sangue)