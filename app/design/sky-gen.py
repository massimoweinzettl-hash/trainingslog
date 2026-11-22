# Eigene Zeichnungen für das Design „Sky Blue“ (Küken-Familie, frei gestaltet nach dem Konzept des Nutzers)
OL = "#2f2a2a"; CREAM = "#fff4d6"; SHADE = "#ffe6a6"
def face(cx, cy, s=1.0, mood="happy"):
    e = []
    if mood == "happy":   # ^ ^
        e.append(f'<path d="M{cx-5*s} {cy}q{2*s} {-2.6*s} {4*s} 0M{cx+1*s} {cy}q{2*s} {-2.6*s} {4*s} 0" stroke="{OL}" stroke-width="{1.4*s}" fill="none" stroke-linecap="round"/>')
    else:
        e.append(f'<circle cx="{cx-3*s}" cy="{cy-1*s}" r="{1.3*s}" fill="{OL}"/><circle cx="{cx+3*s}" cy="{cy-1*s}" r="{1.3*s}" fill="{OL}"/>')
    e.append(f'<path d="M{cx-2.2*s} {cy+2.2*s}q{2.2*s} {2.2*s} {4.4*s} 0" stroke="{OL}" stroke-width="{1.2*s}" fill="none" stroke-linecap="round"/>')
    e.append(f'<ellipse cx="{cx-5.6*s}" cy="{cy+2*s}" rx="{1.8*s}" ry="{1.1*s}" fill="#ff9fb0" opacity=".8"/><ellipse cx="{cx+5.6*s}" cy="{cy+2*s}" rx="{1.8*s}" ry="{1.1*s}" fill="#ff9fb0" opacity=".8"/>')
    return "".join(e)
