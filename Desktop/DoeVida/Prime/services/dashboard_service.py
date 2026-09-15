class DashboardService:
    def __init__(self, usuario_repo, dashboard_repo):
        self.dashboard_repo = dashboard_repo
        self.usuario_repo = usuario_repo

    def obter_dados(self):
        usuarios = self.usuario_repo.listar_todos()
        total = len(usuarios)

        admins = len([u for u in usuarios if u["perfil"] == "admin"])

        doadores = total - admins

        perfis = {}
        for usuario in usuarios:
            perfil = usuario["perfil"]
            perfis[perfil] = perfis.get(perfil, 0) + 1
        
        return {
            "admins": admins,
            "doadores": doadores,
            "total_de_usuarios": total,
            "usuarios_por_perfil": [
                {"perfil": perfil, "total": quantidade}
                for perfil, quantidade in perfis.items()
            ]
        }
    
    # "dPrimeira": dPrimeira,
    #         "regulares": regulares,
    #         "esporadicos": esporadicos,
    #         "voluntarios": voluntarios,
    #         "direcionados": direcionados,