#!/usr/bin/env python3
"""Erzeugt die eingefrorene Freunde-Version unter freunde/ aus dem aktuellen Stand im Hauptordner.

Aufruf (im Hauptordner des Repos):  python3 app/freunde-build.py

Die Freunde-Version ist eine eigenständige Kopie (eigene index.html, sw.js, Manifest, Schriften, Bilder).
Sie ändert sich nur, wenn dieses Skript neu läuft und das Ergebnis hochgeladen wird – normale Versionen
der App fassen freunde/ nicht an. Der Update-Hinweis in der Kopie prüft freunde/index.html, meldet sich
bei den Freunden also erst nach einem solchen Lauf.

Getrennt von der Haupt-App (gleiche Adresse = gleicher Browser-Speicher):
- Speicher: alle Schlüssel, die Datenbank und der Kanal heißen „tlfreunde…“ statt „trainingslog…“,
  damit ein alter eingefrorener Stand nie die Daten einer neueren Haupt-App liest oder überschreibt.
- Offline-Cache: „tlfreunde-v<Version>“; der Service Worker räumt nur eigene alte Caches weg.
Gleich bleiben mit Absicht: Backup-Format (app: "trainingslog"), Plan-Code, Health-Format, Dateinamen –
Backups lassen sich also zwischen beiden Fassungen austauschen.

„Was ist neu?“: Die Freunde bekommen nicht die lange Einzelliste der Haupt-App, sondern eine kurze
Zusammenfassung aus app/freunde-neu.json (Wunsch des Nutzers, 17.11.). Für die Version, die gerade
eingefroren wird, muss dort ein Block stehen – sonst bricht das Skript ab.

Das Skript bricht ab, sobald im Code ein „trainingslog…“-Text auftaucht, den es nicht kennt
(z. B. ein neuer Speicherschlüssel) – dann unten in STORE oder KEEP eintragen.
"""
import json, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "freunde"
NEW = "tlfreunde"

# Texte in Anführungszeichen, die Speicher/Kanal/Datenbank benennen -> werden umbenannt.
STORE = {
    '"trainingslog"',             # Hauptdaten (localStorage), IndexedDB-Name, BroadcastChannel, Präfix im storage-Ereignis
    '"trainingslog-"',            # Präfix in keyFor/skey
    '"trainingslog-backup"',      # Reserve im alten Speicher
    '"trainingslog-profiles"', '"trainingslog-look"', '"trainingslog-seen"', '"trainingslog-tab"',
    '"trainingslog-planclosed"', '"trainingslog-calview"', '"trainingslog-tour-"',
    '"trainingslog-theme"', '"trainingslog-cvd"',  # v137/v138: Hell/Dunkel, Farbenblind-Modus
    '"trainingslog-errors"',  # v177: Fehlerprotokoll
}
# Texte, die bleiben müssen (Dateiformate und Dateinamen).
KEEP = {
    '"trainingslog-plan"', '"trainingslog-backup-"', '"trainingslog-bericht-"',
    '"trainingslog-saetze-"', '"trainingslog-koerper-"',
}
# "trainingslog" ist an diesen Stellen das Backup-Kennzeichen, nicht der Speicher.
BACKUP_MARK = ['o.app !== "trainingslog"', 'app: "trainingslog"']


def die(msg):
    sys.exit("freunde-build: " + msg)


def news_js(version):
    data = json.loads((ROOT / "app" / "freunde-neu.json").read_text(encoding="utf-8"))
    tabs = {"home", "train", "prog", "body", "plan", "data"}
    rows, have = [], False
    for blk in data["versionen"]:
        v = int(blk["v"])
        if v > version:
            continue
        have = have or v == version
        for pt in blk["punkte"]:
            if pt["tab"] not in tabs or not pt["text"].strip():
                die("freunde-neu.json: ungültiger Punkt bei v%d" % v)
            rows.append("    { v: %d, tab: %s, text: %s }" % (v, json.dumps(pt["tab"]), json.dumps(pt["text"], ensure_ascii=False)))
    if not have:
        die("freunde-neu.json: bitte erst einen kurzen Block für v%d eintragen (Zusammenfassung für die Freunde)" % version)
    return ",\n".join(rows)


