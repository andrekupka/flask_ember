from sqlalchemy.ext.declarative.base import _declarative_constructor

from flask_ember.database.flask_ember_database import FlaskEmberDatabase
from flask_ember.generator.resource_generator import ResourceGenerator
from flask_ember.model.model_generator import ModelGenerator
from flask_ember.resource.resource_base import ResourceBase
from flask_ember.resource.resource_meta import ResourceMeta
from flask_ember.resource.resource_registry import ResourceRegistry
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

        self.resource_registry = ResourceRegistry()

        #: The internally used database abstraction.
        self.database = FlaskEmberDatabase(self, **database_options)
        #: The generated base class to inherit from when creating custom
        #: resources.
        self.Resource = self._create_resource_base()

        #: The internally used model generator which is responsible for
        #: generating the backing sqlalchemy models of resources.
        self.model_generator = ModelGenerator()

        # TODO manage resources in a proper way

        #: If an application is directly passed to this flask ember object
        #: it will be stored here and initialized.
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

    def _create_resource_base(self):
        """ Creates the abstract resource base class that is finally
        inherited from by user resources. While generating the base class
        other instance like the internal database abstraction layer can
        contribute properties to the dictionary of the generated class.

        :rtype: ResourceMeta
        """
        bases = (ResourceBase,)
        class_dict = {
            '_ember': self,
            '_registry': self.resource_registry,
            '__init__': _declarative_constructor
        }
        self.database.contribute_to_resource_base(class_dict)
        return ResourceMeta('Base', bases, class_dict)

    def get_database(self):
        """Returns the internal database.

        :rtype: :class:`database.FlaskEmberDatabase`
        """
        return self.database

    def get_resource_registry(self):
        """Returns the internal resource registry.

        :type: :class:`resource.ResourceRegistry`
        """
        return self.resource_registry

    def get_resources(self):
        return self.resource_registry.values()

    def setup(self, create_tables=False):
        self.model_generator.generate_models(self.get_resources())
        if create_tables:
            self.database.create_all()

    def generate_resources(self, app):
        for resource in self.resource_registry.values():
            generator = ResourceGenerator(self, resource)
            generator.generate(app)

    def register_resource(self, resource_class):
        """ Registers the given resource class and makes it thus known to
        the central instance.

        :param resource_class: The resource class that is to be registered.
        :type resource_class: ResourceMeta
        """
        self.resource_registry[resource_class.__name__] = resource_class

    def get_app(self, reference_app=None):
        """ Returns the current application. If a reference application is
        given it is directly returned, otherwise :attr:`app` is used. If
        both is None an application from the flask application context stack
        will be returned. For more details see
        :meth:`util.flask.get_current_app`.

        :param reference_app: The reference application that is directly
                              returned.
        :type reference_app: flask.Flask
        :rtype: flask.Flask
        """
        return get_current_app(reference_app or self.app, 'Application is '
                               'not registered and there is no application '
                               'bound to the current context.')
