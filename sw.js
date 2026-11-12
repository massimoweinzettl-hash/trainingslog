/* Trainingslog – Service Worker: macht die App offline nutzbar.
   Antwortet aus dem Cache und holt im Hintergrund die neue Fassung. Anfragen mit dem Parameter „fresh“
   (Versionsprüfung der App) gehen direkt ans Netz. CACHE nur ändern, wenn sich FILES ändert. */
const CACHE = "trainingslog-v2";
const FILES = [
  "./",
  "./index.html",
  "./manifest.webmanifest",
  "./icon-192.png",
  "./icon-512.png",
  "./apple-touch-icon.png",
  "./inter.woff2",
  "./space-grotesk.woff2"
];

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE).then((c) => c.addAll(FILES)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

/* Sofort aus dem Cache antworten, im Hintergrund die neue Fassung holen.
   Eine aktualisierte App erscheint dadurch beim übernächsten Öffnen. */
self.addEventListener("fetch", (event) => {
  const req = event.request;
  const url = new URL(req.url);
  if (req.method !== "GET" || url.origin !== self.location.origin || url.searchParams.has("fresh")) return;
  event.respondWith((async () => {
    const cache = await caches.open(CACHE);
    const hit = await cache.match(req, { ignoreSearch: true });
    const fresh = fetch(req).then((res) => {
      if (res.ok) cache.put(req, res.clone());
      return res;
    });
    if (hit) { event.waitUntil(fresh.catch(() => {})); return hit; }
    return fresh;
  })());
});
