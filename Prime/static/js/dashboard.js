class Dashboard {
    constructor() {
        this.graficoUsuarios = document.querySelector("#graficoUsuarios");
        this.graficoDefeitos = document.querySelector("#graficoDefeitos");
        this.graficoGrupos = document.querySelector("#graficoGrupos");

        this.graficoEvolucao = document.querySelector("#graficoEvolucao");
        this.graficoRanking = document.querySelector("#graficoRanking");
        this.graficoArea = document.querySelector("#graficoArea");

        this.dados = null;

        this.inicializar();
    }

    inicializar() {
        this.carregarDados();
    }

    async carregarDados() {
        const res = await fetch("/api/dashboard");
        this.dados = await res.json();

        console.log("Dados API:", this.dados);

        this.renderizarGraficos();
    }

    renderizarGraficos() {
        new Chart(this.graficoUsuarios, {
            type: "bar",
            data: {
                labels: ["Admins", "Usuários"],
                datasets: [{
                    label: "Usuários",
                    data: [
                        this.dados.admins,
                        this.dados.dPrimeira,
                        this.dados.regulares,
                        this.dados.esporadicos,
                        this.dados.voluntarios,
                        this.dados.direcionados,
                        this.dados.total
                    ],
                    backgroundColor: ["#ff6384, #36a2eb"]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });

        const defeitos = this.dados.defeitos_por_modulo || [];

        new Chart(this.graficoDefeitos, {
            type: "doughnut",
            data: {
                labels: defeitos.map(d => d.modulo),
                datasets: [{
                    label: "Defeitos",
                    data: defeitos.map(d => d.total),
                    backgroundColor: [
                        "#ffcd56",
                        "#4bc0c0",
                        "#9966ff",
                        "#ff9f40"
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });

        const grupos = this.dados.usuarios_por_grupo || [];

        new Chart(this.graficoGrupos, {
            type: "pie",
            data: {
                labels: grupos.map(g => g.grupo),
                datasets: [{
                    data: grupos.map(g => g.total),
                    backgroundColor: [
                        "#36a2eb",
                        "#ff6384",
                        "#ffcd56",
                        "#4bc0c0",
                        "#9966ff",
                        "#ff9f40"
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });

        new Chart(this.graficoEvolucao, {
            type: "line",
            data: {
                labels: ["Jan", "Fev", "Mar"],
                datasets: [{
                    label: "Cadastros no sistema",
                    data: [5, 12, 20],
                    borderColor: "#4bc0c0",
                    backgroundColor: "rgba(54, 162, 235, 0.2)",
                    fill: true,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });

        new Chart(this.graficoRanking, {
            type: "bar",
            data: {
                labels: ["Login", "Cadastro", "Relatórios", "Erros"],
                datasets: [{
                    label: "Uso do sistema",
                    data: [80, 60, 40, 20], 
                    backgroundColor: "#4bc0c0"
                }]
            },
            options: {
                indexAxis: "y",
                responsive: true,
                maintainAspectRatio: false
            }
        });

        new Chart(this.graficoArea, {
            type: "line",
            data: {
                labels: ["Seg", "Ter", "Qua", "Qui", "Sex"],
                datasets: [{
                    label: "Acessos",
                    data: [10, 25, 30, 45, 60],
                    borderColor:rgb(255, 0, 55),
                    backgroundColor: rgba(255, 0, 55, 0.2),
                    fill: true,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }
}

document.addEventListener("DOMContentLoaded", () => {
    new Dashboard();
});