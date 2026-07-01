const CACHE_NAME = 'cs-notes-v10';

const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './favicon.svg',
  './subjects/system_design/index.html',
  './subjects/oops/index.html',
  './subjects/computer_networks/index.html',
  './subjects/operating_systems/index.html',
  './subjects/dsa_basics/index.html',
  './subjects/dsa_advanced/index.html',
  './subjects/api_design/index.html',
  './subjects/git_github/index.html',
  './subjects/machine_learning_ai/index.html',
  './subjects/dbms/index.html',
];

// Install — pre-cache all pages
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(ASSETS))
      .then(() => self.skipWaiting())
  );
});

// Activate — delete old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

// Fetch — network first for navigation, cache first for assets
self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);

  // Navigation requests: try network, fall back to cache
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request)
        .then(res => {
          // Cache the fresh page
          const clone = res.clone();
          caches.open(CACHE_NAME).then(c => c.put(event.request, clone));
          return res;
        })
        .catch(() => caches.match(event.request).then(r => r || caches.match('./index.html')))
    );
    return;
  }

  // Assets: cache first, then network
  event.respondWith(
    caches.match(event.request).then(cached => {
      if (cached) return cached;
      return fetch(event.request).then(res => {
        if (!res || res.status !== 200 || res.type === 'opaque') return res;
        const clone = res.clone();
        caches.open(CACHE_NAME).then(c => c.put(event.request, clone));
        return res;
      }).catch(() => caches.match('./index.html'));
    })
  );
});
