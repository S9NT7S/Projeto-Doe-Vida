import bcrypt

class SeedsBanco:
    def __init__(self, cursor, conexao):
        self.cursor = cursor
        self.conexao = conexao

    def executar(self):
        self.criar_grupos_padrao()
        self.criar_admin()

    def criar_grupos_padrao(self):
        grupos = ['admin', 'Doador de primeira vez', 'Doador regular', 'Doador esporádico', 'Doador voluntário', 'Doador direcionado']
        
        for grupo in grupos:
            self.cursor.execute("""
            INSERT IGNORE INTO grupos (nome) VALUES (%s)
        """, (grupo,))
        
        self.conexao.commit()

    def criar_admin(self):
        self.cursor.execute(
            "SELECT COUNT(*) AS total FROM usuarios WHERE usuario = %s", ("admin",)
        )

        resultado = self.cursor.fetchone()

        existe = resultado["total"] > 0

        if existe:
            return
        
        senha_hash = bcrypt.hashpw("4444".encode(), bcrypt.gensalt()).decode()
        sexo = "Outro"
        sangue = "Não tenho certeza"
        idade = 40

        self.cursor.execute(
                "INSERT INTO usuarios (nome, usuario, senha, perfil, sexo, sangue, idade) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                ("admin", "admin", senha_hash, "admin", sexo, sangue, idade)
            )
        
        self.conexao.commit()