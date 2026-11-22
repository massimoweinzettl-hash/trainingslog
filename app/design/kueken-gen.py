# Eigene Küken-Zeichnungen für das Design „Gym Kawaii“ (keine fremde Figur, frei gestaltet)
OL = "#3a2a22"
def chick(x, y, s=1.0, pose="lift", flip=False):
    """Küken-Körper (rund), Kamm, Augen, Wangen, Schnabel, Flügel je nach Pose. Ursprung = Mitte unten."""
    t = f'translate({x} {y}) scale({-s if flip else s} {s})'
    g = [f'<g transform="{t}">']
    # Füße
    g.append(f'<path d="M-9 0v4M-12 4h6M9 0v4M6 4h6" stroke="#f59a2b" stroke-width="2.4" stroke-linecap="round" fill="none"/>')
    # Körper
    g.append(f'<path d="M0 -50C18 -50 28 -36 28 -20C28 -6 17 1 0 1S-28 -6 -28 -20C-28 -36 -18 -50 0 -50Z" fill="#fff6cf" stroke="{OL}" stroke-width="2"/>')
    g.append('<path d="M-22 -10C-14 -2 14 -2 22 -10C18 -2 10 1 0 1S-18 -2 -22 -10Z" fill="#ffe7a3" opacity=".9"/>')
    # Kamm
    g.append(f'<path d="M-7 -49c-3-6 2-10 6-6c0-7 7-8 8-2c4-4 9 0 5 6z" fill="#ff5b5b" stroke="{OL}" stroke-width="1.6" stroke-linejoin="round"/>')
    if pose == "sleep":
        g.append(f'<path d="M-15 -30q4 3 8 0M7 -30q4 3 8 0" stroke="{OL}" stroke-width="2" fill="none" stroke-linecap="round"/>')
    else:
        g.append(f'<ellipse cx="-11" cy="-30" rx="3.4" ry="4.2" fill="{OL}"/><ellipse cx="11" cy="-30" rx="3.4" ry="4.2" fill="{OL}"/>')
        g.append('<circle cx="-10" cy="-31.6" r="1.3" fill="#fff"/><circle cx="12" cy="-31.6" r="1.3" fill="#fff"/>')
        if pose in ("lift", "over"):
            g.append(f'<path d="M-16 -38l8 3M16 -38l-8 3" stroke="{OL}" stroke-width="2" stroke-linecap="round"/>')
    g.append('<ellipse cx="-17" cy="-22" rx="4.5" ry="2.8" fill="#ff9bb0" opacity=".85"/><ellipse cx="17" cy="-22" rx="4.5" ry="2.8" fill="#ff9bb0" opacity=".85"/>')
    g.append(f'<path d="M-4 -25l4 4l4 -4z" fill="#ffa22e" stroke="{OL}" stroke-width="1.3" stroke-linejoin="round"/>')
    # Flügel
    if pose == "lift":   # Hantel vor der Brust
        g.append(dumbbell(0, -14, 1.0))
        g.append(f'<path d="M-27 -20c-6 2-6 8-1 9c3 1 6-1 7-3" fill="#fff6cf" stroke="{OL}" stroke-width="2"/><path d="M27 -20c6 2 6 8 1 9c-3 1-6-1-7-3" fill="#fff6cf" stroke="{OL}" stroke-width="2"/>')
    elif pose == "over":  # Hantel über dem Kopf
        g.append(f'<path d="M-25 -30c-6-6-6-16-2-22M25 -30c6-6 6-16 2-22" fill="none" stroke="{OL}" stroke-width="2"/>')
        g.append(f'<path d="M-27 -52c-3 0-4 3-2 5M27 -52c3 0 4 3 2 5" fill="#fff6cf" stroke="{OL}" stroke-width="2"/>')
        g.append(dumbbell(0, -60, 1.15))
    elif pose == "flex":  # Bizeps-Pose mit einem Flügel
        g.append(f'<path d="M24 -26c8-4 12-12 9-20c-1-3-5-4-7-1c-1 2 0 5 2 6c-4 3-8 7-9 10" fill="#fff6cf" stroke="{OL}" stroke-width="2" stroke-linejoin="round"/>')
        g.append(f'<path d="M29 -40c2-1 4 0 4 2" stroke="{OL}" stroke-width="1.4" fill="none"/>')
        g.append(f'<path d="M-27 -18c-5 3-5 9 0 10c3 0 5-2 5-4" fill="#fff6cf" stroke="{OL}" stroke-width="2"/>')
    else:  # sleep: Flügel angelegt
        g.append(f'<path d="M-26 -18c-4 4-3 10 2 10M26 -18c4 4 3 10-2 10" fill="none" stroke="{OL}" stroke-width="2"/>')
    g.append('</g>')
    return "".join(g)
