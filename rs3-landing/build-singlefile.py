"""Crea dist/rs3-landing.html: tutta la landing in un unico file (CSS, JS, font, foto e video incorporati).
Utile per l'anteprima o per caricarla su hosting che accettano un solo file.
Uso: python3 build-singlefile.py
"""
import base64, mimetypes, pathlib, re

ROOT = pathlib.Path(__file__).parent
MIME = {".ttf": "font/ttf", ".mp4": "video/mp4", ".jpg": "image/jpeg", ".png": "image/png"}


def data_uri(path):
    p = (ROOT / path).resolve()
    mime = MIME.get(p.suffix) or mimetypes.guess_type(p.name)[0]
    return f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}"


html = (ROOT / "index.html").read_text()
css = (ROOT / "css/style.css").read_text()
css = re.sub(r"url\(\.\./(assets/[^)]+)\)", lambda m: f"url({data_uri(m.group(1))})", css)
js = (ROOT / "js/main.js").read_text()

html = html.replace('<link rel="stylesheet" href="css/style.css">', f"<style>{css}</style>")
html = html.replace('<script src="js/main.js"></script>', f"<script>{js}</script>")
html = re.sub(r'(src|poster|href)="(assets/[^"]+)"', lambda m: f'{m.group(1)}="{data_uri(m.group(2))}"', html)
html = re.sub(r"url\((assets/[^)]+)\)", lambda m: f"url({data_uri(m.group(1))})", html)
html = re.sub(r'<meta property="og:image"[^>]*>\n', "", html)

out = ROOT / "dist/rs3-landing.html"
out.parent.mkdir(exist_ok=True)
out.write_text(html)
print(f"{out} · {out.stat().st_size / 1e6:.1f} MB")
