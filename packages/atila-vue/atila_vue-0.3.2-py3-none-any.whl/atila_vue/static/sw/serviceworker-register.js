if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js').then(function(registration) {
            console.log('[serviceworker] registration successful with scope', registration.scope)
            registration.addEventListener('updatefound', () => {
                const newWorker = registration.installing
                console.log('[serviceworker] service worker update found')
                newWorker.addEventListener('statechange', () => {
                    console.log('[serviceworker] service worker state changed', newWorker.state)
                })
            })
        }, function(err) {
            console.log('[serviceworker] registration failed', err)
        })

        navigator.serviceWorker.addEventListener ('controllerchange', () => {
            console.log('[serviceworker] controller changed')
        })
    })
}