#!/usr/bin/env python3
"""
Bildaufbereitung · lilly-stradner
Muster übernommen von websites/Kunden/evelyn-weidner/optimize-images.py

Quelle : material/ (Originale, gitignoriert — nie deployt)
Ziel   : assets/img/<motiv>-<breite>.webp + <motiv>-<breite>.jpg

HEIC-Vorstufe (macOS-Bordmittel, einmalig, liegt in material/konvertiert/):
    for f in *.HEIC; do sips -s format jpeg -s formatOptions 95 "$f" \
        --out "konvertiert/${f%.HEIC}.jpg"; done

Freisteller (rembg, u2net_human_seg) liegen als PNG mit Alpha in material/freisteller/.

Aufruf:  python3 optimize-images.py
"""
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance

WURZEL = Path(__file__).parent
MATERIAL = WURZEL / "material"
KONV = MATERIAL / "konvertiert"
FREI = MATERIAL / "freisteller"
ZIEL = WURZEL / "assets" / "img"
ZIEL.mkdir(parents=True, exist_ok=True)

# ── Palette (Design-Brief) ────────────────────────────────────────────────
NACHT = (0x14, 0x10, 0x0C)

# ── Aufträge ──────────────────────────────────────────────────────────────
# name: (quelle, breiten, seitenverhaeltnis|None, saettigung, waerme)
#   seitenverhaeltnis = (w, h) → mittiger Beschnitt; None = Originalformat
#   saettigung 1.0 = unveraendert · waerme 0.0 = unveraendert
#
# Lilly hat den Farbeingriff ausdruecklich erlaubt:
#   „wenn ein Bild vielleicht nicht so die Farben hat, kannst du ja auch die
#    Farben ein bisschen anpassen, dass das irgendwie mit reinpasst."
# Bewusst zurueckhaltend dosiert — das Vorher-Bild wird NICHT dramatisiert.
AUFTRAEGE = {
    # Hero-Diptychon — gleiche Kadrierung, damit die Haltung den Unterschied macht
    "frueher":     ("IMG_4721.jpg",  [440, 880],  (4, 5), 0.68, 0.04),
    "heute":       ("IMG_4068.PNG",  [440, 880],  (4, 5), 1.00, 0.06),

    # Kapitelbilder
    "atem":        ("IMG_4744.PNG",  [580, 1160], (4, 5), 0.94, 0.06),
    "raum":        ("IMG_4757.PNG",  [580, 1160], (3, 2), 0.90, 0.05),
    "umarmung":    ("IMG_4066.PNG",  [580, 1160], (4, 5), 0.96, 0.05),
    "online":      ("IMG_4005.jpg",  [580, 1160], (3, 2), 0.92, 0.05),
    "offline":     ("IMG_4724.jpg",  [580, 1160], (3, 2), 0.90, 0.05),

    # Atmosphaere-Flaechen (liegen sehr dunkel unter Text — W23)
    # Diese beiden liegen HINTER Text. Gleichmaessig abdunkeln macht sie
    # unsichtbar (gemessen: nur noch ein einziger Farbton). Stattdessen
    # werden unten in `deckel()` gezielt die LICHTER gekappt — die Textur
    # bleibt, die hellen Kerzenpunkte koennen den Text nicht mehr fressen.
    "altar-glut":  ("IMG_4749.PNG",  [420, 900, 1600], (16, 10), 0.80, 0.12),
    "altar-nacht": ("IMG_3814.jpg",  [420, 900, 1600], (16, 10), 0.76, 0.10),
}

# Bilder mit Alpha (Freisteller + Siegel) — kein JPEG-Fallback, kein Beschnitt
ALPHA = {
    "siegel":     ("IMG_4719.PNG",   [120, 240, 480]),
    "lilly-frei": ("lilly-frei.png", [420, 840]),
}


def quelle(name: str) -> Path:
    """material/ zuerst, dann konvertiert/, dann freisteller/."""
    for ordner in (MATERIAL, KONV, FREI):
        p = ordner / name
        if p.exists():
            return p
    raise FileNotFoundError(name)


