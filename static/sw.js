/* Service Worker for FreeMovieSearcher - PWA Caching Strategy */

const CACHE_VERSION = 'v1.0.0';
const CACHE_NAME = `freemoviesearcher-${CACHE_VERSION}`;

const STATIC_CACHE = [
    '/',
    '/static/style.css',
    '/static/favicon-clapper-modern.svg',
    '/offline.html'
];

const CACHE_STRATEGIES = {
    images: 'cache-first',
    api: 'network-first',
    pages: 'network-first',
    static: 'cache-first'
};

// Install event - cache static assets
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(STATIC_CACHE))
            .then(() => self.skipWaiting())
    );
});

// Activate event - clean old caches
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys()
            .then(cacheNames => {
                return Promise.all(
                    cacheNames
                        .filter(name => name !== CACHE_NAME)
                        .map(name => caches.delete(name))
                );
            })
            .then(() => self.clients.claim())
    );
});

// Fetch event - intelligent caching strategy
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);

    // Skip non-GET requests
    if (request.method !== 'GET') return;

    // API requests - network first
    if (url.pathname.startsWith('/recommend') || 
        url.pathname.startsWith('/search') || 
        url.pathname.startsWith('/popular')) {
        event.respondWith(networkFirst(request));
        return;
    }

    // Images - cache first
    if (request.destination === 'image') {
        event.respondWith(cacheFirst(request));
        return;
    }

    // Static assets - cache first
    if (url.pathname.startsWith('/static/')) {
        event.respondWith(cacheFirst(request));
        return;
    }

    // HTML pages - network first
    if (request.headers.get('accept').includes('text/html')) {
        event.respondWith(networkFirst(request));
        return;
    }

    // Default - network first
    event.respondWith(networkFirst(request));
});

// Cache first strategy
async function cacheFirst(request) {
    const cache = await caches.open(CACHE_NAME);
    const cached = await cache.match(request);
    
    if (cached) {
        return cached;
    }

    try {
        const response = await fetch(request);
        if (response.ok) {
            cache.put(request, response.clone());
        }
        return response;
    } catch (error) {
        return new Response('Offline', { status: 503 });
    }
}

// Network first strategy
async function networkFirst(request) {
    const cache = await caches.open(CACHE_NAME);

    try {
        const response = await fetch(request);
        if (response.ok) {
            cache.put(request, response.clone());
        }
        return response;
    } catch (error) {
        const cached = await cache.match(request);
        if (cached) {
            return cached;
        }
        
        // Return offline page for HTML requests
        if (request.headers.get('accept').includes('text/html')) {
            return cache.match('/offline.html');
        }
        
        return new Response('Network error', { status: 503 });
    }
}

// Background sync for API requests
self.addEventListener('sync', (event) => {
    if (event.tag === 'sync-recommendations') {
        event.waitUntil(syncRecommendations());
    }
});

async function syncRecommendations() {
    // Placeholder for background sync logic
    console.log('Background sync triggered');
}
