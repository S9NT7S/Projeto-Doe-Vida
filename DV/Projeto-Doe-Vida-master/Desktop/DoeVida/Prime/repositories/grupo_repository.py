from banco.BancoMySQL import BancoMySQL

class GrupoRepository:
    def __init__(self, banco: BancoMySQL):
        self.banco = banco

    def listar_todos(self):
        sql = "SELECT id, nome FROM grupos"
        cursor = self.banco.conexao.cursor()
        cursor.execute(sql)
        resultados = cursor.fetchall()

        grupos = []
        for r in resultados:
            grupos.append({
                "id": r[0],
                "nome": r[1]
            })
        return grupos