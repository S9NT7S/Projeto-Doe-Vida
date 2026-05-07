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
    
    