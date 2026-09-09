import mysql.connector
import os
from banco.criador_tabelas import CriadorTabelas

class InicializadorBancos:
    def init(self):
        self.conexao = None
        self.cursor = None

    def inicializar(self):
        self.conectar()

        criador = CriadorTabelas(self.cursor)
        criador.criar_todas_as_tabelas()

        self.conexao.commit()
        self.fechar()

    def conectar(self):
        self.conexao = mysql.connector.connect(
            host = os.getenv("DB_HOST"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            database = os.getenv("DB_NAME")
        )

        self.cursor = self.conexao.cursor()

    def fechar(self):
        if self.cursor:
            self.cursor.close()

        if self.conexao:
            self.conexao.close()