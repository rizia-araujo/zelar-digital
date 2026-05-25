document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector("[data-menu-toggle]");
  const nav = document.querySelector("[data-nav]");
  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      nav.classList.toggle("is-open");
      document.body.classList.toggle("menu-open");
      if (window.innerWidth <= 760) {
        nav.style.display = nav.style.display === "flex" ? "none" : "flex";
        nav.style.flexDirection = "column";
        nav.style.alignItems = "stretch";
      }
    });
  }
});
