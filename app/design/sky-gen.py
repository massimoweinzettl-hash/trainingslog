# Design „Sky Blue“: Küken-Maskottchen je Reiter (eigene Zeichnung, seit v264 im Kawaii-/Chibi-Stil).
# Eine Figur in fünf Posen: gleiche Kopf-/Körperform, Augen, Schnabel, Feder, Farben, Proportionen.
# Weiche Verläufe statt flacher Farben, große glänzende Augen, rosige Wangen, kleine Flügel und Füße.
#   python3 app/design/sky-gen.py --apply index.html     # Bilder in index.html ersetzen (Regeln [data-skin="sky"] … .top::after)
#   python3 app/design/sky-gen.py --preview /tmp/sky.html # Vorschau groß und in App-Größe (220×108 px)
OL = "#7a4a2e"          # warme braune Kontur statt Schwarz
DEFS = '''<defs>
<radialGradient id="bd" cx="42%" cy="34%" r="70%"><stop offset="0" stop-color="#fffdf5"/><stop offset=".55" stop-color="#fff1cc"/><stop offset="1" stop-color="#f3d08e"/></radialGradient>
<radialGradient id="wg" cx="40%" cy="30%" r="80%"><stop offset="0" stop-color="#fff6dc"/><stop offset="1" stop-color="#efc879"/></radialGradient>
<linearGradient id="ey" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a1810"/><stop offset=".65" stop-color="#3d2418"/><stop offset="1" stop-color="#6e3f22"/></linearGradient>
<radialGradient id="ck" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#ff8fa6" stop-opacity=".85"/><stop offset="1" stop-color="#ff8fa6" stop-opacity="0"/></radialGradient>
<linearGradient id="bk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffc46b"/><stop offset="1" stop-color="#f08a24"/></linearGradient>
<linearGradient id="ft" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffb24d"/><stop offset="1" stop-color="#e9791c"/></linearGradient>
<linearGradient id="cm" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff8a74"/><stop offset="1" stop-color="#e2423a"/></linearGradient>
<radialGradient id="sh" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#5a7fa3" stop-opacity=".28"/><stop offset="1" stop-color="#5a7fa3" stop-opacity="0"/></radialGradient>
<linearGradient id="sk" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8fcdf7"/><stop offset=".5" stop-color="#c9e7fc"/><stop offset="1" stop-color="#7bbbec"/></linearGradient>
<linearGradient id="skl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3d8fd6"/><stop offset="1" stop-color="#1d6fb3"/></linearGradient>
<linearGradient id="gd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffe27a"/><stop offset=".55" stop-color="#ffc93d"/><stop offset="1" stop-color="#e3a11a"/></linearGradient>
<linearGradient id="tp" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe36a"/><stop offset="1" stop-color="#f5bd1f"/></linearGradient>
<linearGradient id="cap" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff6b5e"/><stop offset="1" stop-color="#d8392f"/></linearGradient>
<radialGradient id="br" cx="40%" cy="30%" r="75%"><stop offset="0" stop-color="#8fd16b"/><stop offset="1" stop-color="#3f8d2b"/></radialGradient>
<linearGradient id="bs" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c3e48a"/><stop offset="1" stop-color="#8dc153"/></linearGradient>
<radialGradient id="rc" cx="40%" cy="30%" r="75%"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#eae4d6"/></radialGradient>
<linearGradient id="bw" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4f9fe"/><stop offset="1" stop-color="#c9def0"/></linearGradient>
</defs>'''
def eye(cx, cy, s=1.0, gx=0, gy=0):
    """Großes glänzendes Auge: dunkler Verlauf, warmer Rand unten, zwei Lichtpunkte."""
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{7.2*s}" ry="{8.6*s}" fill="url(#ey)"/>'
            f'<ellipse cx="{cx+gx}" cy="{cy+3.6*s+gy}" rx="{4.4*s}" ry="{2.6*s}" fill="#8a5232" opacity=".55"/>'
            f'<circle cx="{cx+2.2*s+gx}" cy="{cy-3.4*s+gy}" r="{2.9*s}" fill="#fff"/>'
            f'<circle cx="{cx-2.6*s+gx}" cy="{cy+2.6*s+gy}" r="{1.3*s}" fill="#fff" opacity=".9"/>'
            f'<circle cx="{cx+3.6*s+gx}" cy="{cy+1.2*s+gy}" r="{.7*s}" fill="#fff" opacity=".7"/>')
