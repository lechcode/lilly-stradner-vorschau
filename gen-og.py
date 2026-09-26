#!/usr/bin/env python3
"""
Baut assets/og.jpg (1200x630) fuer Social-Media-Vorschauen.

Die Schriften liegen nur als woff2 vor; PIL kann die nicht lesen. Deshalb
werden sie hier ueber fontTools kurz nach TTF entpackt (in den Scratch-Pfad,
nicht ins Projekt) und dann gezeichnet.

Aufruf:  python3 gen-og.py
"""
import tempfile
from pathlib import Path

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

W = Path(__file__).parent
IMG = W / "assets" / "img"
BREITE, HOEHE = 1200, 630

NACHT = (0x14, 0x10, 0x0C)
LICHT = (0xF4, 0xEB, 0xDF)
DAEMMER = (0xC9, 0xB7, 0xA4)
GLUT = (0x79, 0x24, 0x27)


def ttf(name: str) -> Path:
    """woff2 → ttf, in einen temporaeren Ordner."""
    ziel = Path(tempfile.gettempdir()) / f"lilly-{name}.ttf"
    if not ziel.exists():
        f = TTFont(W / "assets" / "fonts" / f"{name}.woff2")
        f.flavor = None
        f.save(ziel)
    return ziel


def portrait(datei: str, breite: int, hoehe: int, oben: float = 0.0) -> Image.Image:
    """Mittiger Beschnitt auf Zielformat, Gesicht bleibt oben im Bild."""
    im = Image.open(IMG / datei).convert("RGB")
    ziel = breite / hoehe
    b, h = im.size
    if b / h > ziel:
        nb = int(h * ziel)
        im = im.crop(((b - nb) // 2, 0, (b - nb) // 2 + nb, h))
    else:
        nh = int(b / ziel)
        y = int((h - nh) * oben)
        im = im.crop((0, y, b, y + nh))
    return im.resize((breite, hoehe), Image.LANCZOS)


def main():
    serif = ImageFont.truetype(str(ttf("inter-600")), 72)
    sans6 = ImageFont.truetype(str(ttf("inter-600")), 15)
    serif_klein = ImageFont.truetype(str(ttf("inter-600")), 27)

    og = Image.new("RGB", (BREITE, HOEHE), NACHT)

    # ── Diptychon links, je 4:5, mit Rand statt randlos ──────────────────
    rand, luecke, sp_breite = 44, 10, 430
    bb = (sp_breite - luecke) // 2
    bh = int(bb * 5 / 4)
    y = (HOEHE - bh) // 2
    for i, datei in enumerate(("frueher-880.jpg", "heute-880.jpg")):
        p = portrait(datei, bb, bh, oben=0.06)
        if i == 0:                                   # „frueher" bleibt dunkler
            p = Image.eval(p, lambda v: int(v * 0.86))
        og.paste(p, (rand + i * (bb + luecke), y))

    d = ImageDraw.Draw(og)
    x = rand + sp_breite + 56

    # ── Marke ────────────────────────────────────────────────────────────
    d.line([(x, 184), (x + 34, 184)], fill=GLUT, width=2)
    d.text((x + 48, 175), "SOMATISCHE PROZESSBEGLEITUNG", font=sans6,
           fill=DAEMMER, spacing=0, features=None)

    # ── Schlagzeile ──────────────────────────────────────────────────────
    d.text((x, 220), "Transformation", font=serif, fill=LICHT)
    d.text((x, 302), "ist möglich.", font=serif, fill=LICHT)

    # ── Siegel + Wortmarke ───────────────────────────────────────────────
    siegel = Image.open(IMG / "siegel-240.webp").convert("RGBA")
    sh = 78
    sw = round(siegel.width * sh / siegel.height)
    siegel = siegel.resize((sw, sh), Image.LANCZOS)
    og.paste(siegel, (x, 432), siegel)

    d.text((x + sw + 20, 440), "Lilly Stradner", font=serif_klein, fill=LICHT)
    d.text((x + sw + 22, 480), "SPIRIT OF BODY AND BREATH", font=sans6, fill=DAEMMER)

    ziel = W / "assets" / "og.jpg"
    og.save(ziel, quality=88, optimize=True, progressive=True)
    print(f"assets/og.jpg · {og.size[0]}x{og.size[1]} · "
          f"{ziel.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
