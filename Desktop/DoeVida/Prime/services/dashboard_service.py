class DashboardService:
    def __init__(self, usuario_repo, dashboard_repo):
        self.dashboard_repo = dashboard_repo
        self.usuario_repo = usuario_repo

    def obter_dados(self):
        usuarios = self.usuario_repo.listar_todos()
        total = len(usuarios)

        admins = len([u for u in usuarios if u["perfil"] == "admin"])

        doadores = total - admins
        
        # dPrimeira = len([u for u in usuarios if u["perfil"] == "primeira"])

        # regulares = len([u for u in usuarios if u["perfil"] == "regular"])

        # esporadicos = len([u for u in usuarios if u["perfil"] == "esporadico"])

        # voluntarios = len([u for u in usuarios if u["perfil"] == "voluntario"])

        # direcionados = len([u for u in usuarios if u["perfil"] == "direcionado"])

        return {
            "admins": admins,
            "doadores": doadores,
            "total_de_usuarios": total
        }
    
    # "dPrimeira": dPrimeira,
    #         "regulares": regulares,
    #         "esporadicos": esporadicos,
    #         "voluntarios": voluntarios,
    #         "direcionados": direcionados,