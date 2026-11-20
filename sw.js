// VYAS ASTRA Service Worker - Web Push & Background Sync v14
'use strict';

self.addEventListener('install', (event) => {
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((keys) => {
            return Promise.all(keys.map((k) => caches.delete(k)));
        }).then(() => self.clients.claim())
    );
});

// Network-only for all requests - ensures zero stale cache
self.addEventListener('fetch', (event) => {
    event.respondWith(fetch(event.request));
});

// ----------------------------------------------------------------------
// VYAS ASTRA PUSH NOTIFICATION ENGINE (DAILY PANCHANG, FESTIVALS & VRAT)
// ----------------------------------------------------------------------
self.addEventListener('push', (event) => {
    let data = {
        title: 'व्यास दैनिक पंचांग व शुभ मुहूर्त',
        body: 'आज का पंचांग, अभिजीत मुहूर्त एवं राहुकाल देखें।',
        icon: '/logo_icon.png',
        badge: '/logo_icon.png',
        data: { url: '/#daily' }
    };

    if (event.data) {
        try {
            data = Object.assign(data, event.data.json());
        } catch (e) {
            data.body = event.data.text();
        }
    }

    const options = {
        body: data.body,
        icon: data.icon || '/logo_icon.png',
        badge: data.badge || '/logo_icon.png',
        vibrate: [100, 50, 100],
        data: data.data || { url: '/#daily' },
        actions: [
            { action: 'open', title: 'पंचांग देखें' },
            { action: 'close', title: 'बंद करें' }
        ]
    };

    event.waitUntil(
        self.registration.showNotification(data.title, options)
    );
});

self.addEventListener('notificationclick', (event) => {
    event.notification.close();
    if (event.action === 'close') return;

    const targetUrl = (event.notification.data && event.notification.data.url) ? event.notification.data.url : '/#daily';

    event.waitUntil(
        clients.matchAll({ type: 'window', includeUncontrolled: true }).then((clientList) => {
            for (let i = 0; i < clientList.length; i++) {
                const client = clientList[i];
                if ('focus' in client) {
                    client.navigate(targetUrl);
                    return client.focus();
                }
            }
            if (clients.openWindow) {
                return clients.openWindow(targetUrl);
            }
        })
    );
});
