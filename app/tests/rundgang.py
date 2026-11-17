#!/usr/bin/env python3
"""Rundgang-Test für den Trainingslog (seit v177, Wunsch des Nutzers: Absturz-Bugs finden).

Lädt die App mit reichhaltigen Beispieldaten (Plan, 6 Wochen Training, Gewicht, Essen, Präparate mit Vorrat,
Ausdauer, Reste) in Chromium auf iPhone-Größe und
  1. Rundgang: öffnet jeden Reiter, klappt alles auf und tippt jeden ungefährlichen Knopf einmal an –
     in Hell und Dunkel und in den Trainingsarten Kraft, Beides und „nur Ernährung“;
  2. Zufall: tippt, wählt und tippt Zahlen in zufälliger Reihenfolge (fester Seed → reproduzierbar).
Jeder Programmfehler (pageerror, console.error, Fehlerprotokoll der App) wird mit den letzten Schritten gemeldet.

Aufruf:  python3 app/tests/rundgang.py [--url http://localhost:8765/trainingslog/] [--seed 1] [--taps 400]
Exit-Code 1, wenn Fehler gefunden wurden.
"""
import argparse, datetime, json, random, re, sys
from playwright.sync_api import sync_playwright

SKIP = {"backup", "csvbody", "csvsets", "hfetch", "hpaste", "migrate", "reload", "repprint", "repshare", "scan",
        "pfadd", "pfdel", "pfswitch", "pfrename", "pfback", "lockretry", "updnow"}
DANGER = re.compile(r"del|^ckx$|^ckrx$|^errclr$|^corrreset$|^mcreset$|^wminus$|^dele$|^tdel$|^sdel$")


