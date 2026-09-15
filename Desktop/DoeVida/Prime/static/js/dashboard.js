class Dashboard {
    constructor() {
        this.status = document.querySelector("#dashboardStatus");
        this.inicializar();
    }

    async inicializar() {
        try {
            const response = await fetch("/api/dashboard");

            if (!response.ok) {
                throw new Error("Nao foi possivel carregar os dados.");
            }

            const dados = await response.json();
            this.atualizarResumo(dados);
            this.renderizarGraficos(dados);
            this.status.textContent = "Dados atualizados";
            this.status.classList.add("status-ok");
        } catch (erro) {
            this.status.textContent = "Nao foi possivel carregar o dashboard.";
            this.status.classList.add("status-erro");
            console.error(erro);
        }
    }

    atualizarResumo(dados) {
        document.querySelector("#totalUsuarios").textContent = dados.total_de_usuarios ?? 0;
        document.querySelector("#totalAdmins").textContent = dados.admins ?? 0;
        document.querySelector("#totalDoadores").textContent = dados.doadores ?? 0;
    }

    renderizarGraficos(dados) {
        this.criarGraficoUsuarios(dados);

        const perfis = dados.usuarios_por_perfil || [];
        if (perfis.length === 0) {
            this.status.textContent = "Nenhum usuario cadastrado ainda.";
            return;
        }

        new Chart(document.querySelector("#graficoPerfis"), {
            type: "bar",
            data: {
                labels: perfis.map((item) => item.perfil),
                datasets: [{
                    label: "Usuarios",
                    data: perfis.map((item) => item.total),
                    backgroundColor: "#d32f2f",
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: { beginAtZero: true, ticks: { precision: 0 } }
                }
            }
        });
    }

    criarGraficoUsuarios(dados) {
        new Chart(document.querySelector("#graficoUsuarios"), {
            type: "doughnut",
            data: {
                labels: ["Administradores", "Doadores"],
                datasets: [{
                    data: [dados.admins ?? 0, dados.doadores ?? 0],
                    backgroundColor: ["#7f1d1d", "#ef4444"]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: "bottom" }
                }
            }
        });
    }
}

document.addEventListener("DOMContentLoaded", () => {
    new Dashboard();
});
