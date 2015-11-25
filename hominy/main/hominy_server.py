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


class IndexHandler(web.RequestHandler):
    def get(self):
        self.render('hominy.html')


app = web.Application(
    [(r'/', IndexHandler),
     (r'/static/(.*)', web.StaticFileHandler, {'path': '../../www/'}),
     (r'/local_static/(.*)', web.StaticFileHandler, {'path': './'}),
    ],
    debug = True
)

if __name__=='__main__':
    import logging
    logging.getLogger().setLevel(logging.DEBUG)

    app.listen(8001)
    ioloop.IOLoop.instance().start()
  
