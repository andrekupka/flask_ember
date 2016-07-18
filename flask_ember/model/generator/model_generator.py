import sqlalchemy as sql

from flask_ember.database import DeclarativeModelMeta
from flask_ember.resource import Resource
from flask_ember.resource_options import ResourceOptions


class ModelGenerator:

    def __init__(self, ember, database=None, registry=None):
        self.ember = ember
        self.database = database or ember.get_database()
        self.registry = registry or ember.model_registry

        self.model_base = self.database.get_model_base()

    def generate_abstract(self, resource_class):
        return self.generate_model(resource_class, abstract=True)

    def generate(self, resource_class):
        return self.generate_model(resource_class)

    def generate_model(self, resource_class, abstract=False):
        model_name = resource_class.__name__

        if model_name in self.registry:
            return self.registry[model_name]

        bases = self.get_bases(resource_class)
        class_dict = self.build_class_dict(resource_class, abstract=abstract)

        new_model_class = DeclarativeModelMeta("New" + model_name, bases, class_dict)
        self.registry[model_name] = new_model_class
        return new_model_class

    def get_bases(self, resource_class):
        bases = list()
        for original_base in resource_class.__bases__:
            if not issubclass(original_base, Resource):
                bases.append(original_base)
        bases.append(self.model_base,)
        return tuple(bases)

    def build_class_dict(self, resource_class, abstract):
        # TODO remove primary key generation
        class_dict = dict(
            _resource_class=resource_class,
            _is_model=True
        )

        class_dict['__abstract__'] = abstract
        if not abstract:
            from flask_ember.util.string import underscore
            tablename = (resource_class._options.tablename or
                         underscore(resource_class.__name__))
            class_dict['__tablename__'] = tablename

        for field_name, field in resource_class._fields:
            class_dict[field_name] = sql.Column(field.create_sql_type(),
                                                **field.column_options)

        for method_name, method in resource_class._methods:
            class_dict[method_name] = method

        return class_dict
