# A simple tornado server

import os.path
import json

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from tornado import web, ioloop


# Absolute paths
app_path = os.path.split(os.path.abspath(__file__))[0]
pkg_path = os.path.split(app_path)[0]
hominy_path = os.path.split(pkg_path)[0]

# Computed paths
global_static = os.path.join(hominy_path, os.path.join('lib', 'www', 'static'))
DOC_STATIC = os.path.join(hominy_path, 'doc', 'html')


class AppHandler(web.RequestHandler):
    @web.authenticated
    @web.asynchronous
    def get(self, app, mode):
        if not mode:
            mode = app
        self.render(os.path.join(app, 'html', (mode + '.html')))

        
class IndexHandler(web.RequestHandler):
    def get(self):
        self.render('hominy.html')



urls = [
    (r'/', IndexHandler),
    (r'/app/(.*)/(.*)', AppHandler),
    (r'/static/(.*)', web.StaticFileHandler, {'path': '../../www/'}),
    (r'/main/static/(.*)', web.StaticFileHandler, {'path': app_path}),
]
        

app = web.Application(
    urls,
    debug = True
)



if __name__=='__main__':
    import logging
    logging.getLogger().setLevel(logging.DEBUG)

    app.listen(8001)
    ioloop.IOLoop.instance().start()
  
