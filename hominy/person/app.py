# A simple tornado server

import json
import os.path
import sys
from tornado import web
import traceback

import hominy.person.api as api
from hominy.person.models import WorkflowInstance


# Absolute paths
app_path = os.path.split(os.path.abspath(__file__))[0]
pkg_path = os.path.split(app_path)[0]
hominy_path = os.path.split(pkg_path)[0]

# Computed paths
global_static = os.path.join(hominy_path, os.path.join('lib', 'www', 'static'))
DOC_STATIC = os.path.join(hominy_path, 'doc', 'html')


class PersonHandler(web.RequestHandler):
    """
    Handles create (POST), retrieve (GET), update (PUT), delete (DELETE),
    and query (GET) for People.
    """

    @web.asynchronous
    def get(self, uuid, fragment=None):
        if uuid is None or fragment is None:
            api.request_person(self, uuid)
        else:
            raise Exception('Invalid UUID: ' + uuid + '/' + fragment)

        return

    @web.asynchronous
    def post(self, uuid, fragment=None):
        # Create
        if uuid is None and not fragment:
            other_opts = {}
            person_dict = api.create_person(steps, **other_opts)
            self.write(json.dumps(person_dict))
            self.finish()
        else:
            raise Exception('Invalid UUID: ' + uuid + '/' + fragment)
        return

    @web.asynchronous
    def put(self, uuid, fragment=None):
        # Update
        if uuid is not None:
            other_opts = {}
            person_dict = api.update_person(uuid, **other_opts)
            self.write(json.dumps(person_dict))
            self.finish()
        else:
            raise Exception('Invalid UUID: ' + uuid + '/' + fragment)
        return



urls = [
    (r'/api/people(/[a-f\d\-]+)?(/.*)?', PersonHandler),
]

