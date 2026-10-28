// Header, menu mobile, tendina "Soluzioni", pulsante "torna su", animazioni allo scroll e form di contatto.
(function () {
  var body = document.body;
  var header = document.querySelector('.site-header');
  var toTop = document.querySelector('.to-top');

  function onScroll() {
    var y = window.scrollY;
    header.classList.toggle('solid', y > 24);
    if (toTop) toTop.classList.toggle('show', y > 600);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  if (toTop) toTop.addEventListener('click', function () { window.scrollTo({ top: 0 }); });

  var toggle = document.querySelector('.menu-toggle');
  function closeMenu() {
    body.classList.remove('menu-open');
    if (toggle) toggle.setAttribute('aria-expanded', 'false');
  }
  if (toggle) {
    toggle.addEventListener('click', function () {
      var open = body.classList.toggle('menu-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }
  document.querySelectorAll('.main-nav a').forEach(function (a) { a.addEventListener('click', closeMenu); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { closeMenu(); closeDropdowns(); } });

  function closeDropdowns() {
    document.querySelectorAll('.dd.open').forEach(function (d) {
      d.classList.remove('open');
      d.querySelector('.dd-btn').setAttribute('aria-expanded', 'false');
    });
  }
  document.querySelectorAll('.dd-btn').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var dd = btn.closest('.dd');
      var open = dd.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });
  document.addEventListener('click', function (e) { if (!e.target.closest('.dd')) closeDropdowns(); });

  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
    document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('in'); });
  }

  // Form: controllo antispam ("La capitale della Francia?") e invio a Netlify Forms.
  document.querySelectorAll('form.form').forEach(function (form) {
    var msg = form.querySelector('.form-msg');
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var answer = (form.elements['antispam'].value || '').trim().toLowerCase();
      if (answer !== 'parigi' && answer !== 'paris') {
        msg.className = 'form-msg err';
        msg.textContent = 'La risposta alla domanda di sicurezza non è corretta.';
        form.elements['antispam'].focus();
        return;
      }
      var button = form.querySelector('button[type="submit"]');
      button.disabled = true;
      var body = new URLSearchParams(new FormData(form)).toString();
      fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: body })
        .then(function (r) {
          if (!r.ok) throw new Error(r.status);
          form.reset();
          msg.className = 'form-msg ok';
          msg.textContent = 'Grazie! Abbiamo ricevuto la tua richiesta: ti ricontatteremo al più presto.';
        })
        .catch(function () {
          msg.className = 'form-msg err';
          msg.textContent = 'Invio non riuscito. Riprova più tardi oppure chiamaci direttamente.';
        })
        .then(function () { button.disabled = false; });
    });
  });
})();
