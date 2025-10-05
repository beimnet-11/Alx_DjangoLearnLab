document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.querySelector(".toggle_btn");
    const sideNav = document.querySelector(".side-nav");
    const closeBtn = document.querySelector(".close_btn");

    toggleBtn.addEventListener("click", () => {
        sideNav.classList.add("active");
    });

    closeBtn.addEventListener("click", () => {
        sideNav.classList.remove("active");
    });
});
