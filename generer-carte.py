#!/usr/bin/env python3
"""Régénère la carte des consultants nexoLink dans index.html.

Usage :
    python3 generer-carte.py [consultants-carte.csv] [index.html]

Le CSV (non versionné, une ligne par consultant) : label;latitude;longitude
Les labels servent uniquement à la maintenance, ils ne sont jamais publiés.
Le script remplace le SVG entre les marqueurs CARTE-CONSULTANTS:DEBUT / FIN.
"""
import csv
import math
import re
import sys
from pathlib import Path

# Contour simplifié de la France métropolitaine (lon, lat)
OUTLINE = [
    (2.38, 51.03), (1.85, 50.95), (1.60, 50.73), (1.56, 50.40), (1.55, 50.20),
    (1.08, 49.93), (0.20, 49.71), (0.11, 49.49), (0.23, 49.42), (-0.45, 49.34),
    (-1.27, 49.40), (-1.62, 49.65), (-1.94, 49.72), (-1.56, 49.05), (-1.51, 48.64),
    (-2.03, 48.65), (-2.32, 48.68), (-3.05, 48.78), (-3.98, 48.72), (-4.55, 48.40),
    (-4.74, 48.03), (-4.20, 47.80), (-3.37, 47.72), (-3.12, 47.48), (-2.35, 47.27),
    (-2.15, 46.98), (-1.78, 46.50), (-1.15, 46.16), (-1.03, 45.62), (-1.06, 45.57),
    (-1.20, 45.00), (-1.16, 44.66), (-1.25, 44.40), (-1.45, 43.65), (-1.79, 43.37),
    (-1.30, 43.05), (-0.30, 42.80), (0.65, 42.70), (1.40, 42.60), (2.00, 42.35),
    (2.90, 42.47), (3.17, 42.43), (3.04, 42.75), (3.05, 43.15), (3.70, 43.40),
    (4.13, 43.53), (4.43, 43.45), (4.94, 43.43), (5.36, 43.30), (5.60, 43.21),
    (5.93, 43.10), (6.13, 43.08), (6.64, 43.27), (7.02, 43.55), (7.27, 43.70),
    (7.51, 43.79), (7.66, 44.17), (7.07, 44.25), (6.95, 44.65), (7.05, 45.10),
    (7.10, 45.45), (6.90, 45.85), (6.20, 46.20), (6.06, 46.42), (6.45, 46.78),
    (7.00, 47.35), (7.59, 47.56), (7.58, 48.10), (7.80, 48.60), (8.23, 48.97),
    (7.95, 49.03), (7.05, 49.11), (6.60, 49.30), (6.20, 49.45), (5.90, 49.50),
    (5.47, 49.50), (5.00, 49.80), (4.85, 50.10), (4.20, 50.00), (3.98, 50.30),
    (3.20, 50.70), (2.90, 50.75), (2.55, 51.09),
]

MARK_DEBUT = "<!-- CARTE-CONSULTANTS:DEBUT -->"
MARK_FIN = "<!-- CARTE-CONSULTANTS:FIN -->"
INDENT = " " * 16


def build_svg(consultants):
    k = math.cos(math.radians(46.6))
    pts = [(lon * k, -lat) for lon, lat in OUTLINE]
    minx = min(p[0] for p in pts)
    miny = min(p[1] for p in pts)
    maxx = max(p[0] for p in pts)
    maxy = max(p[1] for p in pts)
    width, pad = 440.0, 20.0
    s = width / (maxx - minx)
    vw, vh = width + 2 * pad, (maxy - miny) * s + 2 * pad

    def tr(lon, lat):
        return ((lon * k - minx) * s + pad, (-lat - miny) * s + pad)

    path = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in (tr(lon, lat) for lon, lat in OUTLINE)) + " Z"
    lines = [
        f'<svg viewBox="0 0 {vw:.0f} {vh:.0f}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Carte de France des consultants nexoLink" style="width: 100%; height: auto; display: block;">',
        f'    <path d="{path}" fill="rgba(106, 13, 173, 0.05)" stroke="var(--light-purple)" stroke-width="2" stroke-linejoin="round"/>',
    ]
    for _, lat, lon in consultants:
        x, y = tr(lon, lat)
        lines.append(
            f'    <circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="var(--primary-purple)" stroke="white" stroke-width="2.5" opacity="0.9"><title>Consultant nexoLink</title></circle>'
        )
    lines.append("</svg>")
    return "\n".join(INDENT + l for l in lines)


def main():
    csv_path = Path(sys.argv[1] if len(sys.argv) > 1 else "consultants-carte.csv")
    html_path = Path(sys.argv[2] if len(sys.argv) > 2 else "index.html")

    consultants = []
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.reader(f, delimiter=";"):
            if not row or row[0].strip().startswith("#"):
                continue
            consultants.append((row[0].strip(), float(row[1]), float(row[2])))

    html = html_path.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(MARK_DEBUT) + ".*?" + re.escape(MARK_FIN), re.DOTALL)
    if not pattern.search(html):
        sys.exit(f"Marqueurs {MARK_DEBUT} / {MARK_FIN} introuvables dans {html_path}")
    bloc = MARK_DEBUT + "\n" + build_svg(consultants) + "\n" + INDENT + MARK_FIN
    html_path.write_text(pattern.sub(lambda _: bloc, html), encoding="utf-8")
    print(f"Carte régénérée : {len(consultants)} consultants -> {html_path}")


if __name__ == "__main__":
    main()
