from banco.BancoMySQL import BancoMySQL

class UsuarioRepository:
    def __init__(self, banco: BancoMySQL):
        self.banco = banco

    def salvar(self, nome, email, senha, perfil, sexo, sangue, idade):
        sql = "INSERT INTO usuarios (nome, usuario, senha, perfil, sexo, sangue, idade) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        self.banco.executar(sql, (nome, email, senha, perfil, sexo, sangue, idade))
        usuario_id = self.banco.cursor.lastrowid

    def validar_login(self, email, senha):
        sql = "SELECT * FROM usuarios WHERE usuario = %s AND senha = %s"
        resultado = self.banco.query(sql, (email, senha))
        return resultado[0] if resultado else None
    
    def check_admin(self, user):
        self.banco.executar("SELECT CURRENT_USER", (user,))

    def check_perfil(self):
        self.banco.executar("SELECT * FROM 'usuarios' WHERE perfil = 'admin';")

    def excluir(self, usuario_id):
        sql = "DELETE FROM usuarios WHERE id=%s"
        return self.banco.executar(sql, (usuario_id))
        
        # try:
        #     cursor = self.banco.conexao.cursor()

        #     cursor.execute("DELETE FROM usuarios WHERE id=%s", (usuario_id,))
        #     cursor.execute("DELETE FROM usuario_grupo WHERE usuario_id=%s", (usuario_id,))

        #     return self.banco.conexao.commit()
            
        # except Exception as e:
        #     print("usuario_repository")

    def atualizar(self, usuario_id, novo_nome, nova_senha, novo_perfil, novo_sexo, novo_sangue, nova_idade): #Esta função não está sendo utilizada

        if novo_nome:
            try:
                self.update_nome(usuario_id, novo_nome)
            except Exception:
                print("Update nome")

        if nova_senha:
            try:
                self.update_senha(usuario_id, nova_senha)
            except Exception:
                print("Update senha")
                print(Exception)


    """" Aqui é onde o update acontece, como podem ver, um a um    """
    
    def update_senha(self, usuario_id, nova_senha):
        sql = "UPDATE usuarios SET senha=%s WHERE id=%s"
        self.banco.executar(sql, (nova_senha, usuario_id))

    def update_nome(self, usuario_id, nome):
        sql = "UPDATE usuarios SET nome=%s WHERE id=%s"
        self.banco.executar(sql, (nome, usuario_id))

    def update_perfil(self, usuario_id, perfil):
        sql = "UPDATE usuarios SET perfil=%s WHERE id=%s"
        self.banco.executar(sql, (perfil, usuario_id))

    def update_sexo(self, usuario_id, sexo):
        sql = "UPDATE usuarios SET sexo=%s WHERE id=%s"
        self.banco.executar(sql, (sexo, usuario_id))

    def update_sangue(self, usuario_id, sangue):
        sql = "UPDATE usuarios SET sexo=%s WHERE id=%s"
        self.banco.executar(sql, (sangue, usuario_id))

    def update_idade(self, usuario_id, idade):
        sql = "UPDATE usuarios SET idade=%s WHERE id=%s"
        self.banco.executar(sql, (idade, usuario_id))

    def listar_todos(self):
        sql = "SELECT id, nome, usuario, perfil, sexo, sangue, idade FROM usuarios"
        cursor = self.banco.conexao.cursor()
        cursor.execute(sql)
        resultados = cursor.fetchall()

        usuarios = []
        for r in resultados:
            usuarios.append({
                "id": r[0],
                "nome": r[1],
                "usuario": r[2],
                "perfil": r[3],
                "sexo": r[4],
                "sangue": r[5],
                "idade": r[6],
            })
        return usuarios

    def buscar_por_id(self, usuario_id):
        sql = "SELECT * FROM usuarios WHERE id=%s"
        resultado = self.banco.query(sql, (usuario_id,))
        return resultado[0] if resultado else None

    def buscar_por_nome(self, nome):
        sql = "SELECT * FROM usuarios WHERE nome=%s"
        resultado = self.banco.query(sql, (nome,))
        return resultado[0] if resultado else None
    
    def listar_grupos_do_usuario(self, usuario_id):
        sql = """
            SELECT g.id, g.nome
            FROM grupos g
            JOIN usuario_grupo ug ON g.id = ug.grupo_id
            WHERE ug.usuario_id = %s    
        """
        cursor = self.banco.conexao.cursor()
        cursor.execute(sql, (usuario_id,))
        resultados = cursor.fetchall()
        grupos = [{"id": r[0], "nome": r[1]} for r in resultados]
        return grupos
    
    def valida_admin(self, usuario_id):
        return