// define prototype methods -----------------------------------
Number.prototype.format = function () {
  if(this==0) return "0"
  var reg = /(^[+-]?\d+)(\d{3})/
  var n = (this + '')
  while (reg.test(n)) n = n.replace (reg, '$1' + ',' + '$2')
    return n
}
String.prototype.format = function () {
  var num = parseFloat (this)
  if( isNaN(num) ) return "0"
  return num.format ()
}
String.prototype.titleCase = function () {
  return this.replace (/\w\S*/g, function (txt) {return txt.charAt(0).toUpperCase () + txt.substr (1).toLowerCase ();})
}
Date.prototype.unixepoch = function () {
  return Math.floor(this.getTime() / 1000)
}

Date.prototype.format = function(f) {
  if (!this.valueOf()) return " "
  var d = this;
  return f.replace(/(%Y|%y|%m|%d|%H|%I|%M|%S|%p|%a|%A|%b|%B|%w|%c|%x|%X|%k|%n|%D)/gi, function($1) {
    switch ($1) {
    case "%Y":
      return d.getFullYear()
    case "%y":
      return (d.getFullYear() % 1000).zfill(2)
    case "%m":
      return (d.getMonth() + 1).zfill(2)
    case "%d":
      return d.getDate().zfill(2);
    case "%H":
      return d.getHours().zfill(2)
    case "%I":
      return ((h = d.getHours() % 12) ? h : 12).zfill(2)
    case "%M":
      return d.getMinutes().zfill(2)
    case "%S":
      return d.getSeconds().zfill(2)
    case "%p":
      return d.getHours() < 12 ? "AM" : "PM"
    case "%w":
      return d.getDay()
    case "%c":
      return d.toLocaleString()
    case "%x":
      return d.toLocaleDateString()
    case "%X":
      return d.toLocaleTimeString()
    case "%b":
      return ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][d.getMonth()]
    case "%B":
      return ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][d.getMonth()]
    case "%a":
      return ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'][d.getDay()]
    case "%A":
      return ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][d.getDay()]
    case "%k":
      return ['일', '월', '화', '수', '목', '금', '토'][d.getDay()]
    case "%n":
      return ( d.getMonth() + 1)
    case "%D":
      return d.getDate()
    default:
      return $1
    }
  })
}
String.prototype.repeat = function(len){var s = '', i = 0; while (i++ < len) { s += this; } return s;}
String.prototype.zfill = function(len){return "0".repeat(len - this.length) + this}
Number.prototype.zfill = function(len){return this.toString().zfill(len)}


// utilities ---------------------------------------------
function load_script (src, callback = () => {}) {
  let current = null
  if (typeof (src) === "string") {
    current = src
    src = []
  } else {
    current = src.shift ()
  }
  var script = document.createElement('script')
  script.setAttribute('src', current)
  script.setAttribute('async', true)
  if (src.length) {
    script.addEventListener('load', () => { this.$load_script (src, callback) })
  } else {
    script.addEventListener('load', callback)
  }
  document.head.appendChild(script)
}

function notify (title, message, icon, timeout = 5000) {
  var options = {
    body: message,
    icon: icon
  }
  const n = new Notification(title, options)
  n.onclick = (event) => {
  n.close ()
  }
  n.onshow = (event) => {
  setTimeout(function(){ n.close () }, timeout)
  }
}

function log (msg, type = 'info') {
  if (store.state.$debug) {
    console.log (`[${type}] ${msg}`)
  }
}

function set_cloak (flag) {
  store.state.$cloak = flag
}

function traceback (e) {
  let msg = ''
  if (e.response !== undefined) {
    const r = e.response
    let code = r.data.code || 70000
    let message = r.data.message || 'no message'
    msg = `${message} (status: ${r.status}, error: ${code})`
    log (msg + ' ' + JSON.stringify (r.data), 'expt')
  }
  else {
    msg = `${e.name}: ${e.message}`
    log (msg + ' ' + e, 'expt')
  }
  return msg
}

function sleep (ms) {
  return new Promise (resolve => setTimeout(resolve, ms))
}