def seed_data(ttype="kraft", notrain=False):
    td = datetime.date.today(); D = lambda k: (td - datetime.timedelta(days=k)).isoformat(); T = td.isoformat()
    def ex(i, n, s, a, b, st): return {"id": "e%d" % i, "name": n, "sets": s, "repMin": a, "repMax": b, "step": st}
    days = [{"id": "dA", "name": "Oberkörper A", "exercises": [ex(1, "Bankdrücken", 3, 6, 10, 2.5), ex(2, "Langhantelrudern", 3, 8, 12, 2.5), ex(3, "Seitheben", 3, 12, 15, 1)]},
            {"id": "dB", "name": "Unterkörper A", "exercises": [ex(4, "Kniebeuge", 3, 6, 10, 2.5), ex(5, "Rumänisches Kreuzheben", 3, 8, 12, 2.5), ex(6, "Wadenheben", 3, 10, 15, 5)]}]
    d = {"plan": {"kind": "plan", "fav3": 1, "m58": 1, "days": days},
         "settings": {"kind": "settings", "phases": [{"type": "cut", "start": D(40), "goal": 84}], "sched": {},
                      "person": {"sex": "m", "year": 1990, "height": 180, "act": 1.55, "job": "mix", "tmin": 60, "tdays": [1, 3, 5],
                                 "ttype": ttype if ttype != "kraft" else None, "notrain": 1 if notrain else None}, "macro": None, "hide": []}}
    for k in range(60):
        d["b_" + D(k)] = {"kind": "body", "date": D(k), "weight": round(88 - (60 - k) * 0.05 + (k % 3) * 0.2, 1), **({"waist": 90 - k * 0.02} if k % 7 == 0 else {})}
    for k in range(1, 43, 2):
        day = days[(k // 2) % 2]
        d["w_" + D(k) + "_x"] = {"kind": "workout", "date": D(k), "dayId": day["id"], "dayName": day["name"], "updated": D(k) + "T18:00:00Z", "done": "18:40",
                                 "entries": [{"exId": e["id"], "name": e["name"], "sets": [{"w": 40 + i * 5 + (42 - k) * 0.3, "r": 8} for _ in range(3)]} for i, e in enumerate(day["exercises"])]}
    n = [None] * 24; n[5] = 140; n[7] = 200
    d["food"] = {"kind": "food", "v": 5, "fav": [], "meals": [{"id": "m1", "name": "Frühstück", "parts": [{"item": "f_oats", "amt": 80}]}], "scan": [],
                 "items": [{"id": "fdd3", "name": "Vitamin D3K2", "per": "st", "p": 0, "f": 0, "c": 0, "kcal": 0, "amt": 1, "cat": "Nahrungsergänzung", "n": n, "pack": 60, "stock": {"d": D(3), "c": 30, "full": 1}},
                           {"id": "fdcr", "name": "Creatin", "per": "g", "p": 0, "f": 0, "c": 0, "kcal": 0, "amt": 5, "cat": "Nahrungsergänzung", "pack": 500, "stock": {"d": T, "c": 40, "full": 0}}],
                 "daily": [{"id": "dl1", "item": "fdd3", "amt": 1, "from": D(10), "every": 3}, {"id": "dl2", "item": "fdcr", "amt": 5, "from": D(5)}, {"id": "dl3", "item": "f_v8_athmen", "amt": 7, "from": D(20)}],
                 "cooks": [{"id": "ck1", "name": "Hähnchen-Reis", "portions": 4, "date": D(1), "done": True, "left": 2, "parts": [{"item": "f_rice", "amt": 300}, {"item": "f_chick", "amt": 600}]}]}
    for k in range(10):
        d["n_" + D(k)] = {"kind": "nutri", "date": D(k), "entries": [{"id": "a%d" % k, "name": "Haferflocken 80 g", "p": 11, "f": 5, "c": 46, "kcal": 296, "t": "08:00"},
                                                                     {"id": "b%d" % k, "name": "Cola 330 ml", "p": 0, "f": 0, "c": 35, "kcal": 139, "t": "13:00", "ml": 330, "caf": 32}],
                          "water": [{"t": "09:00", "ml": 300}]}
    for k in (2, 6, 9):
        d["c_%s_r" % D(k)] = {"kind": "cardio", "date": D(k), "type": "run", "min": 35}
    return d


def run(url, seed, taps):
    rnd = random.Random(seed); problems = []
    with sync_playwright() as p:
        br = p.chromium.launch()
        for theme, ttype, notrain in [("light", "kraft", False), ("dark", "both", False), ("light", "kraft", True)]:
            ctx = br.new_context(viewport={"width": 440, "height": 956}, is_mobile=True, has_touch=False, locale="de-DE", color_scheme=theme, accept_downloads=False)
            pg = ctx.new_page(); log = []
            def bad(kind, msg):
                problems.append({"lauf": "%s/%s%s" % (theme, ttype, "/nurEssen" if notrain else ""), "art": kind, "meldung": msg[:500], "schritte": log[-8:]})
            pg.on("pageerror", lambda e: bad("pageerror", str(e) + "\n" + (e.stack or "")[:400]))
            pg.on("console", lambda m: m.type == "error" and not re.search(r"favicon|Failed to load resource|net::", m.text) and bad("console", m.text))
            pg.on("dialog", lambda d: d.accept())
            pg.goto(url); pg.wait_for_timeout(300)
            ver = pg.evaluate("window.TL_VER")
            pg.evaluate("""([d, v]) => { localStorage.clear(); indexedDB.deleteDatabase("trainingslog"); localStorage.setItem("trainingslog", JSON.stringify(d));
                localStorage.setItem("trainingslog-seen", String(v)); localStorage.setItem("trainingslog-tour-main", "1"); }""", [seed_data(ttype, notrain), ver])
            pg.reload(); pg.wait_for_timeout(800)

            def cands(scope="body", allow_danger=False):
                return pg.evaluate("""([sc, skip, dz]) => { const re = new RegExp(dz); const out = [];
                  document.querySelectorAll(sc + " [data-act], " + sc + " [data-tab]").forEach((b, i) => {
                    const r = b.getBoundingClientRect(); if (!r.width || !r.height || b.disabled || b.closest("[hidden]")) return;
                    const a = b.dataset.act || ""; if (skip.includes(a)) return; if (!""" + ("true" if allow_danger else "false") + """ && (re.test(a) || b.classList.contains("danger"))) return;
                    b.dataset.rg = String(i); out.push({ rg: String(i), key: a + "|" + (b.dataset.id || b.dataset.tab || "") + "|" + (b.textContent || "").trim().slice(0, 30) });
                  }); return out; }""", [scope, sorted(SKIP), DANGER.pattern])

            def tap(rg, key):
                log.append("tippe " + key)
                try: pg.click('[data-rg="%s"]' % rg, timeout=1500, force=True)
                except Exception as e: log.append("  (nicht tippbar)")
                pg.wait_for_timeout(60)

            def click(sel):
                try: pg.click(sel, timeout=1500, force=True); pg.wait_for_timeout(80); return True
                except Exception: log.append("  (%s nicht tippbar)" % sel); return False

            def close_overlays():
                for sel in ["[data-act=setclose]", "[data-act=newsok]", "[data-act=tourskip]", "[data-act=repclose]", "[data-act=partyx]", "#errtoast .et-x"]:
                    if pg.locator(sel).count():
                        try: pg.locator(sel).first.click(timeout=800, force=True)
                        except Exception: pass

            # 1. Rundgang
            tabs = pg.evaluate("[...document.querySelectorAll('.tabs button[data-tab]')].filter(b=>!b.hidden && b.offsetWidth).map(b=>b.dataset.tab)")
            for t in tabs:
                log.append("Reiter " + t); click('.tabs button[data-tab="%s"]' % t); pg.wait_for_timeout(120)
                done = set()
                for _ in range(90):
                    pg.evaluate("document.querySelectorAll('details:not([open])').forEach(d => { if (d.offsetParent) d.open = true; })")
                    c = [x for x in cands("#tab-" + t) if x["key"] not in done]
                    if not c: break
                    x = c[0]; done.add(x["key"]); tap(x["rg"], x["key"])
                    if pg.locator(".overlay, #setp, dialog[open]").count(): close_overlays()
                    cur = pg.evaluate("document.querySelector('.tabs button[aria-selected=true]')?.dataset.tab")
                    if cur != t and not click('.tabs button[data-tab="%s"]' % t): break
                close_overlays()
            # Einstellungen
            log.append("Einstellungen"); click("[data-act=setopen]")
            for x in cands("#setp")[:40]:
                if x["key"].startswith(("setnews", "settour", "sethelp", "setclose")): continue
                tap(x["rg"], x["key"])
                if not pg.locator("#setp").count(): click("[data-act=setopen]")
            close_overlays()

            # 2. Zufall
            for i in range(taps):
                kind = rnd.random()
                if kind < 0.12:
                    t = rnd.choice(tabs); log.append("Reiter " + t); click('.tabs button[data-tab="%s"]' % t); continue
                if kind < 0.30:
                    els = pg.evaluate("""() => { const o=[]; document.querySelectorAll('select, input:not([type=file]):not([type=checkbox]):not([type=search])').forEach((e,i)=>{ const r=e.getBoundingClientRect(); if(!r.width||e.disabled||e.closest('[hidden]')) return; e.dataset.rg='f'+i; o.push({rg:'f'+i, tag:e.tagName, type:e.type||'', n:e.options?e.options.length:0, id:e.id||e.name||Object.keys(e.dataset).join(',')}); }); return o; }""")
                    if els:
                        e = rnd.choice(els); sel = '[data-rg="%s"]' % e["rg"]
                        try:
                            if e["tag"] == "SELECT" and e["n"]:
                                v = pg.evaluate("([s,i]) => document.querySelector(s).options[i].value", [sel, rnd.randrange(e["n"])]); log.append("wähle %s = %s" % (e["id"], v)); pg.select_option(sel, v, timeout=1000)
                            elif e["type"] == "date":
                                v = (datetime.date.today() - datetime.timedelta(days=rnd.randrange(0, 30))).isoformat(); log.append("Datum %s = %s" % (e["id"], v)); pg.fill(sel, v, timeout=1000); pg.press(sel, "Tab")
                            elif e["type"] == "time":
                                v = "%02d:%02d" % (rnd.randrange(24), rnd.randrange(60)); log.append("Zeit %s = %s" % (e["id"], v)); pg.fill(sel, v, timeout=1000); pg.press(sel, "Tab")
                            else:
                                v = rnd.choice(["0", "1", "7,5", "120", "-3", "", "abc", "99999", "2.5"]); log.append("tippe in %s: %r" % (e["id"], v)); pg.fill(sel, v, timeout=1000); pg.press(sel, "Tab")
                        except Exception: log.append("  (Feld nicht bedienbar)")
                        pg.wait_for_timeout(60)
                    continue
                c = cands("body", allow_danger=rnd.random() < 0.15)
                if c:
                    x = rnd.choice(c); tap(x["rg"], x["key"])
                    if DANGER.search(x["key"].split("|")[0]): tap(x["rg"], x["key"] + " (bestätigen)")
                if i % 40 == 39: close_overlays()
            print("  Lauf %s/%s%s fertig: %d Schritte, bisher %d Meldungen" % (theme, ttype, "/nurEssen" if notrain else "", len(log), len(problems)), flush=True)
            errs = pg.evaluate("window.TLErrList ? window.TLErrList() : []")
            for e in errs:
                bad("app-protokoll", "%s @ %s (Reiter %s, %s×) %s" % (e.get("msg"), e.get("src"), e.get("tab"), e.get("n", 1), e.get("st", "")[:300]))
            ctx.close()
        br.close()
    seen, uniq = set(), []
    for pr in problems:
        k = pr["meldung"].split("\n")[0]
        if k in seen: continue
        seen.add(k); uniq.append(pr)
    if not uniq:
        print("Rundgang ok: keine Fehler (Seed %d, %d Zufallsschritte je Lauf)." % (seed, taps)); return 0
    print("%d Fehler gefunden:" % len(uniq))
    for pr in uniq:
        print("\n[%s] %s: %s\n  letzte Schritte: %s" % (pr["lauf"], pr["art"], pr["meldung"], " · ".join(pr["schritte"])))
    return 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--url", default="http://localhost:8765/trainingslog/"); ap.add_argument("--seed", type=int, default=1); ap.add_argument("--taps", type=int, default=400)
    a = ap.parse_args(); sys.exit(run(a.url, a.seed, a.taps))
