/* =========================================================
   LA SCOTTONERIA — script principale
   ========================================================= */
document.addEventListener('DOMContentLoaded', () => {

  document.getElementById('year').textContent = new Date().getFullYear();

  /* ---------- preloader ---------- */
  const preloader = document.getElementById('preloader');
  window.addEventListener('load', () => {
    setTimeout(() => preloader.classList.add('hidden'), 400);
  });
  // fallback in case 'load' already fired
  setTimeout(() => preloader.classList.add('hidden'), 2500);

  /* ---------- header scroll state ---------- */
  const header = document.getElementById('siteHeader');
  const onScroll = () => {
    header.classList.toggle('scrolled', window.scrollY > 40);
    backToTop.classList.toggle('show', window.scrollY > 500);
  };
  const backToTop = document.getElementById('backToTop');
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  backToTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

  /* ---------- mobile nav ---------- */
  const hamburger = document.getElementById('hamburger');
  const mainNav = document.getElementById('mainNav');
  hamburger.addEventListener('click', () => {
    const open = mainNav.classList.toggle('open');
    hamburger.classList.toggle('open', open);
    hamburger.setAttribute('aria-expanded', open);
  });
  document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
      mainNav.classList.remove('open');
      hamburger.classList.remove('open');
      document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
      link.classList.add('active');
    });
  });

  /* ---------- scroll reveal ---------- */
  const revealEls = document.querySelectorAll('.reveal-up, .reveal-left, .reveal-right');
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in-view');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });
  revealEls.forEach(el => revealObserver.observe(el));

  /* ---------- active nav link on scroll ---------- */
  const sections = document.querySelectorAll('main, section[id]');
  const navLinks = document.querySelectorAll('.nav-link');
  const navObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute('id');
        navLinks.forEach(l => l.classList.toggle('active', l.getAttribute('href') === `#${id}`));
      }
    });
  }, { rootMargin: '-45% 0px -45% 0px' });
  document.querySelectorAll('section[id]').forEach(sec => navObserver.observe(sec));

  /* ---------- ember cursor glow ---------- */
  const emberGlow = document.getElementById('emberGlow');
  window.addEventListener('mousemove', (e) => {
    emberGlow.style.left = `${e.clientX}px`;
    emberGlow.style.top = `${e.clientY}px`;
  });

  /* ---------- 3D tilt effect ---------- */
  const tiltCards = document.querySelectorAll('.tilt-card');
  const maxTilt = 8;
  tiltCards.forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width - 0.5;
      const y = (e.clientY - rect.top) / rect.height - 0.5;
      card.style.transform = `perspective(900px) rotateX(${(-y * maxTilt).toFixed(2)}deg) rotateY(${(x * maxTilt).toFixed(2)}deg) translateZ(6px)`;
    });
    card.addEventListener('mouseleave', () => {
      card.style.transform = 'perspective(900px) rotateX(0) rotateY(0) translateZ(0)';
    });
  });

  /* ---------- hero plate parallax ---------- */
  const heroPlate = document.getElementById('heroPlate');
  if (heroPlate) {
    window.addEventListener('mousemove', (e) => {
      const x = (e.clientX / window.innerWidth - 0.5) * 30;
      const y = (e.clientY / window.innerHeight - 0.5) * 30;
      heroPlate.style.transform = `translate(calc(-0% + ${x}px), calc(-50% + ${y}px))`;
    });
  }

  /* ---------- ember particles canvas ---------- */
  (function embersCanvas() {
    const wrap = document.getElementById('emberCanvas');
    if (!wrap) return;
    const canvas = document.createElement('canvas');
    wrap.appendChild(canvas);
    const ctx = canvas.getContext('2d');
    let w, h, particles = [];
    const count = window.innerWidth < 700 ? 25 : 55;

    function resize() {
      w = canvas.width = wrap.offsetWidth;
      h = canvas.height = wrap.offsetHeight;
    }
    function makeParticle() {
      return {
        x: Math.random() * w,
        y: h + Math.random() * 100,
        r: Math.random() * 2.2 + 0.6,
        speed: Math.random() * 0.6 + 0.25,
        drift: (Math.random() - 0.5) * 0.6,
        alpha: Math.random() * 0.5 + 0.3,
        hue: Math.random() > 0.5 ? '179,20,31' : '255,59,63'
      };
    }
    function init() {
      resize();
      particles = Array.from({ length: count }, makeParticle);
    }
    function tick() {
      ctx.clearRect(0, 0, w, h);
      particles.forEach(p => {
        p.y -= p.speed;
        p.x += p.drift;
        if (p.y < -10) { Object.assign(p, makeParticle(), { y: h + 10 }); }
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${p.hue},${p.alpha})`;
        ctx.shadowBlur = 8;
        ctx.shadowColor = `rgba(${p.hue},0.8)`;
        ctx.fill();
      });
      requestAnimationFrame(tick);
    }
    init();
    tick();
    window.addEventListener('resize', resize);
  })();

  /* ---------- menu tabs ---------- */
  const tabBtns = document.querySelectorAll('.tab-btn');
  const panels = document.querySelectorAll('.menu-panel');
  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => { b.classList.remove('active'); b.setAttribute('aria-selected', 'false'); });
      btn.classList.add('active');
      btn.setAttribute('aria-selected', 'true');
      const target = btn.dataset.tab;
      panels.forEach(p => {
        const match = p.id === `panel-${target}`;
        p.classList.toggle('active', match);
        p.hidden = !match;
      });
    });
  });

  /* ---------- reviews carousel ---------- */
  const track = document.getElementById('reviewsTrack');
  const cards = track ? Array.from(track.children) : [];
  const dotsWrap = document.getElementById('reviewDots');
  let current = 0;
  let autoplayId;

  function renderDots() {
    dotsWrap.innerHTML = '';
    cards.forEach((_, i) => {
      const dot = document.createElement('span');
      if (i === current) dot.classList.add('active');
      dot.addEventListener('click', () => goTo(i));
      dotsWrap.appendChild(dot);
    });
  }
  function goTo(index) {
    cards[current].classList.remove('active');
    current = (index + cards.length) % cards.length;
    cards[current].classList.add('active');
    dotsWrap.querySelectorAll('span').forEach((d, i) => d.classList.toggle('active', i === current));
  }
  function startAutoplay() {
    clearInterval(autoplayId);
    autoplayId = setInterval(() => goTo(current + 1), 6000);
  }
  if (cards.length) {
    cards[0].classList.add('active');
    renderDots();
    startAutoplay();
    document.getElementById('nextReview').addEventListener('click', () => { goTo(current + 1); startAutoplay(); });
    document.getElementById('prevReview').addEventListener('click', () => { goTo(current - 1); startAutoplay(); });
  }

  /* ---------- reservation form ---------- */
  const form = document.getElementById('reservationForm');
  const successMsg = document.getElementById('formSuccess');
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }

      const data = new FormData(form);
      const name = data.get('name');
      const phone = data.get('phone');
      const date = data.get('date');
      const time = data.get('time');
      const guests = data.get('guests');
      const message = data.get('message') || 'Nessuna richiesta particolare';

      const subject = encodeURIComponent(`Richiesta di prenotazione - ${name}`);
      const body = encodeURIComponent(
        `Nome: ${name}\nTelefono: ${phone}\nData: ${date}\nOra: ${time}\nPersone: ${guests}\nNote: ${message}`
      );

      window.location.href = `mailto:info@lascottoneria.it?subject=${subject}&body=${body}`;

      successMsg.hidden = false;
      form.reset();
      setTimeout(() => { successMsg.hidden = true; }, 6000);
    });
  }

  /* ---------- gallery lightbox (simple caption toast) ---------- */
  document.querySelectorAll('.gallery-item').forEach(item => {
    item.addEventListener('click', () => {
      item.classList.add('in-view');
    });
  });

});
