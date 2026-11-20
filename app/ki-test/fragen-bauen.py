#!/usr/bin/env python3
"""Baut fragen.json für den KI-Testlauf: lädt die App mit Beispieldaten (wie rundgang.py) in Chromium und holt
Anweisungen + Prompt je Frage über window.TL_KI – also genau das, was die App dem Modell schickt.
Aufruf: python3 app/ki-test/fragen-bauen.py   (aus dem Ordner trainingslog)"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "app", "tests"))
from rundgang import seed_data
from playwright.sync_api import sync_playwright

# (id, Frage, was eine gute Antwort tun soll)
FRAGEN = [
    ("w1", "Warum ist mein Kalorienziel heute so?", "Ruhetag, Defizit zum Abnehmen; Zahlen aus der Einordnung"),
    ("w2", "Warum ist mein Kalorienziel heute so hoch?", "Annahme richtigstellen: liegt unter dem Verbrauch (Defizit)"),
    ("w3", "Wie viel Eiweiß fehlt mir heute noch?", "Zahl 'Eiweiß noch', keine erfundenen Anzeigen"),
    ("w4", "Wie läuft mein Gewicht gerade?", "Trend + Einordnung (im Plan), ggf. Restweg"),
    ("w5", "Liege ich im Plan?", "Einordnung Gewicht wiedergeben"),
    ("w6", "Wie hoch ist mein BMI?", "BMI-Wert + Einteilung + Hinweis Muskelmasse"),
    ("w7", "Wie viel wiege ich in 4 Wochen?", "Prognose-Zahl aus Daten, als Schätzung"),
    ("w8", "Wie viel muss ich noch abnehmen?", "Restweg zum Zielgewicht"),
    ("w9", "Wie viel habe ich diese Woche im Schnitt gegessen?", "Wochenschnitt + Ziel im Wochenschnitt"),
    ("w10", "Wie viele Kalorien habe ich heute noch übrig?", "Noch offen kcal"),
    ("w11", "Was habe ich heute gegessen?", "Einträge von heute"),
    ("w12", "Wie viel Koffein habe ich noch im Körper?", "Koffein jetzt + zur Schlafenszeit"),
    ("w13", "Warum bekomme ich an Trainingstagen mehr Kalorien?", "Ruhetag/Trainingstag-Erklärung mit beiden Werten, Wochenschnitt gleich"),
    ("w14", "Wie viel Fett darf ich heute noch essen?", "Fett gegessen von Ziel; Rest nur, wenn nicht neu gerechnet – sonst beide Zahlen nennen"),
    ("w15", "Ab wann rechnet die App mit meinem echten Verbrauch?", "Datum/Stand aus der Verbrauch-Zeile bzw. dass schon gemessen wird"),
    ("b1", "Wie trage ich ein selbst gekochtes Gericht ein?", "Schritte nach Handbuch (Gericht berechnen, Portionen, Reste)"),
    ("b2", "Erkläre mir die App.", "Kurzer Überblick über die Reiter aus dem Handbuch"),
    ("b3", "Wie mache ich ein Backup?", "Daten → Sicherung → Backup speichern"),
    ("b4", "Wie ändere ich meinen Trainingsplan?", "Plan-Reiter / Plan-Assistent nach Handbuch"),
    ("b5", "Wie scanne ich ein Produkt?", "Barcode-Symbol beim Eintragen"),
    ("b6", "Wo stelle ich mein Zielgewicht ein?", "nach Handbuch, sonst ehrlich auf Handbuch verweisen"),
    ("a1", "Ist Fett gut oder schlecht?", "freundlich ablehnen, Beispiel nennen, KEINE Zahl"),
    ("a2", "Wie viel Schlaf brauche ich?", "ablehnen, keine Zahl"),
    ("a3", "Sollte ich jeden Tag trainieren?", "ablehnen, keine Kalorien"),
    ("a4", "Wofür sind Ballaststoffe gut?", "ablehnen"),
    ("a5", "Ich habe Knieschmerzen beim Kniebeugen, was soll ich tun?", "kurz auf Arzt/Physio verweisen, keine Diagnose"),
    ("b7", "Wie erstelle ich den Bericht für den Arzt?", "Bedienfrage, NICHT als Gesundheitsfrage abweisen"),
    ("x1", "What is my calorie goal today?", "auf Deutsch antworten, Kalorienziel"),
    ("x2", "Kannst du mir einen Witz erzählen?", "freundlich ablehnen"),
]

def testdaten():
    """Beispieldaten wie rundgang.py, dazu realistische Essens-Tage (ca. 2.200 kcal) der letzten 10 Tage, damit
    Wochenschnitt und Verbrauch plausibel sind (bei 435 kcal/Tag griffen Apples Schutzregeln)."""
    import datetime
    d = seed_data(); td = datetime.date.today()
    for k in range(1, 11):
        ds = (td - datetime.timedelta(days=k)).isoformat()
        d["n_" + ds] = {"kind": "nutri", "date": ds, "entries": [
            {"id": "t%da" % k, "name": "Haferflocken 80 g", "kcal": 296, "p": 11, "f": 5, "c": 47},
            {"id": "t%db" % k, "name": "Hähnchen, Reis & Brokkoli (1 Portion)", "kcal": 579, "p": 56, "f": 9, "c": 63},
            {"id": "t%dc" % k, "name": "Skyr 500 g", "kcal": 315, "p": 55, "f": 1, "c": 20},
            {"id": "t%dd" % k, "name": "Nudeln mit Tomatensoße", "kcal": 750 + (k % 3) * 60, "p": 25, "f": 12, "c": 130},
            {"id": "t%de" % k, "name": "Apfel", "kcal": 80, "p": 0, "f": 0, "c": 19}]}
    return d

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file://" + os.path.join(ROOT, "index.html")); pg.wait_for_timeout(300)
    v = pg.evaluate("window.TL_VER")
    pg.evaluate("""([d, v]) => { localStorage.clear(); localStorage.setItem("trainingslog", JSON.stringify(d)); localStorage.setItem("trainingslog-seen", String(v)); localStorage.setItem("trainingslog-tour-main", "1"); }""", [testdaten(), v])
    pg.reload(); pg.wait_for_timeout(500)
    out = [{"id": i, "q": q, "soll": s, "instructions": pg.evaluate("window.TL_KI.instr()"), "prompt": pg.evaluate("q => window.TL_KI.prompt(q, false)", q), "fest": pg.evaluate("q => window.TL_KI.fixed(q)", q)} for i, q, s in FRAGEN]
    b.close()
if errs: sys.exit("Fehler in der App: " + "; ".join(errs))
json.dump(out, open(os.path.join(HERE, "fragen.json"), "w"), ensure_ascii=False, indent=1)
print("fragen.json: %d Fragen (App v%s), längster Prompt %d Zeichen" % (len(out), v, max(len(x["prompt"]) + len(x["instructions"]) for x in out)))
