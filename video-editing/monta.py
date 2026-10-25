#!/usr/bin/env python3
"""Montaggio automatico nello stile del cliente Pescheria.

Pipeline: taglio silenzi (soglia adattiva) -> 1080x1920 30fps con punch-in alternati
-> titolo animato (box blu) -> sottotitoli karaoke da .srt (box blu sulla parola attiva).

Uso:
  monta.py GREZZO.mp4 --titolo "SCAMPI PULITI" --titolo2 "IN POCHI SECONDI" \
           --srt sottotitoli.srt --out finale.mp4 [--sub-y 0.55] [--no-cut]
L'.srt deve avere i tempi del video GREZZO (come lo esporta CapCut): li rimappo io dopo i tagli.
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
W, H, FPS = 1080, 1920, 30

TITLE_FONT = os.path.join(FONTS, "Montserrat-Bold.ttf")
SUB_FONT = os.path.join(FONTS, "Montserrat-ExtraBold.ttf")
TITLE_BLUE = (3, 61, 193, 255)        # #033DC1 campionato dai riferimenti
HILITE_BLUE = (30, 123, 224, 255)     # box parola attiva
TITLE_DUR = 3.0
TITLE_ANIM = 0.6


def run(cmd, **kw):
    kw.setdefault("text", True)
    return subprocess.run(cmd, check=True, **kw)


def probe(path):
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type",
               "-of", "json", path], capture_output=True).stdout
    j = json.loads(out)
    kinds = {s["codec_type"] for s in j["streams"]}
    return float(j["format"]["duration"]), "audio" in kinds


# ---------------------------------------------------------------- silenzi
def keep_segments(path, dur, min_sil, pad):
    log = run(["ffmpeg", "-hide_banner", "-i", path, "-map", "0:a:0", "-af",
               "loudnorm=print_format=json", "-f", "null", "-"], capture_output=True).stderr
    m = re.search(r'"input_thresh"\s*:\s*"(-?[\d.]+|-inf)"', log)
    thresh = float(m.group(1)) if m and m.group(1) != "-inf" else -50.0
    log = run(["ffmpeg", "-hide_banner", "-i", path, "-map", "0:a:0", "-af",
               f"silencedetect=noise={thresh}dB:d={min_sil}", "-f", "null", "-"],
              capture_output=True).stderr
    vals = [float(v) for v in re.findall(r"silence_(?:start|end): (-?[\d.]+)", log)]
    segs, cur = [], 0.0
    for i in range(0, len(vals), 2):
        s = max(vals[i], 0.0)
        e = vals[i + 1] if i + 1 < len(vals) else dur
        a, b = cur, min(s + pad, dur)
        if b - a > 2 * pad + 0.05:
            segs.append((a, b))
        cur = max(e - pad, 0.0)
    if dur - cur > 2 * pad + 0.05:
        segs.append((cur, dur))
    print(f"Soglia {thresh:.1f} dB, silenzi {len(vals) // 2}, segmenti tenuti {len(segs)}")
    return segs


def time_mapper(segs):
    """Tempo del grezzo -> tempo del montato (None se cade in un taglio)."""
    offs, acc = [], 0.0
    for a, b in segs:
        offs.append(acc)
        acc += b - a

    def f(t, snap_forward):
        for (a, b), o in zip(segs, offs):
            if a <= t <= b:
                return o + t - a
            if t < a:
                return o if snap_forward else None
        return acc if not snap_forward else None
    return f, acc


# ---------------------------------------------------------------- srt
def parse_srt(path):
    txt = open(path, encoding="utf-8-sig").read().replace("\r", "")
    out = []
    for block in re.split(r"\n\s*\n", txt.strip()):
        lines = block.split("\n")
        for k, ln in enumerate(lines):
            m = re.match(r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)", ln)
            if m:
                g = [int(x) for x in m.groups()]
                s = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
                e = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
                text = " ".join(lines[k + 1:]).strip()
                if text:
                    out.append((s, e, text))
                break
    return out


def word_timings(cues, mapper):
    """Divide ogni blocco in parole con durata proporzionale alla lunghezza."""
    blocks = []
    for s, e, text in cues:
        ns, ne = mapper(s, True), mapper(e, False)
        if ne is None:
            ne = mapper(e, True)
        if ns is None or ne is None or ne - ns < 0.1:
            continue
        words = text.upper().split()
        weights = [len(w) + 1 for w in words]
        tot, t, wt = sum(weights), ns, []
        for w, k in zip(words, weights):
            d = (ne - ns) * k / tot
            wt.append((w, t, t + d))
            t += d
        # max 2 righe per schermata: se il blocco è più lungo lo spezzo
        font = ImageFont.truetype(SUB_FONT, SUB_SIZE)
        cur = []
        for item in wt:
            if cur and len(wrap([w for w, _, _ in cur + [item]], font)) > 2:
                blocks.append((cur[0][1], cur[-1][2], cur))
                cur = []
            cur.append(item)
        if cur:
            blocks.append((cur[0][1], cur[-1][2], cur))
    return blocks


# ---------------------------------------------------------------- trascrizione
MODEL_DIR = os.path.join(HERE, "wmodel", "small")


def transcribe(path):
    """Whisper locale: lista di parole [{"w","s","e"}] coi tempi del grezzo."""
    import numpy as np
    from faster_whisper import WhisperModel
    raw = run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
              capture_output=True, text=False).stdout
    model = WhisperModel(MODEL_DIR, device="cpu", compute_type="int8", cpu_threads=os.cpu_count())
    segs, _ = model.transcribe(np.frombuffer(raw, np.float32), language="it", word_timestamps=True)
    return [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3)}
            for s in segs for w in s.words if w.word.strip()]


def words_to_blocks(words, mapper):
    """Raggruppa le parole in schermate (max 2 righe, si spezza su punteggiatura e pause)."""
    font = ImageFont.truetype(SUB_FONT, SUB_SIZE)
    items = []
    for d in words:
        s, e = mapper(d["s"], True), mapper(d["e"], False)
        if e is None:
            e = mapper(d["e"], True)
        if s is None or e is None or e - s <= 0:
            continue
        txt = re.sub(r"[^\w'’?!À-ÿ%€]", "", d["w"].upper())
        if txt:
            items.append([txt, s, e, bool(re.search(r"[.?!,;:]$", d["w"]))])
    blocks, cur = [], []
    for i, it in enumerate(items):
        if cur:
            prev = cur[-1]
            too_long = len(wrap([w for w, *_ in cur] + [it[0]], font)) > 2 or len(cur) >= 7
            if too_long or prev[3] or it[1] - prev[2] > 0.4:
                blocks.append(cur)
                cur = []
        cur.append(it)
    if cur:
        blocks.append(cur)
    out = []
    for bi, b in enumerate(blocks):
        # la parola resta evidenziata fino all'inizio della successiva
        for k in range(len(b) - 1):
            b[k][2] = b[k + 1][1]
        end = b[-1][2]
        if bi + 1 < len(blocks) and blocks[bi + 1][0][1] - end < 0.3:
            end = blocks[bi + 1][0][1]
        b[-1][2] = end
        out.append((b[0][1], end, [(w, s, e) for w, s, e, _ in b]))
    return out


# ---------------------------------------------------------------- grafica
def text_w(font, s, track):
    return sum(font.getlength(c) for c in s) + track * max(len(s) - 1, 0)


def draw_tracked(draw, xy, s, font, fill, track):
    x, y = xy
    for c in s:
        draw.text((x, y), c, font=font, fill=fill)
        x += font.getlength(c) + track


def shadowed(base_draw_fn, blur=4, offset=(0, 3), alpha=170):
    """Disegna testo con ombra morbida scura sotto."""
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    base_draw_fn(ImageDraw.Draw(sh), (0, 0, 0, alpha), offset)
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    fg = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    base_draw_fn(ImageDraw.Draw(fg), (255, 255, 255, 255), (0, 0))
    return sh, fg


SUB_SIZE, SUB_TRACK, SUB_MAXW = 42, 3, 820


def wrap(words, font):
    lines, cur = [], []
    for w in words:
        if cur and text_w(font, " ".join(cur + [w]), SUB_TRACK) > SUB_MAXW:
            lines.append(cur)
            cur = []
        cur.append(w)
    if cur:
        lines.append(cur)
    return lines


def render_sub(words, active, sub_y):
    font = ImageFont.truetype(SUB_FONT, SUB_SIZE)
    lines = wrap(words, font)
    asc, desc = font.getmetrics()
    lh = int((asc + desc) * 0.92)
    top = int(H * sub_y - lh * len(lines) / 2)
    space = font.getlength(" ") + SUB_TRACK
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    placed, idx = [], 0
    for li, line in enumerate(lines):
        lw = text_w(font, " ".join(line), SUB_TRACK)
        x, y = (W - lw) / 2, top + li * lh
        for w in line:
            ww = text_w(font, w, SUB_TRACK)
            placed.append((idx, w, x, y, ww))
            x += ww + space
            idx += 1
    d = ImageDraw.Draw(img)
    for i, w, x, y, ww in placed:
        if i == active:
            bb = font.getbbox("H")
            d.rounded_rectangle([x - 8, y + bb[1] - 7, x + ww + 8, y + bb[3] + 8],
                                radius=9, fill=HILITE_BLUE)

    def txt(dr, fill, off):
        for i, w, x, y, ww in placed:
            draw_tracked(dr, (x + off[0], y + off[1]), w, font, fill, SUB_TRACK)
    sh, fg = shadowed(txt)
    return Image.alpha_composite(Image.alpha_composite(sh, img), fg)


def title_frame(t, l1, l2):
    """Titolo a 2 righe: riga 1 su box blu entra da sinistra, riga 2 da destra."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if t >= TITLE_DUR:
        return img
    p = min(t / TITLE_ANIM, 1.0)
    ease = 1 - (1 - p) ** 3
    size1 = 112
    f1 = ImageFont.truetype(TITLE_FONT, size1)
    while text_w(f1, l1, 1) > W * 0.84 and size1 > 40:
        size1 -= 2
        f1 = ImageFont.truetype(TITLE_FONT, size1)
    w1 = text_w(f1, l1, 1)
    bb = f1.getbbox("H")
    padx, pady = 26, 22
    boxw, boxh = w1 + 2 * padx, (bb[3] - bb[1]) + 2 * pady
    y1 = int(H * 0.085)
    x_final = (W - boxw) / 2
    x1 = -boxw + (x_final + boxw) * ease
    d = ImageDraw.Draw(img)
    d.rectangle([x1, y1, x1 + boxw, y1 + boxh], fill=TITLE_BLUE)
    draw_tracked(d, (x1 + padx, y1 + pady - bb[1]), l1, f1, (255, 255, 255, 255), 1)
    if l2:
        size2 = int(size1 * 1.12)
        f2 = ImageFont.truetype(TITLE_FONT, size2)
        while text_w(f2, l2, 1) > W * 0.90 and size2 > 40:
            size2 -= 2
            f2 = ImageFont.truetype(TITLE_FONT, size2)
        w2 = text_w(f2, l2, 1)
        b2 = f2.getbbox("H")
        x2f = (W - w2) / 2
        x2 = W + (x2f - W) * ease
        y2 = y1 + boxh + 4 - b2[1]
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))

        def t2(dr, fill, off):
            draw_tracked(dr, (x2 + off[0], y2 + off[1]), l2, f2, fill, 1)
        sh, fg = shadowed(t2, blur=6, offset=(0, 2), alpha=90)
        layer = Image.alpha_composite(sh, fg)
        r, g, b, a = layer.split()
        a = a.point(lambda v: int(v * 0.9))
        layer = Image.merge("RGBA", (r, g, b, a))
        img = Image.alpha_composite(img, layer)
    if t > TITLE_DUR - 0.15:  # uscita rapida
        k = (TITLE_DUR - t) / 0.15
        r, g, b, a = img.split()
        img = Image.merge("RGBA", (r, g, b, a.point(lambda v: int(v * k))))
    return img


