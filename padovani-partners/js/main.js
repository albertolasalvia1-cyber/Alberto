// Menu mobile, pulsante "torna su", animazioni allo scroll e invio dei form di contatto.
(function () {
  var toggle = document.querySelector('.menu-toggle');
  var nav = document.querySelector('.main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      document.body.classList.toggle('menu-open', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  var toTop = document.querySelector('.to-top');
  if (toTop) {
    window.addEventListener('scroll', function () {
      toTop.classList.toggle('show', window.scrollY > 400);
    }, { passive: true });
    toTop.addEventListener('click', function () { window.scrollTo({ top: 0 }); });
  }

  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.12 });
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
        msg.textContent = 'Risposta alla domanda di sicurezza non corretta.';
        return;
      }
      var body = new URLSearchParams(new FormData(form)).toString();
      fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: body })
        .then(function (r) {
          if (!r.ok) throw new Error(r.status);
          form.reset();
          msg.className = 'form-msg ok';
          msg.textContent = 'Grazie! La tua richiesta è stata inviata, ti ricontatteremo al più presto.';
        })
        .catch(function () {
          msg.className = 'form-msg err';
          msg.textContent = 'Invio non riuscito. Riprova più tardi oppure contattaci telefonicamente.';
        });
    });
  });
})();
