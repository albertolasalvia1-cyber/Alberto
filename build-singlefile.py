#!/usr/bin/env python3
"""Costruisce dist/index.html: un unico file con CSS, JS e foto incorporati.

Serve per caricare il sito su hosting drag-and-drop (es. Netlify Drop) trascinando
un solo file. La versione multi-file in cartella resta quella di riferimento.

Uso:  python3 build-singlefile.py
"""
import base64
import mimetypes
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


MAX_WIDTH = {"hero-salone.jpg": 1400}
DEFAULT_MAX_WIDTH = 1000
JPEG_QUALITY = 78


def image_bytes(path):
    """Ridimensiona e ricomprime la foto per tenere il file finale leggero.
    Senza Pillow usa il file originale."""
    full = os.path.join(ROOT, path)
    raw = open(full, "rb").read()
    try:
        from PIL import Image
    except ImportError:
        return raw
    import io
    im = Image.open(io.BytesIO(raw)).convert("RGB")
    cap = MAX_WIDTH.get(os.path.basename(path), DEFAULT_MAX_WIDTH)
    if im.width > cap:
        im = im.resize((cap, round(im.height * cap / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
    return buf.getvalue() if buf.tell() < len(raw) else raw


def data_uri(path):
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    blob = image_bytes(path) if mime.startswith("image/") else open(os.path.join(ROOT, path), "rb").read()
    return f"data:{mime};base64," + base64.b64encode(blob).decode("ascii")


def main():
    html = read("index.html")
    css = read("css/style.css")
    js = read("js/main.js")

    # foto: da url('../assets/img/x.jpg') a data URI
    def css_img(match):
        rel = match.group(1).replace("../", "")
        full = os.path.join(ROOT, rel)
        if not os.path.exists(full):
            print(f"  ! manca {rel}, lascio il riferimento originale")
            return match.group(0)
        print(f"  + {rel}")
        return f"url('{data_uri(rel)}')"

    css = re.sub(r"url\('(\.\./assets/img/[^']+)'\)", css_img, css)

    # foto referenziate direttamente nell'HTML (style="background-image:url('assets/img/x.jpg')")
    def html_img(match):
        rel = match.group(1)
        full = os.path.join(ROOT, rel)
        if not os.path.exists(full):
            print(f"  ! manca {rel}, lascio il riferimento originale")
            return match.group(0)
        print(f"  + {rel}")
        return f"url('{data_uri(rel)}')"

    html = re.sub(r"url\('(assets/img/[^']+)'\)", html_img, html)

    html = html.replace(
        '<link rel="stylesheet" href="css/style.css">',
        "<style>\n" + css + "\n</style>")
    html = html.replace(
        '<script src="js/main.js"></script>',
        "<script>\n" + js + "\n</script>")

    os.makedirs(DIST, exist_ok=True)
    out = os.path.join(DIST, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)

    size = os.path.getsize(out)
    print(f"\ndist/index.html creato — {size/1024/1024:.2f} MB")

    # i commenti non contano: si controllano solo i riferimenti veri
    checked = re.sub(r"/\*.*?\*/", "", html, flags=re.S)
    leftovers = [p for p in ('href="css/', 'src="js/', 'href="assets/',
                             'src="assets/', "url('../assets", 'url("../assets')
                 if p in checked]
    if leftovers:
        print("  ATTENZIONE: riferimenti esterni rimasti ->", ", ".join(leftovers))
        return 1
    print("Nessun riferimento a file esterni: il file funziona da solo.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