def body(eyes="dot", brows=False, comb=True):
    g = [f'<path d="M-9 0v4M-12 4h6M9 0v4M6 4h6" stroke="#f59a2b" stroke-width="2.4" stroke-linecap="round" fill="none"/>',
         f'<path d="M0 -50C18 -50 28 -36 28 -20C28 -6 17 1 0 1S-28 -6 -28 -20C-28 -36 -18 -50 0 -50Z" fill="{CREAM}" stroke="{OL}" stroke-width="2"/>',
         f'<path d="M-22 -10C-14 -2 14 -2 22 -10C18 -2 10 1 0 1S-18 -2 -22 -10Z" fill="{SHADE}" opacity=".9"/>',
         f'<path d="M-8 -14q4 3 8 0q4 3 8 0" stroke="#e8c98a" stroke-width="1.4" fill="none" stroke-linecap="round"/>']   # angedeutete Bauchmuskeln
    if comb: g.append(f'<path d="M-7 -49c-3-6 2-10 6-6c0-7 7-8 8-2c4-4 9 0 5 6z" fill="#e84a3f" stroke="{OL}" stroke-width="1.6" stroke-linejoin="round"/>')
    if eyes == "happy":
        g.append(f'<path d="M-15 -30q4-5 8 0M7 -30q4-5 8 0" stroke="{OL}" stroke-width="2.2" fill="none" stroke-linecap="round"/>')
    elif eyes == "squint":
        g.append(f'<path d="M-15 -33l7 3l-7 3M15 -33l-7 3l7 3" stroke="{OL}" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    else:
        g.append(f'<ellipse cx="-11" cy="-30" rx="3.4" ry="4.2" fill="{OL}"/><ellipse cx="11" cy="-30" rx="3.4" ry="4.2" fill="{OL}"/><circle cx="-10" cy="-31.6" r="1.3" fill="#fff"/><circle cx="12" cy="-31.6" r="1.3" fill="#fff"/>')
    if brows: g.append(f'<path d="M-16 -38l8 3M16 -38l-8 3" stroke="{OL}" stroke-width="2" stroke-linecap="round"/>')
    g.append('<ellipse cx="-17" cy="-22" rx="4.5" ry="2.8" fill="#ffa3b3" opacity=".8"/><ellipse cx="17" cy="-22" rx="4.5" ry="2.8" fill="#ffa3b3" opacity=".8"/>')
    return g
def beak(open_=False):
    if open_: return f'<path d="M-5 -25l5 3l5-3l-5 7z" fill="#ffa22e" stroke="{OL}" stroke-width="1.3" stroke-linejoin="round"/>'
    return f'<path d="M-4 -25l4 4l4 -4z" fill="#ffa22e" stroke="{OL}" stroke-width="1.3" stroke-linejoin="round"/>'
def flexwing(side=1, up=True):
    # angespannter Flügel mit kleinem Bizeps, side=1 rechts, -1 links
    s = side
    return (f'<g transform="scale({s} 1)"><path d="M24 -24c9-3 15-11 12-21c-1-4-6-5-8-1c-1 3 0 5 2 6c-1 3-3 5-6 6c-3-4-9-3-10 2" fill="{CREAM}" stroke="{OL}" stroke-width="2" stroke-linejoin="round"/>'
            f'<path d="M27 -33c3-2 6-1 7 2" stroke="{OL}" stroke-width="1.4" fill="none" stroke-linecap="round"/></g>')
def wing_down(side=1):
    return f'<g transform="scale({side} 1)"><path d="M27 -20c6 2 6 8 1 9c-3 1-6-1-7-3" fill="{CREAM}" stroke="{OL}" stroke-width="2"/></g>'
def shake(x, y, s=1.0, face_=True):
    g = (f'<g transform="translate({x} {y}) scale({s})"><path d="M-10 -32h20l-2.5 32h-15z" fill="#5fb2ee" stroke="{OL}" stroke-width="1.6" stroke-linejoin="round"/>'
         f'<path d="M-9 -20h18l-1.6 20h-14.8z" fill="#2f8fd6" opacity=".55"/>'
         f'<rect x="-11" y="-39" width="22" height="8" rx="2.5" fill="#1d6fb3" stroke="{OL}" stroke-width="1.6"/><rect x="-3.5" y="-45" width="7" height="6" rx="2" fill="#1d6fb3" stroke="{OL}" stroke-width="1.4"/>'
         f'<path d="M-6 -28v8" stroke="#fff" stroke-width="2" stroke-linecap="round" opacity=".6"/>')
    if face_: g += face(1, -14, 1.0, "dot")
    return g + "</g>"
def rice(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M-17 -12c1-7 7-11 11-9c2-4 8-5 11-2c4-3 10-2 12 3c-1 0 0 0 0 8z" fill="#fffdf6" stroke="{OL}" stroke-width="1.4"/>'
            f'<path d="M-19 -12h38c0 8-8 13-19 13s-19-5-19-13z" fill="#eef6fd" stroke="{OL}" stroke-width="1.6"/>' + face(0, -6.5, .9, "happy") + "</g>")
def broccoli(x, y, s=1.0, flex=True):
    g = (f'<g transform="translate({x} {y}) scale({s})"><path d="M-6 -16h12l3 16h-18z" fill="#9ccc5b" stroke="{OL}" stroke-width="1.4" stroke-linejoin="round"/>'
         f'<circle cx="-9" cy="-21" r="7.5" fill="#4a9a31" stroke="{OL}" stroke-width="1.4"/><circle cx="9" cy="-21" r="7.5" fill="#4a9a31" stroke="{OL}" stroke-width="1.4"/><circle cx="0" cy="-27" r="8.5" fill="#55a83a" stroke="{OL}" stroke-width="1.4"/>'
         f'<circle cx="-4" cy="-30" r="1.6" fill="#86c95e"/><circle cx="6" cy="-24" r="1.4" fill="#86c95e"/>')
    g += face(0, -8, .85, "dot")
    if flex: g += f'<path d="M7 -9c5-1 8-5 7-9c-.5-2-3-2-3.5 0c-.3 1.2.3 2 1 2.3c-1.5 2-3.5 3-5 3.2" fill="#9ccc5b" stroke="{OL}" stroke-width="1.3" stroke-linejoin="round"/>'
    return g + "</g>"
def trophy(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M-10 -24h20v6c0 8-5 13-10 13s-10-5-10-13z" fill="#ffc83d" stroke="{OL}" stroke-width="1.6" stroke-linejoin="round"/>'
            f'<path d="M-10 -20h-5c0 6 3 9 7 9M10 -20h5c0 6-3 9-7 9" fill="none" stroke="{OL}" stroke-width="1.6"/>'
            f'<path d="M-2 -5h4v5h-4zM-7 0h14v4h-14z" fill="#e0a61f" stroke="{OL}" stroke-width="1.4" stroke-linejoin="round"/>'
            f'<path d="M0 -20l1.5 3h3.2l-2.6 2l1 3.2l-3.1-2l-3.1 2l1-3.2l-2.6-2h3.2z" fill="#fff4c2"/></g>')
def chart(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><rect x="-16" y="-30" width="34" height="30" rx="4" fill="#fff" stroke="{OL}" stroke-width="1.4"/>'
            f'<rect x="-11" y="-11" width="5" height="8" fill="#9fd0f5"/><rect x="-3" y="-16" width="5" height="13" fill="#5fb2ee"/><rect x="5" y="-23" width="5" height="20" fill="#1683d8"/>'
            f'<path d="M-12 -14l7-5l7 2l9-9" stroke="#1d6fb3" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M8 -26h4v4" stroke="#1d6fb3" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>')
def sparkle(x, y, s=1.0, c="#ffc83d"):
    return f'<path transform="translate({x} {y}) scale({s})" d="M0 -6l1.6 4.4l4.4 1.6l-4.4 1.6l-1.6 4.4l-1.6-4.4l-4.4-1.6l4.4-1.6z" fill="{c}"/>'
def clipboard(x, y, s=1.0, rot=10):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})"><rect x="-13" y="-34" width="26" height="34" rx="3" fill="#fff" stroke="{OL}" stroke-width="1.6"/>'
            f'<rect x="-6" y="-37" width="12" height="6" rx="2" fill="#9aa7b4" stroke="{OL}" stroke-width="1.3"/>'
            f'<path d="M-8 -26l2 2l3-3M-8 -17l2 2l3-3M-8 -8l2 2l3-3" stroke="#1683d8" stroke-width="1.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M0 -25h8M0 -16h8M0 -7h6" stroke="#9aa7b4" stroke-width="1.6" stroke-linecap="round"/></g>')