def chick(x, y, s=1.0, wings="down", mouth="smile", gx=0, gy=0, brows=False, cap=False):
    """Ein Küken; Ursprung = Mitte unten (Füße). Körpermaße ~ 84 breit, 82 hoch (Chibi: Kopf und Körper eins, weich wie Mochi)."""
    g = [f'<g transform="translate({x} {y}) scale({s})">']
    g.append('<ellipse cx="0" cy="1" rx="34" ry="5.5" fill="url(#sh)"/>')
    # Füße (klein, drei Zehen, weich)
    for fx in (-13, 13):
        g.append(f'<path d="M{fx-7} 1.5c1.5-3.5 3.2-5 4.6-5.2c.4-.1 .8.1 1.2.5c.4-.4 1-.6 1.6-.2c.5-.3 1.2-.3 1.6.1c1.5 1.1 2.8 2.6 4 4.8c-4.3 1.2-9 1.2-13 0z" fill="url(#ft)" stroke="{OL}" stroke-width="1.3" stroke-linejoin="round"/>')
    # Körper (Mochi-Form)
    g.append(f'<path d="M0 -80C25 -80 42 -63 42 -40C42 -14 25 -3 0 -3S-42 -14 -42 -40C-42 -63 -25 -80 0 -80Z" fill="url(#bd)" stroke="{OL}" stroke-width="2.2"/>')
    g.append('<ellipse cx="0" cy="-17" rx="24" ry="12" fill="#fff8e6" opacity=".75"/>')                     # heller Bauch
    g.append('<ellipse cx="-17" cy="-63" rx="11" ry="6.5" transform="rotate(-24 -17 -63)" fill="#fff" opacity=".55"/>')  # Glanz oben links
    # Feder (Schopf)
    if not cap:
        g.append(f'<path d="M-2 -79c-6-4-7-12-1-14c2-.7 4 .3 4.6 2c.8-4.5 6-6.5 8.8-3.4c2.2 2.4 1 6.2-2.4 7.4c3.2.3 4.6 3.8 2.4 6c-3.2 3.2-8.6 3.6-12.4 2z" fill="url(#cm)" stroke="{OL}" stroke-width="1.6" stroke-linejoin="round"/>')
        g.append('<path d="M3 -90c1.5-1.2 3.5-1.2 4.5 0" stroke="#ffd1c7" stroke-width="1.4" fill="none" stroke-linecap="round"/>')
    # Wangen
    g.append('<ellipse cx="-25" cy="-34" rx="9" ry="6" fill="url(#ck)"/><ellipse cx="25" cy="-34" rx="9" ry="6" fill="url(#ck)"/>')
    # Augen
    g.append(eye(-14, -45, 1.0, gx, gy)); g.append(eye(14, -45, 1.0, gx, gy))
    if brows: g.append(f'<path d="M-21 -58.5q5 -1 9 2.5M21 -58.5q-5 -1 -9 2.5" stroke="{OL}" stroke-width="2" fill="none" stroke-linecap="round"/>')
    # Schnabel
    if mouth == "open":
        g.append(f'<path d="M-5.5 -35.5c2.5-2 8.5-2 11 0c-.5 4-2.8 6.6-5.5 6.6s-5-2.6-5.5-6.6z" fill="#e8605a" stroke="{OL}" stroke-width="1.2" stroke-linejoin="round"/>')
        g.append(f'<path d="M-6 -36c2.6-3.4 9.4-3.4 12 0c-3.4 1.6-8.6 1.6-12 0z" fill="url(#bk)" stroke="{OL}" stroke-width="1.2" stroke-linejoin="round"/>')
    else:
        g.append(f'<path d="M-5.5 -37c2.4-2.6 8.6-2.6 11 0c-1.4 3.6-3.4 5.4-5.5 5.4s-4.1-1.8-5.5-5.4z" fill="url(#bk)" stroke="{OL}" stroke-width="1.2" stroke-linejoin="round"/>')
        g.append('<path d="M-2.4 -36.6c1.2-.7 3-.7 4 0" stroke="#fff1d6" stroke-width="1" fill="none" stroke-linecap="round"/>')
    # Flügel
    def wing(side, kind):
        sx = side
        if kind == "down":
            return f'<path transform="scale({sx} 1)" d="M39 -40c7 1 10 7 8 13c-1.5 4-6.5 5-9.5 2" fill="url(#wg)" stroke="{OL}" stroke-width="1.9" stroke-linejoin="round"/>'
        if kind == "flex":   # angespannter Flügel mit kleinem Bizeps
            return (f'<g transform="scale({sx} 1)"><path d="M38 -36c8-2 14-8 15-16c.5-4-3.5-6.5-6.5-4.3c-2.3 1.7-2 4.6 0 5.8c-1.6 2.8-4.8 4.6-8 5" fill="url(#wg)" stroke="{OL}" stroke-width="1.9" stroke-linejoin="round"/>'
                    f'<path d="M42 -44.5c2.2-2.4 5.4-2.6 7.4-.6" stroke="{OL}" stroke-width="1.3" fill="none" stroke-linecap="round" opacity=".7"/></g>')
        if kind == "up":     # Flügel nach oben (hält etwas über dem Kopf)
            return f'<path transform="scale({sx} 1)" d="M37 -52c5-6 7-14 5-21c-1.2-3.8 2.6-6.6 5.4-3.6c3.4 3.8 2.6 13-2.2 22c-1.6 3-4.2 5-7.2 5.6" fill="url(#wg)" stroke="{OL}" stroke-width="1.9" stroke-linejoin="round"/>'
        if kind == "lift":   # Flügel schräg nach oben-innen, halten etwas über dem Kopf
            return f'<path transform="scale({sx} 1)" d="M37 -50c3-9 1-20-5-30c-2-3.4 1.2-6.4 4.4-4c5 4 7.6 14 6 24c-.8 5-2.6 9-5.4 11.6" fill="url(#wg)" stroke="{OL}" stroke-width="1.9" stroke-linejoin="round"/>'
        if kind == "hold":   # Flügel nach vorn/oben-seitlich, hält etwas neben dem Körper
            return f'<path transform="scale({sx} 1)" d="M38 -42c6-4 12-4 15 0c2.4 3.2 0 7.6-4 7.4c-3.6-.2-6.6-1.8-9.4-2.8" fill="url(#wg)" stroke="{OL}" stroke-width="1.9" stroke-linejoin="round"/>'
        return ""
    wl, wr = wings if isinstance(wings, tuple) else (wings, wings)
    g.append(wing(-1, wl)); g.append(wing(1, wr))
    g.append("</g>")
    return "".join(g)
