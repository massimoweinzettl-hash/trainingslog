# Verlauf

Archiv der Änderungen und Entscheidungen. Wird nur bei Bedarf gelesen. Neue Einträge unten anhängen.
Repo ist öffentlich: hier nur technische Entscheidungen, keine persönlichen Daten.

## 10.11.2026
- v1–2: Grundgerüst (PWA, `index.html`, offline per `sw.js`)
- v3: Abfrage „Wer trainiert?“ (Profile), Markierung von Neuerungen
- v4: Gewichtsvorschlag bei unterschiedlichen Gewichten pro Satz
- v5: Kalender im Reiter Fortschritt
- v6: Block „Kalorien und Makros“ im Reiter Körper
- v7: Kalorienbedarf pro Tag im Kalender, Trainings- und Ruhetage
- v8: Plan-Code zum Einfügen von Plan-Änderungen
- v9: Übungsauswahl im Plan, Phasenbalken im Kalender
- v10: Trainingstage im Plan einklappbar
- v11: Kalender blättert in künftige Monate, Phasenbalken nur bis heute
- v12: Trainings im Kalender einplanen
- v13: Ansicht „Alle Übungen“ im Plan
- v14: Phasen klarer, Trainingstage gelten sofort
- v15: größerer Übungskatalog, Zuordnung zu Trainingstagen in der Übungsliste
- v16: Symbole für Übungen nach Muskelgruppe

## 11.11.2026
- v17: Reihenfolge der Übungen im Trainingstag anpassbar
- v18: Reiter Start als Dashboard
- v19: Zielkorridor in Phasenfarbe, Datumsachse mit Vorschau
- v20: Gewichtskurve mit jedem Tag als Datum und Hilfslinie
- v21: Symbole in den Reitern
- v22: Suchfeld in „Alle Übungen“ mit Löschen-Knopf
- v23: Körperwerte-Formular neu angeordnet, Datumsfelder begrenzt
- v24: Zielgewicht für Cut und Aufbau
- v25: Ringdiagramm mit Tageskalorien und Makroverteilung im Start
- v26: Makros einstellbar, Gewichtswerte in der Kurve, Ring-Legende unter dem Ring
- v27: Hinweise außerhalb des Korridors, Korridor neu starten
- v28: Kalender in den Reiter Training verschoben
- v29: Kraft seit Phasenstart, Sätze pro Muskelgruppe, Rekorde, Krafttest, Sterne, Schwerpunktübungen
- v30: Übungen löschen oder zusammenführen
- v31: Defizit und Verbrauch heute im Dashboard
- v32: eigene SVG-Piktogramme je Bewegungsart (Entscheidung: keine fremden Bilder, Repo ist öffentlich)
- v33: Katalog anpassen, Übungen aus- und einblenden
- v34: Bewertung mit drei Stufen (Okay, Mittel, Sehr gut), später zu Sternen 1–3
- v35: Trainingstage aufgeräumt, Piktogramme für Sitz- und Stehvarianten
- v36: Aufwärmsätze für jede Übung, Langhantel mit fortlaufendem Scheibenaufbau
- v37: Scheiben im Studio, Aufwärmsätze mit vorhandenen Scheiben
- v38: Aufwärmsätze vereinfacht, Scheibenverwaltung entfernt (Entscheidung: Scheibenplanung zu aufwendig, nur Rundung auf 5 / 2,5 kg)
- v39: Erklärtexte hinter einem i-Symbol
- v40: Essen heute – Eiweiß und Kalorien mit festen Mahlzeiten und Schätzungen

