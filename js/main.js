(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- preloader ---------- */
  window.addEventListener("load", function () {
    var pl = document.getElementById("preloader");
    if (pl) setTimeout(function () { pl.classList.add("done"); }, 350);
  });

  /* ---------- header scroll state ---------- */
  var header = document.getElementById("siteHeader");
  var backToTop = document.getElementById("backToTop");
  function onScroll() {
    var y = window.scrollY || window.pageYOffset;
    if (header) header.classList.toggle("scrolled", y > 40);
    if (backToTop) backToTop.hidden = y < 500;
  }
  document.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
  if (backToTop) {
    backToTop.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: reduceMotion ? "auto" : "smooth" });
    });
  }

  /* ---------- mobile nav ---------- */
  var hamburger = document.getElementById("hamburger");
  var mainNav = document.getElementById("mainNav");
  if (hamburger && mainNav) {
    hamburger.addEventListener("click", function () {
      var open = mainNav.classList.toggle("open");
      hamburger.setAttribute("aria-expanded", open ? "true" : "false");
    });
    mainNav.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        mainNav.classList.remove("open");
        hamburger.setAttribute("aria-expanded", "false");
      });
    });
  }

  /* ---------- active nav link on scroll ---------- */
  var navLinks = document.querySelectorAll(".nav-link");
  var sections = Array.prototype.slice.call(document.querySelectorAll("section[id]"));
  if (sections.length && navLinks.length) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var id = entry.target.id;
        navLinks.forEach(function (l) {
          l.classList.toggle("active", l.getAttribute("href") === "#" + id);
        });
      });
    }, { rootMargin: "-40% 0px -55% 0px" });
    sections.forEach(function (s) { spy.observe(s); });
  }

  /* ---------- scroll reveal ---------- */
  var revealEls = document.querySelectorAll("[data-reveal]");
  if (revealEls.length) {
    if (reduceMotion) {
      revealEls.forEach(function (el) { el.classList.add("in"); });
    } else {
      var revealObs = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("in");
            revealObs.unobserve(entry.target);
          }
        });
      }, { threshold: 0.15 });
      revealEls.forEach(function (el) { revealObs.observe(el); });
    }
  }

  /* ---------- animated counters ---------- */
  var counters = document.querySelectorAll(".num[data-count]");
  function animateCount(el) {
    var target = parseFloat(el.getAttribute("data-count"));
    var isDecimal = String(target).indexOf(".") !== -1;
    var start = 0;
    var duration = 1400;
    var t0 = null;
    function step(ts) {
      if (!t0) t0 = ts;
      var p = Math.min((ts - t0) / duration, 1);
      var val = start + (target - start) * (1 - Math.pow(1 - p, 3));
      el.textContent = isDecimal ? val.toFixed(1) : Math.round(val);
      if (p < 1) requestAnimationFrame(step);
      else el.textContent = isDecimal ? target.toFixed(1) : target;
    }
    if (reduceMotion) { el.textContent = isDecimal ? target.toFixed(1) : target; return; }
    requestAnimationFrame(step);
  }
  if (counters.length) {
    var countObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          animateCount(entry.target);
          countObs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });
    counters.forEach(function (c) { countObs.observe(c); });
  }

  /* ---------- 3D tilt cards ---------- */
  if (!reduceMotion && window.matchMedia("(hover: hover)").matches) {
    document.querySelectorAll("[data-tilt]").forEach(function (card) {
      var rect;
      card.addEventListener("mouseenter", function () { rect = card.getBoundingClientRect(); });
      card.addEventListener("mousemove", function (e) {
        if (!rect) rect = card.getBoundingClientRect();
        var x = (e.clientX - rect.left) / rect.width - 0.5;
        var y = (e.clientY - rect.top) / rect.height - 0.5;
        card.style.transform = "rotateY(" + (x * 10) + "deg) rotateX(" + (-y * 10) + "deg) translateY(-4px)";
      });
      card.addEventListener("mouseleave", function () {
        card.style.transform = "rotateY(0) rotateX(0) translateY(0)";
      });
    });
  }

  /* ---------- hero particles ---------- */
  var particleHost = document.getElementById("heroParticles");
  if (particleHost && !reduceMotion) {
    var n = window.innerWidth < 700 ? 14 : 26;
    for (var i = 0; i < n; i++) {
      var s = document.createElement("span");
      s.style.left = Math.random() * 100 + "%";
      s.style.bottom = "-10px";
      s.style.animationDuration = (10 + Math.random() * 14) + "s";
      s.style.animationDelay = (Math.random() * 14) + "s";
      s.style.opacity = String(0.3 + Math.random() * 0.5);
      particleHost.appendChild(s);
    }
  }

  /* ---------- tabs (servizi) ---------- */
  var tabBtns = document.querySelectorAll(".tab-btn");
  var panels = document.querySelectorAll(".tab-panel");
  tabBtns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var name = btn.getAttribute("data-tab");
      tabBtns.forEach(function (b) {
        b.classList.toggle("active", b === btn);
        b.setAttribute("aria-selected", b === btn ? "true" : "false");
      });
      panels.forEach(function (p) {
        p.classList.toggle("active", p.getAttribute("data-panel") === name);
      });
    });
  });

  /* ---------- fidelity flip card ---------- */
  var flipCard = document.getElementById("flipCard");
  if (flipCard) {
    flipCard.addEventListener("click", function () { flipCard.classList.toggle("flipped"); });
    flipCard.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        flipCard.classList.toggle("flipped");
      }
    });
  }

  /* ---------- gallery filter ---------- */
  var filterBtns = document.querySelectorAll(".filter-btn");
  var galleryItems = document.querySelectorAll(".g-item");
  filterBtns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var f = btn.getAttribute("data-filter");
      filterBtns.forEach(function (b) { b.classList.toggle("active", b === btn); });
      galleryItems.forEach(function (item) {
        var match = f === "all" || item.getAttribute("data-cat") === f;
        item.classList.toggle("hide", !match);
      });
    });
  });

  /* ---------- testimonial carousel ---------- */
  var track = document.getElementById("carouselTrack");
  if (track) {
    var cards = Array.prototype.slice.call(track.querySelectorAll(".review-card"));
    var dotsHost = document.getElementById("carDots");
    var idx = 0;
    var timer;

    cards.forEach(function (_, i) {
      var d = document.createElement("span");
      d.addEventListener("click", function () { show(i); });
      dotsHost.appendChild(d);
    });
    var dots = Array.prototype.slice.call(dotsHost.children);

    function show(i) {
      idx = (i + cards.length) % cards.length;
      cards.forEach(function (c, ci) { c.classList.toggle("active", ci === idx); });
      dots.forEach(function (d, di) { d.classList.toggle("active", di === idx); });
    }
    function next() { show(idx + 1); }
    function prev() { show(idx - 1); }

    document.getElementById("carNext").addEventListener("click", function () { next(); restart(); });
    document.getElementById("carPrev").addEventListener("click", function () { prev(); restart(); });

    function restart() {
      clearInterval(timer);
      if (!reduceMotion) timer = setInterval(next, 6000);
    }
    show(0);
    restart();
  }

  /* ---------- contact form (mailto compose) ---------- */
  var form = document.getElementById("contactForm");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var data = new FormData(form);
      var nome = (data.get("nome") || "").toString();
      var telefono = (data.get("telefono") || "").toString();
      var email = (data.get("email") || "").toString();
      var messaggio = (data.get("messaggio") || "").toString();

      var subject = "Richiesta informazioni — " + nome;
      var body = "Nome: " + nome + "\n" +
        "Email: " + email + "\n" +
        (telefono ? "Telefono: " + telefono + "\n" : "") +
        "\nMessaggio:\n" + messaggio;

      window.location.href = "mailto:roomh74@gmail.com" +
        "?subject=" + encodeURIComponent(subject) +
        "&body=" + encodeURIComponent(body);
    });
  }

  /* ---------- footer year ---------- */
  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

})();