function build_url (baseurl, kargs = {}) {
  let url = baseurl
  let newquery = ''
  for (let [k, v] of Object.entries (kargs)) {
    if (v === null) {
      continue
    }
  if (!!newquery) {
    newquery += '&'
  }
  newquery += k + "=" + encodeURIComponent (v)
  }
  if (!!newquery) {
    return url + "?" + newquery
  }
  return url
}

const _deviceDetect = {
  android: function() {
    return navigator.userAgent.match(/Android/i)
  },
  ios: function() {
    return navigator.userAgent.match(/iPhone|iPad|iPod/i)
  },
  mobile: function() {
    return (deviceDetect.android() || deviceDetect.ios())
  },
  touchable: function () {
    return (navigator.maxTouchPoints || 'ontouchstart' in document.documentElement)
  },
  rotatable: function () {
    return window.orientation > -1
  },
  width: function () {
    return window.innerWidth
  },
  height: function () {
    return window.innerHeight
  }
}

function date (dt = null) {
  if (dt === null) {
    return new Date ()
  }
  if (dt.indexOf ('-') === -1) {
    return new Date (parseFloat (dt) * 1000.)
  }
  const [a, b] = dt.split (' ')
  const [Y, m, d] = a.split ("-")
  const [H, M, S] = b.substring (0, 8).split (":")
  return new Date (Date.UTC (Y, parseInt (m) - 1, d, H, M, S))
}

function _check_url (url) {
  if (url.substring (0, 1) == '/') {
    throw new Error ('url cannot be started with /')
  }
}

function _urlfor (urlspecs, name, args = [], _kargs = {}) {
  const target = urlspecs [name]
  if (!target) {
    throw new Error (`route ${name} not found`)
  }

  let url = target.path

  let kargs = {}
  if (Object.prototype.toString.call(args).indexOf ("Array") != -1) {
    let i = 0
    for (let k of target.params) {
      kargs [k] = args [i]
      i += 1
    }
    for (let k of target.query) {
      kargs [k] = args [i]
      i += 1
    }
  } else {
   kargs = args
  }

  for (let k of target.params) {
    if (kargs [k] !== undefined ) {
      url = url.replace (":" + k, kargs [k])
    }
  }

  let newquery = ''
  for (let k of target.query) {
    if (kargs [k] === undefined ) {
      continue
    }
  const v = kargs [k]
  if (!!newquery) {
    newquery += '&'
  }
  newquery += k + "=" + encodeURIComponent (v)
  }

  if (!!newquery) {
    return url + "?" + newquery
  }
  return url
}


function dejwt (token) {
  try {
    return JSON.parse (atob (token.split ('.') [1]))
  } catch (e) {
    return null
  }
}

function urlfor (name, args = [], _kargs = {}) {
  return _urlfor (store.state.$urlspecs, name, args, _kargs)
}

function apifor (name, args = [], _kargs = {}) {
  return _urlfor (store.state.$apispecs, name, args, _kargs)
}

function staticfor (relurl) {
  _check_url (relurl)
  return store.state.$static_url + relurl
}

function mediafor (relurl) {
  _check_url (relurl)
  return store.state.$media_url + relurl
}

// websocket ---------------------------------------------------
class AsynWebSocket extends WebSocket {
  constructor (url, read_handler = (evt) => log (evt.data)) {
    super (url)
    this.onmessage = read_handler
    this.buffer = []
    this.connected = false
  }

  onwrite() {
    for (var i = 0; i < this.buffer.length; i++) {
      msg = this.buffer.shift ()
      log (`send: ${ msg }`, 'websocket')
      this.sock.send (msg)
    }
  }

  onopen() {
    this.connected = true
    log ('connected', 'websocket')
    this.onwrite ()
  }

  onclose (evt) {
    this.connected = false
    log ('closed', 'websocket')
  }

  push(msg) {
    if (!msg) { return }
    this.buffer.push (msg)
    if (!this.connected) {
      return
    }
    this.onwrite ()
  }
}

function FailSafeWebSocket (buffer = []) {
  const ws = store.state.$websocket
  ws.sock = new AsynWebSocket (ws.url, ws.read_handler)
  ws.sock.buffer = buffer
  ws.push = ws.sock.push
  log ('connecting...', 'websocket')

  ws.sock.onerror = function (e) {
    log ('error occurred, try to reconnect...', 'websocket')
    const buffer = [...ws.sock.buffer]
    ws.sock.close ()
    FailSafeWebSocket (buffer)
  }
}

