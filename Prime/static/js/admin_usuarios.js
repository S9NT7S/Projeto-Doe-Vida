function abrirModal() {
    document.getElementById("modalErro").style.display = "block";
}

function fecharModal() {
    document.getElementById("modalErro").style.display = "none";
}

window.onclick = function(event) {
    let modal = document.getElementById("modalErro");
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

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
        document.getElementById("formExcluir" + usuarioParaExcluir).onsubmit();
    }
}