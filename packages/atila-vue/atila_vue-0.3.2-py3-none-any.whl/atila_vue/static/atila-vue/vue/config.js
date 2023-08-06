class CachableStorage {
  constructor (loc) {
    if (loc == 'session') {
      this.__s = window.sessionStorage
    } else {
      this.__s = window.localStorage
    }
  }
  now () {
    return Math.floor(new Date().getTime() / 1000)
  }
  set (name, data, timeout = 0) {
    this.__s.setItem (name, JSON.stringify ([ timeout ? this.now () + timeout : 0, data ]))
  }
  get (name) {
    const _val = this.__s.getItem (name)
    if (_val == null) {
      return null
    }
    const _cached = JSON.parse (_val)
    if (_cached [0] && _cached [0] < this.now ()) {
      this.remove (name)
      return null
    }
    return _cached [1]
  }
  remove (name) {
    this.__s.removeItem (name)
  }
  clear () {
    this.__s.clear ()
  }
}

function unint8array (decoded) {
  let arr = []
  for (let i = 0; i < decoded.length; i++) {
    arr.push (decoded.charCodeAt(i))
  }
  return new Uint8Array (arr)
}

function bytes2string (bytes) {
  let decoded = atob (bytes)
  if (decoded.charCodeAt(0) == 88) {
    decoded = decoded.substring (5, decoded.length - 3)
    return new TextDecoder().decode (unint8array (decoded))
  }
  else if (decoded.charCodeAt(0) == 78) { // None
    return null
  }
  else if (decoded.charCodeAt(0) == 77) { // short int
    decoded = decoded.substring (1, 3)
    return new Int16Array (unint8array (decoded).buffer) [0]
  }
  else if (decoded.charCodeAt(0) == 75) { // char int
    decoded = decoded.substring (1, 2)
    return new Int8Array (unint8array (decoded).buffer) [0]
  }
  else if (decoded.charCodeAt(0) == 74) { // int
    decoded = decoded.substring (1, 5)
    return new Int32Array (unint8array (decoded).buffer) [0]
  }
  throw new Error ('Unknown pickle type')
}

function parse_session () {
  let session = null
  for (let each of document.cookie.split ("; ")) {
    if (each.indexOf ('ATLSES_STK=') == 0) {
      session = each
      break
    }
  }
  if (!session) {
    return null
  }
  const user = {}
  const sessionval = session.split ('?')
  if (sessionval.length == 1) {
    return null
  }
  for (let each of sessionval [1].split ('&')) {
    const [name, val] = each.split ('=')
    if (name == 'nick_name' || name == 'uid' || name == 'lev' || name == 'status') {
      user [name] = bytes2string (val)
    }
  }
  return user
}

function get_csrf () {
  const meta = document.querySelector ('head > meta[name=csrf]')
  if (meta == null) {
    return null
  }
  const [token, name] = meta.getAttribute ('content').split (';')
  return {token, name}
}

function prefetch (href) {
  const s = document.createElement('link')
  s.rel = 'prefetch'
  s.as = 'fetch'
  s.href = href
  document.body.appendChild (s)
}

function decode_jwt (token) {
  try {
    return JSON.parse (atob (token.split ('.') [1]))
  } catch (e) {
    return null
  }
}

// vuex initial state --------------------------------------
_vuexState.$uid = null
_vuexState.$grp = null
_vuexState.$claims = null
_vuexState.$location = location
_vuexState.$location.uri = location.pathname + (location.search || '') + (location.hash || '')
_vuexState.$ls = new CachableStorage ('local')
_vuexState.$ss = new CachableStorage ('session')
_vuexState.$urlspecs = {}
_vuexState.$websocket = {url: null, sock: null, read_handler: null, push: null}
_vuexState.$csrf = get_csrf ()
_vuexState.$next_route = null
_vuexState.$refresh_token_api = null

axios.defaults.withCredentials = true

function mapVuexItems () {
  return Vuex.mapState ([...Object.keys (_vuexState)])
}

// vuex data loader ----------------------------------------
function _getTargetStore (schema, props) {
  let attr_name = schema.dataset.name
  let target_object = props.store
  const variables = schema.dataset.name.split ('.')
  if (variables.length == 2) {
    target_object = props.store [variables [0]]
    attr_name = variables [1]
  } else if (variables.length > 2) {
    throw new Error ('invalid map_data name')
  }
  return [target_object, attr_name]
}

function _getDataset (css, typeref) {
  const els = document.querySelectorAll (css)
  let rows = []
  els.forEach ((el, index) => {
  let row = {}
  for (let [key, val] of Object.entries (el.dataset)) {
    const t = typeof (typeref [key])
    if (val == 'null') {
      val = null
    } else if (t == 'boolean') {
      val = (val == 'true')
    } else if (t == 'number') {
      if (val.indexOf (".") != -1) {
        val = parseFloat (val)
      } else {
        val = parseInt (val)
      }
    }
    row [key] = val
  }
  rows.push (row)
  })
  return rows
}

function _getSchemaProps (schema) {
  let store = Vuex.useStore ().state
  const type = schema.dataset.type
  const container = schema.dataset.container
  let dataSize = 0
  if (!!schema.dataset.maxSize) {
    dataSize = parseInt (schema.dataset.maxSize)
  }
  return {type, store, dataSize, container}
}

function _readSchemas () {
  const schemas = document.querySelectorAll ('#state-map > .veux-state')
  schemas.forEach (schema => {
  props = _getSchemaProps (schema)
  let [target_object, attr_name] = _getTargetStore (schema, props)
  if (props.type == undefined) {
    let d = []
    for (let i = 0; i < props.dataSize; i++ ) {
      d.push (JSON.parse (schema.dataset.default))
    }
    target_object [attr_name] = d
  }
  else {
    target_object [attr_name] = ''
  }
  })
}

function _readDataset () {
  const schemas = document.querySelectorAll ('#state-map > .veux-state')
  for (let i=0; i<schemas.length; i++) {
    let schema = schemas [i]
    props = _getSchemaProps (schema)

    let [target_object, attr_name] = _getTargetStore (schema, props)
    let typeref = target_object [attr_name]
    if (props.dataSize) {
      typeref = target_object [attr_name][0]
    }

    const container = document.querySelector (props.container)
    if (!!container) {
      if (props.type === 'html' && !!props.container) {
        target_object [attr_name] = container.innerHTML
      }
      else if (props.type === 'text' && !!props.container) {
        target_object [attr_name] = container.innerText
      }
      else {
        r = _getDataset (props.container, typeref)
        for (let i = 0; i < r.length; i++) {
          target_object [attr_name].splice (i, 1, r [i])
        }
      }
    }
  }
}
