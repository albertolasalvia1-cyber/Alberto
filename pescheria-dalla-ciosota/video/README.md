# video/ — video del sito

Stessi nomi delle foto in `img/`, con estensione `.mp4` (consigliato), `.webm` o `.mov`.
Il video, se presente, ha la precedenza sulla foto; parte da solo, muto e in loop, solo quando è visibile.
Con "riduci movimento" attivo o in modalità risparmio dati i video non vengono caricati e si usa la foto
(o il segnaposto).

| File | Dove appare |
| --- | --- |
| `hero.mp4` | sfondo a tutto schermo della home (senza video resta il gradiente blu navy) |
| `pesce-intero.mp4` `molluschi-crostacei.mp4` `crudo-di-pesce.mp4` `pesce-di-stagione.mp4` | reel nella sezione "Il pescato" |
| `serena.mp4` `serena-ritratto.mp4` `bancone.mp4` | home e pagina Chi siamo |
| `galleria-1.mp4` … `galleria-8.mp4` | galleria della pagina Chi siamo |
| `<prodotto>.mp4` | schede della pagina Prodotti (es. `canocchie.mp4`) |

Consigli per non appesantire il sito:
- H.264 in MP4, senza audio, 8–15 secondi, max ~720p per i reel e 1080p per l'hero, 2–5 MB ciascuno.
- I `.mov` dell'iPhone funzionano bene su Safari ma non sempre su Chrome/Android: meglio convertirli in MP4,
  ad esempio: `ffmpeg -i input.mov -an -vcodec libx264 -crf 26 -preset slow -vf scale=-2:1080 -movflags +faststart hero.mp4`
