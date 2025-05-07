// quantity box
document.addEventListener("DOMContentLoaded", function () {
    const decreaseBtn = document.querySelector(".btn-decrease");
    const increaseBtn = document.querySelector(".btn-increase");
    const quantityInput = document.querySelector(".input-quantity");

    // Set default quantity to 1 if input is empty or invalid
    if (!quantityInput.value || isNaN(quantityInput.value) || quantityInput.value < 1) {
        quantityInput.value = 1;
    }

    increaseBtn.addEventListener("click", () => {
        let currentValue = parseInt(quantityInput.value);
        quantityInput.value = currentValue + 1;
    });

    decreaseBtn.addEventListener("click", () => {
        let currentValue = parseInt(quantityInput.value);
        if (currentValue > 1) {
            quantityInput.value = currentValue - 1;
        }
    });
});


// carousel box
document.addEventListener("DOMContentLoaded", function () {
    const mainImage = document.querySelector(".main-image img");
    const mainLink = document.querySelector(".main-image a");
    const thumbnails = document.querySelectorAll(".thumbnail-container a");

    thumbnails.forEach(thumbnail => {
        thumbnail.addEventListener("click", function (e) {
            e.preventDefault();

            // Get current thumbnail img and href
            const thumbImg = this.querySelector("img");
            const thumbSrc = thumbImg.getAttribute("src");
            const thumbHref = this.getAttribute("href");

            // Get current main image src and href
            const currentMainSrc = mainImage.getAttribute("src");
            const currentMainHref = mainLink.getAttribute("href");

            // Swap thumbnail with main image
            mainImage.setAttribute("src", thumbSrc);
            mainLink.setAttribute("href", thumbHref);

            thumbImg.setAttribute("src", currentMainSrc);
            this.setAttribute("href", currentMainHref);
        });
    });
});



// similar products js code
function openModal(id) {
    const modal = document.getElementById('modalSimilar-' + id);
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
    index = (index + 1) % Math.ceil(totalCards / cardsPerSlide);
    track.style.transform = `translateX(-${index * (100 / cardsPerSlide)}%)`;
}

setInterval(autoSlide, 3000); // Change cards every second


// comment


// فقط روی دکمه کلیک رو گوش می‌کنیم
document.querySelector('.comment-btn').addEventListener('click', function (e) {
    e.preventDefault();

    const container = this.closest('.btn-add-comment');
    const form = container.querySelector('.comment-form');
    const spanText = this.querySelector('span');
    const icon = this.querySelector('i');

    container.classList.toggle('active');
    form.classList.toggle('d-none');
    form.classList.toggle('d-flex');
    spanText.classList.toggle('d-none');

    icon.classList.toggle('bi-plus-lg');
    icon.classList.toggle('bi-x-lg');
});

// این قسمت جدید اضافه میشه:
document.querySelector('.comment-form').addEventListener('click', function (e) {
    // جلو انتشار رویداد رو می‌گیره تا toggle دوباره فعال نشه
    e.stopPropagation();
});




 document.querySelectorAll('.reply-btn').forEach(btn => {
    btn.addEventListener('click', function (e) {
        e.preventDefault();

        const commentId = this.id.split('-')[2];

        const replyForm = document.getElementById(`reply-form-${commentId}`);
        const repliesContainer = document.getElementById(`show-replies-${commentId}`);
        const replyItems = repliesContainer.querySelectorAll('.reply-item');
        const loadMoreBtn = document.getElementById(`load-more-${commentId}`);

        if (replyForm && repliesContainer) {
            replyForm.classList.toggle('d-none');
            replyForm.classList.toggle('d-flex');

            repliesContainer.classList.toggle('d-none');
            repliesContainer.classList.toggle('d-flex');
        }

        // وقتی برای اولین بار باز میشه، فقط یکی نشون بده
        if (repliesContainer.classList.contains('d-flex')) {
            let visibleCount = 0;
            replyItems.forEach((item, index) => {
                if (index === 0) {
                    item.classList.remove('d-none');
                    visibleCount++;
                } else {
                    item.classList.add('d-none');
                }
            });

            // اگر بیشتر از ۱ ریپلای داریم، دکمه "نمایش بیشتر" رو نشون بده
            if (replyItems.length > 1) {
                loadMoreBtn.classList.remove('d-none');
                loadMoreBtn.dataset.visible = visibleCount; // ذخیره چندتا نمایش داده شده
            } else {
                loadMoreBtn.classList.add('d-none');
            }
        }
    });
});

// comment reply
// هندل کردن کلیک روی دکمه "نمایش بیشتر"
document.querySelectorAll('.load-more-replies').forEach(btn => {
    btn.addEventListener('click', function (e) {
        e.preventDefault();

        const commentId = this.id.split('-')[2];
        const repliesContainer = document.getElementById(`show-replies-${commentId}`);
        const replyItems = repliesContainer.querySelectorAll('.reply-item');
        let visibleCount = parseInt(this.dataset.visible) || 1;

        // نمایش ۳ تا دیگه
        for (let i = visibleCount; i < visibleCount + 3 && i < replyItems.length; i++) {
            replyItems[i].classList.remove('d-none');
        }

        // آپدیت تعداد
        this.dataset.visible = visibleCount + 3;

        // اگه همه ریپلای ها باز شده بودن، دکمه رو مخفی کن
        if (visibleCount + 3 >= replyItems.length) {
            this.classList.add('d-none');
        }
    });
});
