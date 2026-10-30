// Padovani & Partners — comportamento del sito.
// Menu e pannello "Società e partner", header, animazioni di ingresso e allo scorrimento,
// globo 3D in canvas, card con profondità, contatori, form di contatto.
// Con "riduci movimento" attivo il sito resta completamente statico.
(function () {
  var doc = document.documentElement;
  var body = document.body;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var desktop = window.matchMedia('(min-width: 1081px) and (hover: hover)');
  var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var header = document.querySelector('.site-header');

  // ------------------------------------------------------------ titoli parola per parola
  document.querySelectorAll('.split').forEach(function (el) {
    var words = el.textContent.trim().split(/\s+/);
    el.setAttribute('aria-label', el.textContent.trim());
    el.innerHTML = words.map(function (w, i) {
      return '<span class="w" aria-hidden="true"><span style="--d:' + (0.18 + i * 0.055).toFixed(3) + 's">' + w + '</span></span>';
    }).join(' ');
  });

  // ------------------------------------------------------------ testo che si "accende" scorrendo
  var fills = [];
  document.querySelectorAll('.statement-fill').forEach(function (el) {
    el.innerHTML = el.textContent.trim().split(/\s+/).map(function (w) { return '<span class="w">' + w + '</span>'; }).join(' ');
    fills.push({ el: el, words: el.querySelectorAll('.w') });
  });

  // ------------------------------------------------------------ elementi che compaiono allo scorrimento
  var autoReveal = '.prose > *, .features > div, .sidebar, .form, .contact-grid .intro, .others > a, .companies > li, .contact-band .wrap > div, .footer-grid > div';
  document.querySelectorAll(autoReveal).forEach(function (el) {
    if (el.hasAttribute('data-reveal')) return;
    var i = Array.prototype.indexOf.call(el.parentNode.children, el);
    el.setAttribute('data-reveal', '');
    el.style.setProperty('--d', Math.min(i, 6) * 0.07 + 's');
  });
  var revealEls = document.querySelectorAll('[data-reveal]');
  if (reduce || !('IntersectionObserver' in window)) {
    revealEls.forEach(function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add('in');
        io.unobserve(e.target);
        if (e.target.querySelector('[data-count]')) countUp(e.target.querySelector('[data-count]'));
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
    revealEls.forEach(function (el) { io.observe(el); });
  }

  // ------------------------------------------------------------ contatori
  function countUp(el) {
    var to = parseInt(el.getAttribute('data-count'), 10);
    var from = parseInt(el.getAttribute('data-from') || '0', 10);
    if (reduce) { el.textContent = to; return; }
    var t0 = null, dur = 1800;
    function step(t) {
      if (!t0) t0 = t;
      var k = Math.min(1, (t - t0) / dur);
      var e = 1 - Math.pow(1 - k, 4);
      el.textContent = Math.round(from + (to - from) * e);
      if (k < 1) requestAnimationFrame(step);
    }
    el.textContent = from;
    requestAnimationFrame(step);
  }

  // ------------------------------------------------------------ ingresso pagina e uscita morbida
  function ready() { body.classList.add('ready'); }
  if (document.readyState === 'complete') requestAnimationFrame(ready);
  else window.addEventListener('load', function () { requestAnimationFrame(ready); });
  setTimeout(ready, 1200);
  window.addEventListener('pageshow', function (e) { if (e.persisted) { body.classList.remove('leaving'); ready(); } });

  document.addEventListener('click', function (e) {
    var a = e.target.closest('a');
    if (!a || reduce || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || a.target === '_blank') return;
    var href = a.getAttribute('href');
    if (!href || href.charAt(0) === '#' || /^(tel:|mailto:|https?:)/.test(href)) return;
    var url = new URL(a.href);
    if (url.pathname === location.pathname && url.hash) return;
    e.preventDefault();
    body.classList.add('leaving');
    setTimeout(function () { location.href = a.href; }, 260);
  });

  // ------------------------------------------------------------ pannello "Società e partner"
  document.querySelectorAll('.dd').forEach(function (dd) {
    var btn = dd.querySelector('.nav-link');
    var timer;
    function open() { clearTimeout(timer); dd.classList.add('open'); btn.setAttribute('aria-expanded', 'true'); updateHeader(); }
    function close() { clearTimeout(timer); dd.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); updateHeader(); }
    btn.addEventListener('click', function (e) { e.stopPropagation(); dd.classList.contains('open') ? close() : open(); });
    dd.addEventListener('mouseenter', function () { if (desktop.matches) open(); });
    dd.addEventListener('mouseleave', function () { if (desktop.matches) timer = setTimeout(close, 220); });
    dd.addEventListener('focusout', function (e) { if (desktop.matches && !dd.contains(e.relatedTarget)) close(); });
    document.addEventListener('click', function (e) { if (desktop.matches && !dd.contains(e.target)) close(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && dd.classList.contains('open')) { close(); btn.focus(); } });
  });

  // ------------------------------------------------------------ menu mobile
  var toggle = document.querySelector('.menu-toggle');
  function closeMenu() { body.classList.remove('menu-open'); toggle.setAttribute('aria-expanded', 'false'); updateHeader(); }
  toggle.addEventListener('click', function () {
    var open = body.classList.toggle('menu-open');
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    updateHeader();
  });
  document.querySelectorAll('.main-nav a').forEach(function (a) { a.addEventListener('click', closeMenu); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeMenu(); });
  if (desktop.addEventListener) desktop.addEventListener('change', closeMenu);

  // ------------------------------------------------------------ header, avanzamento lettura, parallasse
  var progress = document.createElement('div');
  progress.className = 'progress';
  body.appendChild(progress);
  var toTop = document.querySelector('.to-top');
  var lastY = window.scrollY;
  var heroContent = document.querySelector('.hero-content');
  var heroGlobe = document.querySelector('.hero-globe');
  var stepsWrap = document.querySelector('.steps-wrap');
  var steps = stepsWrap ? stepsWrap.querySelectorAll('.steps li') : [];
  var cards = [];

  function updateHeader() {
    var y = window.scrollY;
    var forced = body.classList.contains('menu-open') || document.querySelector('.dd.open');
    header.classList.toggle('is-solid', y > 40 || !!forced);
    var goingDown = y > lastY && y > 400;
    header.classList.toggle('is-hidden', goingDown && !forced);
    lastY = y;
  }

  function onScroll() {
    var y = window.scrollY, vh = window.innerHeight;
    updateHeader();
    var max = doc.scrollHeight - vh;
    progress.style.setProperty('--p', max > 0 ? (y / max).toFixed(4) : 0);
    toTop.classList.toggle('show', y > 700);
    if (reduce) return;

    if (heroContent && y < vh * 1.2) {
      heroContent.style.transform = 'translate3d(0,' + (y * 0.18).toFixed(1) + 'px,0)';
      heroContent.style.opacity = Math.max(0, 1 - y / (vh * 0.75)).toFixed(3);
      if (heroGlobe) heroGlobe.style.translate = '0 ' + (y * 0.32).toFixed(1) + 'px';
    }

    fills.forEach(function (f) {
      var r = f.el.getBoundingClientRect();
      var k = (vh * 0.85 - r.top) / (vh * 0.85 - vh * 0.35 + r.height * 0.4);
      k = Math.max(0, Math.min(1, k));
      var n = Math.round(k * f.words.length);
      for (var i = 0; i < f.words.length; i++) f.words[i].classList.toggle('on', i < n);
    });

    if (stepsWrap) {
      var r = stepsWrap.getBoundingClientRect();
      var p = Math.max(0, Math.min(1, (vh * 0.8 - r.top) / (vh * 0.45)));
      stepsWrap.style.setProperty('--p', p.toFixed(3));
      var track = stepsWrap.querySelector('.track span');
      if (track) track.style.setProperty('--p', p.toFixed(3));
      for (var j = 0; j < steps.length; j++) steps[j].classList.toggle('active', p >= j / steps.length + 0.02);
    }
  }
  var ticking = false;
  window.addEventListener('scroll', function () {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () { ticking = false; onScroll(); });
  }, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();
  if (reduce) {
    fills.forEach(function (f) { f.words.forEach(function (w) { w.classList.add('on'); }); });
    steps.forEach(function (s) { s.classList.add('active'); });
    if (stepsWrap) stepsWrap.querySelector('.track span').style.setProperty('--p', 1);
  }
  toTop.addEventListener('click', function () { window.scrollTo({ top: 0 }); });

  // ------------------------------------------------------------ card con profondità
  if (finePointer && !reduce) {
    document.querySelectorAll('.card3d').forEach(function (card) {
      card.addEventListener('pointermove', function (e) {
        var r = card.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
        card.classList.add('tilting');
        card.style.setProperty('--ry', ((x - 0.5) * 10).toFixed(2) + 'deg');
        card.style.setProperty('--rx', ((0.5 - y) * 8).toFixed(2) + 'deg');
        card.style.setProperty('--mx', (x * 100).toFixed(1) + '%');
        card.style.setProperty('--my', (y * 100).toFixed(1) + '%');
      });
      card.addEventListener('pointerleave', function () {
        card.classList.remove('tilting');
        card.style.setProperty('--rx', '0deg');
        card.style.setProperty('--ry', '0deg');
      });
    });
  }

  // ------------------------------------------------------------ globo 3D
  // Sfera di punti in proiezione prospettica, con un nodo centrale (la holding)
  // collegato da archi alle società; ruota lentamente e si inclina seguendo il mouse.
  function Globe(canvas, small) {
    var ctx = canvas.getContext('2d');
    var N = small ? 700 : 1300;
    var pts = [];
    var golden = Math.PI * (3 - Math.sqrt(5));
    for (var i = 0; i < N; i++) {
      var y = 1 - (i / (N - 1)) * 2, r = Math.sqrt(1 - y * y), th = golden * i;
      pts.push([Math.cos(th) * r, y, Math.sin(th) * r]);
    }
    function ll(lat, lon) {
      var la = lat * Math.PI / 180, lo = lon * Math.PI / 180;
      return [Math.cos(la) * Math.cos(lo), Math.sin(la), Math.cos(la) * Math.sin(lo)];
    }
    var hub = ll(45.4, 11.9);
    var nodes = [ll(64, -14), ll(26, 44), ll(12, 2), ll(56, 52), ll(30, -32)];
    function slerp(a, b, t) {
      var d = a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
      var om = Math.acos(Math.max(-1, Math.min(1, d))), so = Math.sin(om);
      var ka = Math.sin((1 - t) * om) / so, kb = Math.sin(t * om) / so;
      return [a[0] * ka + b[0] * kb, a[1] * ka + b[1] * kb, a[2] * ka + b[2] * kb];
    }
    var arcs = nodes.map(function (n) {
      var seg = [];
      for (var s = 0; s <= 48; s++) {
        var t = s / 48, p = slerp(hub, n, t), lift = 1 + 0.16 * Math.sin(Math.PI * t);
        seg.push([p[0] * lift, p[1] * lift, p[2] * lift]);
      }
      return seg;
    });

    var w = 0, h = 0, dpr = 1, R = 0, cx = 0, cy = 0;
    // orientamento iniziale: il nodo centrale (Padova) rivolto verso chi guarda
    var BASE = 1.05, TILT = 0.36;
    var rotY = BASE, tiltX = TILT, tTilt = TILT, tYaw = 0, yaw = 0;
    var running = false, visible = true, t0 = performance.now();

    function resize() {
      var b = canvas.getBoundingClientRect();
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      w = b.width; h = b.height;
      canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr);
      R = Math.min(w, h) * 0.34; cx = w / 2; cy = h / 2;
    }

    function project(p) {
      var cyw = Math.cos(rotY + yaw), syw = Math.sin(rotY + yaw);
      var x = p[0] * cyw - p[2] * syw, z = p[0] * syw + p[2] * cyw;
      var ct = Math.cos(tiltX), st = Math.sin(tiltX);
      var y = p[1] * ct - z * st; z = p[1] * st + z * ct;
      var k = 4.6 / (4.6 - z);
      return [cx + x * R * k, cy - y * R * k, z, k];
    }

    function draw(now) {
      var time = Math.max(0, (now - t0) / 1000);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, w, h);

      // alone e contorno della sfera
      var g = ctx.createRadialGradient(cx, cy, R * 0.2, cx, cy, R * 1.25);
      g.addColorStop(0, 'rgba(120,170,150,0.07)');
      g.addColorStop(1, 'rgba(120,170,150,0)');
      ctx.fillStyle = g;
      ctx.beginPath(); ctx.arc(cx, cy, R * 1.25, 0, Math.PI * 2); ctx.fill();
      ctx.strokeStyle = 'rgba(214,228,222,0.10)';
      ctx.lineWidth = 1;
      ctx.beginPath(); ctx.arc(cx, cy, R * 1.08, 0, Math.PI * 2); ctx.stroke();

      // orbita inclinata
      ctx.lineWidth = 1;
      var orbit = [];
      for (var o = 0; o <= 120; o++) {
        var a = o / 120 * Math.PI * 2;
        var op = [Math.cos(a) * 1.24, Math.sin(a) * 1.24 * 0.18, Math.sin(a) * 1.24];
        orbit.push(project([op[0], op[1] + op[2] * 0.25, op[2]]));
      }
      for (var oi = 1; oi < orbit.length; oi++) {
        var oz = (orbit[oi][2] + 1.25) / 2.5;
        ctx.strokeStyle = 'rgba(214,228,222,' + (0.04 + oz * 0.14).toFixed(3) + ')';
        ctx.beginPath(); ctx.moveTo(orbit[oi - 1][0], orbit[oi - 1][1]); ctx.lineTo(orbit[oi][0], orbit[oi][1]); ctx.stroke();
      }
      var oa = time * 0.25 % (Math.PI * 2);
      var sat = project([Math.cos(oa) * 1.24, Math.sin(oa) * 1.24 * 0.18 + Math.sin(oa) * 1.24 * 0.25, Math.sin(oa) * 1.24]);
      ctx.fillStyle = 'rgba(230,214,179,' + (0.35 + (sat[2] + 1.25) / 2.5 * 0.6).toFixed(3) + ')';
      ctx.beginPath(); ctx.arc(sat[0], sat[1], 2.2 * sat[3], 0, Math.PI * 2); ctx.fill();

      // punti della sfera
      for (var i = 0; i < N; i++) {
        var q = project(pts[i]);
        var depth = (q[2] + 1) / 2;
        if (depth < 0.08) continue;
        ctx.fillStyle = 'rgba(214,228,222,' + (0.05 + Math.pow(depth, 1.6) * 0.62).toFixed(3) + ')';
        var s = (0.55 + depth * 0.95) * (small ? 0.9 : 1);
        ctx.fillRect(q[0] - s / 2, q[1] - s / 2, s, s);
      }

      // archi hub → società, con un impulso che li percorre
      arcs.forEach(function (seg, ai) {
        var P = seg.map(project);
        for (var s2 = 1; s2 < P.length; s2++) {
          var dz = (P[s2][2] + 1.2) / 2.4;
          ctx.strokeStyle = 'rgba(230,214,179,' + (0.06 + Math.pow(dz, 2) * 0.5).toFixed(3) + ')';
          ctx.lineWidth = 1;
          ctx.beginPath(); ctx.moveTo(P[s2 - 1][0], P[s2 - 1][1]); ctx.lineTo(P[s2][0], P[s2][1]); ctx.stroke();
        }
        var tt = ((time * 0.28 + ai * 0.21) % 1);
        var pi2 = P[Math.round(tt * (P.length - 1))];
        var pz = (pi2[2] + 1.2) / 2.4;
        ctx.fillStyle = 'rgba(245,235,212,' + (0.2 + pz * 0.8).toFixed(3) + ')';
        ctx.beginPath(); ctx.arc(pi2[0], pi2[1], 1.8 * pi2[3], 0, Math.PI * 2); ctx.fill();
        var end = P[P.length - 1], ez = (end[2] + 1) / 2;
        ctx.fillStyle = 'rgba(230,214,179,' + (0.15 + ez * 0.75).toFixed(3) + ')';
        ctx.beginPath(); ctx.arc(end[0], end[1], 2.6 * end[3], 0, Math.PI * 2); ctx.fill();
      });

      // nodo centrale con onda
      var hq = project(hub), hz = (hq[2] + 1) / 2;
      var pulse = (time * 0.45) % 1;
      ctx.strokeStyle = 'rgba(230,214,179,' + ((1 - pulse) * 0.5 * hz).toFixed(3) + ')';
      ctx.lineWidth = 1;
      ctx.beginPath(); ctx.arc(hq[0], hq[1], (4 + pulse * 22) * hq[3], 0, Math.PI * 2); ctx.stroke();
      ctx.fillStyle = 'rgba(245,235,212,' + (0.3 + hz * 0.7).toFixed(3) + ')';
      ctx.beginPath(); ctx.arc(hq[0], hq[1], 3.6 * hq[3], 0, Math.PI * 2); ctx.fill();
    }

    var last = performance.now();
    function frame(now) {
      if (!running) return;
      last = now;
      // oscillazione lenta, così la rete delle società resta in vista
      rotY = BASE + Math.sin((now - t0) / 1000 * 0.11) * 0.75;
      tiltX += (tTilt - tiltX) * 0.04;
      yaw += (tYaw - yaw) * 0.04;
      draw(now);
      requestAnimationFrame(frame);
    }
    function start() { if (running || reduce || !visible || document.hidden) return; running = true; last = performance.now(); requestAnimationFrame(frame); }
    function stop() { running = false; }

    resize();
    draw(performance.now());
    if (window.ResizeObserver) new ResizeObserver(function () { resize(); draw(performance.now()); }).observe(canvas);
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (en) { visible = en[0].isIntersecting; visible ? start() : stop(); }).observe(canvas);
    }
    document.addEventListener('visibilitychange', function () { document.hidden ? stop() : start(); });
    if (finePointer) {
      window.addEventListener('pointermove', function (e) {
        var nx = e.clientX / window.innerWidth - 0.5, ny = e.clientY / window.innerHeight - 0.5;
        tYaw = nx * 0.5;
        tTilt = TILT + ny * 0.26;
      }, { passive: true });
    }
    start();
  }
  document.querySelectorAll('canvas[data-globe]').forEach(function (c) {
    if (c.getContext) Globe(c, c.getAttribute('data-globe') === 'small');
  });

  // ------------------------------------------------------------ form: antispam e invio a Netlify Forms
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
