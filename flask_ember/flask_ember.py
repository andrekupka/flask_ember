from .database import FlaskEmberDatabase
from .generator import ResourceGenerator
from .model.generator import ModelGenerator
from .model import ModelRegistry

from flask import _app_ctx_stack as ctx_stack


EXTENSION_NAME = 'ember'


def get_ember(app):
    assert (EXTENSION_NAME in app.extension,
            'The flask_ember extension was not registered to the current '
            'application. Please make sure to call init_app first.')
    return app.extension[EXTENSION_NAME]


class FlaskEmber:
    def __init__(self, app=None, database_options=None):
        database_options = database_options or dict()

        self.database = FlaskEmberDatabase(self, **database_options)
        self.model_registry = ModelRegistry()
        self.model_generator = ModelGenerator(self)

        # TODO manage resources in a proper way
        self.resources = list()

        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if not hasattr(app, 'extensions'):
            app.extensions = dict()
        if EXTENSION_NAME in app.extensions:
            # TODO already initialized
            return

        app.extensions[EXTENSION_NAME] = self

        self.database.init_app(app)
        self.generate_resources(app)

    def get_database(self):
        return self.database

    def generate_resources(self, app):
        for resource in self.resources:
            generator = ResourceGenerator(self, resource)
            generator.generate(app)

    def abstractresource(self, resource_class):
        return self.model_generator.generate_abstract(resource_class)

    def resource(self, resource_class):
        # TODO generate model here
        self.resources.append(resource_class)
        return self.model_generator.generate(resource_class)

    def get_app(self, reference_app=None):
        if reference_app:
            return reference_app
        if self.app is not None:
            return self.app
        ctx = ctx_stack.top
        if ctx is not None:
            return ctx.app
        raise RuntimeError('application is not registered and there is no '
                           'application bound to the current context')
