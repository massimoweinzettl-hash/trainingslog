// Kopiert die Web-App (index.html und Zubehör) nach www/, das Capacitor in die iPhone-App packt.
// Gibt es schon das Xcode-Projekt (ios/), wird auch das App-Symbol eingesetzt.
import { mkdirSync, copyFileSync, rmSync, existsSync } from "node:fs";
const files = ["index.html", "manifest.webmanifest", "sw.js", "inter.woff2", "space-grotesk.woff2", "icon-192.png", "icon-512.png", "apple-touch-icon.png", "SCHRIFTEN-LIZENZ.txt"];
rmSync("www", { recursive: true, force: true });
mkdirSync("www");
for (const f of files) if (existsSync(f)) copyFileSync(f, "www/" + f);
const iconDir = "ios/App/App/Assets.xcassets/AppIcon.appiconset";
if (existsSync(iconDir)) { copyFileSync("app/AppIcon-1024.png", iconDir + "/AppIcon-512@2x.png"); console.log("App-Symbol eingesetzt"); }
console.log("www/ bereit: " + files.length + " Dateien");
