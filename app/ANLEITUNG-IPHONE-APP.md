# Trainingslog als iPhone-App (Testumgebung)

Die Web-App bleibt `index.html` im Hauptordner. Capacitor packt sie in eine echte iPhone-App.

## Einmalig einrichten (Terminal auf dem Mac)
```
cd ~
git clone https://github.com/massimoweinzettl-hash/trainingslog.git
cd trainingslog
npm install
npx cap add ios
npm run ios
```
`npm run ios` kopiert die Web-App nach `www/`, überträgt sie ins Xcode-Projekt und öffnet Xcode.

## In Xcode
1. Xcode → Settings → Accounts → „+“ → Apple ID anmelden.
2. Links „App“ anklicken → Ziel „App“ → Reiter „Signing & Capabilities“ → Team: „(Personal Team)“.
3. iPhone per Kabel anschließen, „Vertrauen“ bestätigen; Entwicklermodus einschalten (Einstellungen → Datenschutz & Sicherheit → Entwicklermodus, iPhone startet neu).
4. Oben in der Leiste das iPhone als Ziel wählen, ▶ drücken.
5. Beim ersten Start auf dem iPhone: Einstellungen → Allgemein → VPN & Geräteverwaltung → Entwickler-App vertrauen.

## Aktualisieren und alle 7 Tage neu signieren
```
cd ~/trainingslog
git pull
npm run ios
```
Dann in Xcode ▶ drücken. Die Daten in der App bleiben erhalten.

## Daten umziehen
Web-App: Daten → Sicherung → „Backup speichern“. iPhone-App: Daten → Sicherung → „Backup einspielen“.
Beide Apps speichern getrennt; nach dem Umzug nur noch in einer eintragen.
