# A simple tornado server

import json
import os.path
import sys
from tornado import web
import traceback

import hominy.place.api as api
from hominy.place.models import Place
from hominy.main.db import get_session
# from hominy.main.hominy_server import session


# Absolute paths
app_path = os.path.split(os.path.abspath(__file__))[0]
pkg_path = os.path.split(app_path)[0]
hominy_path = os.path.split(pkg_path)[0]

# Computed paths
global_static = os.path.join(hominy_path, os.path.join('lib', 'www', 'static'))
DOC_STATIC = os.path.join(hominy_path, 'doc', 'html')

local_css = os.path.join(app_path, 'css')
local_html = os.path.join(app_path, 'html')
local_js = os.path.join(app_path, 'js')


class PlaceHandler(web.RequestHandler):
    """
    Handles create (POST), retrieve (GET), update (PUT), delete (DELETE),
    and query (GET) for Places.
    """

    @web.asynchronous
    def get(self, uuid, fragment=None):
        if uuid is None or fragment is None:
            api.request_place(uuid, session=session)
        else:
            raise Exception('Invalid UUID: ' + uuid + '/' + fragment)

        return

    @web.asynchronous
    def post(self, uuid, fragment=None):
        # Create
        if uuid is None and not fragment:
            other_opts = {}
            place_dict = api.create_place(session=session, **other_opts)
            self.write(json.dumps(place_dict))
            self.finish()
        else:
            raise Exception('Invalid UUID: ' + uuid + '/' + fragment)
        return

    @web.asynchronous
    def put(self, uuid, fragment=None):
        # Update
        if uuid is not None:
            other_opts = {}
            place_dict = api.update_place(uuid, session=session, **other_opts)
            self.write(json.dumps(place_dict))
            self.finish()
        else:
            raise Exception('Invalid UUID: ' + uuid + '/' + fragment)
        return


class PlaceLibHandler(web.RequestHandler):
    """
    Place library page.
    """
    def get(self, fragment=None):
        session = get_session()
        places = api.request_places(session=session)
        self.render(
            local_html + '/place.html',
            places = places,
        )



urls = [
    (r'/api/place(/[a-f\d\-]+)?(/.*)?', PlaceHandler),

    (r'/place/css/(.*)', web.StaticFileHandler, {'path': local_css}),
    (r'/place/js/(.*)', web.StaticFileHandler, {'path': local_js}),
    (r'/app/place/lib', PlaceLibHandler),
]
