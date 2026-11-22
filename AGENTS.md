# AGENTS.md – Arbeitsstand und Regeln für KI-Assistenten

Diese Datei ist der gemeinsame Stand für alle KI-Assistenten, die an diesem Repo arbeiten (Claude, ChatGPT/Codex). **Zuerst lesen, bei jeder Änderung mitpflegen.** Kurz halten: nur der aktuelle Stand, keine Geschichte (die steht in `VERLAUF.md`). Das Repo ist öffentlich – hier nichts Persönliches eintragen.

**Stand:** v262 (22.11.2026)

## Vor jeder Arbeit
1. `git pull` und `git log --oneline -15`: Hat der andere Assistent seit dem letzten Mal etwas geändert? Dann diese Änderungen zuerst durchsehen und Auffälligkeiten dem Besitzer melden, nicht ungefragt im fremden Bereich umbauen.
2. Diese Datei lesen. Für Details zu einer Funktion die passende Zeile in `VERLAUF.md` suchen (`grep`), nicht die ganze Datei.

## Nach jeder Änderung
- `APP_VERSION` in `index.html` +1 und ein Eintrag in `CHANGES` (`{ v, tab, text }`, `tab` = `home` | `train` | `prog` | `body` | `plan`; kurzer, verständlicher Satz für den Nutzer – erscheint unter „Was ist neu?“).
- Eine Zeile in `VERLAUF.md` (technisch: was, wo, welche Funktionen).
- Handbuch `HELP` in `index.html` anpassen, wenn sich Bedienung ändert (ggf. auch `TOUR` = Rundgang und `KI_HOW`).
- **Diese Datei aktualisieren:** Stand-Zeile oben, betroffene Abschnitte, Erledigtes aus „Offen“ streichen.
- Jede Version einzeln committen; `main` wird über GitHub Pages veröffentlicht.

## Arbeitsweise mit dem Besitzer
- Die App wird fast nur auf dem iPhone (17 Pro Max) genutzt: **platzsparend**, nichts doppelt anzeigen, lieber vorhandene Listen/Auswahlen erweitern als neue Knöpfe.
- **Aussehen und Bedienung erst abstimmen:** Bei Farben, Anordnung, Wegfall oder neuen Symbolen vorher fragen bzw. 2–3 Varianten zeigen. Eindeutige Fehler und klar beschriebene Kleinigkeiten direkt umsetzen.
- Größere Umbauten in kleinen Schritten, jede Version wird vom Besitzer auf dem iPhone geprüft.
- **Weniger Dauertext:** sichtbar nur Ergebnisse, Aufforderungen, Warnungen (möglichst eine Zeile). Erklärungen und Rechenwege hinter das blaue i (`tip(id, Frage, Text)` bzw. `ib(id)` + `itx(id, Text)`).
- **Ehrlich statt geschönt:** Rechnungen realistisch, Vereinfachungen offen benennen, aber nicht verkomplizieren.
- **Offline zuverlässig:** Alles Wesentliche ohne Internet; Online-Abfragen (Open Food Facts) nur als Zusatz, Ergebnisse lokal speichern.
- **Auswahlrad statt Tippen** für Werte mit festen Stufen (`selWheel`, `<select>`), nicht beim Satz-Eintragen und bei Essensmengen.
- **Zahlenfelder** bekommen `inputmode="decimal"` bzw. `"numeric"`: Dann markiert die App beim Antippen den vorhandenen Wert automatisch (v253), die Eingabe ersetzt ihn; nach dem ersten Tippen wird nicht erneut markiert (v258). Neue Zahlenfelder immer mit `inputmode` anlegen.
- Antworten an den Besitzer auf Deutsch, kurz; Terminal-Befehle als kopierbaren Codeblock.

## Technik
- **Alles in `index.html`** (HTML, CSS, JS in einer IIFE, kein Build). Einzige Bibliothek: `zxing.min.js` (Barcode). `sw.js` = Service Worker (Offline-Cache, Updates). Schriften und Icons im Repo.
- **Daten nur lokal** (IndexedDB „trainingslog“ + Journal in localStorage, Reserve im alten localStorage). Schreiben nur über `put()`/`persist()`. Bestehende Daten müssen nach Updates lesbar bleiben (Migrationen); neue Felder auch in der Import-Prüfung (`importText`/`clean`) erlauben.
- Docs: `workout` (`w_<Datum>_<Tag>`), `body` (`b_<Datum>`), `nutri` (`n_<Datum>`, Einträge mit `p`, `kcal`, `f`, `c`, `n` = Nährstoffvektor nach `NUTK`, `it`/`amt` = Lebensmittel und Menge), `settings`, `food` (eigene Lebensmittel, Favoriten, Meal Prep, Präparate, Gerichte), `cardio` (`c_<Datum>_<id>`), `plan`.
- **Farben nur über CSS-Tokens** (`:root`, Dunkel-Blöcke, Design-Blöcke `data-look`/`data-skin`). Makros: Protein `--pr` Orange, Fett `--m-f` Gelb, Kohlenhydrate `--m-c` Neon Mint, Koffein `--caf` Lila.
- Klick-Handler reagiert auf `button[data-act]`; Ausnahmen mit eigenem Zweig davor (`[data-eat]`, `.nutrow[data-ns]`).
- Lebensmittel: Bibliothek `FOODLIB` im Code, Nährstoffe `NUTR` (Bundeslebensmittelschlüssel 4.0), Markenprodukte `PROD` (Open Food Facts). Eigene Lebensmittel ohne Nährstoffwerte nutzen die Bibliothekswerte gleichen Namens (`nutSrc`/`nutTwin`).
- Keine persönlichen Daten in den Code. Keine fremden Bilder; Piktogramme und Symbole sind eigene SVGs.
- **iPhone-App:** Capacitor (`package.json`, `capacitor.config.json`, `app/copy-web.mjs`); `ios/`, `www/`, `node_modules/` nur lokal beim Besitzer. Lokale KI „Frag die App“ nur dort (Plugin `app/ki-plugin`, Apples On-Device-Modell); in der Web-App kein KI-Knopf.
- **Freunde-Version** `freunde/`: eingefrorene Kopie, nur auf ausdrückliche Ansage des Besitzers neu erzeugen (`python3 app/freunde-build.py`, Zusammenfassung in `app/freunde-neu.json`).

