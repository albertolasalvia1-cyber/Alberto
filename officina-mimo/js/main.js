// Officina Mimo — interazioni: menu mobile, header, animazioni, contatori, form.
(function () {
  "use strict";

  var header = document.querySelector(".header");
  var burger = document.getElementById("burger");
  var nav = document.getElementById("nav");

  // Menu mobile
  function closeNav() {
    nav.classList.remove("is-open");
    burger.setAttribute("aria-expanded", "false");
  }
  burger.addEventListener("click", function () {
    var open = nav.classList.toggle("is-open");
    burger.setAttribute("aria-expanded", open ? "true" : "false");
  });
  nav.addEventListener("click", function (e) {
    if (e.target.closest("a")) closeNav();
  });

  // Ombra dell'header allo scroll
  function onScroll() {
    header.classList.toggle("is-scrolled", window.scrollY > 10);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // Contatore numerico
  function countUp(el) {
    var target = parseInt(el.getAttribute("data-count"), 10);
    var suffix = el.getAttribute("data-suffix") || "";
    var start = null;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / 1400, 1);
      el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3))) + suffix;
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  // Animazioni allo scroll
  var items = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-in");
        var counter = entry.target.querySelector("[data-count]");
        if (counter) countUp(counter);
        io.unobserve(entry.target);
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    items.forEach(function (el, i) {
      el.style.transitionDelay = (i % 4) * 70 + "ms";
      io.observe(el);
    });
  } else {
    items.forEach(function (el) { el.classList.add("is-in"); });
  }

  // Form: compone una mail con i dati inseriti
  var form = document.getElementById("form");
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var ok = true;
    form.querySelectorAll("[required]").forEach(function (f) {
      var bad = !f.value.trim();
      f.classList.toggle("is-invalid", bad);
      if (bad) ok = false;
    });
    if (!ok) return;
    var d = new FormData(form);
    var subject = "Richiesta " + d.get("servizio") + " - " + d.get("nome");
    var body = [
      "Nome / Azienda: " + d.get("nome"),
      "Telefono: " + d.get("tel"),
      "Targa: " + (d.get("targa") || "-").toUpperCase(),
      "Servizio: " + d.get("servizio"),
      "",
      d.get("msg") || ""
    ].join("\n");
    window.location.href = "mailto:info@officinamimo.com?subject=" +
      encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
  });

  document.getElementById("year").textContent = new Date().getFullYear();
})();