def mini_face(cx, cy, s=1.0, gx=0, mouth="smile"):
    e = (f'<ellipse cx="{cx-4.2*s}" cy="{cy}" rx="{2.2*s}" ry="{2.7*s}" fill="url(#ey)"/><ellipse cx="{cx+4.2*s}" cy="{cy}" rx="{2.2*s}" ry="{2.7*s}" fill="url(#ey)"/>'
         f'<circle cx="{cx-3.5*s+gx}" cy="{cy-1*s}" r="{.9*s}" fill="#fff"/><circle cx="{cx+4.9*s+gx}" cy="{cy-1*s}" r="{.9*s}" fill="#fff"/>'
         f'<ellipse cx="{cx-7.4*s}" cy="{cy+2.6*s}" rx="{2.6*s}" ry="{1.6*s}" fill="url(#ck)"/><ellipse cx="{cx+7.4*s}" cy="{cy+2.6*s}" rx="{2.6*s}" ry="{1.6*s}" fill="url(#ck)"/>')
    if mouth == "open": e += f'<path d="M{cx-2*s} {cy+2.6*s}q{2*s} {3.4*s} {4*s} 0z" fill="#e8605a" stroke="{OL}" stroke-width="{.8*s}" stroke-linejoin="round"/>'
    else: e += f'<path d="M{cx-2*s} {cy+2.8*s}q{2*s} {2*s} {4*s} 0" stroke="{OL}" stroke-width="{1*s}" fill="none" stroke-linecap="round"/>'
    return e
