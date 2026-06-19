class CriadorTabelas:
    def __init__(self, cursor):
        self.cursor = cursor

    def criar_todas_as_tabelas(self):
        self.criar_tabelas_usuarios()
        self.criar_tabela_logins()
        self.criar_tabela_grupos()
        self.criar_tabela_usuario_grupo()

    
    def criar_tabelas_usuarios(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                usuario VARCHAR(255) UNIQUE NOT NULL,
                senha VARCHAR(255) NOT NULL,
                perfil VARCHAR(50) NOT NULL DEFAULT 'Doador de primeira vez',
                sexo VARCHAR(50) NOT NULL,
                sangue VARCHAR(50) NOT NULL DEFAULT 'Não tenho certeza',
                idade INT NOT NULL
            )
        """)

    def criar_tabela_logins(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS logins (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT NOT NULL,
                data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
            )
        """)

    def criar_tabela_grupos(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS grupos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) UNIQUE  NOT NULL
            )
        """)

    def criar_tabela_usuario_grupo(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario_grupo (
                usuario_id INT NOT NULL,
                grupo_id INT NOT NULL,
                PRIMARY KEY (usuario, grupo_id),
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
                FOREIGN KEY (grupo_id) REFERENCES grupos(id) ON DELETE CASCADE
            )
        """)
