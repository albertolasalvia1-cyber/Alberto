// Menu (pannello "Società e partner" e menu mobile), pulsante "torna su", form di contatto.
(function () {
  var body = document.body;
  var desktop = window.matchMedia('(min-width: 1081px) and (hover: hover)');

  // ---- Pannello a tendina: si apre al passaggio del mouse (desktop) o al clic/tocco, con un breve ritardo in chiusura
  document.querySelectorAll('.dd').forEach(function (dd) {
    var btn = dd.querySelector('.nav-link');
    var timer;
    function open() { clearTimeout(timer); dd.classList.add('open'); btn.setAttribute('aria-expanded', 'true'); }
    function close() { clearTimeout(timer); dd.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); }
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      dd.classList.contains('open') ? close() : open();
    });
    dd.addEventListener('mouseenter', function () { if (desktop.matches) open(); });
    dd.addEventListener('mouseleave', function () { if (desktop.matches) timer = setTimeout(close, 220); });
    dd.addEventListener('focusout', function (e) { if (desktop.matches && !dd.contains(e.relatedTarget)) close(); });
    document.addEventListener('click', function (e) { if (desktop.matches && !dd.contains(e.target)) close(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && dd.classList.contains('open')) { close(); btn.focus(); } });
  });

  // ---- Menu mobile
  var toggle = document.querySelector('.menu-toggle');
  function closeMenu() { body.classList.remove('menu-open'); toggle.setAttribute('aria-expanded', 'false'); }
  toggle.addEventListener('click', function () {
    var open = body.classList.toggle('menu-open');
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  document.querySelectorAll('.main-nav a').forEach(function (a) { a.addEventListener('click', closeMenu); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeMenu(); });
  desktop.addEventListener && desktop.addEventListener('change', closeMenu);

  // ---- Torna su
  var toTop = document.querySelector('.to-top');
  window.addEventListener('scroll', function () { toTop.classList.toggle('show', window.scrollY > 700); }, { passive: true });
  toTop.addEventListener('click', function () { window.scrollTo({ top: 0 }); });

  // ---- Form: controllo antispam ("La capitale della Francia?") e invio a Netlify Forms
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
      fetch('/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams(new FormData(form)).toString()
      })
        .then(function (r) {
          if (!r.ok) throw new Error(r.status);
          form.reset();
          msg.className = 'form-msg ok';
          msg.textContent = 'Richiesta inviata correttamente. Sarete ricontattati al più presto.';
        })
        .catch(function () {
          msg.className = 'form-msg err';
          msg.textContent = 'Invio non riuscito. Riprovare più tardi oppure contattarci telefonicamente.';
        })
        .then(function () { button.disabled = false; });
    });
  });
})();
