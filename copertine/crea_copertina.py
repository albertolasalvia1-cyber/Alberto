#!/usr/bin/env python3
"""Crea una copertina verticale 9:16 (Reels / TikTok / Shorts) partendo da una foto.

Uso:
    python3 crea_copertina.py foto.jpg "CAPESANTE IN PADELLA" -o copertina.jpg
    python3 crea_copertina.py foto.jpg "CAPESANTE|IN PADELLA" --etichetta "RICETTA FACILE" --firma "@profilo"

Nel titolo il carattere "|" forza l'a capo; dalla seconda riga in poi il testo viene
evidenziato con il colore d'accento. L'etichetta va nella fascia colorata in basso. Richiede Pillow (pip install pillow).
"""
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

W, H = 1080, 1920
FONT_DIR = Path(__file__).parent / "font"
FONT_TITOLO = FONT_DIR / "Anton.ttf"
FONT_TESTO = FONT_DIR / "Montserrat.ttf"

# colore fascia in basso, colore evidenziatore del titolo
PALETTE = {
    "blu": ((6, 72, 150), (255, 204, 0)),
    "rosso": ((150, 16, 22), (255, 255, 255)),
    "nero": ((10, 10, 10), (230, 30, 40)),
    "verde": ((16, 96, 60), (255, 214, 64)),
}


def ritaglia_9_16(img):
    """Ritaglio centrato al formato 9:16, poi ridimensiona a 1080x1920."""
    w, h = img.size
    if w / h > W / H:
        nw = round(h * W / H)
        img = img.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = round(w * H / W)
        img = img.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    return img.resize((W, H), Image.LANCZOS)


def migliora(img):
    """Ritocco leggero: contrasto, colore e nitidezza."""
    img = ImageEnhance.Contrast(img).enhance(1.08)
    img = ImageEnhance.Color(img).enhance(1.15)
    img = ImageEnhance.Brightness(img).enhance(1.03)
    return img.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=3))


def sfumatura(colore, altezza, dal_basso, opacita_max):
    """Livello RGBA con sfumatura verticale (easing quadratico)."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for i in range(altezza):
        t = i / altezza
        a = int(opacita_max * min(1.0, t * t * 1.6))
        y = H - altezza + i if dal_basso else altezza - 1 - i
        d.line([(0, y), (W, y)], fill=colore + (a,))
    return layer


def font_montserrat(size, peso=800):
    f = ImageFont.truetype(str(FONT_TESTO), size)
    try:
        f.set_variation_by_axes([peso])
    except (OSError, AttributeError):
        pass
    return f


def adatta_font(testo, larghezza_max, size_max):
    size = size_max
    while size > 40:
        f = ImageFont.truetype(str(FONT_TITOLO), size)
        if f.getbbox(testo)[2] <= larghezza_max:
            return f
        size -= 4
    return ImageFont.truetype(str(FONT_TITOLO), size)


def spezza_titolo(titolo):
    if "|" in titolo:
        return [r.strip() for r in titolo.split("|")]
    parole = titolo.split()
    if len(parole) <= 2:
        return [titolo]
    # prima riga = parola principale, seconda = il resto
    return [parole[0], " ".join(parole[1:])]


def testo_con_ombra(base, pos, testo, font, riempimento, ombra=18):
    x, y = pos
    shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).text((x + 6, y + 10), testo, font=font, fill=(0, 0, 0, 170))
    shadow = shadow.filter(ImageFilter.GaussianBlur(ombra))
    base.alpha_composite(shadow)
    ImageDraw.Draw(base).text((x, y), testo, font=font, fill=riempimento)


def disegna_titolo(img, righe, accento, margine, y, scala, disegna=False):
    """Disegna il titolo a partire da y; restituisce la y finale."""
    for i, riga in enumerate(righe):
        evidenziata = i > 0
        size = int((170 if i == 0 else 130) * scala)
        font = adatta_font(riga, W - 2 * margine - (60 if evidenziata else 0), size)
        bb = font.getbbox(riga)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        x = (W - tw) // 2 - bb[0]
        if evidenziata:
            # riga evidenziata: box colorato leggermente ruotato, testo scuro
            pad_x, pad_y = int(28 * scala) + 6, int(20 * scala) + 6
            box = Image.new("RGBA", (tw + 2 * pad_x, th + 2 * pad_y), accento + (255,))
            box = box.rotate(-2, expand=True, resample=Image.BICUBIC)
            if disegna:
                bx = (W - box.width) // 2
                ombra = Image.new("RGBA", img.size, (0, 0, 0, 0))
                ombra.paste((0, 0, 0, 140), (bx + 8, y + 12, bx + box.width + 8, y + box.height + 12))
                img.alpha_composite(ombra.filter(ImageFilter.GaussianBlur(16)))
                img.alpha_composite(box, (bx, y))
                ImageDraw.Draw(img).text((x, y + (box.height - th) // 2 - bb[1]), riga, font=font, fill=(15, 15, 15))
            y += box.height + int(18 * scala)
        else:
            if disegna:
                testo_con_ombra(img, (x, y - bb[1]), riga, font, (255, 255, 255))
            y += th + int(30 * scala)
    return y


def crea(foto, titolo, uscita, etichetta=None, colore="blu", firma=None, altezza_titolo=430):
    fascia, accento = PALETTE[colore]
    img = migliora(ritaglia_9_16(Image.open(foto).convert("RGB"))).convert("RGBA")

    img.alpha_composite(sfumatura((0, 0, 0), 620, dal_basso=False, opacita_max=185))
    img.alpha_composite(sfumatura(fascia, 440, dal_basso=True, opacita_max=255))

    righe = spezza_titolo(titolo.upper())
    margine = 70
    # il titolo sta nella fascia alta (sopra il viso), la dimensione si adatta
    for scala in [x / 100 for x in range(100, 30, -5)]:
        y = disegna_titolo(img.copy(), righe, accento, margine, 80, scala)
        if y <= altezza_titolo:
            break
    disegna_titolo(img, righe, accento, margine, 80, scala, disegna=True)

    if etichetta:
        f = font_montserrat(38)
        tb = f.getbbox(etichetta)
        pw, ph = tb[2] - tb[0] + 64, tb[3] - tb[1] + 36
        px, py = (W - pw) // 2, H - (135 if firma else 90) - ph
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((px, py, px + pw, py + ph), radius=ph // 2, fill=accento + (255,))
        d.text((px + 32 - tb[0], py + 18 - tb[1]), etichetta, font=f, fill=(15, 15, 15))

    if firma:
        f = font_montserrat(32, 600)
        tb = f.getbbox(firma)
        ImageDraw.Draw(img).text(((W - (tb[2] - tb[0])) // 2 - tb[0], H - 95), firma, font=f, fill=(255, 255, 255, 230))

    img.convert("RGB").save(uscita, quality=95)
    return uscita


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("foto")
    p.add_argument("titolo", help='usa "|" per andare a capo')
    p.add_argument("-o", "--uscita", default="copertina.jpg")
    p.add_argument("--etichetta", help="piccola etichetta sopra il titolo, es. RICETTA FACILE")
    p.add_argument("--firma", help="testo in basso, es. @nomeprofilo")
    p.add_argument("--colore", choices=PALETTE, default="blu")
    p.add_argument("--altezza-titolo", type=int, default=430,
                   help="il titolo non scende oltre questa y (px su 1920): alzala o abbassala per non coprire il viso")
    a = p.parse_args()
    print(crea(a.foto, a.titolo, a.uscita, a.etichetta, a.colore, a.firma, a.altezza_titolo))
