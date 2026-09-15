# La Scottoneria — Sito Web

Sito vetrina per il ristorante **La Scottoneria** (Via Strada Battaglia 145, Albignasego – Padova), pensato per invogliare i visitatori a prenotare un tavolo. Nessun framework/build: HTML + CSS + JS puri, pronto per essere pubblicato su qualsiasi hosting statico (GitHub Pages, Netlify, hosting tradizionale...).

Stile grafico: bianco / nero / rosso, coerente con l'identità reale del locale (logo, menù e carta vini "rosso e nero").

## Struttura

```
index.html                         pagina unica con tutte le sezioni
css/style.css                      stile, animazioni, effetti 3D
js/main.js                         interattività (menu a tab, carosello recensioni, form, particelle, tilt 3D)
assets/img/                        cartella per le foto reali del locale
assets/menu/menu-la-scottoneria.pdf         menù ufficiale (scaricabile dal sito)
assets/menu/carta-vini-la-scottoneria.pdf   carta dei vini ufficiale (scaricabile dal sito)
```

## Dati usati (fonti reali)

- **Menù e prezzi**: presi dal PDF ufficiale `MENU-scottoneria-2026-x-sito.pdf` fornito dal locale — tutti i piatti, prezzi e allergeni riportati nella sezione "Menù Digitale" sono quelli reali.
- **Carta dei vini**: presa dal PDF ufficiale `CARTA-DEI-VINI-scottoneria-rosso-e-nero.pdf` — bollicine, bianchi e rossi con prezzi reali.
- **Testo "Chi siamo"**: ripreso dal sito ufficiale lascottoneria.it.
- **Contatti**: indirizzo, telefono (049 573 5845) ed email (info@lascottoneria.it) da fonti pubbliche verificate.
- **Colori/stile**: replicati dalle foto dello schermo del sito reale fornite dall'utente (logo nero con accenti rossi, sfondo bianco, foto scure a tutta larghezza, titoli in serif corsivo).

## Cosa completare prima della pubblicazione

Instagram, Facebook, TripAdvisor e il sito lascottoneria.it non erano raggiungibili da questo ambiente di lavoro (rete bloccata), quindi:

1. **Foto** — al posto delle immagini reali ci sono dei riquadri stilizzati scuri (icona + etichetta), pensati per essere sostituiti 1:1 con le foto vere. Aggiorna i placeholder `.photo-placeholder` in `index.html` con le foto migliori da Instagram [@la_scottoneria_ristorante](https://www.instagram.com/la_scottoneria_ristorante/) e dalla pagina Facebook: hero (tagliata alla brace), sala, tagliolini al tartufo, tartare, galleria.
2. **Recensioni** — le testimonianze in home sono riformulate a partire dai commenti pubblici trovati su Tripadvisor/Google; sostituiscile pure con recensioni vere (con il permesso dei clienti) quando disponibili.
3. **Verifica prezzi/orari** — il menù caricato è quello più recente disponibile: controlla che non ne esista una versione più aggiornata prima di pubblicare online.

## Funzionalità incluse

- Hero a tutta larghezza con foto scura, particelle "brace" animate e overlay con il nome del locale.
- Effetto tilt 3D al passaggio del mouse su tutte le card (menu, galleria, recensioni, feature, vini).
- Badge circolare con testo curvo animato (stile "dove la carne è l'anima del piacere" del menù originale).
- Menu digitale a tab con 8 categorie reali (Antipasti, Primi, Secondi, Contorni, Bruschettine, Insalatone, Dolci, Bevande) e download del PDF ufficiale.
- Sezione Carta dei Vini con Bollicine/Bianchi/Rossi e download del PDF ufficiale.
- Galleria con hover e caption in overlay.
- Carosello recensioni con autoplay, dot e freccette.
- Form di prenotazione che compone automaticamente un'email con i dettagli inseriti (nome, telefono, data, ora, persone).
- Mappa Google integrata, click-to-call, link diretti a Instagram/Facebook/Tripadvisor.
- Design responsive (da mobile a desktop), rispetto di `prefers-reduced-motion` per l'accessibilità.

## Anteprima locale

Basta aprire `index.html` in un browser, oppure servire la cartella con un piccolo server statico, ad esempio:

```bash
python3 -m http.server 8080
```

e visitare `http://localhost:8080`.
