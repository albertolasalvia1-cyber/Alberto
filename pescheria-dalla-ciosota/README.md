# Pescheria dalla Ciosota — sito web

Sito vetrina per la **Pescheria dalla Ciosota** (Piazzale Santa Croce 8, 35123 Padova) di Serena Boscolo Berto.
HTML5 + CSS + JavaScript puri, nessuna dipendenza esterna (solo Google Fonts): si pubblica su qualsiasi hosting
statico caricando questa cartella così com'è.

## Pagine
- `index.html` — home: hero con video, info, chi siamo, il pescato (card stile reel), Serena, dove siamo, seguici
- `chi-siamo.html` — storia della pescheria, Serena, come scegliamo il pesce, galleria
- `prodotti.html` — 28 prodotti con filtri (Pesci, Molluschi, Crostacei, Stagionale) e stagionalità mese per mese
- `contatti.html` — mappa Google, orari completi, form contatto (apre il programma di posta), social

## Foto e video
Copia i file in `img/` e `video/` con i nomi indicati nei rispettivi `README.md`: compaiono in automatico.
Finché mancano, il sito mostra segnaposto SVG coordinati (mai immagini "rotte").

## Da completare prima della pubblicazione
- **Partita IVA** nel footer di ogni pagina (cerca `TODO` / "da inserire").
- **Link Facebook**: verificare l'indirizzo esatto della pagina (attualmente `facebook.com/pescheriadallaciosota`).
- **Testi e citazioni** di Serena: sono bozze da far rileggere/approvare a lei.
- **Stagionalità** dei prodotti: indicativa, da confermare con Serena.
- Immagine di anteprima per i social (`og:image`, 1200×630 JPG) se desiderata.

## Note tecniche
- Mobile-first, breakpoint 600px e 800px; font Barlow Condensed + Barlow con `display=swap`.
- Scroll reveal one-shot con IntersectionObserver; animazioni solo `transform`/`opacity`; `prefers-reduced-motion` rispettato.
- Foto e video caricati in lazy loading solo quando si avvicinano allo schermo; i video vanno in pausa fuori schermo.
- Dati strutturati schema.org (Store) in home e contatti, `sitemap.xml` e `robots.txt` per il dominio pescheriadallaciosota.it.
