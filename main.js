// =============================================
// COUNT-UP UTILITY
// =============================================
function easeOutCubic(t) {
  return 1 - Math.pow(1 - t, 3);
}

function countUp(el, target, decimals, suffix, duration) {
  const start = performance.now();
  function step(now) {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    const eased = easeOutCubic(progress);
    const value = eased * target;
    el.textContent = value.toFixed(decimals) + suffix;
    if (progress < 1) {
      requestAnimationFrame(step);
    }
  }
  requestAnimationFrame(step);
}

// =============================================
// STATS COUNT-UP — IntersectionObserver
// =============================================
const statData = [
  { target: 120, suffix: "ms", decimals: 0, duration: 1500, delay: 480 },
  { target: 99.99, suffix: "%", decimals: 2, duration: 1580, delay: 570 },
  { target: 24, suffix: "/7", decimals: 0, duration: 1660, delay: 660 },
  { target: 2.4, suffix: "M", decimals: 1, duration: 1740, delay: 750 },
];

const statValues = document.querySelectorAll(".stat-value[data-target]");
let statsTriggered = false;

const statsObserver = new IntersectionObserver(
  (entries) => {
    if (entries[0].isIntersecting && !statsTriggered) {
      statsTriggered = true;
      statValues.forEach((el, i) => {
        const d = statData[i];
        setTimeout(() => {
          countUp(el, d.target, d.decimals, d.suffix, d.duration);
        }, d.delay);
      });
      statsObserver.disconnect();
    }
  },
  { threshold: 0.25 }
);

const statsSection = document.querySelector(".stats");
if (statsSection) {
  statsObserver.observe(statsSection);
}

// =============================================
// MOBILE MENU
// =============================================
const burgerBtn = document.getElementById("burger-btn");
const menuOverlay = document.getElementById("menu-overlay");
const mobileMenu = document.getElementById("mobile-menu");
const mobileLinks = document.querySelectorAll(".mobile-nav-links a, .mobile-signin-btn");

function openMenu() {
  burgerBtn.setAttribute("aria-expanded", "true");
  menuOverlay.removeAttribute("hidden");
  mobileMenu.removeAttribute("hidden");
  document.body.classList.add("menu-open");
}

function closeMenu() {
  burgerBtn.setAttribute("aria-expanded", "false");
  menuOverlay.setAttribute("hidden", "");
  mobileMenu.setAttribute("hidden", "");
  document.body.classList.remove("menu-open");
}

function toggleMenu() {
  const isOpen = burgerBtn.getAttribute("aria-expanded") === "true";
  if (isOpen) {
    closeMenu();
  } else {
    openMenu();
  }
}

if (burgerBtn) {
  burgerBtn.addEventListener("click", toggleMenu);
}

if (menuOverlay) {
  menuOverlay.addEventListener("click", closeMenu);
}

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    closeMenu();
  }
});

mobileLinks.forEach((link) => {
  link.addEventListener("click", closeMenu);
});

window.addEventListener("resize", () => {
  if (window.innerWidth > 720) {
    closeMenu();
  }
});
