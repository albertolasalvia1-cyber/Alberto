# Hair Room 74 — Sito Web

Sito vetrina per il salone **Hair Room 74** (Via F. G. D'Acquapendente 74, Padova),
il salone di Stefano Borella per uomo e donna. HTML + CSS + JS puri, nessun
framework e nessuna dipendenza esterna (a parte i Google Fonts): si pubblica
su qualsiasi hosting statico — GitHub Pages, Netlify, Aruba, hosting tradizionale.

Stile: nero / crema / rame, elegante e leggero, con effetti 3D e animazioni
pensati per non appesantire la navigazione.

## Struttura

```
index.html                pagina unica con tutte le sezioni + icone SVG integrate
css/style.css              stile, animazioni, effetti 3D
js/main.js                 menu, tab servizi, carosello recensioni, filtri gallery,
                            tilt 3D, contatori animati, flip card fidelity, form
assets/img/                ← qui vanno le foto reali del salone (vedi sotto)
```

## Foto

Le foto in `assets/img/` sono quelle reali del salone, fornite direttamente
dal titolare. Il sito le riprende in automatico in base al nome del file,
senza bisogno di toccare il codice:

| File in `assets/img/` | Dove appare |
| --- | --- |
| `hero-salone.jpg` | sfondo (con parallasse 3D) della prima schermata |
| `salone-1.jpg` / `salone-2.jpg` | sezione "Chi siamo" (team al lavoro, dettaglio) |
| `gallery-1.jpg` … `gallery-8.jpg` | griglia della gallery (taglio donna, uomo, colore, salone) |

Per sostituire una foto basta salvarne una nuova con lo stesso nome esatto.
Formato consigliato: JPG, lato lungo ~1600 px. Se un file dovesse mancare,
al suo posto resta uno sfondo scuro/rame elegante: il sito non risulta mai "rotto".

## Dati usati (fonti pubbliche)

- **Contatti**: Via F. G. D'Acquapendente 74, 35126 Padova · 049 680603 · roomh74@gmail.com.
- **Titolare**: Stefano Borella.
- **Listino prezzi**: tutte le 7 categorie e i relativi prezzi (Taglio,
  Acconciature, Colorazioni, Cura del Capello, Effetti Luce, Trattamento
  Forma, Depilazione) sono presi dal listino reale del sito ufficiale
  hairroom74.it, incluse le descrizioni di ogni trattamento.
- **Promozioni**: Gift Card (tagli da €35/€50/€90/€150 o importo
  personalizzato), VIP Card (bonus 10%), VIP Client, Porta un Amico
  (sconto 50% per entrambi) — riprese dalla sezione "Promozioni" del sito ufficiale.
- **Blog**: i tre articoli in home rimandano al blog reale (hairroom74.it/blog-hair-room-74).
- **Prenotazioni**: tramite Treatwell (collegamento diretto in tutto il sito).
- **Social**: Instagram @hair_room74, Facebook Hair Room 74.
- **Valutazioni**: ~4.6/5 con oltre 130 recensioni Google (dati pubblici).
- **Orari**: indicativi da fonti pubbliche; verificare sempre con il salone,
  come indicato anche nel sito stesso.
- La citazione in home ("La bellezza salverà il mondo" — Dostoevskij) è la stessa
  presente sul sito ufficiale.

## Funzionalità

- Hero a tutta pagina con foto reale del salone, parallasse 3D che segue il
  mouse, zoom cinematico lento, fili "capelli" animati in SVG, particelle
  fluttuanti, entrata dei testi con effetto 3D e pulsanti di prenotazione/chiamata.
- Preloader con forbici che ruotano in 3D all'apertura del sito.
- Header sticky che si compatta allo scroll, menu mobile a comparsa.
- Sezione "Chi Siamo" con foto reali del team a tilt 3D e badge circolare con testo rotante.
- Servizi divisi in tab (Donna · Uomo & Barba · Colore & Trattamenti · Styling & Extension).
- Sezione **Fidelity Card** con card 3D che si gira al click/tap.
- Gallery con filtri per categoria e card a tilt 3D.
- Carosello recensioni con contatori animati (rating, numero recensioni).
- Banner di richiamo alla prenotazione, mappa Google integrata, form contatti
  che compone in automatico l'email con i dati inseriti.
- Pulsanti flottanti "Chiama" e "Prenota", pulsante torna-su.
- Icone SVG integrate: nessuna libreria esterna, caricamento immediato anche offline.
- Responsive da mobile a desktop e supporto `prefers-reduced-motion`.

## Versione in un unico file (hosting drag-and-drop)

Per pubblicare il sito trascinando un solo file (es. Netlify Drop):

```bash
python3 build-singlefile.py
```

Genera `dist/index.html` con CSS, JavaScript e foto incorporati: non dipende
da nessun'altra cartella. È la versione da usare se il pannello dell'hosting
accetta un singolo file; per un deploy normale (GitHub, FTP, Netlify da repo)
usa la versione in cartella, che è più leggera da caricare.

## Anteprima locale

```bash
python3 -m http.server 8080
```

poi apri `http://localhost:8080`.