def shake(x, y, s=1.0, rot=0):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})"><path d="M-11 -36h22l-2.6 34c-.2 2-1.8 3.4-3.8 3.4h-9.2c-2 0-3.6-1.4-3.8-3.4z" fill="url(#sk)" stroke="{OL}" stroke-width="1.6" stroke-linejoin="round"/>'
            '<path d="M-10 -22h20l-1.4 18.6c-.1 1.6-1.4 2.8-3 2.8h-11.2c-1.6 0-2.9-1.2-3-2.8z" fill="#4ea3e3" opacity=".35"/>'
            f'<rect x="-12.5" y="-44" width="25" height="9" rx="3" fill="url(#skl)" stroke="{OL}" stroke-width="1.6"/><rect x="-4" y="-50" width="8" height="7" rx="2.4" fill="url(#skl)" stroke="{OL}" stroke-width="1.4"/>'
            '<path d="M-7 -32v12" stroke="#fff" stroke-width="2.4" stroke-linecap="round" opacity=".75"/>' + mini_face(1, -14, 1.0, .4, "open") + "</g>")
def rice(x, y, s=1.0, gx=1):
    return (f'<g transform="translate({x} {y}) scale({s})"><ellipse cx="0" cy="1" rx="22" ry="3.5" fill="url(#sh)"/>'
            f'<path d="M-19 -14c0-7 6-11 10.5-9.5c1.6-4.4 8.4-5.6 11.8-2.2c3.8-2.6 10.4-1.6 12 3.6c3.2.8 4.6 4.4 3.6 8.1z" fill="url(#rc)" stroke="{OL}" stroke-width="1.4" stroke-linejoin="round"/>'
            '<path d="M-10 -19.5c1-.6 2.2-.6 3 0M2 -22c1-.6 2.2-.6 3 0M9 -18c1-.6 2.2-.6 3 0" stroke="#d9d1c0" stroke-width="1.1" fill="none" stroke-linecap="round"/>'
            f'<path d="M-21 -14h42c0 9.5-9.4 15-21 15s-21-5.5-21-15z" fill="url(#bw)" stroke="{OL}" stroke-width="1.6" stroke-linejoin="round"/>'
            '<path d="M-14 -11.5h9" stroke="#fff" stroke-width="2" stroke-linecap="round" opacity=".8"/>' + mini_face(1, -6.6, .95, gx, "open") + "</g>")
