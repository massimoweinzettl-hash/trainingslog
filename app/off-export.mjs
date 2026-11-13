// Lädt die in Deutschland am häufigsten gescannten Produkte von Open Food Facts (https://openfoodfacts.org, Lizenz ODbL)
// und speichert sie kompakt als trainingslog-produkte.json auf dem Schreibtisch. Aufruf: node app/off-export.mjs [Anzahl]
// Open Food Facts erlaubt etwa 10 Suchanfragen pro Minute, deshalb wartet das Skript zwischen den Seiten.
import { writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";

const WANT = Math.min(5000, Math.max(100, +(process.argv[2] || 3000)));
const PAGE = 100, WAIT = 7000;
const FIELDS = "code,product_name,product_name_de,brands,quantity,serving_quantity,nutriments,categories_tags,lang";
const UA = "Trainingslog/1.0 (private Trainings-App, einmaliger Export)";
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const urls = (p) => [
  `https://world.openfoodfacts.org/api/v2/search?countries_tags_en=germany&sort_by=unique_scans_n&page_size=${PAGE}&page=${p}&fields=${FIELDS}`,
  `https://world.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=countries&tag_contains_0=contains&tag_0=germany&sort_by=unique_scans_n&page_size=${PAGE}&page=${p}&json=1&fields=${FIELDS}`
];
async function getPage(p) {
  for (const u of urls(p)) {
    for (let t = 0; t < 3; t++) {
      try {
        const r = await fetch(u, { headers: { "User-Agent": UA } });
        if (r.status === 429) { console.log("  Zu viele Anfragen, warte 60 s …"); await sleep(60000); continue; }
        if (!r.ok) throw new Error("HTTP " + r.status);
        const j = await r.json();
        if (Array.isArray(j.products)) return j.products;
      } catch (e) { console.log(`  Seite ${p}: ${e.message}, neuer Versuch …`); await sleep(8000); }
    }
  }
  return null;
}
const num = (v) => (typeof v === "number" ? v : typeof v === "string" && v.trim() !== "" ? +v.replace(",", ".") : NaN);
const r1 = (v) => Math.round(v * 10) / 10;
const seen = new Set(), out = [];
let skipped = 0;
console.log(`Lade bis zu ${WANT} Produkte aus Deutschland (dauert etwa ${Math.ceil(WANT / PAGE * WAIT / 60000)} Minuten) …`);
for (let p = 1; out.length < WANT && p <= Math.ceil(WANT / PAGE) + 15; p++) {
  const list = await getPage(p);
  if (!list) { console.log("Abbruch: Open Food Facts antwortet nicht. Später noch einmal versuchen."); break; }
  if (!list.length) break;
  for (const x of list) {
    const code = String(x.code || "").replace(/\D/g, ""), n = x.nutriments || {};
    const name = String(x.product_name_de || x.product_name || "").replace(/\s+/g, " ").trim();
    const kcal = num(n["energy-kcal_100g"]), pr = num(n.proteins_100g), f = num(n.fat_100g), c = num(n.carbohydrates_100g);
    if (code.length < 8 || seen.has(code) || name.length < 2 || [kcal, pr, f, c].some((v) => !(v >= 0)) || kcal > 950 || pr > 100 || f > 100 || c > 100) { skipped++; continue; }
    const est = 4 * pr + 9 * f + 4 * c;
    if (Math.abs(est - kcal) > Math.max(25, kcal * 0.25)) { skipped++; continue; }
    const q = String(x.quantity || "").toLowerCase(), ml = /\d\s*(ml|cl|l)\b/.test(q) && !/\d\s*(g|kg)\b/.test(q);
    const sv = num(x.serving_quantity);
    seen.add(code);
    out.push([code, name.slice(0, 60), String(x.brands || "").split(",")[0].trim().slice(0, 30), ml ? "ml" : "g", r1(pr), Math.round(kcal), r1(f), r1(c), sv > 0 && sv <= 1000 ? Math.round(sv) : 100, x.lang === "de" || x.product_name_de ? 1 : 0]);
  }
  console.log(`Seite ${p}: ${out.length} Produkte übernommen, ${skipped} aussortiert`);
  if (out.length < WANT) await sleep(WAIT);
}
const file = join(homedir(), "Desktop", "trainingslog-produkte.json");
writeFileSync(file, JSON.stringify({ source: "Open Food Facts", license: "ODbL 1.0", url: "https://openfoodfacts.org", date: new Date().toISOString().slice(0, 10),
  fields: ["barcode", "name", "marke", "einheit", "eiweiss", "kcal", "fett", "kh", "portion", "deutsch"], products: out }));
console.log(`Fertig: ${out.length} Produkte in ${file}`);
