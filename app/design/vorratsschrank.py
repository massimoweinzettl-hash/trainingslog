# Design „Vorratsschrank“ (seit v277, Vorlagen des Nutzers aus ChatGPT nach Claudes Vorgaben):
# app/design/vorratsschrank/schrank.png (leerer Schrank, 3 Böden), lebensmittel.png (12 Behälter, 3×4), supplemente.png (6 Behälter, 2×3),
# alle mit echter Transparenz. Das Skript schneidet den Schrank zu, zerlegt die Sammelbilder an den leeren Zeilen/Spalten und schreibt
# kleine PNGs (256 Farben) nach vorrat/. Aufruf:  python3 app/design/vorratsschrank.py
# Danach die Seitenverhältnisse (Ausgabe „VS_AR“) in index.html übernehmen. Eingebunden über vsManage() in index.html,
# offline über sw.js (FILES), SWF in index.html und app/copy-web.mjs.
import json
import numpy as np
from PIL import Image

SRC, OUT = "app/design/vorratsschrank", "vorrat"
FOOD = ["flocken", "reis", "nudeln", "whey", "fischdose", "erdnuss", "oel", "obstkorb", "eier", "becher", "beeren", "karton"]
SUPP = ["kapseldose", "beutel", "tropfen", "schachtel", "riegelbox", "riegel"]
ICON_H = 180        # Behälter höchstens ~55 px hoch angezeigt → gut dreifach für Retina
SCHRANK_BOX = (110, 4, 1426, 1012)   # Zuschnitt des Schranks (Rand ohne Inhalt weg); Maße der Böden in index.html beziehen sich darauf


def small(im, path):
    im.quantize(colors=256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE).save(path, optimize=True)


def bands(p, minw=20):
    b, s = [], None
    for i, v in enumerate(p):
        if v and s is None: s = i
        if not v and s is not None: b.append((s, i)); s = None
    if s is not None: b.append((s, len(p)))
    return [x for x in b if x[1] - x[0] > minw]


def split(path, names):
    im = Image.open(path).convert("RGBA"); a = np.array(im); al = a[..., 3] > 24; out = []
    for y0, y1 in bands(al.any(1)):
        for x0, x1 in bands(al[y0:y1].any(0)):
            c = a[y0:y1, x0:x1].copy(); m = c[..., 3] > 24; ys, xs = np.where(m)
            c = c[ys.min():ys.max() + 1, xs.min():xs.max() + 1]; c[..., 3][c[..., 3] <= 24] = 0; out.append(Image.fromarray(c, "RGBA"))
    assert len(out) == len(names), (path, len(out))
    return dict(zip(names, out))


def main():
    ar = {}
    s = Image.open(f"{SRC}/schrank.png").convert("RGBA").crop(SCHRANK_BOX); small(s, f"{OUT}/schrank.png")
    for d in (split(f"{SRC}/lebensmittel.png", FOOD), split(f"{SRC}/supplemente.png", SUPP)):
        for n, im in d.items():
            w = round(im.width * ICON_H / im.height); ar[n] = [w, ICON_H]
            small(im.convert("RGBa").resize((w, ICON_H), Image.LANCZOS).convert("RGBA"), f"{OUT}/{n}.png")
    print("Schrank", s.size); print("VS_AR =", json.dumps(ar, separators=(",", ":")))


if __name__ == "__main__":
    main()