def broccoli(x, y, s=1.0, gx=-1):
    return (f'<g transform="translate({x} {y}) scale({s})"><ellipse cx="0" cy="1" rx="16" ry="3" fill="url(#sh)"/>'
            f'<path d="M-7 -18h14l2.6 16.4c.3 1.8-1 3.4-2.8 3.4h-13.6c-1.8 0-3.1-1.6-2.8-3.4z" fill="url(#bs)" stroke="{OL}" stroke-width="1.4" stroke-linejoin="round"/>'
            f'<path d="M-15 -22c-5 0-7.5-5.6-4.4-9.2c-1.4-5 3.2-9 7.8-7.4c2.4-5.6 10.4-6 13.4-.6c4.6-1 8.6 3.4 7 7.8c3.4 3.2 1.2 9.4-3.8 9.4c-2.6 3.2-8 3.6-10.6.6c-3 2.4-7.4 2.2-9.4-.6z" fill="url(#br)" stroke="{OL}" stroke-width="1.5" stroke-linejoin="round"/>'
            '<path d="M-8 -35c1.6-1.4 4-1.6 5.6-.4M5 -38c1.4-.8 3.2-.6 4.2.4" stroke="#b8e895" stroke-width="1.4" fill="none" stroke-linecap="round"/>'
            f'<path d="M8 -11c5.4-.8 9-4.6 8.6-9.4c-.2-2.4-3.2-3-4.4-1c-.8 1.4-.2 2.8.8 3.2c-1.4 2.4-3.6 3.6-5.6 3.8" fill="url(#bs)" stroke="{OL}" stroke-width="1.3" stroke-linejoin="round"/>'
            + mini_face(-1, -9.5, .85, gx, "smile") + "</g>")
def trophy(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M-12 -28h24v7c0 9.4-5.6 15-12 15s-12-5.6-12-15z" fill="url(#gd)" stroke="{OL}" stroke-width="1.6" stroke-linejoin="round"/>'
            f'<path d="M-12 -24h-5.5c-.3 7 3.6 10.6 8.6 10.6M12 -24h5.5c.3 7-3.6 10.6-8.6 10.6" fill="none" stroke="{OL}" stroke-width="1.6" stroke-linecap="round"/>'
            f'<path d="M-2.6 -6h5.2v5.6h-5.2zM-8.5 -.6h17v5h-17z" fill="url(#gd)" stroke="{OL}" stroke-width="1.4" stroke-linejoin="round"/>'
            '<path d="M-7 -25v8c0 2 .8 4 2 5.4" stroke="#fff6c8" stroke-width="2.2" fill="none" stroke-linecap="round" opacity=".9"/>'
            '<path d="M1.5 -22.5l1.5 3.1l3.4.5l-2.5 2.4l.6 3.4l-3-1.6l-3 1.6l.6-3.4l-2.5-2.4l3.4-.5z" fill="#fff9d9"/></g>')
def chart(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><rect x="-18" y="-32" width="38" height="32" rx="6" fill="#ffffff" stroke="{OL}" stroke-width="1.4"/>'
            '<rect x="-12" y="-12" width="6" height="8" rx="1.5" fill="#a9d6f6"/><rect x="-3" y="-18" width="6" height="14" rx="1.5" fill="#62b3ee"/><rect x="6" y="-25" width="6" height="21" rx="1.5" fill="#1d7fcf"/>'
            '<path d="M-13 -15l7.5-5.5l7.5 2l10-9.5" stroke="#1d6fb3" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M8.5 -28.5h4.5v4.5" stroke="#1d6fb3" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>')
def sparkle(x, y, s=1.0, c="#ffd34d"):
    return f'<path transform="translate({x} {y}) scale({s})" d="M0 -7c.8 3.6 2.6 5.4 6.2 6.2c-3.6.8-5.4 2.6-6.2 6.2c-.8-3.6-2.6-5.4-6.2-6.2c3.6-.8 5.4-2.6 6.2-6.2z" fill="{c}"/>'
def tape_wrap():
    # gelbes Maßband um den Bauch, Ende im rechten Flügel
    return (f'<path d="M-41 -26c10 8 72 8 82 0l1 8c-12 9.4-72 9.4-84 0z" fill="url(#tp)" stroke="{OL}" stroke-width="1.4" stroke-linejoin="round"/>'
            '<path d="M-30 -21v-3M-20 -19.4v-3.4M-10 -18.6v-3M0 -18.3v-3.6M10 -18.6v-3M20 -19.4v-3.4M30 -21v-3" stroke="#7a4a2e" stroke-width="1.1" stroke-linecap="round"/>'
            '<text x="0" y="-12.6" text-anchor="middle" font-family="Arial, sans-serif" font-size="4.2" font-weight="700" fill="#7a4a2e">85</text>')
def clipboard(x, y, s=1.0, rot=12):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})"><rect x="-14" y="-36" width="28" height="36" rx="4" fill="#ffffff" stroke="{OL}" stroke-width="1.6"/>'
            f'<rect x="-6.5" y="-40" width="13" height="7" rx="2.4" fill="#a9b7c4" stroke="{OL}" stroke-width="1.3"/>'
            '<path d="M-9 -27l2.2 2.2l3.4-3.6M-9 -17.5l2.2 2.2l3.4-3.6M-9 -8l2.2 2.2l3.4-3.6" stroke="#1d7fcf" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M0 -26h8.5M0 -16.5h8.5M0 -7h6" stroke="#b9c6d2" stroke-width="1.8" stroke-linecap="round"/></g>')
