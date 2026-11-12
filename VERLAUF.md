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
