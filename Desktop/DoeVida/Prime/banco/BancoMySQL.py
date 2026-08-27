import mysql.connector
from mysql.connector import Error
import bcrypt
import re

from dotenv import load_dotenv
load_dotenv()
import os

class BancoMySQL:
    def __init__(self):
        cnx = mysql.connector.connect(
            host = os.getenv("DB_HOST"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            database = os.getenv("DB_NAME")
        )
        cursor = cnx.cursor()
        cursor.execute("SELECT COUNT(*) FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = 'santos_application';")
        num_results = cursor.fetchone()[0]
        cnx.close()

        if num_results == 0:
            cnx = mysql.connector.connect(
                host = os.getenv("DB_HOST"),
                user = os.getenv("DB_USER"),
                password = os.getenv("DB_PASSWORD"),
                database = os.getenv("DB_NAME")
            )
            cursor = cnx.cursor()
            #cursor.execute("CREATE DATABASE santos_application;")
            cnx.commit()
            cnx.close()

        try:
            self.conexao = mysql.connector.connect(
                host = os.getenv("DB_HOST"),
                user = os.getenv("DB_USER"),
                password = os.getenv("DB_PASSWORD"),
                database = os.getenv("DB_NAME")
            )
            self.cursor = self.conexao.cursor()

            self.criar_tabela_usuarios()
            self.criar_tabela_logins()
            self.criar_tabela_grupos()
            self.criar_grupos_padrao()
            self.usuario_admin()
            self.criar_indices()
            self.criar_tabela_testes()
            self.criar_tabela_defeitos()
            self.criar_tabela_horarios()
            self.criar_hemocentros()

        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")
            raise

    # def criar_tabela_usuarios(self):
    #     self.cursor.execute("""
    #         CREATE TABLE IF NOT EXISTS usuarios (
    #             id INT AUTO_INCREMENT PRIMARY KEY,
    #             nome VARCHAR(100) NOT NULL,
    #             sobrenome VARCHAR(100),
    #             cpf INT(11) UNIQUE NOT NULL,
    #             idade VARCHAR(50) NOT NULL,
    #             usuario VARCHAR(100) UNIQUE NOT NULL,
    #             senha VARCHAR(100) NOT NULL,
    #             perfil VARCHAR(50) NOT NULL DEFAULT 'Doador de primeira vez',
    #             sexo VARCHAR(50) NOT NULL,
    #             sangue VARCHAR(50) NOT NULL DEFAULT 'Não tenho certeza',
    #             telefone INT(11),
    #             cep INT(8),
    #         )
    #     """)
    #     self.conexao.commit()

    def criar_tabela_usuarios(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                usuario VARCHAR(100) UNIQUE NOT NULL,
                senha VARCHAR(100) NOT NULL,
                perfil VARCHAR(50) NOT NULL DEFAULT 'Doador de primeira vez',
                sexo VARCHAR(50) NOT NULL,
                sangue VARCHAR(50) NOT NULL DEFAULT 'Não tenho certeza',
                idade VARCHAR(50) NOT NULL
            )
        """)
        self.conexao.commit()

    def criar_tabela_logins(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS logins (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT NOT NULL,
                data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
            )
        """)
        self.conexao.commit()

    def criar_tabela_grupos(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS grupos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL UNIQUE
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario_grupo (
                usuario_id INT NOT NULL,
                grupo_id INT NOT NULL,
                PRIMARY KEY (usuario_id, grupo_id),
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
                FOREIGN KEY (grupo_id) REFERENCES grupos(id) ON DELETE CASCADE
            )
        """)
        self.conexao.commit()

    def criar_tabela_horarios(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS horarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                hemocentro VARCHAR(50) NOT NULL,
                usuario_id INT NOT NULL,
                data DATE,
                hora TIME,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
            );
        """)

    def criar_hemocentros(self):
        hemocentros = ['Hemorgs', 'Hemopel', 'Hemopasso', 'Hemosm', 'Hemocruz']
        for i in hemocentros:
            self.adcionar_hemo(i)
        self.conexao.commit()

    def adcionar_hemo(self, nome):
        try:
            self.cursor.execute("INSERT INTO horarios (hemocentro) VALUES (%s)", (nome,))
            self.conexao.commit()
        except mysql.connector.IntegrityError:
            pass    

    def criar_grupos_padrao(self):
        grupos = ['admin', 'Doador de primeira vez', 'Doador regular', 'Doador esporádico', 'Doador voluntário', 'Doador direcionado']
        for grupo in grupos:
            self.adicionar_grupo(grupo)
        self.conexao.commit()

    def adicionar_grupo(self, nome_grupo):
        try:
            self.cursor.execute("INSERT INTO grupos (nome) VALUES (%s)", (nome_grupo,))
            self.conexao.commit()
        except mysql.connector.IntegrityError:
            pass

    def associar_usuario_grupo(self, usuario_id, grupo_nome):
        self.cursor.execute("SELECT id FROM grupos WHERE nome = %s", (grupo_nome,))
        grupo = self.cursor.fetchone()
        if not grupo:
            self.adicionar_grupo(grupo_nome)
            self.cursor.execute("SELECT id FROM grupos WHERE nome = %s", (grupo_nome,))
            grupo = self.cursor.fetchone()
            
        grupo_id = grupo[0]

        self.cursor.execute(
            "SELECT * FROM usuario_grupo WHERE usuario_id = %s AND grupo_id = %s",
            (usuario_id, grupo_id)
        )
        if self.cursor.fetchone():
            return
        
        self.cursor.execute(
            "INSERT INTO usuario_grupo (usuario_id, grupo_id) VALUES (%s, %s)",
            (usuario_id, grupo_id)
        )
        self.conexao.commit()

    # def salvar_usuario(self, nome, sobrenome, cpf, idade, usuario, senha, perfil, sexo, sangue, telefone, cep):
        
    #     if not re.match(r"[^@]+@[^@]+\.[^@]+", usuario):
    #         raise ValueError("Email inválido")
        
    #     try:
    #         self.cursor.execute(
    #             "SELECT * FROM cpfs WHERE cpf = %s",
    #             (cpf,)
    #         )
    #         if self.cursor.fetchone():
    #             self.registrar_teste(
    #                 funcao="salvar_usuario",
    #                 tipo="Dinâmico",
    #                 caso="Tentativa de cadastro com usuário existente",
    #                 entrada={"usuario": usuario},
    #                 esperado="Erro de usuário duplicado",
    #                 obtido="Usuário já existe",
    #                 status="Falha",
    #                 observacoes="Validação de unicidade falhou - usuário duplicado"
    #             )
    #             self.registrar_defeito("BancoMySQL.salvar_usuario", f"Tentativa de criar usuário duplicado: {usuario}")
    #             raise ValueError("O usuário já existe.")
            
    #         senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

    #         self.cursor.execute(
    #             "INSERT INTO usuarios (nome, sobrenome, cpf, usuario, senha, perfil, sexo, sangue, idade) VALUES (%s, %s, %s, %s, %s, %s, %s)",
    #             (nome, usuario, senha_hash, perfil, sexo, sangue, idade)
    #         )
    #         self.conexao.commit()

    #         self.cursor.execute("SELECT id FROM usuarios WHERE usuario = %s", (usuario,))
    #         usuario_id = self.cursor.fetchone()[0]

    #         self.registrar_teste(
    #             funcao="salvar_usuario",
    #             tipo="Dinâmico",
    #             caso="Cadastro de novo usuário",
    #             entrada={"usuario": usuario, "perfil": perfil},
    #             esperado="Usuário criado com sucesso",
    #             obtido="Usuário criado com sucesso",
    #             status="Sucesso"
    #         )

    #     except mysql.connector.IntegrityError as e:
            
    #         self.registrar_defeito("BancoMySQL.salvar_usuario", f"Erro de integridade ao salvar usuário: {e}")
    #         self.registrar_teste(
    #             funcao="salvar_usuario",
    #             tipo="Dinâmico",
    #             caso="Erro de integridade ao salvar usuário",
    #             entrada={"usuario": usuario},
    #             esperado="Cadastro bem-sucedido",
    #             obtido=str(e),
    #             status="Falha",
    #             observacoes="Erro de integridade ao tentar salvar usuário"
    #         )
    #         raise

    #     except Exception as e:
    #         self.registrar_defeito("BancoMySQL.salvar_usuario", f"Erro inesperado ao salvar usuário: {e}")
    #         self.registrar_teste(
    #             funcao="salvar_usuario",
    #             tipo="Dinâmico",
    #             caso="Erro inesperado ao salvar usuário",
    #             entrada={"usuario": usuario},
    #             esperado="Usuário criado com sucesso",
    #             obtido=str(e),
    #             status="Falha",
    #             observacoes="Erro inesperado ao tentar salvar usuário"
    #         )
    #         raise
        
    def salvar_usuario(self, nome, usuario, senha, perfil, sexo, sangue, idade):
        
        if not re.match(r"[^@]+@[^@]+\.[^@]+", usuario):
            raise ValueError("Email inválido")
        
        try:
            self.cursor.execute(
                "SELECT * FROM usuarios WHERE usuario = %s",
                (usuario,)
            )
            if self.cursor.fetchone():
                self.registrar_teste(
                    funcao="salvar_usuario",
                    tipo="Dinâmico",
                    caso="Tentativa de cadastro com usuário existente",
                    entrada={"usuario": usuario},
                    esperado="Erro de usuário duplicado",
                    obtido="Usuário já existe",
                    status="Falha",
                    observacoes="Validação de unicidade falhou - usuário duplicado"
                )
                self.registrar_defeito("BancoMySQL.salvar_usuario", f"Tentativa de criar usuário duplicado: {usuario}")
                raise ValueError("O usuário já existe.")
            
            senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

            self.cursor.execute(
                "INSERT INTO usuarios (nome, usuario, senha, perfil, sexo, sangue, idade) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (nome, usuario, senha_hash, perfil, sexo, sangue, idade)
            )
            self.conexao.commit()

            self.cursor.execute("SELECT id FROM usuarios WHERE usuario = %s", (usuario,))
            usuario_id = self.cursor.fetchone()[0]

            self.registrar_teste(
                funcao="salvar_usuario",
                tipo="Dinâmico",
                caso="Cadastro de novo usuário",
                entrada={"usuario": usuario, "perfil": perfil},
                esperado="Usuário criado com sucesso",
                obtido="Usuário criado com sucesso",
                status="Sucesso"
            )

        except mysql.connector.IntegrityError as e:
            
            self.registrar_defeito("BancoMySQL.salvar_usuario", f"Erro de integridade ao salvar usuário: {e}")
            self.registrar_teste(
                funcao="salvar_usuario",
                tipo="Dinâmico",
                caso="Erro de integridade ao salvar usuário",
                entrada={"usuario": usuario},
                esperado="Cadastro bem-sucedido",
                obtido=str(e),
                status="Falha",
                observacoes="Erro de integridade ao tentar salvar usuário"
            )
            raise

        except Exception as e:
            self.registrar_defeito("BancoMySQL.salvar_usuario", f"Erro inesperado ao salvar usuário: {e}")
            self.registrar_teste(
                funcao="salvar_usuario",
                tipo="Dinâmico",
                caso="Erro inesperado ao salvar usuário",
                entrada={"usuario": usuario},
                esperado="Usuário criado com sucesso",
                obtido=str(e),
                status="Falha",
                observacoes="Erro inesperado ao tentar salvar usuário"
            )
            raise

    def validar_credenciais(self, usuario, senha):
        query = "SELECT senha FROM usuarios WHERE usuario = %s"
        self.cursor.execute(query, (usuario,))
        resultado = self.cursor.fetchone()
        if resultado:
            senha_hash = resultado[0]
            return bcrypt.checkpw(senha.encode(), senha_hash.encode())
        return False
    
    def registrar_login(self, usuario):
        self.cursor.execute("SELECT id FROM usuarios WHERE usuario = %s", (usuario,))
        usuario_id = self.cursor.fetchone()[0]
        if usuario_id:
            self.cursor.execute("INSERT INTO logins (usuario_id) VALUES (%s)", (usuario_id[0],))
            self.conexao.commit()

    def usuario_admin(self):
        self.cursor.execute("SELECT COUNT(*) FROM usuarios WHERE usuario = %s", ("admin",))
        if self.cursor.fetchone()[0] == 0:
            senha_hash = bcrypt.hashpw("4444".encode(), bcrypt.gensalt()).decode()
            sexo = "Outro"
            sangue = "Não tenho certeza"
            idade = 40

            self.cursor.execute(
                "INSERT INTO usuarios (nome, usuario, senha, perfil, sexo, sangue, idade) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                ("admin", "admin", senha_hash, "admin", sexo, sangue, idade)
            )
            self.conexao.commit()
            self.cursor.execute("SELECT id FROM usuarios WHERE usuario = %s", ("admin",))
            admin_id = self.cursor.fetchone()[0]
            self.associar_usuario_grupo(admin_id, "admin")
            print("Admin criado com sucesso.")

    def obter_grupos_usuario(self, usuario):
        query = """
            SELECT g.nome FROM grupos g
            JOIN usuario_grupo ug ON g.id = ug.grupo_id
            JOIN usuarios u ON ug.id = ug.usuario_id
            WHERE u.usuario = %s
            """
        
        self.cursor.execute(query, (usuario,))
        return [row[0] for row in self.cursor.fetchall()]

    def criar_indices(self):
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_usuarios_perfil ON usuarios (perfil)")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_logins_data_hora ON logins (data_hora)")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_usuario_grupo_usuario_id ON usuario_grupo (usuario_id)")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_usuario_grupo_grupo_id ON usuario_grupo (grupo_id)")
        self.conexao.commit()

    def obter_usuarios_com_grupos_inner_join(self):
        query = """
            SELECT u.usuario, u.perfil, GROUP_CONCAT(g.nome SEPARATOR ', ') AS grupos
            FROM usuarios u
            LEFT JOIN usuario_grupo ug ON u.id = ug.usuario_id
            LEFT JOIN grupos g ON ug.grupo_id = g.id
            GROUP BY u.id, u.usuario, u.perfil
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def obter_todos_usuarios_com_grupos_left_join(self):
        query = """
            SELECT u.usuario, g.nome, AS grupo
            FROM usuarios u
            LEFT JOIN usuario_grupo ug ON u.id = ug.usuario_id
            LEFT JOIN grupos g ON g.id = ug.grupo_id
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def obter_todos_grupos_com_usuarios_right_join(self):
        query = """
            SELECT u.usuario, g.nome AS grupo
            FROM grupos g
            RIGHT JOIN usuario_grupo ug ON g.id = ug.grupo_id
            RIGHT JOIN usuarios u ON u.id = ug.usuario_id
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def obter_todos_usuarios_e_grupos_full_join(self):
        query = """
            SELECT u.usuario, g.nome AS grupo
            FROM usuarios u
            LEFT JOIN usuario_grupo ug ON u.id = ug.usuario_id
            LEFT JOIN grupos g ON g.id = ug.grupo_id
            UNION
            SELECT u.usuario, g.nome AS grupo
            FROM grupos g
            LEFT JOIN usuario_grupo ug ON g.id = ug.grupo_id
            LEFT JOIN usuarios u ON u.id = ug.usuario_id
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def criar_tabela_testes(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS testes_sistema (
                id INT AUTO_INCREMENT PRIMARY KEY,
                data_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                funcao_testada VARCHAR(255) NOT NULL,
                tipo_teste VARCHAR(50) NOT NULL,
                caso_teste VARCHAR(255) NOT NULL,
                entrada TEXT,
                esperado TEXT,
                obtido TEXT,
                status VARCHAR(20),
                observacoes TEXT
            );
        """)
        self.conexao.commit()

    def executar(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        self.conexao.commit()

    def force(self, sql, atributos):
        self.cursor.execute(sql, atributos)
        self.conexao.commit()
    
    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.cursor.fetchall()
    
    def registrar_teste(self, funcao, tipo, caso, entrada, esperado, obtido, status, observacoes=""):
        self.cursor.execute("""
            INSERT INTO testes_sistema (funcao_testada, tipo_teste, caso_teste, entrada, esperado, obtido, status, observacoes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (funcao, tipo, caso, str(entrada), str(esperado), str(obtido), status, observacoes))
        self.conexao.commit()

    def criar_tabela_defeitos(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS defeitos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                modulo VARCHAR(100),
                descricao VARCHAR(255),
                data_ocorrencia DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conexao.commit()

    def registrar_defeito(self, modulo, descricao):
        self.cursor.execute("""
            INSERT INTO defeitos (modulo, descricao) VALUES (%s, %s)
        """, (modulo, descricao))
        self.conexao.commit()

    def verificar_integridade(self):
        tabelas_necessarias = ['usuarios', 'logins', 'grupos', 'usuario_grupo', 'testes_sistema', 'defeitos']

        self.cursor.execute("SHOW TABLES")
        existentes = [t[0] for t in self.cursor.fetchall()]
        faltando = [t for t in tabelas_necessarias if t not in existentes]

        if faltando:
            status = "Falha"
            resultado = f"Tabelas faltando: {', '.join(faltando)}"
            self.registrar_defeito("BancoMySQL", resultado)
        else:
            status = "Sucesso"
            resultado = "Todas as tabelas necessárias estão presentes."

        self.registrar_teste(
            funcao="verificar_integridade",
            tipo="Estático",
            caso="Verificação de integridade do banco de dados",
            entrada="Inicialização do sistema",
            esperado="Todas as tabelas necessárias presentes",
            obtido=resultado,
            status=status,
            observacoes="Teste automático ao iniciar o sistema"
        )

        self.cursor.execute("SLECT COUNT(*) FROM usuarios WHERE usuario = 'admin'")
        tem_admin = self.cursor.fetchone()[0] > 0

        if not tem_admin:
            self.registrar_defeito("BancoMySQL", "Usuário admin ausente")
            self.registrar_teste(
                funcao="usuario_admin",
                tipo="Estático",
                caso="Criação automática do usuário admin",
                entrada="Banco inicializado",
                esperado="Usuário admin presente",
                obtido="Usuário admin ausente",
                status="Falha",
                observacoes="Recriar o admin automaticamente"
            )
        else:
            self.registrar_teste(
                funcao="usuario_admin",
                tipo="Estático",
                caso="Verificação do usuário admin",
                entrada="Banco inicializado",
                esperado="Usuário admin presente",
                obtido="Usuário admin presente",
                status="Sucesso"
            )

    def __del__(self):
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'conexao') and self.conexao:
            self.conexao.close()