## 12.11.2026
- Veröffentlichung von v40 erneut angestoßen; seitdem nach jedem Push den Pages-Lauf prüfen
- v41: Kalender auf Start, Stammdaten in Daten, Essen mit Auswahlmenü und Uhrzeit, „Was ist neu?“ nach Versionen
- v42: kompakte Kalorienzeile, Gewichtsverlauf auf Start, Lebensmittel-Datenbank mit Gruppen und Suche
- Arbeitsweise: Projektnotizen enthalten nur noch den aktuellen Stand; Geschichte steht hier und in alten Chats
- v43: Gewicht und KFA aus Apple Health per Kurzbefehl „Trainingslog Health“ (Zwischenablage, Knopf „Einfügen“; je Tag früheste Messung, vorhandene Werte bleiben). Keine tägliche Automation, weil sie die Zwischenablage überschreiben würde. `VERLAUF.md` angelegt.
- v44: Start: Ring und „Essen heute“ zu einem Block „Heute“ zusammengelegt (Ladebalken „Noch … kcal“, Eiweißbalken, Fett/KH nur als Ziel, weil Lebensmittel nur Eiweiß und kcal kennen). Aufwärmsätze bleiben offen. Krafttest: Zeile „Test“ markiert und mit Testgewicht vorbelegt; Testsatz zählt nicht für den Gewichtsvorschlag (übrige Sätze gelten ab `sets − 1` als vollständig).
- v45: Kopf des Blocks „Heute“ nach Entwurf des Nutzers: Datum (+ Trainings-/Ruhetag) und Phasen-Pille oben, „Noch … kcal“ und Protein groß mit Balken (Protein orange, Token `--pr`), Tagesdefizit und Verbrauch als zwei Kacheln. Fett/KH-Zielzeile entfällt (steht im Reiter Körper). Eigene Strich-Icons (`ICONS`, `ic()`).
- v46: Fett und Kohlenhydrate: Lebensmittel mit `f`/`c` (food.v 3, Migration ergänzt vorbelegte, eigene als „Fett/KH fehlt“ markiert), Einträge speichern `f`/`c`, Schätzungen grob 40 % Fett/60 % KH der übrigen kcal. Block „Heute“: Kalorienbalken in Makrofarben (grau = ohne Angabe), Protein/Fett/KH als Zahlen „gegessen / Ziel“ (Protein-Balken entfällt auf Wunsch), Defizit und Verbrauch in einer kleinen Zeile.
- v47: Krafttest bei jeder Übung (Knopf „Krafttest“ neben „+ Satz“ bei Nicht-Schwerpunkt-Übungen, gleiche Logik, `testBox()`); Fortschritt listet auch getestete Nicht-Schwerpunkt-Übungen, „fällig“-Erinnerung nur für Schwerpunkt.
- v48: Übungen außerhalb des Plans: „+ Übung für heute“ (Position wählbar), „Ersetzen“ nur für heute (Rückgängig stellt die ursprüngliche wieder her), Häkchen „auch in den Plan übernehmen“ (gleiche Stelle). Eigene Liste der Einheit als `exs` im Trainingseintrag; Einträge ohne Sätze zählen nirgends als Training. Katalog: „Latzug Maschine“. Piktogramm `rowmachine` mit Brustpolster für „Rudern Maschine“ (Kabel-Variante behält `rowcable`).

## 12.11.2026 – unabhängige Prüfung (Fable) und Korrekturen
- v49: Befunde der Prüfung behoben: Körperwerte mit Grenzen (Gewicht 20–400, KFA 2–75, Umfänge 10–250) und Rückfrage bei > 5 % Gewichtssprung; Test-Einheit nur mit Testsatz zählt nicht für den Vorschlag; „Letzter Test“ = 1RM des Testsatzes (`testE1`); Korridor-/Phasenbasis `phaseBasePoint` (Messung max. 7 Tage vor Start, sonst erste Messung danach, Korridor beginnt dort); voller Speicher → bleibende Warnung + erneuter Speicherversuch; Training über Mitternacht bleibt offen („Auf heute wechseln“); Essen nach Mitternacht ohne Fehler; Rückgängig/Ersetzen-Fehler; Plan ohne Doppelung beim Zurücktauschen; `fav3` in neuen Plänen; 0-kg-Übungen ohne kg-Vorschlag, kein NaN; Health-Knöpfe nur auf iPhone/iPad, nicht erkannte Zeilen werden gemeldet; Update-Hinweis „Neu laden“ (Prüfung von `index.html?fresh=…`, SW lässt `fresh` durch, Cache v2).
- v50: Katalog „Hohes Rudern Maschine“ (Piktogramm `highrow`: aufrecht, Oberschenkelpolster, Hebel von vorne oben). Klimmzüge und Dips neu gezeichnet: Seitenansicht mit Zusatzgewicht senkrecht am Gürtel vorne, Dips in der unteren Position (Nutzer macht beide nur mit Zusatzgewicht).

