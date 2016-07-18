from sqlalchemy.orm.session import Session

import flask_ember


class FlaskEmberSession(Session):
    def __init__(self, database, autocommit=False, autoflush=True, app=None,
                 **options):
        self.app = database.get_app()

        bind = options.pop('bind', None) or database.engine
        binds = options.pop('binds', None) or database.get_binds(app)

        super().__init__(bind=bind, binds=binds, autocommit=autocommit,
                         autoflush=autoflush, **options)

    def get_bind(self, mapper=None, clause=None):
        if mapper is not None:
            info = getattr(mapper.mapped_table, 'info', dict())
            bind_key = info.get('bind_key')
            if bind_key is not None:
                # TODO retrieve the database from the ember object registered
                # at the current application
                ember = flask_ember.get_ember(self.app)
                return ember.get_database().get_engine(self.app, bind=bind_key)
        return super().get_bind(mapper, clause)
