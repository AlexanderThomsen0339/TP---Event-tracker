import { registerRoute } from 'workbox-routing'
import { NetworkFirst } from 'workbox-strategies'
import { CacheableResponsePlugin } from 'workbox-cacheable-response'
import { ExpirationPlugin } from 'workbox-expiration'

// Cache kun det specifikke API-endpoint, du bruger
registerRoute(
  ({ url }) => url.pathname === '/api/events/get_users_within_radius',
  new NetworkFirst({
    cacheName: 'events-api-cache',
    plugins: [
      new CacheableResponsePlugin({
        statuses: [0, 200] // 0 for offline, 200 for succesfulde kald
      }),
      new ExpirationPlugin({
        maxEntries: 10, // Behold de 10 seneste responses
        maxAgeSeconds: 60 * 60 // Gem cache i 1 time
      })
    ]
  })
)

self.addEventListener('install', (event) => {
  console.log('Service Worker installing.')
  self.skipWaiting()
})

self.addEventListener('activate', (event) => {
  console.log('Service Worker activating.')
  event.waitUntil(self.clients.claim())
})
