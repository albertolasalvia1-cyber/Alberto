# video/ — video del sito (facoltativi)

Stessi nomi delle foto, in `.mp4` (consigliato), `.webm` o `.mov`. Se c'è il video prende il posto della foto:
parte da solo, muto e in loop, solo quando è visibile. Non viene caricato con "riduci movimento" o risparmio dati.

- `hero.mp4` — prima schermata della home
- `serena.mp4` — sezione Serena
- `reel-<titolo>.mp4` — anteprima animata nella griglia dei video (es. `reel-canocchie-preparazione.mp4`)

Consiglio: MP4 H.264 senza audio, 8–15 s, 720p, 2–5 MB. I `.mov` dell'iPhone conviene convertirli:
`ffmpeg -i input.mov -an -vcodec libx264 -crf 26 -vf scale=-2:1280 -movflags +faststart hero.mp4`
