from banco.BancoMySQL import BancoMySQL

class DashboardRepository:
    def __init__(self, banco : BancoMySQL):
        self.banco = banco

    def contar_usuarios(self):
        sql = "SELECT COUNT(*) AS total FROM usuarios"
        return self.banco.query(sql)[0]["total"]
    
    def contar_admins(self):
        sql = "SELECT COUNT(*) AS TOTAL FROM usuarios WHERE perfil = 'admin'"
        return self.banco.query(sql)[0]["total"]
    
    def contar_doadores_primeira(self):
        # Primeira vez doando sangue
        sql = "SELECT COUNT(*) AS total FROM usuarios WHERE perfil = 'primeira'"
        return self.banco.query(sql)[0]["total"]
    
    def contar_doadores_regulares(self):
        # Doadores que doaram duas ou mais vezes em um período de 12 meses
        sql = "SELECT COUNT(*) AS total FROM usuarios WHERE perfil = 'regular'"
        return self.banco.query(sql)[0]["total"]
    
    def contar_doadores_esporadicos(self):
        # Doadores que doaram em um período superior a 12 meses
        sql = "SELECT COUNT(*) AS total FROM usuarios WHERE perfil = 'esporadico'"
        return self.banco.query(sql)[0]["total"]
    
    def contar_doadores_voluntarios(self):
        # Redundante!
        sql = "SELECT COUNT(*) AS total FROM usuarios WHERE perfil = 'voluntario'"
        return self.banco.query(sql)[0]["total"]
    
    def contar_doadores_direcionados(self):
        # Doadores que doaram a uma pessoa direcionada
        sql = "SELECT COUNT(*) AS total FROM usuarios WHERE perfil = 'direcionado'"
        return self.banco.query(sql)[0]["total"]
    
    def contar_perfil(self):
        # Contador de perfis ativos no sistema
        sql = "SELECT COUNT(*) AS total FROM perfil"
        return self.banco.query(sql)[0]["total"]
    
    def logins(self):
        # Contador de logins realizados ao longo do dia
        sql = """
            SELECT DATE(data_hora) AS data, COUNT(*) AS total
            FROM logins
            GROUP BY DATE(data_hora)
            ORDER BY data DESC
            LIMIT 7
        """
        return self.banco.query(sql)