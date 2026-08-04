/* 
A+ 65%
A- 20%
B+ 48%
B- 8%
O+ 72%
O- 14%
AB+ 83%
AB- 31%
*/

const tipoSangue = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"];
const litros = [65, 20, 48, 8, 72, 14, 83, 31];
const barColors = ["red", "red", "red", "red", "red", "red", "red", "red"];

new Chart("Sangue", {
    type: "bar",
    data: {
        labels: tipoSangue,
        datasets: [{
            backgroundColor: barColors,
            data: litros
        }]
    },
    options: {
        plugins: {
            legend: {display: false},
            title: {
                display: true,
                text: "Estoques de Sangue",
                font: {size: 16}
            }
        }
    }
});