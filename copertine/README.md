# Copertine da foto

Trasforma una foto in una copertina verticale 1080×1920 (Reels / TikTok / Shorts):
ritocco colore, titolo grande in alto (con la seconda riga evidenziata), fascia colorata in basso.

```bash
pip install pillow
python3 crea_copertina.py foto.jpg "CAPESANTE|IN PADELLA" --etichetta "PRONTE IN 10 MINUTI" -o copertina.jpg
```

Opzioni:
- `|` nel titolo = a capo (la seconda riga va nel riquadro colorato)
- `--etichetta` testo nella pillola in basso
- `--firma` testo piccolo in fondo, es. `@nomeprofilo`
- `--colore` blu (default), rosso, nero, verde
- `--altezza-titolo` limite in basso del titolo (default 430 px): abbassalo se copre il viso

Esempio: `esempio-foto.jpg` → `esempio-copertina.jpg`. Font: Anton e Montserrat (licenza OFL, in `font/`).
