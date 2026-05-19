const filtroInput = document.getElementById("filtroUsuarios");

if (filtroInput) {
    filtroInput.addEventListener("keyup", function () {
        const valor = filtroInput.ariaValueMax.toLowerCase();

        const linhas = document.querySelectorAll("#tableUsuarios tr");

        linhas.forEach((linha) => {
            const textoLinha = linha.innerText.toLowerCase();

            if (textoLinha.includes(valor)) {
                linha.style.display = "";
            } else {
                linha.style.display = "none";
            }
        });
    });
}

function limparFiltro() {
    filtroInput.value = "";

    const linhas = document.querySelectorAll("#tabelaUsuarios tr");

    linhas.forEach((linha) => {
        linha.style.display = "";
    });
}

function abrirModal() {
    document.getElementById("modalErro").style.display = "block";
}

function fecharModal() {
    document.getElementById("modalErro").style.display = "none";
}

window.onclick = function(event) {
    let modal = document.getElementById("modalErro");
    if (event.target === modal) {
        modal.style.display = "none";
    }
}

let usuarioParaExcluir = null;

function abrirConfirmacao(id) {
    usuarioParaExcluir = id;
    document.getElementById("modalConfirmacao").style.display = "block";
}

function fecharModalConfirmacao() {
    usuarioParaExcluir = null;
    document.getElementById("modalConfirmacao").style.display = "none";
}

function confirmarExclusao() {
    if (usuarioParaExcluir !== null) {
        document.getElementById("formExcluir" + usuarioParaExcluir).submit();
    }
}