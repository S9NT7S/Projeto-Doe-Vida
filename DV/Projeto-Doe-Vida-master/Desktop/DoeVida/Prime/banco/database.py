import os
import mysql.connector
from flask import g

class BancoDeDados:
    def obter_conexao(self):
        if "conexao_banco" not in g:
            g.conexao_banco = mysql.connector.connect(
                host = os.getenv("DB_HOST"),
                user = os.getenv("DB_USER"),
                password = os.getenv("DB_PASSWORD"),
                database = os.getenv("DB_NAME"),
                autocommit = False
            )

        return g.conexao_banco
    
    def fechar_conexao(self, erro=None):
        conexao = g.pop("conexao_banco", None)

        if conexao is not None:
            try:
                conexao.close()
            except Exception:
                pass

    def executar(self, sql: str, parametros: tuple | None = None):
        conexao = self.obter_conexao()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql, parametros or ())
            conexao.commit()

            return cursor.lastrowid
        except Exception:
            conexao.rollback()
            raise
        finally:
            cursor.close()

    def consultar(self, sql: str, parametros: tuple | None = None, unico: bool = False):
        conexao = self.obter_conexao()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql, parametros or ())

            if unico:
                return cursor.fetchone()
            return cursor.fetchall()
        finally:
            cursor.close()