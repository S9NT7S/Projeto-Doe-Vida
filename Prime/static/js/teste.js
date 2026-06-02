// var modal = document.getElementById("meuModal");

// var botao = document.getElementById("abrirModal");

// var span = document.getElementByClassName("close1")[0];

// botao.onclick = function() {
//     modal.style.display = "block";
// }

// span.onclick = function() {
//     modal.style.display = "none";
// }

// modal.onclick = function(event) {
//     if (event.target == modal) {
//         modal.style.display = "none";
//     }
// }

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
    document.getElementById("modalConfirmacao").style.display = "block";
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