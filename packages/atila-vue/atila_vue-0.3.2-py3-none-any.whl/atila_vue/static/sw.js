// caching -----------------------------------------
const DEBUG = true
const ENABLE_LOCALHOST_CACHE = false
let USE_CACHE = true
if (location.hostname == 'localhost' && !ENABLE_LOCALHOST_CACHE) {
  USE_CACHE = false
}
const PRE_CACHE_NAME = 'pre-cache-<<COMMIT_SHA>>'
const DYN_CACHE_NAME = 'dyn-cache-<<COMMIT_SHA>>'
const COR_CACHE_NAME = 'cor-cache-v1'

// config ---------------------------------------------
let URL_TO_CACHE = [ // cache html files for app display
  '/sw/offline.html',
  '/sw/img/rabbit.png',
  '/manifest.json',
]

let DYN_CACHE = {
  enable: true,
  pathes: [ //cache by path
    /\.(svg|jpeg|jpg|png|gif|ico)$/i,
    /\.vue$/i,
    /\.(woff|woff2|ttf)$/i,
    /\.(js|css|map)$/i,
  ],
  mimetypes: []
}

let DYN_NOCACHE = {
  enable: true,
  pathes: [ //no cache by path
    /\/sw\.js$/i
  ],
  mimetypes: []
}

let API_PAYLOAD_CACHE = {
  enable: false,
  pathes: [],
  mimetypes: []
}

let CORS_CACHE = {
  enable: true,
  pathes: [
    /\.(woff|woff2|ttf)$/i,
    /\.(js|css|map)$/i,
  ],
  mimetypes: []
}

// end of config --------------------------------------

function matched (config, url, content_type) {
  if (config.enable === false) return false
  if (config.pathes.filter (re => url.match (re)).length) return true
  if (config.mimetypes.filter (mtype => content_type.startsWith (mtype)).length) return true
  return false
}

function log (msg) {
  if (DEBUG) {
    console.log(`[sw.js] ${ msg }`)
  }
}

if (API_PAYLOAD_CACHE.enable) {
  DYN_CACHE.mimetypes = DYN_CACHE.mimetypes.concat (API_PAYLOAD_CACHE.mimetypes)
}

self.addEventListener('activate', function(event) {
  log ('activated')
  let CACHES_TO_PRESERVE = []
  if (USE_CACHE) {
    CACHES_TO_PRESERVE = [PRE_CACHE_NAME, DYN_CACHE_NAME, COR_CACHE_NAME]
  }
  event.waitUntil(
    caches.keys().then(function(cacheList) {
      return Promise.all(
        cacheList.map(function(cacheName) {
          if (CACHES_TO_PRESERVE.indexOf(cacheName) === -1) {
            log (`cache deleted ${ cacheName }`)
            return caches.delete(cacheName)
          }
        })
      )
    }).catch(function(error) {
      log (`cache deletion error ${ error }`)
    })
  )
})

if (USE_CACHE) {
  self.addEventListener('install', function(event) {
    if (DEBUG) self.skipWaiting()
    event.waitUntil(
      caches.open(PRE_CACHE_NAME).then(function(cache) {
        log (`cache opened: ${PRE_CACHE_NAME}`)
        return cache.addAll(URL_TO_CACHE)
      })
    )
  })

  self.addEventListener('fetch', function(event) {
    let cached_content = null
    event.respondWith(
      caches.match(event.request).then(function(r) {
        const url = event.request.url
        let content_type = ''
        if (r) {
          content_type = r.headers.get ('content-type') || ''
          if (!matched (API_PAYLOAD_CACHE, url, content_type)) {
            log (`cache hit ${url}`)
            return r
          } else {
            cached_content = r
            log (`refreshable cache ${url}`)
          }
        }

        const fetchRequest = event.request.clone()
        return fetch (fetchRequest)
          .then(function(response) {
            if (fetchRequest.method !== 'GET') {
              return response
            }

            if(!response || response.status !== 200) {
              return response
            }

            if (response.type !== 'basic' && !matched (CORS_CACHE, url, content_type)) {
              return response
            }

            content_type = response.headers.get ('content-type') || ''
            if (matched (DYN_NOCACHE, url, content_type)) {
              log (`skip caching ${url}`)
              return response
            }

            if (matched (DYN_CACHE, url, content_type)) {
              return caches.open(response.type === 'basic' ? DYN_CACHE_NAME : COR_CACHE_NAME).then(function(cache) {
                log (`caching ${url}`)
                cache.put(fetchRequest, response.clone ())
                return response
              })
            }

            return response
          })
        })

        .catch (async function(error) {
          if (cached_content !== null) {
            log ('cache fetch error, reuse cached data')
            return cached_content
          }
          log ('cache fetch error')
          return caches.open (PRE_CACHE_NAME).then (function(cache) {
            if (event.request.headers.get ('accept').includes ('text/html')) {
              return cache.match ('/sw/offline.html')
            }
          })
        })
    )
  })
}

// message pushing -------------------------------------
self.addEventListener('push', event => {
  log (`push ${ event.data.text() }`)
  const msg = event.data.json()
  const title = msg.data.title || 'Notification'
  const options = {
    body: msg.data.text,
    icon: '/assets/favicons/favicon-128.png',
    data: msg.data.link,
  }
  event.waitUntil(self.registration.showNotification(title, options));
})

self.addEventListener('notificationclick', function(event) {
  log ('push clicked')
  event.notification.close()
  event.waitUntil(clients.matchAll({
    type: 'window'
  }).then(function(clientList) {
    for (var i = 0; i < clientList.length; i++) {
      var client = clientList[i]
      if (client.url === '/' && 'focus' in client) {
        return client.focus()
      }
    }
    if (clients.openWindow) {
      return clients.openWindow(event.notification.data)
    }
  }))
})

// sync --------------------------------------------------
const SYNC_METHODS = {
  testSync () {
    fetch ('/favicon.ico')
      .then (response => {
        return response
      })
      .then (text => {
        log (`request successful ${ text }`)
      })
      .catch (error => {
        log (`request failed ${ error }`)
      })
  },
}

self.addEventListener ('sync', event => {
  if (event.tag == 'testSync') {
    event.waitUntil (SYNC_METHODS [event.tag] ())
  }
})
