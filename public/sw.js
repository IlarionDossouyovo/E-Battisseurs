// E-Battisseurs Service Worker
const CACHE_NAME = 'ebattisseurs-v1';
const urls = [
  '/',
  '/index.html',
  '/cart.html',
  '/product.html',
  '/dashboard.html'
];

// Install
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(urls))
  );
});

// Fetch
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => response || fetch(event.request))
  );
});

// Activate
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => Promise.all(
      keys.map((key) => key !== CACHE_NAME && caches.delete(key))
    ))
  );
});