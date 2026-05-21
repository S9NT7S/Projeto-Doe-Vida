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

    def check_perfil(self, user_perfil):
        self.banco.executar("SELECT * FROM 'usuarios' WHERE perfil = 'admin';")

    def excluir(self, usuario_id):
        try:
            cursor = self.banco.conexao.cursor()

            cursor.execute("DELETE FROM usuarios WHERE id=%s", (usuario_id,))
            cursor.execute("DELETE FROM usuario_grupo WHERE usuario_id=%s", (usuario_id,))

            self.banco.conexao.commit()
            
        except Exception as e:
            print("usuario_repository")

    def update_nome(self, usuario_id, novo_nome):
        sql = "UPDATE usuarios SET nome=%s"

        params = [novo_nome]

        try:
            sql += " WHERE usuarios.id=%s"
            params.append(usuario_id,)
            self.banco.executar(sql, tuple(params))
        
        except Exception as error:
            print(error)

    def atualizar(self, usuario_id, novo_nome, nova_senha, novo_perfil, novo_sexo, novo_sangue, nova_idade):
        
        sql = "UPDATE usuarios SET nome=%s"

        # UPDATE `usuarios` SET `sexo` = 'outro' WHERE `usuarios`.`id` = 3;

        # UPDATE `usuarios` SET `nome` = 'Nikita1', `sexo` = 'masculino', `idade` = '55' WHERE `usuarios`.`id` = 3;

        params = [novo_nome, nova_senha, novo_perfil, novo_sexo, novo_sangue, nova_idade]

        if nova_senha:
            sql += ", 'senha' = %s"
            params.append(nova_senha)

        if novo_perfil:
            sql += ", 'perfil' = %s"
            params.append(novo_perfil)

        if novo_sexo:
            sql += ", 'sexo' = %s"
            params.append(novo_sexo)

        if novo_sangue:
            sql += ", 'sangue' = %s"
            params.append(novo_sangue)

        if nova_idade:
            sql += ", 'idade' = %s"
            params.append(nova_idade)

        try:
            #FIX, TALVEZ TENHA QUE REVER PQ ESSA VIRGULA VAI DAR PROBLEMA 100%
            #NÃO SALVA DE JEITO NENHUM NO BANCO, CREIO QUE ESSA STREAM DE NOVOS DADOS NÃO IRÃO FUNCIONAR
            #LOGO, FAZER ATUALIZAR UM A UM NA TELA DE EDITAR USUARIOS

            sql += " WHERE usuarios.id = %s"
            params.append(usuario_id,)
            self.banco.executar(sql, tuple(params))

        except Exception as e:
            print("usuario_repository")
            print(e)

    def update_senha(self, usuario_id, nova_senha):
        sql = "UPDATE usuarios SET senha=%s WHERE id=%s"
        self.banco.executar(sql)

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