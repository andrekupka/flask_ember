from flask_ember.database import FlaskEmberDatabase
from flask_ember.generator import ResourceGenerator
from flask_ember.model.generator import ModelGenerator
from flask_ember.model import ModelRegistry
from flask_ember.util.flask import get_current_app


EXTENSION_NAME = 'ember'


def get_ember(app=None):
    """Returns the :class:`FlaskEmber` object that is registered with the given
    :class:`flask.Flask` application. If None is given the current application
    is used.

    :param app: the Flask application
    :type app: flask.Flask
    :rtype: :class:`FlaskEmber`
    """
    app = get_current_app(app, 'There is no application bound to the current '
                          'context.')
    assert app.extensions and EXTENSION_NAME in app.extensions,\
        ('The flask_ember extension was not registered to the current '
         'application. Please make sure to call init_app first.')
    return app.extensions[EXTENSION_NAME]


class FlaskEmber:
    """The flask ember object implements the flask extension. It is the central
    instance that manages backend databases and resources. It is initialized by
    passing an :class:`flask.Flask` application or :class:`flask.Blueprint` to
    either __init__, which will bind the flask ember instance to the single
    application, or :meth:`init_app`, which can make this flask ember instance
    usable by multiple applications.

    :param app: the flask application object
    :type app: flask.Flask
    :param database_options: options that are passed to the internal database
    :type database_options: dict
    """

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
        """Initialize this class with the given :class:`flask.Flask`
        application object.

        :param app: the Flask application
        :type app: flask.Flask
        """
        if not hasattr(app, 'extensions'):
            app.extensions = dict()
        if EXTENSION_NAME in app.extensions:
            # TODO already initialized
            return

        app.extensions[EXTENSION_NAME] = self

        self.database.init_app(app)
        self.generate_resources(app)

    def get_database(self):
        """Returns the internal database.

        :rtype: :class:`database.FlaskEmberDatabase`
        """
        return self.database

    def generate_resources(self, app):
        for resource in self.resources:
            generator = ResourceGenerator(self, resource)
            generator.generate(app)

    def abstractresource(self, resource_class):
        return self.model_generator.generate_abstract(resource_class)

    def resource(self, resource_class):
        self.resources.append(resource_class)
        return self.model_generator.generate(resource_class)

    def get_app(self, reference_app=None):
        return get_current_app(reference_app or self.app, 'Application is '
                               'not registered and there is no application '
                               'bound to the current context.')
