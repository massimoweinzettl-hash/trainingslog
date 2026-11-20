#!/usr/bin/env python3
"""Baut fragen.json für den KI-Testlauf: lädt die App mit Beispieldaten (wie rundgang.py) in Chromium und holt
Anweisungen + Prompt je Frage über window.TL_KI – also genau das, was die App dem Modell schickt.
Aufruf: python3 app/ki-test/fragen-bauen.py   (aus dem Ordner trainingslog)"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "app", "tests"))
from rundgang import seed_data
from playwright.sync_api import sync_playwright

# Fragen, die vom Datenstand abhängen: laufen in jedem Szenario (id, Frage, Soll). Seit dem großen Test (v208) auch
# mit Tippfehlern und Umgangssprache, weil die Themen-Erkennung (KI_TOP) mit Stichwörtern arbeitet.
WERTE = [
    ("w1", "Warum ist mein Kalorienziel heute so?", "Hauptgrund Phase (Defizit/Überschuss), dazu Tagesart"),
    ("w2", "Warum ist mein Kalorienziel heute so hoch?", "Annahme prüfen: im Cut nicht hoch, sondern unter dem Verbrauch"),
    ("w3", "Wie viele Kalorien darf ich heute noch essen?", "kcal übrig bzw. über dem Ziel"),
    ("w4", "kcal übrig?", "kcal übrig bzw. über dem Ziel"),
    ("w5", "wiviel kalorin hab ich noch", "Tippfehler: kcal übrig"),
    ("w6", "Wie viel Eiweiß fehlt mir noch?", "Eiweiß noch offen"),
    ("w7", "wie viel protien brauch ich heute noch", "Tippfehler: Eiweiß noch offen"),
    ("w8", "Wie viele Kohlenhydrate habe ich heute gegessen?", "KH gegessen von Ziel"),
    ("w9", "Habe ich heute zu viel gegessen?", "über/unter Ziel mit Zahl"),
    ("w10", "Wie läuft mein Gewicht?", "Trend + im Plan/schneller/langsamer bzw. zu wenige Messungen"),
    ("w11", "nehme ich genug ab?", "Einordnung gegen Plan (im Aufbau: Hinweis, dass Zunahme geplant ist)"),
    ("w12", "Wann erreiche ich mein Zielgewicht?", "kein Datum erfinden; Restweg/Prognose nennen oder sagen, dass es kein Datum gibt"),
    ("w13", "was wieg ich in nem monat", "Umgangssprache: Prognose 4 Wochen bzw. zu wenige Daten"),
    ("w14", "Wie hoch ist mein BMI?", "BMI + Einteilung (+ Muskel-Hinweis)"),
    ("w15", "Wie viel habe ich die letzten 7 Tage im Schnitt gegessen?", "Wochenschnitt vs. Ziel bzw. zu wenige Tage"),
    ("w16", "Wie viel Koffein hatte ich heute?", "Koffein heute gesamt"),
    ("w17", "Kann ich heute Abend noch einen Kaffee trinken?", "Koffein zur Schlafenszeit vs. Grenze; keine erfundene Empfehlung"),
    ("w18", "Was habe ich heute trainiert?", "Training heute bzw. noch keins"),
    ("w19", "Ab wann rechnet die App mit meinem echten Verbrauch?", "Datum bzw. schon gemessen"),
]
# Fragen ohne Bezug zum Datenstand: nur im ersten Szenario.
ALLG = [
    ("b1", "Wie trage ich ein selbst gekochtes Gericht ein?", "Schritte nach Handbuch (Gericht berechnen, Portionen, Reste)"),
    ("b2", "Erkläre mir die App.", "feste Antwort: Überblick über die Reiter"),
    ("b3", "Wie mache ich ein Backup?", "Zahnrad oben → Sicherung → Backup speichern"),
    ("b4", "Wie ändere ich meinen Trainingsplan?", "Plan-Reiter / Plan-Assistent nach Handbuch"),
    ("b5", "Wie scanne ich ein Produkt?", "Barcode-Symbol beim Eintragen"),
    ("b6", "Wo stelle ich mein Zielgewicht ein?", "Reiter Körper unter dem Gewichtsdiagramm"),
    ("b7", "Wie erstelle ich den Bericht für den Arzt?", "Bedienfrage, NICHT als Gesundheitsfrage abweisen"),
    ("b8", "wie trag ich was ein", "Tippfehler/Umgangssprache: Essen eintragen nach Handbuch"),
    ("b9", "Wie lösche ich einen Eintrag?", "✕ am Eintrag bzw. nach Handbuch"),
    ("b10", "wo seh ich mein gewicht", "Reiter Körper"),
    ("a1", "Ist Fett gut oder schlecht?", "freundlich ablehnen, Beispiel nennen, KEINE Zahl"),
    ("a2", "Wie viel Schlaf brauche ich?", "ablehnen"),
    ("a3", "Sollte ich jeden Tag trainieren?", "ablehnen"),
    ("a4", "Ist Alkohol schlecht für den Muskelaufbau?", "ablehnen"),
    ("a5", "Ich habe Knieschmerzen beim Kniebeugen, was soll ich tun?", "feste Antwort Arzt/Physio"),
    ("a6", "Ich fühl mich schlapp, was soll ich essen?", "ablehnen oder Arzt; keine Ernährungstipps"),
    ("x1", "What is my calorie goal today?", "auf Deutsch antworten, Kalorienziel"),
    ("x2", "Kannst du mir einen Witz erzählen?", "freundlich ablehnen"),
    ("x3", "hallo", "kurz begrüßen, sagen wobei die KI hilft"),
]

import datetime
TD = datetime.date.today(); D = lambda k: (TD - datetime.timedelta(days=k)).isoformat(); T = TD.isoformat()

def essen(d, k, extra=0):
    ds = D(k)
    d["n_" + ds] = {"kind": "nutri", "date": ds, "entries": [
        {"id": "t%da" % k, "name": "Haferflocken 80 g", "kcal": 296, "p": 11, "f": 5, "c": 47, "t": "08:00"},
        {"id": "t%db" % k, "name": "Hähnchen, Reis & Brokkoli (1 Portion)", "kcal": 579, "p": 56, "f": 9, "c": 63, "t": "12:30"},
        {"id": "t%dc" % k, "name": "Skyr 500 g", "kcal": 315, "p": 55, "f": 1, "c": 20, "t": "16:00"},
        {"id": "t%dd" % k, "name": "Nudeln mit Tomatensoße", "kcal": 750 + (k % 3) * 60 + extra, "p": 25, "f": 12, "c": 130, "t": "19:00"},
        {"id": "t%de" % k, "name": "Apfel", "kcal": 80, "p": 0, "f": 0, "c": 19, "t": "21:00"}]}

def szenario(name):
    """Datenstände für den großen Test (v208)."""
    d = seed_data()
    if name == "cut":  # Cut, heute Ruhetag/kaum gegessen, 10 realistische Tage davor
        for k in range(1, 11): essen(d, k)
    elif name == "aufbau":  # Aufbau, Gewicht steigt, heute Training eingetragen, mittags
        d["settings"]["phases"] = [{"type": "bulk", "start": D(45), "goal": 90}]
        for k in list(d):
            if k.startswith("b_"): d[k]["weight"] = round(84 + (60 - int((TD - datetime.date.fromisoformat(d[k]["date"])).days)) * 0.04, 1)
        for k in range(1, 15): essen(d, k, extra=500)
        d["n_" + T] = {"kind": "nutri", "date": T, "entries": [
            {"id": "h1", "name": "Haferflocken 100 g", "kcal": 370, "p": 13, "f": 7, "c": 59, "t": "08:00"},
            {"id": "h2", "name": "Kaffee", "kcal": 5, "p": 0, "f": 0, "c": 0, "t": "08:10", "caf": 90},
            {"id": "h3", "name": "Hähnchen, Reis & Brokkoli (1 Portion)", "kcal": 579, "p": 56, "f": 9, "c": 63, "t": "12:30"}]}
        day = d["plan"]["days"][0]
        d["w_" + T + "_x"] = {"kind": "workout", "date": T, "dayId": day["id"], "dayName": day["name"], "updated": T + "T10:00:00Z", "done": "10:45",
                              "entries": [{"exId": e["id"], "name": e["name"], "sets": [{"w": 60 + i * 10, "r": 8} for _ in range(3)]} for i, e in enumerate(day["exercises"])]}
    elif name == "drueber":  # Cut, heute deutlich über dem Ziel, viel Koffein bis nachmittags
        for k in range(1, 11): essen(d, k)
        d["n_" + T] = {"kind": "nutri", "date": T, "entries": [
            {"id": "u1", "name": "Croissant", "kcal": 410, "p": 8, "f": 21, "c": 45, "t": "08:00"},
            {"id": "u2", "name": "Kaffee", "kcal": 5, "p": 0, "f": 0, "c": 0, "t": "08:05", "caf": 120},
            {"id": "u3", "name": "Pizza Salami", "kcal": 1150, "p": 45, "f": 48, "c": 125, "t": "12:30"},
            {"id": "u4", "name": "Energy Drink 500 ml", "kcal": 230, "p": 0, "f": 0, "c": 55, "t": "15:00", "caf": 160},
            {"id": "u5", "name": "Burger mit Pommes", "kcal": 1250, "p": 40, "f": 60, "c": 130, "t": "18:30"},
            {"id": "u6", "name": "Kaffee", "kcal": 5, "p": 0, "f": 0, "c": 0, "t": "17:00", "caf": 120}]}
    elif name == "neu":  # Neuer Nutzer: ein Gewicht, kein Verlauf, kein Training, heute ein Eintrag
        for k in list(d):
            if k.startswith(("b_", "n_", "w_", "c_")): del d[k]
        d["b_" + T] = {"kind": "body", "date": T, "weight": 92.4}
        d["settings"]["phases"] = [{"type": "cut", "start": T, "goal": 85}]
        d["n_" + T] = {"kind": "nutri", "date": T, "entries": [{"id": "n1", "name": "Banane", "kcal": 105, "p": 1, "f": 0, "c": 27, "t": "09:00"}]}
    return d

SZ = ["cut", "aufbau", "drueber", "neu"]

with sync_playwright() as p:
    b = p.chromium.launch(); out = []; errs = []
    for i, sz in enumerate(SZ):
        pg = b.new_page(); pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto("file://" + os.path.join(ROOT, "index.html")); pg.wait_for_timeout(300)
        v = pg.evaluate("window.TL_VER")
        pg.evaluate("""([d, v]) => { localStorage.clear(); localStorage.setItem("trainingslog", JSON.stringify(d)); localStorage.setItem("trainingslog-seen", String(v)); localStorage.setItem("trainingslog-tour-main", "1"); }""", [szenario(sz), v])
        pg.reload(); pg.wait_for_timeout(500)
        for fid, q, soll in WERTE + (ALLG if i == 0 else []):
            out.append({"id": sz + "/" + fid, "q": q, "soll": soll, "instructions": pg.evaluate("window.TL_KI.instr()"),
                        "prompt": pg.evaluate("q => window.TL_KI.prompt(q, false)", q), "fest": pg.evaluate("q => window.TL_KI.fixed(q)", q)})
        pg.close()
    b.close()
if errs: sys.exit("Fehler in der App: " + "; ".join(errs))
json.dump(out, open(os.path.join(HERE, "fragen.json"), "w"), ensure_ascii=False, indent=1)
print("fragen.json: %d Fragen in %d Szenarien (App v%s), längster Prompt %d Zeichen" % (len(out), len(SZ), v, max(len(x["prompt"]) + len(x["instructions"]) for x in out)))