def dumbbell(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><rect x="-30" y="-1.8" width="60" height="3.6" rx="1.8" fill="#7d7f8c" stroke="{OL}" stroke-width="1.2"/>'
            f'<rect x="-30" y="-8" width="6" height="16" rx="2" fill="#3e4152" stroke="{OL}" stroke-width="1.2"/><rect x="24" y="-8" width="6" height="16" rx="2" fill="#3e4152" stroke="{OL}" stroke-width="1.2"/>'
            f'<rect x="-36" y="-6" width="6" height="12" rx="2" fill="#555a6e" stroke="{OL}" stroke-width="1.2"/><rect x="30" y="-6" width="6" height="12" rx="2" fill="#555a6e" stroke="{OL}" stroke-width="1.2"/></g>')
def shaker(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M-8 -30h16l-2 30h-12z" fill="#a98bff" stroke="{OL}" stroke-width="1.6" stroke-linejoin="round"/>'
            f'<rect x="-9" y="-36" width="18" height="7" rx="2" fill="#6f4fd8" stroke="{OL}" stroke-width="1.6"/><rect x="-3" y="-41" width="6" height="5" rx="1.5" fill="#6f4fd8" stroke="{OL}" stroke-width="1.4"/>'
            f'<path d="M-5 -24v18" stroke="#fff" stroke-width="2" stroke-linecap="round" opacity=".55"/></g>')
def broccoli(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M-4 -14h8l3 14h-14z" fill="#9ccc5b" stroke="{OL}" stroke-width="1.4" stroke-linejoin="round"/>'
            f'<circle cx="-8" cy="-19" r="7" fill="#4a9a31" stroke="{OL}" stroke-width="1.4"/><circle cx="8" cy="-19" r="7" fill="#4a9a31" stroke="{OL}" stroke-width="1.4"/><circle cx="0" cy="-25" r="8" fill="#55a83a" stroke="{OL}" stroke-width="1.4"/>'
            f'<circle cx="-3" cy="-28" r="1.6" fill="#86c95e"/><circle cx="5" cy="-22" r="1.4" fill="#86c95e"/></g>')
def bowl(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M-17 -12c1-7 7-11 11-9c2-4 8-5 11-2c4-3 10-2 12 3c-1 0 0 0 0 8z" fill="#fffdf6" stroke="{OL}" stroke-width="1.4"/>'
            f'<path d="M-19 -12h38c0 8-8 13-19 13s-19-5-19-13z" fill="#f3f0ff" stroke="{OL}" stroke-width="1.6"/><path d="M-12 -6h24" stroke="#c9bcff" stroke-width="2"/></g>')
def zzz(x, y):
    return (f'<g transform="translate({x} {y})" fill="none" stroke="#8c6bff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M0 0h8l-8 9h8"/><path d="M12 -12h6l-6 7h6"/><path d="M21 -21h4.5l-4.5 5h4.5"/></g>')
def scene(parts, w=200, h=74):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"
SC = {
 "lift": scene([chick(92, 66, 1.0, "lift"), shaker(150, 68, .95), broccoli(182, 70, 1.0)]),
 "flex": scene([bowl(40, 70, 1.0), chick(100, 66, 1.0, "flex"), shaker(158, 68, .95), broccoli(186, 70, .9)]),
 "over": scene([chick(95, 72, .92, "over"), broccoli(176, 70, 1.0)]),
 "sleep": scene([bowl(48, 70, .95), chick(108, 68, 1.0, "sleep"), zzz(142, 26), broccoli(182, 70, .95)]),
}
if __name__ == "__main__":
    import json; json.dump(SC, open("/tmp/kw/scenes.json", "w"))
    html = "<html><body style='background:#f6f3fd;margin:0'>" + "".join(f"<div style='display:inline-block;margin:6px;background:#fff'>{v.replace('<svg ', '<svg width=400 height=148 ')}</div>" for v in SC.values()) + "</body></html>"
    open("/tmp/kw/prev.html", "w").write(html)
