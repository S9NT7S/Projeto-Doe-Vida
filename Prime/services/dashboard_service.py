class DashboardService:
    def __init__(self, usuario_repo):
        self.usuario_repo = usuario_repo

    def obter_dados(self):
        usuarios = self.usuario_repo.listar_todos()
        total = len(usuarios)

        admins = len([u for u in usuarios if u["perfil"] == "admin"])
        
        dPrimeira = len([u for u in usuarios if u["perfil"] == "primeira"])

        regulares = len([u for u in usuarios if u["perfil"] == "regular"])

        esporadicos = len([u for u in usuarios if u["perfil"] == "esporadico"])

        voluntarios = len([u for u in usuarios if u["perfil"] == "voluntario"])

        direcionados = len([u for u in usuarios if u["perfil"] == "direcionado"])

        return {
            "Administradores": admins,
            "Doadores de primeira vez": dPrimeira,
            "Doadores regulares": regulares,
            "Doadores esporadicos": esporadicos,
            "Doadores voluntarios": voluntarios,
            "Doadores direcionados": direcionados,
            "Total de usuarios": total
        }