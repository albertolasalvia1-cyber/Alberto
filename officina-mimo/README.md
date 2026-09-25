# Officina Mimo — Sito Web + caroselli Instagram

Nuovo sito vetrina per **Officina Mimo S.r.l.**, centro assistenza per veicoli industriali e bus
(Via Andorra 14, 35127 Padova — dal 1969). HTML + CSS + JS puri, font inclusi nella cartella:
nessuna dipendenza esterna, si pubblica così com'è su qualsiasi hosting statico.

Stile: grafite / acciaio / giallo segnaletica, con strisce "hazard" e un camion illustrato in SVG
al posto della foto principale.

## Struttura

```
index.html          pagina unica: hero, numeri, servizi, soccorso 24h, vendita e noleggio, azienda, contatti
css/style.css       stile, animazioni, responsive
js/main.js          menu mobile, animazioni allo scroll, contatore, form che compone la mail
assets/fonts/       Barlow e Barlow Condensed (SIL Open Font License)
assets/img/         ← qui vanno le foto reali (vedi sotto)
social/             caroselli Instagram (PNG pronti + sorgente + caption)
```

## Foto

Il sito funziona anche senza foto: dove mancano compare uno sfondo grafico. Per aggiungerle
basta salvare i file in `assets/img/` con questi nomi:

| File | Dove appare |
| --- | --- |
| `officina.jpg` | foto grande nella sezione "Vendita & noleggio" (es. camion in officina) |
| `noleggio.jpg` | foto piccola sovrapposta (es. semirimorchi o flotta a noleggio) |

Formato consigliato: JPG, lato lungo ~1600 px.

## Dati usati

Da fonti pubbliche (sito officinamimo.com, schede Pagine Gialle / TopTruck / Yelp):
- Fondata nel 1969 a Padova, specialisti Volvo Trucks, multimarca veicoli industriali e bus.
- Servizi: manutenzione e diagnosi, revisioni mezzi oltre 3,5 t, tachigrafi analogici e digitali,
  ricambi originali nuovi e ricondizionati, pneumatici, cristalli, collaudi, nazionalizzazioni, rinnovi ATP,
  vendita e noleggio camion e semirimorchi, soccorso stradale 24 ore partner ACI Global, rete TopTruck.
- Contatti: +39 049 870 2342, info@officinamimo.com.
- Orari: Lun–Ven 8–12 / 14–18, Sab 8–12, Dom chiuso.

**Da verificare con l'officina prima di pubblicare:** se il soccorso 24/7 ha un numero diverso da
quello dell'officina (in quel caso va sostituito in tutti i `tel:` del sito e nelle slide 4 e 5 del
carosello "Soccorso stradale" e 6 del carosello "Tachigrafo").

## Caroselli Instagram

Tre caroselli 1080×1350 già esportati in PNG, con caption e hashtag in `social/CAPTION.md`:

1. `social/01-soccorso-stradale/` — "Camion in panne? Cosa fare in 4 mosse" (5 slide)
2. `social/02-tachigrafo/` — "Tachigrafo: 4 scadenze da non dimenticare" (6 slide)
3. `social/03-full-service/` — "Oltre 55 anni di camion": storia, servizi, noleggio, contatti (5 slide)

Per cambiare un testo: modifica `social/carousels.html` (aperto nel browser mostra tutte le slide)
e rigenera le immagini con:

```bash
node social/render.js
```

## Anteprima locale

```bash
cd officina-mimo && python3 -m http.server 8080
```

poi apri `http://localhost:8080`.