def beschneiden(im: Image.Image, verhaeltnis) -> Image.Image:
    """Mittiger Beschnitt; bei Portraits etwas nach oben versetzt (Gesicht)."""
    if verhaeltnis is None:
        return im
    zw, zh = verhaeltnis
    ziel = zw / zh
    b, h = im.size
    if b / h > ziel:                       # zu breit → seitlich beschneiden
        neu_b = int(h * ziel)
        links = (b - neu_b) // 2
        return im.crop((links, 0, links + neu_b, h))
    neu_h = int(b / ziel)                  # zu hoch → oben bevorzugen
    oben = int((h - neu_h) * 0.28) if ziel < 1 else (h - neu_h) // 2
    return im.crop((0, oben, b, oben + neu_h))


def deckel(im: Image.Image, max_hell: int = 118) -> Image.Image:
    """Lichter kappen, Mitten und Tiefen lassen.

    Fuer Flaechen, die hinter Text liegen. Gleichmaessiges Abdunkeln nimmt
    die Textur mit; hier bleibt sie erhalten, nur die hellsten Stellen
    werden auf `max_hell` gestaucht.
    """
    kurve = [min(v, int(max_hell * (v / 255) ** 0.55)) for v in range(256)]
    return im.point(kurve * len(im.getbands()))


def toenen(im: Image.Image, saettigung: float, waerme: float) -> Image.Image:
    """Saettigung anpassen und leicht Richtung Nachtbraun stimmen."""
    if saettigung != 1.0:
        im = ImageEnhance.Color(im).enhance(saettigung)
    if waerme > 0:
        schleier = Image.new("RGB", im.size, NACHT)
        im = Image.blend(im, schleier, waerme)
    return im


def schreiben(im: Image.Image, name: str, breiten, mit_jpeg=True, guete=(80, 82)):
    """guete = (webp, jpeg). Das QA-Gate meldet ab 250 KB GELB, ab 500 KB ROT."""
    q_webp, q_jpeg = guete
    ob = im.width
    for w in breiten:
        if w > ob:                          # nie hochskalieren
            w = ob
        h = round(im.height * w / im.width)
        k = im.resize((w, h), Image.LANCZOS)
        k.save(ZIEL / f"{name}-{w}.webp", quality=q_webp, method=6)
        if mit_jpeg:
            k.convert("RGB").save(ZIEL / f"{name}-{w}.jpg",
                                  quality=q_jpeg, optimize=True, progressive=True)
        kb = (ZIEL / f"{name}-{w}.webp").stat().st_size / 1024
        print(f"  {name}-{w}  {w}x{h}  {kb:.0f} KB")


def main():
    print("Fotos:")
    for name, (datei, breiten, verh, sat, warm) in AUFTRAEGE.items():
        im = Image.open(quelle(datei))
        im = ImageOps.exif_transpose(im).convert("RGB")
        im = toenen(beschneiden(im, verh), sat, warm)
        # Atmosphaere-Flaechen liegen sehr dunkel hinter Text — dort faellt
        # staerkere Kompression nicht auf und haelt uns unter der 250-KB-Marke.
        if name.startswith("altar-"):
            im = deckel(im)                 # Lichter kappen, Textur behalten
            # Sehr niedrige Guete ist hier unsichtbar: die Flaeche liegt bei
            # 62 % Deckkraft hinter einem Verlauf. Dafuer laedt sie nicht mehr
            # gegen das Hero-Bild an (LCP).
            guete = (42, 48)
        else:
            guete = (74, 78)
        schreiben(im, name, breiten, guete=guete)

    print("Mit Transparenz:")
    for name, (datei, breiten) in ALPHA.items():
        im = Image.open(quelle(datei))
        im = ImageOps.exif_transpose(im).convert("RGBA")
        im = im.crop(im.getchannel("A").getbbox())    # leeren Rand abschneiden
        schreiben(im, name, breiten, mit_jpeg=False)

    gesamt = sum(p.stat().st_size for p in ZIEL.iterdir())
    print(f"\n{len(list(ZIEL.iterdir()))} Dateien · {gesamt/1024:.0f} KB gesamt")


if __name__ == "__main__":
    main()
