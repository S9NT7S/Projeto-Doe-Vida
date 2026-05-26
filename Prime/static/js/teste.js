var modal = document.getElementById("meuModal");

var botao = document.getElementById("abrirModal");

var span = document.getElementByClassName("close1")[0];

botao.onclick = function() {
    modal.style.display = "block";
}

span.onclick = function() {
    modal.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}