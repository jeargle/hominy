# A simple tornado server

import os.path
import json

# from sqlalchemy import create_engine, event
# from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from tornado import web, ioloop

# from hominy.datafile.app import urls as datafile_urls
from hominy.main.db import get_session
from hominy.main.models import Element, Base
from hominy.person.app import urls as person_urls
# from hominy.place.app import urls as place_urls
# from hominy.organization.app import urls as organization_urls
# from hominy.webpage.app import urls as webpage_urls



# Absolute paths
app_path = os.path.split(os.path.abspath(__file__))[0]
pkg_path = os.path.split(app_path)[0]
hominy_path = os.path.split(pkg_path)[0]

# Computed paths
global_static = os.path.join(hominy_path, os.path.join('lib', 'www', 'static'))
DOC_STATIC = os.path.join(hominy_path, 'doc', 'html')


class AppHandler(web.RequestHandler):
    # @web.authenticated
    @web.asynchronous
    def get(self, app, mode):
        if not mode:
            mode = app
        self.render(os.path.join(app, 'html', (mode + '.html')))

        
class IndexHandler(web.RequestHandler):
    def get(self):
        self.render('html/hominy.html')


class NoteHandler(web.RequestHandler):
    """
    Handles create (POST), retrieve (GET), update (PUT), delete (DELETE),
    and query (GET) for Notes.
    """

    @web.asynchronous
    def get(self, uuid, fragment=None):
        if uuid is None or fragment is None:
            api.request_note(self, uuid, session=session)
        else:
            raise Exception('Invalid UUID: ' + uuid + '/' + fragment)

        return

    @web.asynchronous
    def post(self, uuid, fragment=None):
        # Create
        if uuid is None and not fragment:
            other_opts = {}
            note_dict = api.create_note(session=session, **other_opts)
            self.write(json.dumps(note_dict))
            self.finish()
        else:
            raise Exception('Invalid UUID: ' + uuid + '/' + fragment)
        return

    @web.asynchronous
    def put(self, uuid, fragment=None):
        # Update
        if uuid is not None:
            other_opts = {}
            note_dict = api.update_note(uuid, **other_opts)
            self.write(json.dumps(note_dict))
            self.finish()
        else:
            raise Exception('Invalid UUID: ' + uuid + '/' + fragment)
        return



main_urls = [
    (r'/', IndexHandler),
    (r'/app/(.*)/(.*)', AppHandler),
    (r'/static/(.*)', web.StaticFileHandler, {'path': '../../www/'}),
    (r'/main/(.*)', web.StaticFileHandler, {'path': app_path}),

    (r'/api/notes(/[a-f\d\-]+)?(/.*)?', NoteHandler),
]

urls = (
    # datafile_urls +
    person_urls +
    # place_urls +
    # organization_urls +
    # webpage_urls
    main_urls
)

app = web.Application(
    urls,
    debug = True
)



if __name__=='__main__':
    # import logging
    # logging.getLogger().setLevel(logging.DEBUG)

    # Session = sessionmaker(bind=engine)
    # session = Session()
    session = get_session()

    app.listen(8001)
    ioloop.IOLoop.instance().start()
  
