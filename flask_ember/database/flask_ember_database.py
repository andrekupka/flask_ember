from functools import partial

from flask import _app_ctx_stack as ctx_stack
from sqlalchemy import MetaData
from sqlalchemy.orm import scoped_session
from threading import Lock

from .engine_connector import EngineConnector
from .flask_ember_session import FlaskEmberSession
from flask_ember.config import keys


ALL_TABLES_KEY = '__all__'


class FlaskEmberDatabase:

    def __init__(self, ember, session_options=None):
        self.ember = ember

        session_options = session_options or dict()
        session_options.setdefault('scopefunc', ctx_stack.__ident_func__)

        # TODO define and construct proper declarative base, query and session
        # class, maybe extend query class by some methods in time
        self.metadata = MetaData()
        self.session = self.create_scoped_session(session_options)

        self.connectors = dict()
        self.engine_lock = Lock()

    def contribute_to_resource_base(self, class_dict):
        class_dict.update({
            '_metadata': self.metadata,
            'query': self.session.query_property()
        })

    def init_app(self, app):
        """Initializes this class with the given :class:`flask.Flask`
        application object.

        :param app: the Flask application
        :type app: flask.Flask
        """
        self.set_default_configuration(app)

    def set_default_configuration(self, app):
        """Sets the default configuration options for the given
        :class:`flask.Flask` application object.

        :param app: the Flask application
        :type app: flask.Flask
        """
        app.config.setdefault(keys.EMBER_DATABASE_URI, 'sqlite://')
        app.config.setdefault(keys.EMBER_DATABASE_BINDS, None)
        app.config.setdefault(keys.EMBER_DATABASE_ECHO, False)

    def create_scoped_session(self, options=None):
        options = options or dict()
        scope_function = options.pop('scopefunc', None)
        return scoped_session(partial(self.create_session, options),
                              scopefunc=scope_function)

    def create_session(self, options):
        return FlaskEmberSession(self, **options)

    @property
    def engine(self):
        return self.get_engine(self.get_app())

    def get_engine(self, app, bind=None):
        with self.engine_lock:
            connector = self.connectors.get(bind)
            if connector is None:
                connector = EngineConnector(self, app, bind)
                self.connectors[bind] = connector
            return connector.get_engine()

    def get_binds(self, app=None):
        app = self.get_app(app)
        binds = self._get_all_binds(app)
        bind_dict = dict()
        for bind in binds:
            engine = self.get_engine(app, bind)
            tables = self._get_tables_for_bind(bind)
            bind_dict.update(dict((table, engine) for table in tables))
        return bind_dict

    def get_app(self, app=None):
        return self.ember.get_app(app)

    def create_all(self, bind=ALL_TABLES_KEY, app=None):
        self._execute_for_all_tables(app, bind, 'create_all')

    def drop_all(self, bind=ALL_TABLES_KEY, app=None):
        self._execute_for_all_tables(app, bind, 'drop_all')

    def _execute_for_all_tables(self, app, bind, operation):
        app = self.get_app(app)

        for bind in self._convert_to_binds(app, bind):
            tables = self._get_tables_for_bind()
            operation_function = getattr(self.metadata, operation)
            operation_function(bind=self.get_engine(app, bind), tables=tables)

    def _convert_to_binds(self, app, bind):
        if bind == ALL_TABLES_KEY:
            binds = self._get_all_binds(app)
        elif bind is None or isinstance(bind, str):
            binds = [bind]
        else:
            binds = bind
        return binds

    def _get_all_binds(self, app):
        return [None] + list(app.config.get(keys.EMBER_DATABASE_BINDS) or ())

    def _get_tables_for_bind(self, bind=None):
        result = []
        for table in self.metadata.tables.values():
            if table.info.get('bind_key') == bind:
                result.append(table)
        return result
