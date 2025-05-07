
function openModal(id) {
    const modal = document.getElementById('modal-' + id);
    if (modal) {
        modal.style.display = 'flex';
    }
}

function closeModal(event) {
    const modal = event.target.closest('.modal');
    if (modal && (event.target.classList.contains('modal') || event.target.classList.contains('close'))) {
        modal.style.display = 'none';
    }
}


let index = 0;

function autoSlide() {
    const track = document.querySelector('.carousel-track');
    const totalCards = document.querySelectorAll('.card-popular').length;
    const isMobile = window.innerWidth < 768;
    const cardsPerSlide = isMobile ? 1 : 3;
    index = (index + 1) % (totalCards / cardsPerSlide);
    track.style.transform = `translateX(-${index * (100 / cardsPerSlide)}%)`;
}

setInterval(autoSlide, 3000); // Change cards every second