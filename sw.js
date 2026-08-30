const CACHE_NAME = 'cs-notes-v20';

const ASSETS = [
  './',
  './index.html',
  './css/c-note-theme.css',
  './manifest.json',
  './app-icon.png',
  './icon-192.png',
  './icon-512.png',
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
  './subjects/cryptography/index.html',
  './subjects/genai_fluency/index.html',
  './subjects/Sheet 150/index.html',
];

// Install — pre-cache all pages
self.addEventListener('install', event => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(ASSETS))
  );
});

// Activate — delete old caches and claim clients immediately
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

// Fetch — Network first for all requests to ensure instant updates
self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;

  event.respondWith(
    fetch(event.request)
      .then(res => {
        if (res && res.status === 200 && res.type === 'basic') {
          const clone = res.clone();
          caches.open(CACHE_NAME).then(c => c.put(event.request, clone));
        }
        return res;
      })
      .catch(() => caches.match(event.request).then(r => r || caches.match('./index.html')))
  );
});
