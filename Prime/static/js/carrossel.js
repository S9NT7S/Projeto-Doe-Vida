const track = document.querySelector(".carousel-track");
const slides = document.querySelectorAll(".slide");
const prevBtn = document.querySelector(".prev");
const nextBtn = document.querySelector(".next");
const dotsContainer = document.querySelector(".dots");

let index = 0;

slides.forEach((_, i) => {
    const dot = document.createElement("div");
    dot.classList.add("dot");
    if (i === 0) dot.classList.add("active");

    dot.addEventListener("click", () => goToSlide(i));
    dotsContainer.appendChild(dot);
});

const dots = document.querySelectorAll(".dot");

function updateCarousel() {
    track.style.transform = `translateX(-${index * 100}%)`;

    dots.forEach(d => d.classList.remove("active"));
    dots[index].classList.add("active");
}

function goToSlide(i) {
    index = i;
    updateCarousel();
}

function next() {
    index = (index + 1) % slides.length;
    updateCarousel();
}

function prev() {
    index = (index - 1 + slides.length) % slides.length;
    updateCarousel();
}

nextBtn.addEventListener("click", next);
prevBtn.addEventListener("click", prev);

setInterval(next, 10000);