def build_overlay(tmp, total, blocks, l1, l2, sub_y):
    """Lista concat di PNG (durate allineate ai frame) per titolo + sottotitoli."""
    nframes = int(round(total * FPS))
    states = {}  # frame -> (block_idx, word_idx)
    for bi, (_, _, wt) in enumerate(blocks):
        for wi, (_, ws, we) in enumerate(wt):
            for f in range(int(round(ws * FPS)), int(round(we * FPS))):
                if 0 <= f < nframes:
                    states[f] = (bi, wi)
    title_frames = int(TITLE_ANIM * FPS) + 1
    fade_from = int((TITLE_DUR - 0.15) * FPS)
    cache, entries = {}, []
    blank = os.path.join(tmp, "blank.png")
    Image.new("RGBA", (W, H), (0, 0, 0, 0)).save(blank)

    def key_for(f):
        tk = None
        if l1 and f < TITLE_DUR * FPS:
            tk = f if (f < title_frames or f >= fade_from) else "still"
        return (tk, states.get(f))

    f = 0
    while f < nframes:
        k = key_for(f)
        g = f + 1
        while g < nframes and key_for(g) == k and not isinstance(k[0], int):
            g += 1
        if k not in cache:
            tk, st = k
            img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            if st is not None:
                words = [w for w, _, _ in blocks[st[0]][2]]
                img = Image.alpha_composite(img, render_sub(words, st[1], sub_y))
            if tk is not None:
                tf = title_frame((tk if isinstance(tk, int) else title_frames) / FPS, l1, l2)
                img = Image.alpha_composite(img, tf)
            if tk is None and st is None:
                cache[k] = blank
            else:
                p = os.path.join(tmp, f"ov{len(cache):05d}.png")
                img.save(p)
                cache[k] = p
        entries.append((cache[k], (g - f) / FPS))
        f = g
    lst = os.path.join(tmp, "overlay.txt")
    with open(lst, "w") as fh:
        for p, d in entries:
            fh.write(f"file '{p}'\nduration {d:.6f}\n")
        fh.write(f"file '{entries[-1][0]}'\n")
    return lst


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--out")
    ap.add_argument("--srt", help="sottotitoli esterni (tempi del grezzo)")
    ap.add_argument("--parole", help="JSON parole [{w,s,e}]: se non esiste lo crea trascrivendo")
    ap.add_argument("--solo-trascrivi", action="store_true", help="crea il JSON delle parole ed esce")
    ap.add_argument("--titolo", default="")
    ap.add_argument("--titolo2", default="")
    ap.add_argument("--sub-y", type=float, default=0.55)
    ap.add_argument("--no-cut", action="store_true")
    ap.add_argument("--min-sil", type=float, default=0.5)
    ap.add_argument("--pad", type=float, default=0.15)
    ap.add_argument("--taglia", default="", help="parti da togliere, es. '24.3-26.9,68.8-73.6'")
    ap.add_argument("--fine", type=float, help="taglia tutto dopo questo secondo (es. schermata CapCut)")
    ap.add_argument("--zoom", type=float, default=1.12, help="punch-in sui jump cut alternati (1 = off)")
    a = ap.parse_args()
    out = a.out or os.path.splitext(a.video)[0] + "_montato.mp4"
    dur, has_audio = probe(a.video)
    if not has_audio:
        sys.exit("Il video non ha audio.")
    if a.solo_trascrivi:
        segs = [(0.0, dur)]
    else:
        segs = [(0.0, dur)] if a.no_cut else keep_segments(a.video, dur, a.min_sil, a.pad)
    cuts = [tuple(map(float, r.split("-"))) for r in a.taglia.split(",") if r.strip()]
    if a.fine:
        cuts.append((a.fine, dur))
    for c0, c1 in cuts:
        segs = [p for s0, s1 in segs for p in ((s0, min(s1, c0)), (max(s0, c1), s1)) if p[1] - p[0] > 0.1]
    segs = [(round(s0 * FPS) / FPS, round(s1 * FPS) / FPS) for s0, s1 in segs]  # tagli a frame interi
    mapper, total = time_mapper(segs)
    if a.srt:
        blocks = word_timings(parse_srt(a.srt), mapper)
    else:
        pj = a.parole or os.path.splitext(a.video)[0] + "_parole.json"
        if not os.path.exists(pj):
            print("Trascrivo l'audio...")
            json.dump(transcribe(a.video), open(pj, "w"), ensure_ascii=False, indent=0)
            print(f"Parole salvate in {pj} (correggibili a mano)")
        if a.solo_trascrivi:
            return
        blocks = words_to_blocks(json.load(open(pj)), mapper)
    tmp = tempfile.mkdtemp(prefix="monta_", dir=HERE)
    try:
        lst = build_overlay(tmp, total, blocks, a.titolo.upper(), a.titolo2.upper(), a.sub_y)
        # ogni pezzo codificato a parte (con tutti i tagli in un solo filtro si esaurisce la RAM)
        cover = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}"
        parts = os.path.join(tmp, "parts.txt")
        with open(parts, "w") as fh:
            for i, (s, e) in enumerate(segs):
                z = f",scale=iw*{a.zoom}:ih*{a.zoom},crop={W}:{H}" if a.zoom > 1 and i % 2 == 1 else ""
                pf = os.path.join(tmp, f"part{i:03d}.mkv")
                run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{s:.4f}", "-i", a.video,
                     "-t", f"{e - s:.4f}", "-vf", f"{cover}{z},setsar=1", "-c:v", "libx264",
                     "-preset", "ultrafast", "-crf", "14", "-c:a", "pcm_s16le", "-ar", "44100", "-ac", "2", pf])
                fh.write(f"file '{pf}'\n")
        fc = ["[1:v]format=rgba[ov]",
              "[0:v][ov]overlay=0:0:format=auto:eof_action=pass,format=yuv420p[v]",
              "[0:a]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=44100[a]"]
        run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", parts,
             "-f", "concat", "-safe", "0", "-i", lst, "-filter_complex", ";".join(fc),
             "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
             "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
             "-t", f"{total:.3f}", out])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"Fatto: {out}  ({dur:.1f}s -> {total:.1f}s)")


if __name__ == "__main__":
    main()
