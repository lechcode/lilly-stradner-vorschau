#!/usr/bin/env python3
"""
Erzeugt hell.html und hell-en.html — Richtung B („Pergament mit dunklen Zäsuren").

Identisches Markup wie index.html / en.html, nur mit assets/hell.css zusätzlich.
Dadurch bleiben beide Richtungen automatisch inhaltsgleich: Wer den Text ändert,
ändert ihn in beiden.

Nach jeder Änderung an index.html erneut laufen lassen:
    python3 gen-en.py && python3 gen-hell.py
"""
import sys
from pathlib import Path

W = Path(__file__).parent

PAARE = [
    ("index.html", "hell.html", "hell-en.html", "en.html"),
    ("en.html", "hell-en.html", "hell.html", "index.html"),
]

for quelle, ziel, andere_sprache, _ in PAARE:
    s = (W / quelle).read_text(encoding="utf-8")

    anker = '<link rel="stylesheet" href="assets/site.css">'
    if anker not in s:
        sys.exit(f"ABBRUCH: {anker} nicht in {quelle} gefunden")
    s = s.replace(
        anker,
        anker + '\n<link rel="stylesheet" href="assets/hell.css">'
        '  <!-- Richtung B — s. gen-hell.py -->',
        1,
    )

    # Sprachumschalter soll innerhalb der hellen Richtung bleiben
    s = s.replace('href="index.html"', "§DE§").replace('href="en.html"', "§EN§")
    s = s.replace("§DE§", 'href="hell.html"').replace("§EN§", 'href="hell-en.html"')

    # Rechtsseiten gibt es nur einmal (Richtung A) — Links dorthin zurückdrehen
    for datei in ("impressum", "datenschutz", "agb",
                  "impressum-en", "datenschutz-en", "agb-en"):
        s = s.replace(f'href="hell-{datei}.html"', f'href="{datei}.html"')

    # og:url je Richtung eindeutig halten
    s = s.replace("lilly-stradner-vorschau/en.html", f"lilly-stradner-vorschau/{ziel}")
    s = s.replace('content="https://lechcode.github.io/lilly-stradner-vorschau/"',
                  f'content="https://lechcode.github.io/lilly-stradner-vorschau/{ziel}"')

    (W / ziel).write_text(s, encoding="utf-8")
    print(f"  {ziel} aus {quelle}")

print("\nRichtung B erzeugt. Vergleich: index.html (dunkel) ↔ hell.html (Pergament)")