def chick(x, y, s, pose):
    g = [f'<g transform="translate({x} {y}) scale({s})">']
    if pose == "shake":
        g += body("happy")
        g.append(beak(True)); g.append(wing_down(-1))
        g.append(f'<path d="M24 -24c7-4 10-10 9-17" fill="none" stroke="{OL}" stroke-width="2"/><path d="M27 -42c2-3 7-3 8 0c1 3-1 5-4 5" fill="{CREAM}" stroke="{OL}" stroke-width="2"/>')
        g.append(shake(31, -40, .74))
    elif pose == "double":
        g += body("dot", brows=True)
        g.append(beak(False)); g.append(flexwing(1)); g.append(flexwing(-1))
        g.append(f'<path d="M-40 -58l-4-5M-36 -62l-1-6M40 -58l4-5M36 -62l1-6" stroke="#5fb2ee" stroke-width="2" stroke-linecap="round"/>')
    elif pose == "trophy":
        g += body("happy")
        g.append(beak(True))
        g.append(f'<path d="M-25 -30c-4-8-4-16 0-22M25 -30c4-8 4-16 0-22" fill="none" stroke="{OL}" stroke-width="2"/>')
        g.append(trophy(0, -54, 1.05))
        g.append(f'<path d="M-27 -54c-3-1-5 2-3 4M27 -54c3-1 5 2 3 4" fill="{CREAM}" stroke="{OL}" stroke-width="2"/>')
        g.append(sparkle(-34, -66, .9)); g.append(sparkle(34, -72, .7))
    elif pose == "tape":
        g += body("dot")
        g.append(beak(False))
        # gelbes Maßband um den Bauch
        g.append('<path d="M-28 -17c8 6 48 6 56 0l1 6c-9 7-49 7-58 0z" fill="#ffd23f" stroke="#2f2a2a" stroke-width="1.4" stroke-linejoin="round"/>')
        g.append('<path d="M-20 -12.5v-2.5M-12 -11v-3M-4 -10.5v-2.5M4 -10.5v-3M12 -11v-2.5M20 -12.5v-3" stroke="#2f2a2a" stroke-width="1.1" stroke-linecap="round"/>')
        g.append(f'<path d="M28 -14c6 2 10 7 9 14" fill="none" stroke="#ffd23f" stroke-width="4.5" stroke-linecap="round"/><path d="M28 -14c6 2 10 7 9 14" fill="none" stroke="{OL}" stroke-width=".9" stroke-dasharray="1 3"/>')
        g.append(f'<rect x="33" y="-2" width="9" height="7" rx="2" fill="#e8b417" stroke="{OL}" stroke-width="1.3"/>')
        g.append(wing_down(-1)); g.append(wing_down(1))
    elif pose == "coach":
        g += body("dot", comb=False)
        # Pfeife im Schnabel
        g.append(f'<path d="M-4 -25l4 4l4 -4z" fill="#ffa22e" stroke="{OL}" stroke-width="1.3" stroke-linejoin="round"/>')
        g.append(f'<path d="M3 -22h8a3.5 3.5 0 1 1 0 7h-4" fill="#c9d3dc" stroke="{OL}" stroke-width="1.3"/><path d="M8 -15c-6 6-14 8-20 6" fill="none" stroke="#e84a3f" stroke-width="1.4"/>')
        # rote Cap mit COACH
        g.append(f'<path d="M-24 -42c2-12 12-18 24-18s22 6 24 18c-14-3-34-3-48 0z" fill="#e84a3f" stroke="{OL}" stroke-width="1.8" stroke-linejoin="round"/>')
        g.append(f'<path d="M14 -43c8-1 16 0 22 3c-6 2-14 2-22 1z" fill="#c8362d" stroke="{OL}" stroke-width="1.6" stroke-linejoin="round"/>')
        g.append('<text x="-1" y="-46.5" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-weight="700" font-size="7.4" fill="#fff" letter-spacing=".3">COACH</text>')
        g.append(wing_down(-1))
        g.append(clipboard(34, -4, .78, 12))
        g.append(f'<path d="M27 -20c5 1 7 5 6 9c-2 2-5 1-6-1" fill="{CREAM}" stroke="{OL}" stroke-width="2"/>')
    g.append("</g>")
    return "".join(g)
def scene(parts, w=200, h=84):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"
SC = {
 "home": scene([rice(40, 80, 1.0), chick(100, 78, .96, "shake"), broccoli(168, 80, 1.05)]),
 "train": scene([chick(100, 79, 1.0, "double")]),
 "prog": scene([chick(92, 80, .86, "trophy"), chart(160, 78, 1.0), sparkle(186, 30, .8, "#5fb2ee")]),
 "body": scene([chick(100, 78, 1.0, "tape")]),
 "plan": scene([chick(94, 80, 1.0, "coach")]),
}
if __name__ == "__main__":
    import json; json.dump(SC, open("/tmp/kw/sky.json", "w"))
    html = "<html><body style='background:#f4f8fc;margin:0'>" + "".join(f"<div style='display:inline-block;margin:6px;background:#fff'>{v.replace('<svg ', '<svg width=400 height=170 ')}</div>" for v in SC.values()) + "</body></html>"
    open("/tmp/kw/sky.html", "w").write(html)
