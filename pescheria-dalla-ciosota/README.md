# Pescheria dalla Ciosota — sito web

Sito vetrina per la **Pescheria dalla Ciosota** (Piazzale Santa Croce 8, 35123 Padova) di Serena Boscolo Berto.
HTML5 + CSS + JavaScript puri, nessuna dipendenza esterna (solo Google Fonts): si pubblica su qualsiasi hosting
statico caricando questa cartella così com'è.

## Pagine
- `index.html` — home: foto di Serena, chi siamo, il banco, i video di Serena (griglia stile Instagram), dove siamo
- `chi-siamo.html` — la pescheria, Serena, come lavoriamo, foto (sezione che compare solo se ci sono foto)
- `prodotti.html` — "il banco": 23 prodotti con filtri e calendario di stagione
- `contatti.html` — orari, contatti, mappa Google, form (apre il programma di posta)

Contenuti presi da fonti reali: profilo Instagram (bio, numeri, titoli dei reel), registro imprese
(ragione sociale e P.IVA), pagina Facebook, account TikTok.

## Foto e video
Copiate i file in `img/` e `video/` con i nomi indicati nei rispettivi `README.md`.

## Da verificare prima della pubblicazione
- **Orari**: nel sito Lun–Sab 7:30–13:00. Una scheda online (maggio 2026) riporta invece mar–sab 8:30–13:30,
  chiuso domenica e lunedì. Confermare con Serena (orari in home, contatti, footer e in `js/main.js`, costante `HOURS`).
- **Anno di apertura** (2020, dalla data di iscrizione della società).
- Periodi di stagione dei prodotti: indicativi.
- Logo: il sito usa una scritta che richiama il logo; meglio sostituirla con il file originale.

## Note tecniche
- Mobile-first, breakpoint 600px e 800px; font Barlow Condensed + Barlow con `display=swap`.
- Scroll reveal one-shot con IntersectionObserver; animazioni solo `transform`/`opacity`; `prefers-reduced-motion` rispettato.
- Foto e video caricati in lazy loading solo quando si avvicinano allo schermo; i video vanno in pausa fuori schermo.
- Dati strutturati schema.org (Store) in home e contatti, `sitemap.xml` e `robots.txt` per il dominio pescheriadallaciosota.it.
