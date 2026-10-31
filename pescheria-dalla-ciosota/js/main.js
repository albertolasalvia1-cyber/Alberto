/* ==========================================================================
   Pescheria dalla Ciosota — main.js
   Vanilla JS, nessuna dipendenza esterna.
   - nav trasparente → blu scuro allo scroll + menu mobile
   - scroll reveal one-shot (IntersectionObserver)
   - caricamento lazy di foto/video da img/ e video/ con fallback SVG
   - filtri prodotti, stagionalità, stato aperto/chiuso, form contatti
   ========================================================================== */
(() => {
  'use strict';

  const doc = document;
  const root = doc.documentElement;
  const reduceMQ = window.matchMedia('(prefers-reduced-motion: reduce)');
  const reduced = () => reduceMQ.matches;
  const conn = navigator.connection || {};
  const lowData = Boolean(conn.saveData) || /(^|-)2g$/.test(conn.effectiveType || '');
  const hasIO = 'IntersectionObserver' in window;

  /* ---------- NAV ---------- */
  const nav = doc.querySelector('[data-nav]');
  if (nav) {
    let ticking = false;
    const onScroll = () => {
      nav.classList.toggle('is-scrolled', window.scrollY > 24);
      ticking = false;
    };
    window.addEventListener('scroll', () => {
      if (!ticking) { ticking = true; requestAnimationFrame(onScroll); }
    }, { passive: true });
    onScroll();

    const toggle = nav.querySelector('.nav__toggle');
    const menu = nav.querySelector('.nav__menu');
    const setOpen = (open) => {
      nav.classList.toggle('is-open', open);
      root.classList.toggle('menu-open', open);
      toggle.setAttribute('aria-expanded', String(open));
      toggle.querySelector('.sr-only').textContent = open ? 'Chiudi il menu' : 'Apri il menu';
    };
    if (toggle && menu) {
      toggle.addEventListener('click', () => setOpen(!nav.classList.contains('is-open')));
      menu.addEventListener('click', (e) => { if (e.target.closest('a')) setOpen(false); });
      doc.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && nav.classList.contains('is-open')) { setOpen(false); toggle.focus(); }
      });
      window.matchMedia('(min-width: 800px)').addEventListener('change', (e) => { if (e.matches) setOpen(false); });
    }
  }

  /* ---------- SCROLL REVEAL (one-shot) ---------- */
  const revealEls = doc.querySelectorAll('.reveal');
  if (!hasIO || reduced()) {
    revealEls.forEach((el) => el.classList.add('is-in'));
  } else {
    const revealIO = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-in');
        revealIO.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    revealEls.forEach((el) => revealIO.observe(el));
  }

  /* ---------- MEDIA: foto e video con fallback SVG ----------
     <div class="media" data-img="ombrina" data-video="ombrina"> … placeholder SVG … </div>
     Prova, in ordine: video/ombrina.{mp4,webm,mov} → img/ombrina.{webp,jpg,jpeg,png}.
     Se nessun file esiste resta il placeholder SVG già presente nell'HTML. */
  const IMG_EXT = ['webp', 'jpg', 'jpeg', 'png'];
  const VID_EXT = ['mp4', 'webm', 'mov'];

  const firstAvailable = (sources, probe) =>
    sources.reduce((chain, src) => chain.catch(() => probe(src)), Promise.reject());

  const probeImage = (src) => new Promise((resolve, reject) => {
    const img = new Image();
    img.decoding = 'async';
    img.onload = () => resolve(img);
    img.onerror = reject;
    img.src = src;
  });

  const probeVideo = (src) => new Promise((resolve, reject) => {
    const v = doc.createElement('video');
    v.muted = true;
    v.defaultMuted = true;
    v.loop = true;
    v.playsInline = true;
    ['muted', 'loop', 'playsinline', 'autoplay'].forEach((a) => v.setAttribute(a, ''));
    v.preload = 'metadata';
    v.addEventListener('loadedmetadata', () => resolve(v), { once: true });
    v.addEventListener('error', reject, { once: true });
    v.src = src;
  });

  const videoIO = hasIO ? new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      const v = entry.target;
      if (entry.isIntersecting) {
        const p = v.play();
        if (p) p.catch(() => {});
      } else {
        v.pause();
      }
    });
  }, { threshold: 0.2 }) : null;

  const mount = (box, el, kind) => {
    el.classList.add('media__el');
    if (kind === 'img') {
      el.alt = box.dataset.alt || '';
      box.appendChild(el);
      requestAnimationFrame(() => requestAnimationFrame(() => el.classList.add('is-ready')));
    } else {
      el.setAttribute('aria-hidden', 'true');
      el.preload = 'auto';
      const ready = () => el.classList.add('is-ready');
      el.addEventListener('playing', ready, { once: true });
      box.appendChild(el);
      if (videoIO) videoIO.observe(el);
      else { const p = el.play(); if (p) p.catch(() => {}); }
    }
    box.classList.add('has-media');
    box.dispatchEvent(new Event('media:ok'));
  };

  const loadMedia = (box) => {
    const { video, img } = box.dataset;
    const tryVideo = () => (video && !reduced() && !lowData
      ? firstAvailable(VID_EXT.map((x) => `video/${video}.${x}`), probeVideo).then((el) => mount(box, el, 'video'))
      : Promise.reject());
    const tryImage = () => (img
      ? firstAvailable(IMG_EXT.map((x) => `img/${img}.${x}`), probeImage).then((el) => mount(box, el, 'img'))
      : Promise.reject());
    tryVideo().catch(tryImage).catch(() => {
      box.classList.add('is-placeholder');
      box.dispatchEvent(new Event('media:none'));
    });
  };

  /* Gruppi opzionali (es. galleria): restano nascosti finché non c'è almeno una foto;
     le caselle senza file vengono tolte invece di mostrare un segnaposto. */
  const optionalBoxes = new Set();
  doc.querySelectorAll('[data-optional-group]').forEach((group) => {
    group.querySelectorAll('[data-optional] .media').forEach((box) => {
      optionalBoxes.add(box);
      box.addEventListener('media:ok', () => { group.hidden = false; }, { once: true });
      box.addEventListener('media:none', () => box.closest('[data-optional]').remove(), { once: true });
      loadMedia(box);
    });
  });

  const mediaBoxes = [...doc.querySelectorAll('.media[data-img], .media[data-video]')].filter((b) => !optionalBoxes.has(b));
  if (hasIO) {
    const mediaIO = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        mediaIO.unobserve(entry.target);
        loadMedia(entry.target);
      });
    }, { rootMargin: '400px' });
    mediaBoxes.forEach((box) => mediaIO.observe(box));
  } else {
    mediaBoxes.forEach(loadMedia);
  }

  /* ---------- ORARI: oggi + aperto/chiuso (ora di Roma) ---------- */
  const HOURS = { 1: [450, 780], 2: [450, 780], 3: [450, 780], 4: [450, 780], 5: [450, 780], 6: [450, 780] }; // 7:30–13:00, domenica chiuso
  const DAYS = ['domenica', 'lunedì', 'martedì', 'mercoledì', 'giovedì', 'venerdì', 'sabato'];
  const fmt = (m) => `${Math.floor(m / 60)}:${String(m % 60).padStart(2, '0')}`;
  const romeNow = () => {
    try { return new Date(new Date().toLocaleString('en-US', { timeZone: 'Europe/Rome' })); }
    catch (e) { return new Date(); }
  };

  const now = romeNow();
  const today = now.getDay();
  const minutes = now.getHours() * 60 + now.getMinutes();

  const statusEls = doc.querySelectorAll('[data-open-status]');
  if (statusEls.length) {
    const slot = HOURS[today];
    let open = false;
    let text = '';
    if (slot && minutes >= slot[0] && minutes < slot[1]) {
      open = true;
      text = `Aperto ora · chiude alle ${fmt(slot[1])}`;
    } else {
      for (let i = 0; i < 8; i += 1) {
        const d = (today + i) % 7;
        const h = HOURS[d];
        if (!h || (i === 0 && minutes >= h[0])) continue;
        const when = i === 0 ? 'oggi' : i === 1 ? 'domani' : DAYS[d];
        text = `Chiuso ora · riapre ${when} alle ${fmt(h[0])}`;
        break;
      }
    }
    statusEls.forEach((el) => {
      el.textContent = text;
      el.classList.toggle('is-open', open);
      el.hidden = false;
    });
  }
  doc.querySelectorAll('[data-day]').forEach((row) => {
    row.classList.toggle('is-today', Number(row.dataset.day) === today);
  });

  /* ---------- STAGIONALITÀ ---------- */
  const parseMonths = (str) => {
    const set = new Set();
    str.split(',').forEach((range) => {
      const [a, b] = range.split('-').map(Number);
      let m = a;
      const end = b || a;
      set.add(m);
      while (m !== end) { m = (m % 12) + 1; set.add(m); }
    });
    return set;
  };
  const month = now.getMonth() + 1;
  doc.querySelectorAll('[data-months]').forEach((el) => {
    const months = parseMonths(el.dataset.months);
    const cell = el.querySelectorAll('.season__bar span')[month - 1];
    if (cell) cell.classList.add('now');
    const card = el.closest('[data-cat]');
    if (card && months.size < 12 && months.has(month)) card.classList.add('is-season');
  });

  /* ---------- FILTRI PRODOTTI ---------- */
  const filterBar = doc.querySelector('[data-filters]');
  if (filterBar) {
    const buttons = [...filterBar.querySelectorAll('[data-filter]')];
    const cards = [...doc.querySelectorAll('.board [data-cat]')];
    const counter = doc.querySelector('[data-count]');

    const apply = (wanted, animate) => {
      const cat = buttons.some((b) => b.dataset.filter === wanted) ? wanted : 'tutti';
      buttons.forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.filter === cat)));
      let shown = 0;
      cards.forEach((card) => {
        const show = cat === 'tutti' || card.dataset.cat.split(' ').includes(cat);
        const wasHidden = card.hidden;
        card.hidden = !show;
        if (!show) return;
        shown += 1;
        if (animate && wasHidden) {
          card.classList.add('is-in');
          if (!reduced() && card.animate) {
            card.animate(
              [{ opacity: 0, transform: 'translateY(8px)' }, { opacity: 1, transform: 'none' }],
              { duration: 450, delay: Math.min(shown, 10) * 35, easing: 'cubic-bezier(.22,.7,.2,1)', fill: 'backwards' }
            );
          }
        }
      });
      if (counter) counter.textContent = `${shown} ${shown === 1 ? 'prodotto' : 'prodotti'}`;
      return cat;
    };

    filterBar.addEventListener('click', (e) => {
      const btn = e.target.closest('[data-filter]');
      if (!btn) return;
      const cat = apply(btn.dataset.filter, true);
      history.replaceState(null, '', cat === 'tutti' ? location.pathname : `#${cat}`);
    });
    window.addEventListener('hashchange', () => apply(location.hash.slice(1), true));
    apply(decodeURIComponent(location.hash.slice(1)) || 'tutti', false);
  }

  /* ---------- FORM CONTATTI (apre il client di posta) ---------- */
  const form = doc.querySelector('[data-contact-form]');
  if (form) {
    form.setAttribute('novalidate', '');
    const status = form.querySelector('[data-form-status]');
    const isValid = (f) => (f.type === 'checkbox' ? f.checked : f.value.trim() !== '' && f.checkValidity());

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      let firstBad = null;
      form.querySelectorAll('[required]').forEach((f) => {
        const ok = isValid(f);
        f.closest('.field').classList.toggle('is-invalid', !ok);
        if (ok) f.removeAttribute('aria-invalid'); else f.setAttribute('aria-invalid', 'true');
        if (!ok && !firstBad) firstBad = f;
      });
      if (firstBad) {
        status.textContent = 'Controlla i campi evidenziati, per favore.';
        firstBad.focus();
        return;
      }
      const data = new FormData(form);
      const subject = `[Sito] ${data.get('motivo')} – ${data.get('nome')}`;
      const body = [
        `Nome: ${data.get('nome')}`,
        `Email: ${data.get('email')}`,
        `Telefono: ${data.get('telefono') || '-'}`,
        `Motivo: ${data.get('motivo')}`,
        '',
        data.get('messaggio'),
      ].join('\n');
      window.location.href = `mailto:${form.dataset.to}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
      status.textContent = 'Grazie! Si sta aprendo il tuo programma di posta con il messaggio già compilato: premi «Invia» per spedirlo.';
    });

    form.addEventListener('input', (e) => {
      const f = e.target;
      const field = f.closest('.field');
      if (field && field.classList.contains('is-invalid') && isValid(f)) {
        field.classList.remove('is-invalid');
        f.removeAttribute('aria-invalid');
      }
    });
  }

  /* ---------- Anno nel footer ---------- */
  doc.querySelectorAll('[data-year]').forEach((el) => { el.textContent = String(now.getFullYear()); });
})();
