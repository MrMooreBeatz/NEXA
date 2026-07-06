const CACHE_NAME = "nexa-control-v1";
const ASSETS = [
  "/",
  "/static/css/nexa-control.css"
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    (async () => {
      const cache = await caches.open(CACHE_NAME);
      await cache.addAll(ASSETS);
      await self.skipWaiting();
    })()
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    (async () => {
      const keys = await caches.keys();
      await Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)));
      await self.clients.claim();
    })()
  );
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;
  if (req.url.includes("/api/")) {
    event.respondWith(
      (async () => {
        try {
          const res = await fetch(req);
          return res;
        } catch {
          return new Response(JSON.stringify({"ok": false, "offline": true}), {"content-type": "application/json"});
        }
      })()
    );
    return;
  }
  event.respondWith(
    (async () => {
      const cached = await caches.match(req);
      if (cached) return cached;
      try {
        const res = await fetch(req);
        if (res && res.status === 200) {
          const cache = await caches.open(CACHE_NAME);
          cache.put(req, res.clone());
        }
        return res;
      } catch {
        const fallback = await caches.match("/");
        if (fallback) return fallback;
        return new Response("Offline", {"headers": {"content-type": "text/plain"}});
      }
    })()
  );
});
