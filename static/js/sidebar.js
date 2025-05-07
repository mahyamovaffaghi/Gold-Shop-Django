// sidebar js
function toggleMenu() {
    document.getElementById("sidebar").classList.toggle("open");
}

// Close sidebar when clicking outside
document.addEventListener("click", function (event) {
    let sidebar = document.getElementById("sidebar");
    let menuToggle = document.querySelector(".menu-toggle");

    // Check if the click is outside the sidebar and not on the menu toggle button
    if (!sidebar.contains(event.target) && !menuToggle.contains(event.target)) {
        sidebar.classList.remove("open");
    }
});