## Tests
- Playwright/Chromium in iPhone-Größe (440 × 956, Touch, hell und dunkel) über `file:///…/index.html`.
- `app/tests/rundgang.py`: Beispieldaten (`seed_data()`) und Zufallstest, z. B. `python3 app/tests/rundgang.py --url file:///<pfad>/index.html --seed 1 --taps 150`.
- In eigenen Tests `localStorage["trainingslog-seen"]` auf die aktuelle Version und `trainingslog-tour-main` = "1" setzen, sonst stören „Was ist neu?“ bzw. Einrichtung.
- Vor dem Veröffentlichen den Weg des Nutzers selbst durchklicken, nicht nur die neue Funktion.

## Aufbau der App
- **Reiterleiste bleibt oben** (Reiter unten wurde in v255 getestet und vom Besitzer verworfen).
- **Kopfzeile:** oben links Zahnrad (Einstellungen), KI-Knopf (nur iPhone-App), Glocke (Hinweise, neue Version); rechts Status und Versionsnummer.
- **Reiter:** Ernährung · Training · Fortschritt · Körper · Plan (Wischen zwischen Reitern).
  - **Ernährung** mit Bereichen Heute · Lebensmittel · Meal Prep (Gerichte eingeklappt als Zeile, `S.mpEx`, Aktion `fmtog`) · Supplemente · Vorrat. *Heute:* Koffein, Trinken, Kalorien und Makros, Eintragen (Suche, Scan, Schätzen, Gericht berechnen), Liste nach Mahlzeiten (Frühstück, Mittag, Abendessen, Snacks; automatisch nach Uhrzeit `mzAuto`, fest über `e.mz`; je Gruppe einklappbar, Merker `trainingslog-mzopen` (Heute f|m|a|s, Rückblick rf|rm|ra|rs); Verschieben per Gedrückthalten + Ziehen oder Auswahl im Eintrag; Tagessumme bleibt), Vitamine & Mineralstoffe (Zeile antippen = Quellen), Essen im Rückblick (immer offen, Nachtragen für frühere Tage).
  - **Training:** Kalender, Einheit eintragen, Übungen ersetzen/hinzufügen, Training beenden; Ausdauer.
  - **Fortschritt:** Kraft nach Körperbereichen (Körperkarte), Verlauf je Übung, Rekorde, Ausdauer.
  - **Körper** mit Bereichen wie Ernährung (seit v257, `BSEC`, `S.bodySec`, Start „Übersicht“): Übersicht (Gewichtskorridor, Phase/Ziel, Eintragen) · Messungen (Verläufe, Tabelle) · Phasen · Kalorien (Tabelle, Makroverteilung) · Angaben. Alle Blöcke bleiben im DOM, sichtbar ist nur der Bereich (`data-bsec` je Block, `#tab-body[data-sec]`); neue Blöcke im Körper brauchen ein `data-bsec`. Sprünge in einen Bereich über `bodySecGo(sec)`.
  - **Plan:** Sätze pro Muskelgruppe, Trainingstage, Plan teilen/Plan-Code, Assistent, Übungskatalog.
- **Zahnrad:** Design, Hell/Dunkel, Farbenblind, Haptik, Trainingsart; Daten & Hilfe (Sicherung, Export, Bericht, Profile, Hilfe, Was ist neu?).
- **Modi:** Kraft, Ausdauer (ohne Plan), beides, „Nur Ernährung“ (nur Ernährung und Körper) – `TABS_FOOD`/`TABS_CARDIO`.
- **Designs:** Standard, Magerquark (`data-skin="quark"`, hell), Hähnchen, Reis & Brokkoli (`data-skin="huhn"`, hell, seit v259), Gym Kawaii (`data-skin="kawaii"`, folgt Hell/Dunkel, seit v261; Küken-Szenen je Reiter über `html[data-tab]`/`html[data-bsec]`, Zeichnungen aus `app/design/kueken-gen.py`), Aurora, Diät (`data-look="hell"`), Aufbau (`data-look="winter"`). Designs mit eigenem `data-skin` stehen in `SKINS` (Wert = erzwungenes Hell/Dunkel oder "" = folgt der Einstellung); interne Kennungen nicht umbenennen (Merker beim Nutzer).
- **Rundgang** (`TOUR`): Willkommen → Ernährung → Training → Fortschritt → Körper → Plan → Zahnrad → Einstellungen.

## Offen
- **Rundgang (v241–v246):** (1) „Zahnrad oben rechts“ ist seit v256 behoben; (2) Station „Fortschritt“ erscheint im Modus „Nur Ernährung“, obwohl der Reiter fehlt; (3) Start aus einem anderen Ernährungsbereich lässt diesen offen, die Karte erklärt aber „Heute“. Der Besitzer entscheidet, wer das behebt.
- Markenprodukte ohne Nährstoffwerte (z. B. Haferflocken einer Marke) haben keine Ballaststoffe/Vitamine – Übernahme vom Grundlebensmittel angeboten, nicht beauftragt.
- Kohlenhydrat-Mint und das Grün abgehakter Supplemente liegen nah beieinander – Besitzer prüft.
