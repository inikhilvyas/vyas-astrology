// VYAS ASTRA High-Performance PWA Service Worker (v2.0)
const CACHE_NAME = 'vyas-astra-v2';
const STATIC_ASSETS = [
    '/',
    '/index.html',
    '/manifest.json',
    '/favicon.ico',
    '/logo_icon.png',
    '/robots.txt',
    '/sitemap.xml',
    '/llms.txt'
];

// Install: Pre-cache core shell assets
self.addEventListener('install', (event) => {
    self.skipWaiting();
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(STATIC_ASSETS).catch((err) => {
                console.warn('[SW] Pre-caching partial fail:', err);
            });
        })
    );
});

// Activate: Purge old cache generations & claim clients immediately
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((keys) => {
            return Promise.all(
                keys.map((key) => {
                    if (key !== CACHE_NAME) {
                        return caches.delete(key);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

// Fetch: Stale-While-Revalidate for HTML, Cache-First for static assets
self.addEventListener('fetch', (event) => {
    const req = event.request;
    const url = new URL(req.url);

    // Skip non-GET requests or WebSocket / Streamlit stream requests
    if (req.method !== 'GET') return;
    if (url.origin !== self.location.origin && !url.hostname.includes('fonts.g') && !url.hostname.includes('raw.githubusercontent.com')) {
        return;
    }

    // Cache-First for Static Assets (Images, Icons, Fonts)
    if (
        req.destination === 'image' ||
        req.destination === 'font' ||
        url.pathname.endsWith('.png') ||
        url.pathname.endsWith('.ico') ||
        url.pathname.endsWith('.woff2')
    ) {
        event.respondWith(
            caches.match(req).then((cached) => {
                if (cached) return cached;
                return fetch(req).then((res) => {
                    if (res && res.status === 200) {
                        const resClone = res.clone();
                        caches.open(CACHE_NAME).then((cache) => cache.put(req, resClone));
                    }
                    return res;
                });
            })
        );
        return;
    }

    // Stale-While-Revalidate for HTML shell (Instant 0ms launch + background sync)
    if (req.destination === 'document' || url.pathname === '/' || url.pathname.endsWith('index.html')) {
        event.respondWith(
            caches.match(req).then((cached) => {
                const fetchPromise = fetch(req).then((networkRes) => {
                    if (networkRes && networkRes.status === 200) {
                        const clone = networkRes.clone();
                        caches.open(CACHE_NAME).then((cache) => cache.put(req, clone));
                    }
                    return networkRes;
                }).catch(() => cached);
                return cached || fetchPromise;
            })
        );
        return;
    }

    // Network with cache fallback for everything else
    event.respondWith(
        fetch(req).catch(() => caches.match(req))
    );
});
