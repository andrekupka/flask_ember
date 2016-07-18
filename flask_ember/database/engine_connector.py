from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
from threading import Lock

from flask_ember.config import keys


class EngineConnector:

    def __init__(self, database, app, bind=None):
        self.database = database
        self.app = app
        self.engine = None
        self.bind = bind
        self.connected_for = None
        self.lock = Lock()

    def get_uri(self):
        if self.bind is None:
            return self.app.config[keys.EMBER_DATABASE_URI]
        binds = self.app.config[keys.EMBER_DATABASE_BINDS]
        assert self.bind in binds,\
            ('Bind {} is not specified. Set it in the {} configuration'
             'variable'.format(self.bind, keys.EMBER_DATABASE_BINDS))
        return binds[self.bind]

    def get_engine(self):
        with self.lock:
            uri = self.get_uri()
            echo = self.app.config[keys.EMBER_DATABASE_ECHO]
            if (uri, echo) == self.connected_for:
                return self.engine
            info = make_url(uri)
            options = dict(
                convert_unicode=True,
                echo=echo
            )
            self.engine = create_engine(info, **options)
            self.connected_for = (uri, echo)
            return self.engine