def build_index(src):
    m = re.search(r"var APP_VERSION = (\d+);", src)
    if not m:
        die("APP_VERSION nicht gefunden")
    version = int(m.group(1))
    a = src.find("var CHANGES = [\n")
    b = src.find("\n  ];", a)
    if a < 0 or b < 0:
        die("CHANGES-Liste nicht gefunden")
    src = src[:a] + "var CHANGES = [ /* Freunde-Version: kurze Liste aus app/freunde-neu.json */\n" + news_js(version) + src[b:]
    cache = "%s-v%d" % (NEW, version)

    # Offline-Cache: Name muss zu sw.js passen.
    swc = re.findall(r'var SWC = "(trainingslog-v\d+)"', src)
    if len(swc) != 1:
        die("SWC nicht eindeutig gefunden")
    src = src.replace('var SWC = "%s"' % swc[0], 'var SWC = "%s"' % cache)

    # Backup-Kennzeichen schützen, dann Speichernamen umbenennen.
    for i, mark in enumerate(BACKUP_MARK):
        if src.count(mark) != 1:
            die("Backup-Kennzeichen %r erwartet 1×, gefunden %d×" % (mark, src.count(mark)))
        src = src.replace(mark, "\x00MARK%d\x00" % i)

    unknown = set()

    def swap(mo):
        lit = mo.group(0)
        if lit in STORE:
            return '"' + NEW + lit[len('"trainingslog'):]
        if lit in KEEP:
            return lit
        unknown.add(lit)
        return lit

    src = re.sub(r'"trainingslog[^"\n]*"', swap, src)
    if unknown:
        die("unbekannte Texte, bitte in STORE oder KEEP eintragen: " + ", ".join(sorted(unknown)))
    for i, mark in enumerate(BACKUP_MARK):
        src = src.replace("\x00MARK%d\x00" % i, mark)

    # Gegenprobe: kein Speicherzugriff darf noch den alten Namen tragen.
    for pat in (r'(?:localStorage|sessionStorage)\.\w+\("trainingslog', r'indexedDB\.\w+\("trainingslog',
                r'BroadcastChannel\("trainingslog', r'indexOf\("trainingslog'):
        if re.search(pat, src):
            die("Speicherzugriff mit altem Namen übrig: " + pat)

    note = "<!-- Freunde-Version: eingefrorener Stand v%d, erzeugt von app/freunde-build.py – nicht von Hand ändern. -->\n" % version
    head = "<!doctype html>\n"
    if not src.startswith(head):
        die("unerwarteter Dateianfang")
    return head + note + src[len(head):], version, cache, swc[0]


def build_sw(src, cache, old_cache):
    a = 'const CACHE = "%s";' % old_cache
    b = "keys.filter((k) => k !== CACHE)"
    if src.count(a) != 1 or src.count(b) != 1:
        die("sw.js sieht anders aus als erwartet (CACHE-Zeile oder Aufräumen)")
    src = src.replace(a, 'const CACHE = "%s";' % cache)
    # Nur eigene alte Caches löschen – der Cache der Haupt-App liegt unter derselben Adresse.
    src = src.replace(b, 'keys.filter((k) => k.indexOf("%s-") === 0 && k !== CACHE)' % NEW)
    return "/* Freunde-Version (eingefroren), erzeugt von app/freunde-build.py. */\n" + src


def main():
    index, version, cache, old_cache = build_index((ROOT / "index.html").read_text(encoding="utf-8"))
    sw_src = (ROOT / "sw.js").read_text(encoding="utf-8")
    sw = build_sw(sw_src, cache, old_cache)

    files = re.findall(r'"\./([^"]+)"', sw_src.split("const FILES = [", 1)[1].split("]", 1)[0])
    assets = [f for f in files if f != "index.html"]
    if "manifest.webmanifest" not in assets or len(assets) < 5:
        die("Dateiliste in sw.js nicht lesbar")

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    (OUT / "index.html").write_text(index, encoding="utf-8")
    (OUT / "sw.js").write_text(sw, encoding="utf-8")
    for f in assets:
        shutil.copyfile(ROOT / f, OUT / f)
    print("freunde/ bereit: Version %d, Cache %s, %d Dateien" % (version, cache, len(assets) + 2))


if __name__ == "__main__":
    main()
