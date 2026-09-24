/* AT Luxury Car Rental · Landing Audi RS3 */
(() => {
  const WA_NUMBER = '393519822171';
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const waLink = (text) => `https://wa.me/${WA_NUMBER}?text=${encodeURIComponent(text)}`;

  /* ---- WhatsApp links ---- */
  $$('[data-wa]').forEach((a) => {
    a.href = waLink(a.dataset.wa);
    a.target = '_blank';
    a.rel = 'noopener';
  });

  /* ---- nav + sticky cta ---- */
  const nav = $('#nav');
  const sticky = $('.sticky-cta');
  const onScroll = () => {
    const y = scrollY;
    nav.classList.toggle('scrolled', y > 40);
    sticky.classList.toggle('show', y > innerHeight * 0.8);
  };
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---- reveal + counters + route ---- */
  const countUp = (el) => {
    const end = parseFloat(el.dataset.count);
    const dec = +(el.dataset.dec || 0);
    const t0 = performance.now();
    const dur = 1600;
    const step = (t) => {
      const p = Math.min((t - t0) / dur, 1);
      const v = end * (1 - Math.pow(1 - p, 3));
      el.textContent = v.toFixed(dec).replace('.', ',');
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      e.target.classList.add('in');
      $$('[data-count]', e.target).forEach(countUp);
      if (e.target.matches('[data-count]')) countUp(e.target);
      io.unobserve(e.target);
    });
  }, { threshold: 0.18 });
  $$('.reveal').forEach((el) => io.observe(el));
  const routePath = $('#routePath');
  if (routePath) routePath.parentNode.parentNode.style.setProperty('--len', Math.ceil(routePath.getTotalLength()));

  /* ---- 3D tilt ---- */
  if (!reduced && matchMedia('(hover: hover)').matches) {
    $$('[data-tilt]').forEach((el) => {
      const max = +(el.dataset.tiltMax || 8);
      const target = el.classList.contains('hero__stage') ? $('.phone', el) : el;
      el.addEventListener('pointermove', (e) => {
        const r = el.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width - 0.5;
        const y = (e.clientY - r.top) / r.height - 0.5;
        target.style.transform = `perspective(1000px) rotateY(${x * max * 2 - (target !== el ? 14 : 0)}deg) rotateX(${-y * max * 2 + (target !== el ? 6 : 0)}deg)`;
        $$('[data-depth]', el).forEach((c) => {
          const d = +c.dataset.depth / 100;
          c.style.transform = `translate(${x * 40 * d}px, ${y * 40 * d}px)`;
        });
      });
      el.addEventListener('pointerleave', () => {
        target.style.transform = '';
        $$('[data-depth]', el).forEach((c) => (c.style.transform = ''));
      });
    });
  }

  /* ---- hero speed lines (canvas) ---- */
  const cv = $('#speedlines');
  if (cv && !reduced) {
    const ctx = cv.getContext('2d');
    let W, H, DPR, stars;
    const N = 140;
    const reset = (s, init) => {
      s.x = (Math.random() - 0.5) * W * 2;
      s.y = (Math.random() - 0.5) * H * 2;
      s.z = init ? Math.random() * W : W;
      s.pz = s.z;
    };
    const size = () => {
      DPR = Math.min(devicePixelRatio || 1, 2);
      W = cv.width = cv.offsetWidth * DPR;
      H = cv.height = cv.offsetHeight * DPR;
      stars = Array.from({ length: N }, () => { const s = {}; reset(s, true); return s; });
    };
    size();
    addEventListener('resize', size);
    let speed = 10;
    let visible = true;
    new IntersectionObserver(([e]) => (visible = e.isIntersecting)).observe(cv);
    const cx = () => W * 0.66;
    const cy = () => H * 0.45;
    const frame = () => {
      requestAnimationFrame(frame);
      if (!visible) return;
      ctx.fillStyle = 'rgba(5,6,5,.35)';
      ctx.fillRect(0, 0, W, H);
      for (const s of stars) {
        s.pz = s.z;
        s.z -= speed * DPR;
        if (s.z < 1) { reset(s); continue; }
        const sx = cx() + (s.x / s.z) * W * 0.5;
        const sy = cy() + (s.y / s.z) * W * 0.5;
        const px = cx() + (s.x / s.pz) * W * 0.5;
        const py = cy() + (s.y / s.pz) * W * 0.5;
        const a = 1 - s.z / W;
        ctx.strokeStyle = `rgba(143,227,26,${a * 0.8})`;
        ctx.lineWidth = a * 2.5 * DPR;
        ctx.beginPath();
        ctx.moveTo(px, py);
        ctx.lineTo(sx, sy);
        ctx.stroke();
      }
    };
    frame();
    // accelerate on CTA hover
    $$('.hero .btn').forEach((b) => {
      b.addEventListener('pointerenter', () => (speed = 34));
      b.addEventListener('pointerleave', () => (speed = 10));
    });
  }

  /* ---- tachometer tied to scroll ---- */
  const fill = $('#tachoFill');
  if (fill) {
    const len = fill.getTotalLength();
    fill.style.strokeDasharray = len;
    fill.style.strokeDashoffset = len;
    const ticks = $('#ticks');
    const NS = 'http://www.w3.org/2000/svg';
    for (let i = 1; i <= 7; i++) {
      const a = (-225 + i * (270 / 8)) * Math.PI / 180;
      const r1 = 128, r2 = 112, rl = 92;
      const l = document.createElementNS(NS, 'line');
      l.setAttribute('x1', 200 + Math.cos(a) * r1); l.setAttribute('y1', 200 + Math.sin(a) * r1);
      l.setAttribute('x2', 200 + Math.cos(a) * r2); l.setAttribute('y2', 200 + Math.sin(a) * r2);
      l.setAttribute('class', 'tacho__tick' + (i >= 7 ? ' tacho__tick--red' : ''));
      ticks.appendChild(l);
      const t = document.createElementNS(NS, 'text');
      t.setAttribute('x', 200 + Math.cos(a) * rl); t.setAttribute('y', 200 + Math.sin(a) * rl);
      t.setAttribute('class', 'tacho__lbl');
      t.textContent = i;
      ticks.appendChild(t);
    }
    const needle = $('#needle');
    const rpm = $('#rpm');
    const gear = $('#gear');
    const sec = $('#auto');
    const setP = (p) => {
      p = Math.max(0, Math.min(1, p));
      fill.style.strokeDashoffset = len * (1 - p);
      needle.style.transform = `rotate(${-135 + 270 * p}deg)`;
      rpm.textContent = Math.round(p * 7000).toLocaleString('it-IT');
      gear.textContent = p < 0.03 ? 'N' : String(Math.min(7, 1 + Math.floor(p * 7)));
    };
    const isMobile = () => innerWidth <= 960;
    const upd = () => {
      if (isMobile()) return;
      const r = sec.getBoundingClientRect();
      const total = sec.offsetHeight - innerHeight;
      setP(-r.top / total);
    };
    addEventListener('scroll', upd, { passive: true });
    upd();
    // mobile: one-shot rev when visible
    new IntersectionObserver(([e]) => {
      if (!e.isIntersecting || !isMobile()) return;
      const t0 = performance.now();
      const a = (t) => {
        const k = Math.min((t - t0) / 1800, 1);
        setP(k < 0.6 ? k / 0.6 : 1 - (k - 0.6) / 0.4 * 0.35);
        if (k < 1) requestAnimationFrame(a);
      };
      requestAnimationFrame(a);
    }, { threshold: 0.5 }).observe($('#tacho'));
  }

  /* ---- 3D ring gallery (drag + inertia + autorotate) ---- */
  const ring = $('#ring');
  const scene = $('#ringScene');
  if (ring) {
    let rot = 0, vel = reduced ? 0 : 0.12, dragging = false, lastX = 0, auto = !reduced;
    const tick = () => {
      if (!dragging) {
        rot += vel;
        const base = auto ? 0.12 : 0;
        vel += (base - vel) * 0.03;
      }
      ring.style.transform = `rotateX(-8deg) rotateY(${rot}deg)`;
      requestAnimationFrame(tick);
    };
    tick();
    scene.addEventListener('pointerdown', (e) => {
      dragging = true; lastX = e.clientX; vel = 0;
      scene.setPointerCapture(e.pointerId);
    });
    scene.addEventListener('pointermove', (e) => {
      if (!dragging) return;
      const dx = e.clientX - lastX;
      lastX = e.clientX;
      rot += dx * 0.3;
      vel = dx * 0.3;
    });
    const end = () => { dragging = false; };
    scene.addEventListener('pointerup', end);
    scene.addEventListener('pointercancel', end);
  }

  /* ---- pricing tabs ---- */
  const tabs = $$('.tab');
  const ink = $('.tabs__ink');
  const moveInk = (t) => {
    ink.style.width = t.offsetWidth + 'px';
    ink.style.transform = `translateX(${t.offsetLeft - 6}px)`;
  };
  tabs.forEach((t) => t.addEventListener('click', () => {
    tabs.forEach((x) => x.classList.toggle('is-active', x === t));
    $$('.plans').forEach((p) => p.classList.toggle('is-active', p.dataset.panel === t.dataset.tab));
    moveInk(t);
  }));
  const syncInk = () => moveInk($('.tab.is-active'));
  addEventListener('resize', syncInk);
  document.fonts ? document.fonts.ready.then(syncInk) : syncInk();
  syncInk();

  /* ---- calculator ---- */
  const cPlan = $('#cPlan'), cKm = $('#cKm'), cDays = $('#cDays');
  const daysField = $('#daysField');
  const eur = (n) => n.toLocaleString('it-IT', { maximumFractionDigits: 2 }) + '€';
  const fillRange = (r) => r.style.setProperty('--p', ((r.value - r.min) / (r.max - r.min)) * 100 + '%');
  let lastPlan = null;
  const calc = () => {
    const [price, kmInc, perDay, label] = cPlan.value.split('|');
    const pd = perDay === '2';
    daysField.hidden = !pd;
    const days = pd ? +cDays.value : 1;
    const base = +price * days;
    const inc = +kmInc * days;
    if (lastPlan !== cPlan.value) { // sensible default km for the plan
      cKm.value = inc; lastPlan = cPlan.value;
    }
    const km = +cKm.value;
    const extraKm = Math.max(0, km - inc);
    const extra = extraKm * 1.5;
    const tot = base + extra;
    $('#cKmOut').textContent = km + ' km';
    $('#cDaysOut').textContent = days;
    $('#rBase').textContent = eur(base);
    $('#rInc').textContent = inc + ' km';
    $('#rExtra').textContent = extraKm ? `${extraKm} km · ${eur(extra)}` : '0€';
    $('#rSave').textContent = eur(extraKm * 1.5);
    $('#rSaveRow').style.display = extraKm ? '' : 'none';
    $('#rTot').textContent = eur(tot);
    [cKm, cDays].forEach(fillRange);
    const msg = `Ciao! Vorrei un preventivo per l'Audi RS3:\n• Formula: ${label}${pd ? ` (${days} giorni)` : ''}\n• Km previsti: ${km} (inclusi ${inc})\n• Totale stimato: ${eur(tot)}${extraKm ? ` con ${extraKm} km extra prepagati` : ''}\nDate che mi interessano: `;
    const send = $('#calcSend');
    send.href = waLink(msg); send.target = '_blank'; send.rel = 'noopener';
  };
  [cPlan, cKm, cDays].forEach((el) => el.addEventListener('input', calc));
  calc();

  /* ---- parallax backgrounds ---- */
  if (!reduced) {
    const pars = $$('.gift__bg, .final__bg');
    addEventListener('scroll', () => {
      pars.forEach((el) => {
        const r = el.parentNode.getBoundingClientRect();
        if (r.bottom < 0 || r.top > innerHeight) return;
        const p = (r.top + r.height / 2 - innerHeight / 2) / innerHeight;
        el.style.transform = `translateY(${p * -60}px) scale(1.1)`;
      });
    }, { passive: true });
  }
})();
