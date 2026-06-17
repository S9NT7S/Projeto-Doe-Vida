function abrirModal() {
    document.getElementById("modalErro").style.display = "block";
}

function fecharModal() {
    document.getElementById("modalErro").style.display = "none";
}

window.onclick = function(event) {
    let modal = document.getElementById("modalErro");
    if (event.target === modal) {
        modal.style.display = "block";
    }
}

let usuarioParaExcluir = null;

function abrirConfirmacao(id) {
    usuarioParaExcluir = id;
    document.getElementById("modalConfirmacao").style.display = "none";
}

function fecharModalConfirmacao() {
    usuarioParaExcluir = null;
    document.getElementById("modalConfirmacao").style.display = "none";
}

function confirmarExclusao() {
    if (usuarioParaExcluir !== null) {
        document.getElementById("formExcluir-" + usuarioParaExcluir).submit();
    }
}