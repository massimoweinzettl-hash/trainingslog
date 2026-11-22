# Design „Magerquark“: fünf Quark-Maskottchen je Reiter (seit v265, Vorlagen seit v266 einzeln).
# Quelle: fünf Einzelbilder des Nutzers aus ChatGPT (1254 × 1254 px, transparent, ohne Markennamen) in
# app/design/quark-vorlagen/{home,train,prog,body,plan}.png. Dieses Skript richtet die Becher aneinander aus
# (Mitte und Unterkante des Deckeltexts „Speisequark Magerstufe“), schneidet alle fünf auf dieselbe Fläche zu und
# schreibt kleine PNGs mit 256 Farben:
#   python3 app/design/quark-maskottchen.py app/design/quark-vorlagen maskottchen
# Ergebnis: maskottchen/quark-{home,train,prog,body,plan}.png, eingebunden in index.html über
# [data-skin="quark"] … .top::after, offline über sw.js (FILES) und SWF in index.html, iPhone-App über app/copy-web.mjs.
import sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

NAMES = ["home", "train", "prog", "body", "plan"]
OUT_H = 400          # Bildhöhe in px (Anzeige 108 px hoch → gut 3,5-fach für Retina)
PAD = 12             # Rand um die gemeinsame Fläche (in Vorlagen-px)

def anchor(a):
    """Mitte (x) und Unterkante (y) des dunklen Deckeltexts – bei allen fünf Bechern gleich groß."""
    r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    lid = (b > 220) & (r < 190) & (g > 170) & (al > 200)
    lb, k = ndi.label(lid)
    big = lb == (np.argmax(ndi.sum(lid, lb, range(1, k + 1))) + 1)
    txt = ndi.binary_fill_holes(big) & ~big & (r < 90) & (g < 90) & (b < 130)
    ty, tx = np.where(txt)
    return (tx.min() + tx.max()) / 2, ty.max(), tx.max() - tx.min()

def main(src, out):
    imgs = [np.array(Image.open(f"{src}/{n}.png").convert("RGBA")) for n in NAMES]
    anc = [anchor(a.astype(int)) for a in imgs]
    for n, (cx, by, w) in zip(NAMES, anc):
        print(f"{n}: Textmitte x {cx:.0f}, Unterkante y {by}, Breite {w}")
    # Ausdehnung jeder Figur relativ zum Anker → gemeinsame Fläche
    ext = []
    for a, (cx, by, w) in zip(imgs, anc):
        ys, xs = np.where(a[..., 3] > 8)
        ext.append((cx - xs.min(), xs.max() - cx, by - ys.min(), ys.max() - by))
    L = max(e[0] for e in ext) + PAD; R = max(e[1] for e in ext) + PAD
    T = max(e[2] for e in ext) + PAD; B = max(e[3] for e in ext) + PAD
    CW, CH = int(round(L + R)), int(round(T + B))
    for n, a, (cx, by, w) in zip(NAMES, imgs, anc):
        can = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
        can.paste(Image.fromarray(a, "RGBA"), (int(round(L - cx)), int(round(T - by))))
        im = can.convert("RGBa").resize((round(CW * OUT_H / CH), OUT_H), Image.LANCZOS).convert("RGBA")
        im.quantize(colors=256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE).save(f"{out}/quark-{n}.png", optimize=True)
    print(f"Fläche {CW} × {CH} → {round(CW * OUT_H / CH)} × {OUT_H} px")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Aufruf: python3 app/design/quark-maskottchen.py app/design/quark-vorlagen maskottchen")
    main(sys.argv[1], sys.argv[2].rstrip("/"))
