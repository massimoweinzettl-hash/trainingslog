// Kopiert die Web-App (index.html und Zubehör) nach www/, das Capacitor in die iPhone-App packt.
// Gibt es schon das Xcode-Projekt (ios/), wird auch das App-Symbol eingesetzt.
import { mkdirSync, copyFileSync, rmSync, existsSync, readFileSync, writeFileSync } from "node:fs";
const files = ["index.html", "manifest.webmanifest", "sw.js", "inter.woff2", "space-grotesk.woff2", "icon-192.png", "icon-512.png", "apple-touch-icon.png", "SCHRIFTEN-LIZENZ.txt", "zxing.min.js", "ZXING-LIZENZ.txt", "koerperkarte.png", "koerperkarte-licht.jpg",
  "maskottchen/quark-home.png", "maskottchen/quark-train.png", "maskottchen/quark-prog.png", "maskottchen/quark-body.png", "maskottchen/quark-plan.png",
  "maskottchen/quark-nacht-home.png", "maskottchen/quark-nacht-train.png", "maskottchen/quark-nacht-prog.png", "maskottchen/quark-nacht-body.png", "maskottchen/quark-nacht-plan.png",
  "maskottchen/quark-morgen-home.png", "maskottchen/quark-morgen-train.png", "maskottchen/quark-morgen-prog.png", "maskottchen/quark-morgen-body.png", "maskottchen/quark-morgen-plan.png",
  "maskottchen/quark-mittag-home.png", "maskottchen/quark-mittag-train.png", "maskottchen/quark-mittag-prog.png", "maskottchen/quark-mittag-body.png", "maskottchen/quark-mittag-plan.png",
  "maskottchen/quark-kaffee-home.png", "maskottchen/quark-kaffee-train.png", "maskottchen/quark-kaffee-prog.png", "maskottchen/quark-kaffee-body.png", "maskottchen/quark-kaffee-plan.png"];
rmSync("www", { recursive: true, force: true });
mkdirSync("www");
mkdirSync("www/maskottchen");   // v265: Quark-Maskottchen
for (const f of files) if (existsSync(f)) copyFileSync(f, "www/" + f);
const iconDir = "ios/App/App/Assets.xcassets/AppIcon.appiconset";
if (existsSync(iconDir)) { copyFileSync("app/AppIcon-1024.png", iconDir + "/AppIcon-512@2x.png"); console.log("App-Symbol eingesetzt"); }
// Kamera für den Barcode-Scan: iOS verlangt eine Begründung in der Info.plist, sonst stürzt die App beim Kamerazugriff ab.
const plist = "ios/App/App/Info.plist";
if (existsSync(plist)) {
  const p = readFileSync(plist, "utf8");
  if (!p.includes("NSCameraUsageDescription")) {
    const i = p.lastIndexOf("</dict>");
    writeFileSync(plist, p.slice(0, i) + "\t<key>NSCameraUsageDescription</key>\n\t<string>Zum Scannen von Barcodes auf Lebensmitteln.</string>\n" + p.slice(i));
    console.log("Kamera-Berechtigung in Info.plist eingetragen");
  }
}
console.log("www/ bereit: " + files.length + " Dateien");
