# Landing page Audi RS3 · AT Luxury Car Rental

Una pagina unica per vendere il noleggio dell'RS3. Tutti i pulsanti aprono WhatsApp (**+39 351 982 2171**) con un messaggio già scritto, così il cliente deve solo premere "invia".
Il sito è fatto con HTML, CSS e JS puri. L'unica libreria è three.js per il badge 3D, già inclusa in `js/vendor/`.
Le sezioni scure (apertura, badge, prezzi, regalo) si alternano a quelle bianche (galleria, come funziona, preventivo, zone, FAQ).
Le anteprime della pagina, desktop e telefono, sono in `anteprime/`.

## Sezioni
1. **Hero**: video dell'RS3 in un pannello 3D che segue il mouse, linee di velocità animate e prezzo "da 280€ al giorno"
2. **Badge RS 3 in 3D**: lettere cromate e blocco rosso in vero 3D (three.js). Entra ruotando, segue mouse e dito e gira con lo scroll. Sotto c'è la targhetta "AT Luxury Car Rental presenta"
2. **Contagiri**: la lancetta sale con lo scroll fino al limitatore. Accanto, i numeri (400 CV, 500 Nm, 3,8 s, 290 km/h) che si animano
3. **Galleria 3D**: un anello di foto che gira da solo e si può trascinare
4. **Come funziona**: 3 passi, con card in 3D
5. **Prezzi**: schede Settimana / Weekend / Lunghe durate, ogni pacchetto con il suo pulsante WhatsApp, più il box del trucco dei km (1,50€ contro 3€)
6. **Calcolatore preventivo**: formula + km previsti → totale, che si invia su WhatsApp con un tocco
7. **Idea regalo**
8. **Zone** (Padova, Venezia, Treviso) con il percorso del weekend disegnato
9. **FAQ**, **invito finale** e **footer**
10. Su mobile: pulsante WhatsApp fisso in basso

## Pubblicarla online (gratis, in 1 minuto)
- **Netlify Drop**: vai su https://app.netlify.com/drop e trascina la cartella `rs3-landing`. Ti dà subito un link, e poi puoi collegare un dominio (es. `atluxurycarental.it`).
- **Un solo file**: `dist/rs3-landing.html` contiene tutto (5 MB). Va bene per un'anteprima o per hosting che accettano un file singolo. Per rigenerarlo: `python3 build-singlefile.py`.

## Modificare
- **Numero WhatsApp**: in `js/main.js`, riga `WA_NUMBER`
- **Prezzi**: nella sezione `PRICING` di `index.html` e nelle `<option>` del calcolatore (formato `prezzo|km inclusi|al giorno?|nome`)
- **Foto**: in `assets/img/`. Sostituendo un file con lo stesso nome, la pagina lo usa senza toccare il codice

## Dopo la pubblicazione
- Mettete il link in bio su Instagram e come destinazione degli annunci Meta
- Installate il **Pixel di Meta** (va incollato nel `<head>`) per misurare i clic su WhatsApp e fare retargeting
