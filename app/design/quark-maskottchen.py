# Design „Magerquark“: fünf Quark-Maskottchen je Reiter (seit v265).
# Quelle: Vorlage des Nutzers (aus ChatGPT, „Fünf Quark-Helden“, 2172 × 724 px, fünf Figuren nebeneinander mit Beschriftung).
# Die Vorlage liegt NICHT im Repo – sie trägt den Markennamen eines Händlers. Dieses Skript schneidet die Figuren aus,
# entfernt das rote Marken-Etikett auf dem Deckel und schreibt fünf gleich große PNGs mit transparentem Hintergrund:
#   python3 app/design/quark-maskottchen.py <vorlage.png> maskottchen/
# Ergebnis: maskottchen/quark-{home,train,prog,body,plan}.png (406 × 360 px, 256 Farben, je ~20–30 KB),
# eingebunden in index.html über [data-skin="quark"] … .top::after, offline über sw.js (FILES) und SWF in index.html.
import sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

NAMES = ["home", "train", "prog", "body", "plan"]
BOUNDS = [455, 890, 1318, 1742]       # Trennlinien zwischen den Figuren (x in der Vorlage)
LABEL_Y = 558                          # ab hier stehen die Beschriftungen
OUT_H = 360

def cut(src):
    H, W, _ = src.shape
    mn, mx = src.min(axis=2), src.max(axis=2)
    cand = (mn >= 185) & ((mx - mn) <= 28)                 # heller, ungesättigter Grund (inkl. Bodenschatten)
    cand[LABEL_Y:] = True
    R = 3
    barrier = ndi.binary_dilation(mn < 150, structure=np.ones((2 * R + 1, 2 * R + 1)))   # Lücken in Konturen schließen
    lab, _ = ndi.label(cand & ~barrier)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(border))
    bg = ndi.binary_dilation(bg, iterations=R + 1, mask=cand)
    a = np.ones((H, W), np.float32)
    ab = np.clip(1 - mn / 252.0, 0, 1); ab[ab < 0.035] = 0      # aus Weiß herausrechnen → weicher Schatten
    a[bg] = ab[bg]
    rgb = src.copy()
    m = bg & (a > 0)
    for c in range(3):
        ch = rgb[..., c]; ch[m] = np.clip((ch[m] - (1 - a[m]) * 255) / a[m], 0, 255)
    rgb[bg & (a == 0)] = 0
    a[LABEL_Y:] = 0
    fg = a > 0.02
    lab2, n2 = ndi.label(fg, structure=np.ones((3, 3)))
    fig = np.full((H, W), -1, np.int8)
    for i, (cy, cx) in enumerate(ndi.center_of_mass(fg, lab2, range(1, n2 + 1)), 1):
        fig[lab2 == i] = int(np.searchsorted(BOUNDS, cx))
    return rgb, a, fig

def remove_label(rgb, fig):
    """Rotes Marken-Etikett oben auf dem Deckel durch die Deckelfarbe daneben ersetzen (Plan: von der Kappe verdeckt)."""
    img = np.clip(rgb, 0, 255).astype(np.uint8)
    out = img.astype(np.float32).copy()
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    red = (r > 160) & (g < 90) & (b < 90) & (np.arange(rgb.shape[0])[:, None] < 220)
    for k in range(4):
        m = red & (fig == k)
        lb, n = ndi.label(ndi.binary_dilation(m, iterations=3))
        big = np.argmax(ndi.sum(m, lb, range(1, n + 1))) + 1
        ys, xs = np.where(m & (lb == big))
        Y0, Y1, X0, X1 = ys.min() - 3, ys.max() + 4, xs.min() - 4, xs.max() + 5
        for y in range(Y0, Y1):
            L = np.median(img[y, X0 - 10:X0 - 3], axis=0); Rr = np.median(img[y, X1 + 3:X1 + 10], axis=0)
            t = np.linspace(0, 1, X1 - X0)[:, None]
            out[y, X0:X1] = L * (1 - t) + Rr * t
        blk = np.stack([ndi.gaussian_filter(out[..., c], 1.6) for c in range(3)], axis=-1)
        out[Y0:Y1, X0:X1] = blk[Y0:Y1, X0:X1]
    return np.clip(out, 0, 255)

def export(rgb, a, fig, outdir):
    H, W = a.shape
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    yy = np.arange(H)[:, None]
    lid = (b > 225) & (r < 205) & (r > 120) & (g > 175) & (yy > 120) & (yy < 250)
    info = []
    for k in range(5):
        ys, xs = np.where(fig == k)
        lb, n = ndi.label(lid & (fig == k))
        big = np.argmax(ndi.sum(lid & (fig == k), lb, range(1, n + 1))) + 1
        lx = np.where(lb == big)[1]
        info.append(((lx.min() + lx.max()) // 2, xs.min(), xs.max()))    # Becher immer an derselben Stelle
    L = max(c - x0 for c, x0, x1 in info) + 6; R = max(x1 - c for c, x0, x1 in info) + 6
    Y0, Y1 = 68, 556
    CW, CH = L + R, Y1 - Y0
    for k, (c, x0, x1) in enumerate(info):
        rgba = np.zeros((H, W, 4), np.uint8)
        rgba[..., :3] = rgb.astype(np.uint8); rgba[..., 3] = (a * (fig == k) * 255).astype(np.uint8)
        can = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
        left = max(0, c - L)
        can.paste(Image.fromarray(rgba[Y0:Y1, left:c + R], "RGBA"), (L - (c - left), 0))
        im = can.convert("RGBa").resize((round(CW * OUT_H / CH), OUT_H), Image.LANCZOS).convert("RGBA")
        im.quantize(colors=256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE).save(f"{outdir}/quark-{NAMES[k]}.png", optimize=True)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Aufruf: python3 app/design/quark-maskottchen.py <vorlage.png> maskottchen/")
    src = np.array(Image.open(sys.argv[1]).convert("RGB")).astype(np.float32)
    rgb, a, fig = cut(src)
    rgb = remove_label(rgb, fig)
    export(rgb, a, fig, sys.argv[2].rstrip("/"))
