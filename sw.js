/* ツリツリバースト：オフラインでも あそべるようにする しくみ
   ------------------------------------------------------------
   「ネットがあれば いつも 最新／なければ 前に見たもの」の やりかた。
   キャッシュを 先に返す やりかたにすると、新しい版を 出しても
   古いままに なりやすいので、わざと 通信を 先に する。 */
const V = 'tsuri-v10-1';

self.addEventListener('install', () => self.skipWaiting());

self.addEventListener('activate', e => {
  e.waitUntil((async () => {
    for (const k of await caches.keys()) if (k !== V) await caches.delete(k);
    await self.clients.claim();
  })());
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  if (new URL(req.url).origin !== self.location.origin) return;
  e.respondWith((async () => {
    try {
      const res = await fetch(req);
      if (res && res.ok) (await caches.open(V)).put(req, res.clone());
      return res;
    } catch (err) {
      const hit = await caches.match(req);
      if (hit) return hit;
      // トップページを 見にきて 通信も キャッシュも ないとき
      if (req.mode === 'navigate') {
        const top = await caches.match('./');
        if (top) return top;
      }
      throw err;
    }
  })());
});