function create_websocket (url, read_handler) {
  const ws = store.state.$websocket
  ws.url = url
  ws.read_handler = read_handler
  FailSafeWebSocket ([])
  return ws
}

// authorization ----------------------------------------
function permission_required (permission, redirect, next) {
  if (store.state.$uid !== null) {
    if (store.state.$grp === null) {
      store.state.$grp = ['user']
    }

    if (store.state.$grp.indexOf ('admin') != -1) {
      return next ()
    }
    if (store.state.$grp.indexOf ('staff') != -1 && permission.indexOf ('staff') != -1) {
      return next ()
    }

    let granted = false
    for (const perm  of store.state.$grp) {
      if (permission.indexOf (perm) != 1) {
        granted = true
        break
      }
    }
    if (granted) {
      return next ()
    }
  }
  store.state.$next_route = {name: router.currentRoute.value.name}
  return next (redirect)
}

async function refresh_access_token (API_ID = null) {
  if (!!API_ID) {
    store.state.$refresh_token_api = apifor (API_ID)
  }
  const endpoint = store.state.$refresh_token_api
  if (!endpoint) {
    log ('does not call refresh_access_token (API_ID)', 'warn')
    return
  }
  const access_token = store.state.$ls.get ('access_token')
  if (!access_token) {
    store.commit ('_clear_credential')
    return
  }

  let claim = dejwt (access_token)
  if (!claim) { // corrupted token
    store.commit ('_clear_credential')
    return
  }

  if (claim.exp > new Date ().unixepoch () + 120) { // over 2 minutes to expiration
    if (!API_ID) {
      return // this is called by axio hook, nothing to do, all is ok
    }
    store.commit ("_save_credential", {uid: claim.uid, grp: claim.grp, access_token})
    return access_token
  }

  const rtk = store.state.$ls.get ('refresh_token')
  if (!rtk) {
    store.commit ('_clear_credential')
    return
  }

  axios.defaults.headers.common ["Authorization"] = `Bearer ${access_token}`
  let r = null
  try {
    r = await axios.post (endpoint, {refresh_token: rtk})
  } catch (e) {
    traceback (e)
    r = e.response
    if (r.status == 401) {
      store.commit ('_clear_credential')
    }
    return
  }
  claim = dejwt (r.data.access_token)
  store.commit ("_save_credential", {uid: claim.uid, grp: claim.grp, access_token: r.data.access_token, refresh_token: r.data.refresh_token})
  return r.data.access_token
}

async function signin_with_id_and_password (API_ID, payload) {
  const endpoint = apifor (API_ID)
  let r = null
  try {
      r = await axios.post (endpoint, payload)
  } catch (e) {
      r = e.response
      const msg = traceback (e)
      if (r.status == 401) {
        store.commit ('_clear_credential')
      }
      return msg
  }
  const claim = dejwt (r.data.access_token)
  store.commit ("_save_credential", {uid: claim.uid, grp: claim.grp, access_token: r.data.access_token, refresh_token: r.data.refresh_token})
}

function restore_route () {
  const next_route = store.state.$next_route || { name: 'index' }
  store.state.$next_route = null
  router.push (next_route)
}

axios.interceptors.request.use ( async (config) => {
  const atk = config.headers.common.Authorization
  if (!atk) {
    return config
  }
  if (config.url == store.state.$refresh_token_api) {
    return config
  }
  if (config.url.substring (0, 1) != '/') {
    return config
  }
  let exp
  if (!!store.state.$claims) {
    exp = store.state.$claims.exp
  } else {
    exp = dejwt (atk.substring (7, atk.length)).exp
  }
  if (exp > new Date ().unixepoch () - 60) {
    const access_token = await refresh_access_token ()
    if (!!access_token) {
      config.headers.common.Authorization = `Bearer ${ access_token }`
    }
  }
  return config
}, (error) => {
  return Promise.reject (error)
})

$http = axios
device = _deviceDetect
