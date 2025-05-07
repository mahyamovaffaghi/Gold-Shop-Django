const dropdownToggle = document.querySelector('.dropdown-toggle');
const dropdownMenu = document.querySelector('.dropdown-menu');
const mainContent = document.getElementById('mainContent');

dropdownToggle.addEventListener('click', () => {
    setTimeout(() => {
        if (dropdownMenu.classList.contains('show')) {
            mainContent.classList.add('blur-bg');
        } else {
            mainContent.classList.remove('blur-bg');
        }
    }, 10); // slight delay to wait for class to toggle
});

// Close blur on outside click
document.addEventListener('click', function (e) {
    if (!dropdownToggle.contains(e.target) && !dropdownMenu.contains(e.target)) {
        mainContent.classList.remove('blur-bg');
    }
});


// for mobile size responsive

document.addEventListener('DOMContentLoaded', function () {
    const isMobile = window.innerWidth <= 767.98;

    if (isMobile) {
        // Prevent Bootstrap dropdown from closing when clicking inside
        document.querySelectorAll('.dropdown-submenu > a').forEach(function (el) {
            el.addEventListener('click', function (e) {
                e.preventDefault();
                e.stopPropagation(); // ✅ Prevent Bootstrap from closing the dropdown
                const parent = this.parentElement;
                parent.classList.toggle('open');
            });
        });

        // Reset all submenus on dropdown hide
        const mainDropdown = document.getElementById('mainDropdown');
        const dropdownParent = mainDropdown.closest('.dropdown');

        dropdownParent.addEventListener('hide.bs.dropdown', function () {
            document.querySelectorAll('.dropdown-submenu.open').forEach(function (submenu) {
                submenu.classList.remove('open');
            });
        });
    }
});
