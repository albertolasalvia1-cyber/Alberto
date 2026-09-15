# La Scottoneria — Sito Web

Sito vetrina per il ristorante **La Scottoneria** (Via Battaglia 145, Albignasego – Padova), pensato per invogliare i visitatori a prenotare un tavolo. Nessun framework/build: HTML + CSS + JS puri, pronto per essere pubblicato su qualsiasi hosting statico (GitHub Pages, Netlify, hosting tradizionale...).

## Struttura

```
index.html        pagina unica con tutte le sezioni
css/style.css      stile, animazioni, effetti 3D
js/main.js         interattività (menu a tab, carosello recensioni, form, particelle, tilt 3D)
assets/img/        cartella per le foto reali del locale
```

## Cosa completare prima della pubblicazione

I link a Instagram, Facebook, TripAdvisor e al sito attuale non erano raggiungibili da questo ambiente di lavoro (rete bloccata), quindi:

1. **Foto** — al posto delle immagini reali ci sono dei riquadri stilizzati (icona + etichetta). Sostituiscili con foto vere in `assets/img/` e aggiorna i tag `<img>`/placeholder in `index.html`:
   - Hero/sfondo, sala, piatti alla brace, antipasti, dettaglio carni, calice di vino → prendi gli scatti migliori dal profilo Instagram [@la_scottoneria_ristorante](https://www.instagram.com/la_scottoneria_ristorante/) e dalla pagina Facebook.
2. **Prezzi del menù** — i piatti nella sezione "Menù Digitale" sono quelli realmente proposti dal locale (bombetta, picanha, filetto, costata, fiorentina, tagliatelle al ragù, orecchiette al cappello del prete, carpaccio di scottona...), ma i **prezzi sono indicativi/segnaposto**: aggiornali con quelli reali della carta ufficiale.
3. **Menù PDF** — il bottone "Scarica il Menù in PDF" punta a `assets/menu-la-scottoneria.pdf`: carica lì il PDF ufficiale del menù.
4. **Dati di contatto** — telefono (049 573 5845), email (info@lascottoneria.it), indirizzo e orari sono presi da fonti pubbliche: verificali e correggili se necessario.
5. **Recensioni** — le testimonianze in home sono riformulate a partire dai commenti pubblici trovati su Tripadvisor/Google; sostituiscile pure con recensioni vere (con il permesso dei clienti) quando disponibili.

## Funzionalità incluse

- Hero animato con particelle "brace" e testo con effetto 3D al passaggio del mouse.
- Effetto tilt 3D su tutte le card (menu, galleria, recensioni, feature).
- Menu digitale a tab (Antipasti, Primi, Carne alla Brace, Contorni, Dolci, Vini) con animazioni di transizione.
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