## 13.11.2026 – Speicher-Umzug nach IndexedDB (zwei Fable-Prüfungen)
- v51: Neuer Speicher IndexedDB (DB „trainingslog“, Stores `docs` mit Schlüssel `<Profil>|<Doc>` und `meta` je Profil). Umzug erst nach Backup (Karte auf Start und unter Sicherung, alternativ „Ohne Backup umziehen“): kopieren, zurücklesen, jedes Doc vergleichen, dann umschalten. Merker `trainingslog-idb-<Profil>`, Journal `trainingslog-jrnl-<Profil>` (jede Änderung synchron, danach IndexedDB; beim Laden übergelegt), alter Speicher 28 Tage als Reserve (mit Stempel `_at`/`_m`), Löschung erst nach Abgleich. Antwortet IndexedDB nicht: Sperrhinweis statt Rückfall auf den alten Speicher. Leerer neuer Speicher: Wiederherstellung aus der Reserve, sonst Hinweis „Backup einspielen“. Ohne IndexedDB weiter localStorage. Erste Prüfung fand 4 kritische Abläufe mit Datenverlust (Rückfall bei hängender IDB, tote Verbindung, Reserve zu früh gelöscht) und Profilwechsel-Fehler → Architektur mit Journal/Merker/Sperre; zweite Prüfung: alle behoben, ein neuer Fall (Umzug gemeldet gescheitert, Meta doch geschrieben) und Kleineres behoben (Zeitlimit bricht Transaktion ab, Nachholen mit wachsendem Abstand, Ladefehler mit Hinweis, Eingabesperre beim Laden).
- v52: Start aufgeräumt: Gewichtsblock (Korridor) nur noch unter Körper, auf Start bleibt ein kleiner Block „Apple Health“ (nur iPhone/iPad); Block „Schwerpunkt“ (`focusBlock()`) ganz oben unter Fortschritt. Im Training trägt der Krafttest-Knopf der Schwerpunktübung „Krafttest fällig · heute markieren“ (Klasse `due`), wenn der letzte Test 28 Tage her ist. Neue Piktogramme `pendulum` (Drehachse vor dem Gesicht, Pendelarm zum Rückenpolster, Scheibe hinten auf Kopfhöhe, Füße vorn auf schräger Platte) und `sissy` (nach Foto des Nutzers, ohne Gewicht), Hilfsfunktion `O()` für Gestellkreise. Speicher: Wiederherstellung aus der Reserve nur mit Merker oder Reserve-Stempel, sonst normaler Umzug; Speicherwarnungen bleiben jetzt auch beim Reiterwechsel stehen.
- v53: Suche wortweise (`qWords`/`qMatch`), Treffer fett (`hl()`, `b.hl`) in `tpResults`, `exListHtml`, `foodListHtml` und den neuen Essen-Suchen. Essen-Eintragen auf Start und „+ Zutat“ als Suchfeld mit Trefferliste (`.cbq`/`cbResults`, Schlüssel "ni" bzw. "fp:<Mahlzeit>", Auswahl `niSel()`), `#ni-sel` und `foodOpts` entfernt. Ersetzen: Häkchen `#tpmove` verschiebt Sätze (`moveSets`), Übungen schon in der Einheit erscheinen als „schon in der Einheit“ (`tpgo`, springt hin, nimmt Sätze mit), ausgeblendete Katalog-Übungen lassen sich wieder anlegen. Maschinenübungen (`MACH`) im Katalog und in der Vorlage 5–8 Wdh.; Karte `m58Card` auf Start fragt einmal nach dem Umstellen vorhandener, Merker `plan.m58` (auch in `clean`).
- v54: Plan: Namensfeld des Trainingstags nur nach „Umbenennen“ (`S.dayRen`, Aktion `dayren`), sonst eine kleine Zeile „Umbenennen · Tag löschen“ (`.dayacts`).
- v55: Plan zeigt je Übung nur Nummer, Bild, Name mit „Einstellungen“, ↑ ↓ und ✕ in einer Zeile (`.pl2`); Felder Sätze/Wdh./Schritt dort entfernt (bleiben unter Daten → Übungen).
- v56: Plan-Assistent (`PAT` Bewegungsmuster mit Kandidaten m/f, `DAYT` Tagestypen, `SPLITS`/`SPLIT_REC`, `WIZ_N` Übungen je Dauer, `wizBuild`/`wizSwap`/`wizApply`, Zustand `S.wiz`; Übungen gleichen Namens werden wiederverwendet). Plan: Wochenübersicht `planVol`/`volChips` (`.pvol`), je Tag `dayMin` + Sätze (`.dmeta`), „Duplizieren“ (`daydup`), „Verschieben“ (`exmv`/`exmvto`, `S.exMv`), Vorschläge als erste Gruppe in `pick-<Tag>` (`pickSugs`). Training ohne Plan: „Plan erstellen lassen“ (`wizstart`).
- v57: Körperfett-Schätzung `kfaEst()` (Waage ≤ 60 Tage → Maßband Navy-Methode mit Taille/Hals/[Hüfte] → Körperbau `BUILD` aus `person.build`), Grundumsatz dann Katch-McArdle (370 + 21,6 × fettfreie Masse), sonst Mifflin. Neue Messfelder `neck`, `hip` in `BF`. Erhaltung aus Essenseinträgen `intakeLog()` (≤ 28 Tage, Tage ≥ 50 % Grundumsatz, mind. 14 Tage und 70 % erfasst), sonst feste Angabe. Hinweis `buildHint` bei > 5 % Gewichtsänderung seit Wahl (`person.buildW`), Aktion `gome`.
- v58: Handbuch `HELP` (Daten → Bereich „help“, `helpHtml`, `<details class="hsec">`), DSEC jetzt 5 Bereiche. Einführung `TOUR` (6 Schritte, Karte `#tour`, `tourShow`/`tourEnd`, Merker `trainingslog-tour-<Profil>` in localStorage, nur bei Profil ohne Plan-Tage, Trainings und Messungen; `tourDue` in `afterLoad`), Schritt Plan öffnet den Assistenten. Aktionen `tournext`/`tourprev`/`tourskip`/`tourstart`.
- (nach v58, ohne Versionssprung): Capacitor 8 für die iPhone-App: `package.json` (Skripte `web`, `ios`), `capacitor.config.json` (appId `io.github.massimoweinzettl.trainingslog`, webDir `www`), `app/copy-web.mjs`, `app/ANLEITUNG-IPHONE-APP.md`; `ios/`, `www/`, `node_modules/` in `.gitignore`. `topNotice`: Capacitor gilt als installiert.
- v59: Einführung hebt den beschriebenen Bereich hervor (`TOUR[i][3]` liefert Elemente, `tourMark` setzt `.tfocus`, `body.tfocusing` graut/verwischt den Rest per `:has`, `tourWatch` setzt nach Neuzeichnen wieder), kurzer Zoom `.tzoom` nur beim Schrittwechsel (aus bei reduzierter Bewegung). iPhone-App: `app/AppIcon-1024.png`, `copy-web.mjs` setzt es ins Xcode-Projekt, falls `ios/` existiert.
- v60: Einführung startet auch bei `switchProfile` (neues/leeres Profil) und bei Auswahl im „Wer trainiert?“-Dialog; beim Wechsel zu einem Profil mit Daten wird eine laufende Einführung ohne Merker geschlossen (`tourHide`). Vorher lief die Prüfung nur in `afterLoad`, das beim Profilwechsel nicht aufgerufen wird.
- v61: „Kraft nach Körperbereichen“ ersetzt `strengthBlock` alt: `strengthData` (je Übung 1RM-Schnitt erste/letzte zwei Einheiten im Zeitraum `S.strP` phase|3m|6m|all, Standard 6m; ohne Gewicht/Krafttests ausgeschlossen; Gruppen und Ober-/Unterkörper nach Einheiten gewichtet), `bodyMap` (SVG vorne/hinten), `regionTrend` (Wochenindex, 3-Wochen-Glättung). Testdatensatz-Generator lag in /home/claude/work/gen_testperson.py (nicht im Repo).
- v62: Körperkarte im Lehrbuch-Stil: `BM_F`/`BM_B` (linke Hälfte, gespiegelt) mit Einträgen [Gruppe | "" Grundmuskel | "T" Sehne, Pfad, Faserwinkel]; Fasern als SVG-Pattern `bmh<Winkel+180>`, Schattierung `bmsh` (radial), Silhouette in `--ms-gap`. Farbe `color-mix(--heat-hi k%, --heat-lo)`, k = pct/30; Tokens `--heat-*`, `--ms-*`, `--tendon`, `--fib`. Legende `.heatleg`.
- v63: Zeitraffer `bmAt`/`bmStop` (`S.bmWeeks` wöchentliche Stichtage ab erster Einheit + 14 Tage, `strengthData(to)`, nur `#strmapw` = `strMapHtml` wird neu gezeichnet, Play 220 ms/Woche, Regler `#bmt`); `HEAT_MAX` 20, `heatCol`; `regionTrend` mit wählbaren Linien `STRL`/`S.strL` (Unterkörper = Beine, keine eigene Beine-Linie), Höhe 230, Farben `--s2`…`--s6`.
- v64: „Essen im Rückblick“ unter Körper (`#eatbox`, `eatBlock`/`eatData`/`eatChart`/`eatDay`): Zeitraum `S.eatP` (1m|3m|6m|all, Standard 3m), Tagesbalken, ab 5 Wochen Linie Wochenschnitt (Wochen mit ≥ 3 erfassten Tagen); eine Tippfläche, Tag aus Klickposition; Ziel je Tag `dayKcal` (geglättet), über Ziel ab +10 %; Lücken ≥ 2 Tage ohne Eintrag grau, ab 5 Tagen Gewichtsänderung (Schnitt 7 Tage davor/danach); Gewicht 7-Tage-Mittel auf zweiter Achse; Tippen auf `[data-eat]` (eigener Zweig im Klick-Handler) bzw. ‹ › (`eatd`) zeigt Einträge des Tages (`S.eatSel`). Testdatensatz: Essen ab zweitem Cut, 12 Tage Urlaub ohne Einträge.
- v65: Essen im Rückblick immer Tagesbalken + Wochenschnitt-Linie `.ewk` ab 35 Tagen; Tippen über eine Fläche `.ehit` (Tag aus Klickposition); ausgewählter Tag in `--accent`.
- v66: Einrichtung für neue Profile (`#setup`, `startIntro`/`setupShow`/`setupRead`/`setupCheck`/`setupSave`, Zustand `SU`, Aktionen `sux`/`sunext`/`suprev`/`suskip`/`sutour`): Willkommen → Über dich → Körper (Gewicht/KFA heute, Körperbau) → Alltag (Aktivität, Trainingstage) → Ziel (Phase ab heute, Zielgewicht) → Empfehlung; danach Rundgang ab `TOUR[1]` (`tourFrom`, Zähler „Rundgang · x von 5“). Ersetzt `tourShow(0)` an allen `tourDue`-Stellen; „Alles überspringen“ speichert gültige Angaben und setzt den Tour-Merker.
- v66: Eiweiß über `E.pw` (Gewicht bei 15 % bzw. 25 % KFA mit gleicher fettfreier Masse, nur wenn kleiner als Gewicht und KFA-Schätzung vorhanden); `macros` erhält `E.pw`.
- v67: Alltag und Training getrennt: `JOB` (sit/mix/feet/hard, 1,25/1,4/1,55/1,75), `TMIN` (30/45/60/90), `actOf` = Alltag + 0,06 × Trainingstage × Dauer/60; gespeichert `act` (berechnet) + `job` + `tmin` (Import-Prüfung erweitert). Alte Profile ohne `job` behalten `act`, Hinweis im Formular. Einrichtung jetzt 5 Schritte (Alltag und Training getrennt).
- v68: „Plan ändern“ (`planedit`) als Link hinter den Tag-Chips im Reiter Training → Plan mit offenem Assistenten; `wizStart` nimmt Tage aus `person.tdays` (2–6) vor der Plan-Tagzahl; Plan-Reiter: Knopf „Plan neu erstellen“, Hinweis bei Abweichung Trainingstage ↔ Plan-Tage; `.linkbtn`-Regel der Einrichtung auf `.suhead` begrenzt.
- v69: `FOOD_V4` (55 Lebensmittel: Schwein, Wurst/Aufschnitt, Milchprodukte, Brot/Brötchen, Gemüse, Fette, neue Gruppe „Fertiges & Süßes“ an FCATS-Index 6 vor „Eigene“), an `FOOD0` angehängt; `food.v` 4: Migration ergänzt aus v2/v3 nur fehlende (Kennung und Name), Import akzeptiert v4.
- v70: Eiweiß-Vorschau im Kalorienbalken (`.sg.pg`, Token `--pg-op`): offenes Eiweiß × 5 kcal als blasser Abschnitt nach dem Gegessenen, bis zum Ziel gekappt; reicht es darüber, `.gov` rötlich; Text in `#tip-gap` angehängt.
- v71: Lebensmittel-Bibliothek `FOOD_V5` (226) + `FOOD0`/`FOOD_V4` = `FOODLIB` (318), `LIBMAP`; nur im Code. `foodItem` fällt auf Bibliothek zurück, `ownItem` kopiert beim Bearbeiten, `foodAll` für Suchen (eigene vor Bibliothek, ohne Doppelte). Favoriten `food.fav` (`fstar`, ★ in Suche und Liste, oben in der leeren Suche). Neue Kategorie „Getränke“. food.v 5: unveränderte Bibliothekseinträge aus `items` entfernt, geänderte bleiben „eigen“; „Auf Bibliothek zurücksetzen“. Mahlzeiten `portions` (1–50, `mealPortion`), Eintrag „(1 Portion)“. Import: `fav`, `portions`, Mahlzeit-Teile mit Bibliotheks-IDs.