def scene(body, w=220, h=96):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">' + DEFS + body + "</svg>"
# Szenen ---------------------------------------------------------------------------------------------
H = 108
home = scene(rice(40, 104, 1.0, 1.4) +
             chick(110, 104, .9, ("down", "up"), "open", gx=1.4, gy=-1) +
             shake(144, 46, .72, 10) + broccoli(186, 104, 1.05, -1.4) + sparkle(168, 30, .8, "#8fcdf7"), h=H)
train = scene(chick(110, 104, .92, ("flex", "flex"), "open", brows=True) + sparkle(60, 40, .9, "#8fcdf7") + sparkle(162, 32, .7, "#8fcdf7") +
              '<path d="M144 55c2.4 3.4 2.4 6.2 0 7.6c-2.4-1.4-2.4-4.2 0-7.6z" fill="#bfe3fb" stroke="#7a4a2e" stroke-width=".9"/>', h=H)
prog = scene(chick(96, 106, .84, ("down", "up"), "open", gx=1.2, gy=-1.4) + '<g transform="translate(135 42) rotate(8)">' + trophy(0, 0, .9) + "</g>" + chart(186, 100, .95) +
             sparkle(60, 40, 1.0) + sparkle(160, 16, .8) + sparkle(112, 14, .6, "#8fcdf7"), h=H)
tape = ('<g transform="translate(110 104) scale(.9)">' + tape_wrap() +
        '<path d="M41 -21c6-3 9-9 9-17" fill="none" stroke="url(#tp)" stroke-width="5" stroke-linecap="round"/>'
        '<path d="M41 -21c6-3 9-9 9-17" fill="none" stroke="#7a4a2e" stroke-width=".8" stroke-dasharray="1 3.4" opacity=".7"/>'
        '<rect x="44" y="-49" width="13" height="11" rx="3" fill="url(#tp)" stroke="#7a4a2e" stroke-width="1.3"/><circle cx="50.5" cy="-43.5" r="2.4" fill="#e3a11a"/>'
        '<path d="M40 -44c5-3.6 11-3.6 14 0c2.4 3.2 0 7.6-4 7.4c-3.6-.2-6.6-1.8-9.4-2.8" fill="url(#wg)" stroke="#7a4a2e" stroke-width="1.9" stroke-linejoin="round"/></g>')
