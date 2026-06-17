from repositories.grupo_repository import GrupoRepository
from banco.BancoMySQL import BancoMySQL

class GrupoService:
    def __init__(self, grupo_repository:GrupoRepository):
        self.grupo_repository = grupo_repository

    def obter_todos(self):
        return self.grupo_repository.listar_todos()