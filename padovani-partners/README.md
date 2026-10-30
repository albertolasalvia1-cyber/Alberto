# Padovani & Partners — Sito Web

Nuova versione di padovaniepartners.it: stessi contenuti e stesse pagine del sito originale, con
un'impostazione istituzionale (bianco e verde scuro del marchio, filetti sottili).
Caratteri: Source Serif 4 per i titoli, Source Sans 3 per il testo (Google Fonts).

## Animazioni

Tutte in `js/main.js`, senza librerie esterne:

- **Globo 3D** (canvas) nella testata: sfera di punti con un nodo centrale collegato alle società da archi
  percorsi da un impulso; oscilla lentamente e si inclina seguendo il mouse. Si ferma quando non è visibile.
- **Titoli** che entrano parola per parola, **testo di presentazione** che si accende scorrendo.
- **Header** trasparente sopra la testata, bianco allo scorrimento, nascosto scendendo e di nuovo visibile risalendo;
  barra di avanzamento della lettura in alto.
- **Card delle società** con inclinazione 3D e riflesso che seguono il mouse.
- **Contatori** dei dati, **linea del metodo** che avanza con lo scorrimento, comparsa morbida delle sezioni,
  dissolvenza tra una pagina e l'altra.

Con l'impostazione di sistema "riduci movimento" il sito resta completamente statico.
HTML + CSS + JS puri, nessuna dipendenza (a parte i Google Fonts): si pubblica su qualsiasi hosting statico.

## Pagine e collegamenti

| Pagina | Contenuto |
| --- | --- |
| `index.html` | Home: testata con globo, chi siamo, dati, società e partner, metodo, contatti |
| `unipol.html` | UnipolSai Assicurazioni |
| `axa.html` | AXA Assicurazioni – Pegaso SRL (referente, telefono, form) |
| `unibrokers.html` | Unibrokers S.r.l. (referenti, telefono, RUI, form) |
| `car-adviser.html` | Car Adviser SRL – noleggio a lungo termine |
| `librici.html` | Antonino Librici & Partners – risk management |
| `contatti.html` | Form di contatto generale (i pulsanti "Contattaci" della home portano qui) |

Ogni pagina ha il menu in alto con il pannello "Società e partner" (si apre al passaggio del mouse o al clic;
su mobile il menu è a schermo intero con la voce che si espande), il logo che riporta alla home, il percorso
(Home / Società e partner / ...), il footer con tutti i collegamenti, i rimandi alle altre società e il
pulsante "torna su". Nelle pagine delle società una scheda laterale riporta referenti, RUI e telefono.
I numeri di telefono sono cliccabili (`tel:`).

## Testi da completare

Il video non mostrava l'interno delle pagine **Unipol**, **Car Adviser** e **Antonino Librici**:
lì ci sono testi provvisori coerenti con il resto del sito, da sostituire con quelli definitivi
(e con i recapiti dei referenti, se presenti sul sito originale).

## Modificare il sito

Le pagine sono generate da `genera.py` (header, menu, card, form e footer sono scritti una volta sola):
modifica i testi lì e rilancia

```
python3 genera.py
```

Lo stile è in `css/style.css` (colori in cima al file), il comportamento in `js/main.js`.

## Immagini

Il logo Padovani & Partners è composto in HTML/CSS (monogramma PP e nome), `img/favicon.svg` è l'icona del browser.
I loghi delle società in `img/` sono ritagliati dalla registrazione dello schermo, quindi a bassa risoluzione.
Ognuno esiste in due versioni: `logo-*.png` bianco (per i fondi scuri) e `logo-*-dark.png` scuro (per i fondi chiari).
Conviene sostituirli con i file originali in PNG trasparente o SVG, mantenendo gli stessi nomi.

## Form di contatto

I form usano **Netlify Forms** (attributo `data-netlify`): pubblicando la cartella su Netlify le richieste
arrivano nella dashboard di Netlify, da cui si può attivare l'inoltro via email.
La domanda antispam ("La capitale della Francia?") accetta "Parigi" e viene controllata nel browser.
Su altri hosting bisogna collegare il form a un servizio di invio (es. Formspree) cambiando `fetch('/')` in `js/main.js`.