body = scene(chick(110, 104, .9, ("down", "none"), "smile", gx=0, gy=2.2) + tape, h=H)
coach = scene(chick(104, 104, .9, ("down", "none"), "smile", cap=True) +
              '<g transform="translate(104 104) scale(.9)">'
              f'<path d="M-33 -66c3-15 16-24 33-24s30 9 33 24c-19-4.6-47-4.6-66 0z" fill="url(#cap)" stroke="{OL}" stroke-width="1.9" stroke-linejoin="round"/>'
              f'<path d="M20 -67.5c9-2 21-1.4 28 2.4c-8 3.4-19 3.6-28 1.6z" fill="#c4322a" stroke="{OL}" stroke-width="1.7" stroke-linejoin="round"/>'
              '<circle cx="0" cy="-90" r="2.6" fill="#c4322a" stroke="#7a4a2e" stroke-width="1.2"/>'
              '<path d="M-20 -82c4-3 9-4.6 14-4.6" stroke="#ff9a90" stroke-width="2" fill="none" stroke-linecap="round" opacity=".8"/>'
              '<text x="0" y="-71" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-weight="800" font-size="9" fill="#fff" letter-spacing=".4">COACH</text>'
              # Pfeife im Schnabel
              f'<path d="M4 -35h9.5a4.6 4.6 0 1 1-1.6 8.9h-7.9z" fill="#d9e2ea" stroke="{OL}" stroke-width="1.3" stroke-linejoin="round"/><circle cx="13" cy="-30.4" r="1.6" fill="#8b99a6"/>'
              '<path d="M6 -33.6h4" stroke="#fff" stroke-width="1.2" stroke-linecap="round" opacity=".9"/>'
              '</g>' + clipboard(158, 98, .9, 12) +
              '<g transform="translate(104 104) scale(.9)"><path d="M38 -42c6-4 12-4 15 0c2.4 3.2 0 7.6-4 7.4c-3.6-.2-6.6-1.8-9.4-2.8" fill="url(#wg)" stroke="#7a4a2e" stroke-width="1.9" stroke-linejoin="round"/></g>', h=H)
SC = {"home": home, "train": train, "prog": prog, "body": body, "plan": coach}
import re
def tidy(svg):
    """Nur benutzte Verläufe behalten, Zahlen auf 2 Stellen kürzen."""
    used = set(re.findall(r"url\(#(\w+)\)", svg))
    def keep(m): return m.group(0) if m.group(2) in used else ""
    svg = re.sub(r'<(radialGradient|linearGradient) id="(\w+)".*?</\1>', keep, svg, flags=re.S)
    return re.sub(r"-?\d+\.\d{3,}", lambda m: ("%.2f" % float(m.group(0))).rstrip("0").rstrip("."), svg)
def data_uri(svg):
    s = tidy(svg).replace("\n", "").replace('"', "'").replace("%", "%25").replace("#", "%23").replace("<", "%3C").replace(">", "%3E")
    return 'url("data:image/svg+xml,' + s + '")'
# Regel-Anfang je Szene in index.html (home = Grundregel)
SEL = {"home": '[data-skin="sky"] .top::after {', "train": '[data-skin="sky"][data-tab="train"] .top::after {',
       "prog": '[data-skin="sky"][data-tab="prog"] .top::after {', "body": '[data-skin="sky"][data-tab="body"] .top::after {',
       "plan": '[data-skin="sky"][data-tab="plan"] .top::after {'}
def apply(path):
    t = open(path, encoding="utf-8").read()
    for k, sel in SEL.items():
        assert t.count(sel) == 1, sel
        a = t.index(sel); b = t.index('url("data:image/svg+xml,', a); c = t.index('")', b) + 2
        assert "}" not in t[a:b], sel
        t = t[:b] + data_uri(SC[k]) + t[c:]
    open(path, "w", encoding="utf-8").write(t)
def preview(path):
    big = "".join(f"<div style='display:inline-block;margin:8px;background:#fff;border-radius:14px;padding:6px'><img src={data_uri(v)[4:-1]} width=440 height=216><div style='font:13px sans-serif;color:#68798a;text-align:center'>{k}</div></div>" for k, v in SC.items())
    small = "".join(f"<div style='display:inline-block;margin:6px;background:#f4f8fc'><img src={data_uri(v)[4:-1]} width=220 height=108></div>" for v in SC.values())
    open(path, "w").write("<html><body style='background:#eef4fa;margin:0'>" + big + "<div style='padding:8px;font:13px sans-serif'>In App-Größe:</div>" + small + "</body></html>")
if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3 and sys.argv[1] == "--apply": apply(sys.argv[2])
    elif len(sys.argv) == 3 and sys.argv[1] == "--preview": preview(sys.argv[2])
    else: print(__doc__ or "Aufruf: --apply index.html | --preview datei.html")
