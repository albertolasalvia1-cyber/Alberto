# Padovani & Partners — Sito Web

Nuova versione di padovaniepartners.it: stessi contenuti e stesse pagine del sito originale, con un design
rifatto da zero (verde foresta e avorio con accenti ottone, titoli serif Fraunces, testo Inter).
HTML + CSS + JS puri, nessuna dipendenza (a parte i Google Fonts): si pubblica su qualsiasi hosting statico.

## Pagine e collegamenti

| Pagina | Contenuto |
| --- | --- |
| `index.html` | Home: presentazione, i 4 punti di forza, card dei partner, invito al contatto |
| `unipol.html` | UnipolSai Assicurazioni |
| `axa.html` | AXA Assicurazioni – Pegaso SRL (referente, telefono, form) |
| `unibrokers.html` | Unibrokers S.r.l. (referenti, telefono, RUI, form) |
| `car-adviser.html` | Car Adviser SRL – noleggio a lungo termine |
| `librici.html` | Antonino Librici & Partners – risk management |
| `contatti.html` | Form di contatto generale (i pulsanti "Contattaci" della home portano qui) |

Ogni pagina ha il menu in alto con tendina "Soluzioni" (menu a schermo intero su mobile), il logo che riporta
alla home, il percorso (Home / Soluzioni / ...), il footer con tutti i collegamenti, le card verso le altre
pagine partner e il pulsante "torna su". Nelle pagine partner una scheda laterale riporta referenti e telefono.
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

Il logo Padovani & Partners è ridisegnato in HTML/CSS (monogramma PP), `img/favicon.svg` è l'icona del browser.
Loghi dei partner e foto in `img/` sono ritagliati dalla registrazione dello schermo, quindi a bassa risoluzione:
conviene sostituirli con i file originali (loghi bianchi su fondo trasparente, PNG o SVG) mantenendo gli stessi nomi.

## Form di contatto

I form usano **Netlify Forms** (attributo `data-netlify`): pubblicando la cartella su Netlify le richieste
arrivano nella dashboard di Netlify, da cui si può attivare l'inoltro via email.
La domanda antispam ("La capitale della Francia?") accetta "Parigi" e viene controllata nel browser.
Su altri hosting bisogna collegare il form a un servizio di invio (es. Formspree) cambiando `fetch('/')` in `js/main.js`.
