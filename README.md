# La Scottoneria — Sito Web

Sito vetrina per il ristorante **La Scottoneria** (Via Strada Battaglia 145, Albignasego – Padova).
HTML + CSS + JS puri, nessun framework e nessuna dipendenza esterna (a parte i Google Fonts):
si pubblica su qualsiasi hosting statico — GitHub Pages, Netlify, Aruba, hosting tradizionale.

Stile: bianco / nero / rosso, coerente con l'identità reale del locale (logo, menù e carta vini "rosso e nero").

## Struttura

```
index.html                                   pagina unica con tutte le sezioni + icone SVG integrate
css/style.css                                stile, animazioni, effetti 3D
js/main.js                                   menu a tab, carosello recensioni, form, particelle, tilt 3D
assets/img/                                  ← qui vanno le foto del ristorante (vedi sotto)
assets/menu/menu-la-scottoneria.pdf          menù ufficiale scaricabile dal sito
assets/menu/carta-vini-la-scottoneria.pdf    carta dei vini ufficiale scaricabile dal sito
```

## Come inserire le foto vere (l'unica cosa che manca)

Il sito è **già collegato** ai file qui sotto: basta salvare le immagini in `assets/img/`
con esattamente questi nomi e compaiono da sole al posto degli sfondi stilizzati.
Non serve toccare il codice.

| File da salvare in `assets/img/` | Dove appare |
| --- | --- |
| `hero.jpg` | sfondo grande della prima schermata (consigliata: tagliata o fiorentina su ardesia) |
| `chi-siamo-1.jpg` | sezione "Chi siamo" – piatto di pasta fresca |
| `chi-siamo-2.jpg` | sezione "Chi siamo" – tartare |
| `specialita.jpg` | tondo animato accanto a "le nostre specialità" |
| `galleria-1.jpg` … `galleria-6.jpg` | griglia della galleria |

Formato consigliato: JPG, lato lungo ~1600 px, foto scure/con fondo nero rendono meglio.
Finché i file non ci sono, il sito mostra sfondi eleganti e non risulta mai "rotto".

## Dati usati (fonti reali)

- **Menù e prezzi**: dal PDF ufficiale `MENU-scottoneria-2026-x-sito.pdf` — piatti, prezzi e allergeni reali.
- **Carta dei vini**: dal PDF ufficiale — bollicine, bianchi e rossi con prezzi bottiglia/calice reali.
- **Testo "Chi siamo"**: dal sito ufficiale lascottoneria.it.
- **Contatti**: Via Strada Battaglia 145, 049 573 5845, info@lascottoneria.it.
- **Valutazioni**: 4.9/5 Tripadvisor (#5 su 52 ad Albignasego), 4.7/5 con 237 recensioni Google.
- **Recensioni in home**: riformulate dai commenti pubblici; sostituibili con recensioni reali.

## Funzionalità

- Hero a tutta pagina con claim, particelle "brace" animate, zoom lento e pulsanti di prenotazione.
- Header bianco sticky con il logo in stile originale (accenti rossi + riga rossa).
- Menù digitale a 8 categorie reali con animazioni di transizione e download del PDF.
- Carta dei vini (Bollicine / Bianchi / Rossi) con download del PDF.
- Galleria, carosello recensioni, banner rosso di richiamo alla prenotazione.
- Form di prenotazione che compone in automatico l'email con i dati inseriti.
- Pulsante WhatsApp flottante, click-to-call, card mappa che apre Google Maps.
- Effetto tilt 3D sulle card, animazioni allo scroll, badge circolare con testo curvo rotante.
- Icone SVG integrate: nessuna libreria esterna, caricamento immediato anche offline.
- Responsive da mobile a desktop e supporto `prefers-reduced-motion`.

## Anteprima locale

```bash
python3 -m http.server 8080
```

poi apri `http://localhost:8080`.
