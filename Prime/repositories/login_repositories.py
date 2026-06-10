class LoginRepository:
    def __init__(self, banco):
        self.banco = banco

    def registrar_login(self, usuario_id):
        sql = """
            INSERT INTO logins (usuario_id) VALUES (%s)
        """
        try:
            self.banco.executar(sql, (usuario_id,))
        except Exception as erro:
            print(f"Não foi possível registar login: {erro}")

    def listar_logins(self):
        sql = """
            SELECT 
                l.id, 
                u.usuario, 
                l.data_hora 
            FROM logins l 
            JOIN usuarios u ON u.id = l.usuario_id
            ORDER BY l.data_hora DESC
            """
        return self.banco.consultar(sql)