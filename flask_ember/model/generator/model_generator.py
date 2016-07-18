import sqlalchemy as sql

from flask_ember.resource_options import ResourceOptions
from flask_ember.model.declarative_resource_meta import DeclarativeResourceMeta



class ModelGenerator:

    def __init__(self, ember, database=None, registry=None):
        self.ember = ember
        self.database = database or ember.database
        self.registry = registry or ember.model_registry

        self.model_base = self.create_model_base()

    def create_model_base(self):
        bases = (self.database.base_class,)
        class_dict = dict(
            __abstract__=True
        )
        return DeclarativeResourceMeta('FlaskEmberModelBase', bases, class_dict)

    def generate_abstract(self, resource_class):
        return self.generate_model(resource_class, abstract=True)

    def generate(self, resource_class):
        return self.generate_model(resource_class)

    def generate_model(self, resource_class, abstract=False):
        model_name = resource_class.__name__
        print("\nGENERATING: %s" % model_name)

        if model_name in self.registry:
            return self.registry[model_name]

        bases = self.get_original_bases(resource_class)
        class_dict = self.build_class_dict(resource_class, abstract=abstract)

        new_model_class = DeclarativeResourceMeta("New" + model_name, bases, class_dict)
        self.registry[model_name] = new_model_class
        return new_model_class

    def get_original_bases(self, resource_class):
        print("ORIGINAL BASES")
        print(resource_class.__bases__)
        bases = resource_class.__bases__ + (self.model_base,)
        print("NEW BASES")
        print(bases)
        return tuple(bases)

    def build_class_dict(self, resource_class, abstract):
        # TODO remove primary key generation
        class_dict = dict(
            id=sql.Column(sql.Integer, primary_key=True),
            _resource_class=resource_class,
            _is_generated=True
        )

        if abstract:
            class_dict['__abstract__'] = True
        else:
            from flask_ember.util.string import underscore
            tablename = (resource_class._options.tablename or
                         underscore(resource_class.__name__))
            class_dict['__tablename__'] = tablename

        for field_name, field in resource_class._fields:
            class_dict[field_name] = sql.Column(field.create_sql_type())

        for method_name, method in resource_class._methods:
            class_dict[method_name] = method

        return class_dict
