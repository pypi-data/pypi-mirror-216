__version__ = "0.3.2"

import os
import json
import atila
import skitai
from skitai.wastuff.api import ISODateTimeWithOffsetEncoder
import re
import sys

RX_SPACE = re.compile (r'\s+')
ROUTES_CACHE = {}
VIEWS_DIR = "/routes"

class User:
    def __init__ (self, claims):
        self.claims = claims
        self.uid = claims ['uid']
        self.grp = claims ['grp']
        self.tuid = None

    def __getattr__ (self, attr):
        try:
            return self.claims [attr]
        except KeyError:
            raise AttributeError

    def __str__ (self):
        return self.uid


def __config__ (pref):
    pref.config.MINIFY_HTML = 'strip'


def __setup__ (context, app):
    from skitai.wastuff import sendmail

    if "SMTP" in app.config:
        smtp = app.config.SMTP
        sendmail.configure (smtp ["SMTP_SERVER"], smtp ["SMTP_AUTH"], smtp ["SMTP_SENDER"])

    @app.permission_handler
    def permission_handler (context, perms):
        if not context.request.get_header ('authorization'):
            raise context.HttpError ("401 Unauthorized")

        context.request.user = None
        claims = context.dejwt ()
        if "err" in claims:
            raise context.HttpError ("401 Unauthorized", claims ["err"])
        context.request.user = User (claims)

        if context.request.user.grp == "test":
            raise context.HttpError ("418 You are a teapot")

        if 'uid' in context.request.PARAMS:
            tuid = context.request.PARAMS ['uid']
            if 'owner' in perms and tuid != 'me':
                raise context.HttpError ("403 Permission Denied", "owners only operation")
            context.request.user.tuid = (tuid == 'me' and context.request.user.uid or (tuid != 'notme' and tuid or None))

        if not perms:
            return
        if context.request.user.grp == "staff":
            return # always vaild
        if "staff" in perms:
            raise context.HttpError ("403 Permission Denied")

    @app.route ('/status')
    @app.permission_required (skitai.isdevel () and ['user'] or ['staff'])
    def status (context, f = ''):
        return context.status (f)

    # template globals ------------------------------------
    @app.template_global ('raise')
    def raise_helper (context, msg):
        raise Exception (msg)

    @app.template_global ('http_error')
    def http_error (context, status):
        raise context.HttpError (status)

    @app.template_global ('get_apispecs')
    def get_apispecs (context):
        return { k.replace ('.', '_').replace (':', '_').upper (): v for k, v in sorted (app.get_urlspecs ().items (), key = lambda x: x [0]) if v ['path'].startswith ('/api') }

    @app.template_global ('build_routes')
    def build_routes (context, base):
        def collect (start, base_len):
            pathes = []
            for fn in os.listdir (start):
                path = os.path.join (start, fn)
                if fn in ('components', '__layout.vue'):
                    continue
                if fn.startswith ('__'):
                    continue

                if os.path.isdir (path):
                    pathes.extend (collect (path, base_len))
                elif fn.endswith ('.vue'):
                    pathes.append ((
                        path [base_len:-4].replace ("\\", '/').replace ('/_', '/:'),
                        path [base_len:].replace ("\\", '/'),
                    ))
            return pathes

        def find (root, base, meta):
            if not os.path.isdir (root):
                return None, [], set ()

            routes = []
            pathes = []
            bases = set ()
            names = set ()
            for path, vue in collect (root, len (root)):
                if path.endswith ('/index'):
                    path = path [:-6] or '/'
                    full_path = (base + path) or '/'
                else:
                    full_path = base + path

                ss = []
                for s in full_path.split ('/') [1:]:
                    if not s or s [0] == ":":
                        break
                    ss.append (s)
                ss = '/' + '/'.join (ss)
                bases.add (ss)

                vue_path = "{}{}{}".format (VIEWS_DIR, base, vue)
                current_meta = {}
                for k, v in meta.items ():
                    if path.startswith (k):
                        current_meta.update (v)
                routes.append ('{name: "%s", path: "%s", component: () => loadModule("%s", options), meta: %s}' % (path [1:] or 'index', path, vue_path, json.dumps (current_meta)))
                if path == '/':
                    context.push (vue_path) # server push
                else:
                    pathes.append (vue_path) # prefetch
            routes_list = ",\n ".join (routes)
            return routes_list, pathes, bases

        def validate_routes (bases):
            match = False
            current_uri = context.request.split_uri () [0]
            if current_uri == '/':
                match = True
            elif bases == {'/'}:
                match = True
            else:
                for base in bases:
                    if base == '/':
                        continue
                    if current_uri.startswith (base):
                        needle = current_uri [len (base):]
                        if not needle or needle [0] == '/':
                            match = True
                            break

            if not match:
                raise context.HttpError ("404 Not Found")

        global ROUTES_CACHE
        if not app.debug and base in ROUTES_CACHE:
            cached = ROUTES_CACHE [base]
            validate_routes (cached [-1])
            return cached [:3]

        if "STATIC_PATH" in app.config:
            static_path = app.config.STATIC_ROOT
        else:
            static_path = os.path.join (app.home, 'static') # default

        current = os.path.join (static_path, VIEWS_DIR [1:], base [1:])
        if not os.path.exists (current):
            raise context.HttpError ("500 Server Error", f"routes not found, `{current}` is missing")

        meta = {}
        meta_file = os.path.join (current, 'meta.json')
        if os.path.isfile (meta_file):
            with open (meta_file) as f:
                meta = json.loads (f.read ())

        routes_list, pathes, bases = find (current, base, meta)
        layout = os.path.join (VIEWS_DIR [1:], base [1:], '__layout.vue')
        assert os.path.isfile (os.path.join (static_path, layout)), f'`{ os.path.join (static_path, layout) }` is missing'

        if not routes_list:
            home = os.path.join (os.path.dirname (__file__), '../static', VIEWS_DIR [1:], base [1:])
            routes_list, pathes, bases = find (home, base, meta)

        assert routes_list, context.HttpError ("500 Server Error", 'no routes for vue-router, at least `index.vue` is expected')
        assert 'name: "index"' in routes_list, context.HttpError (f'`{ os.path.join (static_path, VIEWS_DIR [1:], base [1:], "index.vue") }` is missing')
        ROUTES_CACHE [base] = (routes_list, pathes, layout, bases)
        validate_routes (bases)
        return routes_list, pathes, layout

    # template filters --------------------------------------
    @app.template_filter ('vue')
    def vue (val):
        return '{{ %s }}' % val

    @app.template_filter ('summarize')
    def summarize (val, chars = 60):
        if not val:
            return ''
        s = val.find (" ", chars)
        if s == -1:
            return RX_SPACE.sub (" ", val.strip ())
        else:
            return RX_SPACE.sub (" ", val.strip () [: min (s, chars + 10)]) + '...'

    @app.template_filter ('attr')
    def attr (val):
        if not val:
            return '""'
        return '"{}"'.format (val.replace ('"', '\\"'))

    @app.template_filter ('upselect')
    def upselect (val, *names, **upserts):
        d = {}
        for k, v in val.items ():
            if k in names:
                d [k] = v
        d.update (upserts)
        return d

    @app.template_filter ('tojson_with_datetime')
    def tojson_with_datetime (data):
        return json.dumps (data, cls = ISODateTimeWithOffsetEncoder, ensure_ascii = False)


def __mount__ (context, app):
    import atila_vue

    @app.route ("/ping")
    def ping (context):
        return 'pong'

    @app.route ('/base-template')
    def baee_template (context):
        return f"Template Version: {atila_vue.__version__}"
