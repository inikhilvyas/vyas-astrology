// VYAS ASTRA High-Performance PWA Service Worker (v7.0 Turbo - Ultra Instant Launch)
const CACHE_NAME = 'vyas-astra-v2026-oauth2-fresh-3';
const STATIC_ASSETS = [
    '/',
    '/index.html',
    '/mobile/',
    '/mobile/index.html',
    '/manifest.json',
    '/favicon.ico',
    '/logo_icon.png',
    '/robots.txt',
    '/sitemap.xml',
    '/llms.txt'
];

// Install: Pre-cache core shell assets & skip waiting immediately
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

// Activate: Immediately purge all older cache generations (v1 to v6)
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((keys) => {
            return Promise.all(
                keys.map((key) => {
                    if (key !== CACHE_NAME) {
                        console.log('[SW] Deleting obsolete cache:', key);
                        return caches.delete(key);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

// Fetch: Ultra-Fast Network-First with Cache Fallback for HTML
self.addEventListener('fetch', (event) => {
    const req = event.request;
    const url = new URL(req.url);

    if (req.method !== 'GET') return;
    if (url.origin !== self.location.origin && !url.hostname.includes('fonts.g') && !url.hostname.includes('accounts.google.com')) {
        return;
    }

    // Cache-First for static assets (images, fonts, icons) -> 0ms instant render
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

    // Network-First for HTML document with 800ms timeout fallback to cache
    // This guarantees the user ALWAYS gets the fresh version instantly without lag
    if (req.destination === 'document' || url.pathname === '/' || url.pathname.endsWith('index.html')) {
        event.respondWith(
            new Promise((resolve) => {
                let resolved = false;
                const timeoutId = setTimeout(() => {
                    if (!resolved) {
                        caches.match(req).then((cached) => {
                            if (cached) {
                                resolved = true;
                                resolve(cached);
                            }
                        });
                    }
                }, 800);

                fetch(req).then((networkRes) => {
                    if (!resolved && networkRes && networkRes.status === 200) {
                        resolved = true;
                        clearTimeout(timeoutId);
                        const clone = networkRes.clone();
                        caches.open(CACHE_NAME).then((cache) => cache.put(req, clone));
                        resolve(networkRes);
                    }
                }).catch(() => {
                    if (!resolved) {
                        resolved = true;
                        clearTimeout(timeoutId);
                        caches.match(req).then((cached) => resolve(cached || new Response('Offline', { status: 503 })));
                    }
                });
            })
        );
        return;
    }

    // Default: Fetch from network, fallback to cache
    event.respondWith(
        fetch(req).catch(() => caches.match(req))
    );
});
