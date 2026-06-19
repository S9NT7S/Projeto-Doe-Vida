class IntegridadeBanco:
    def __init__(self, cursor):
        self.cursor = cursor

    def executar_validacoes(self):
        self.verificar_tabelas_basicas()

    def verificar_tabelas_basicas(self):
        self.cursor.execute("SHOW TABLES")
        dados = self.cursor.fetchall()

        existentes = []

        for t in dados:
            if isinstance(t, dict):
                existentes.append(list(t.values())[0])
            else:
                existentes.append(t[0])

        tabelas_obrigatorias = [
            "usuarios",
            "grupos",
            "usuario_grupo",
            "logins"
        ]

        faltando = []

        for tabela in tabelas_obrigatorias:
            if tabela not in existentes:
                faltando.append(tabela)

        if faltando:
            raise Exception(f"Tabelas obrigatórias não encontradas: {faltando}")