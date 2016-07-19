from sqlalchemy.ext.declarative import DeclarativeMeta

from .resource_options import ResourceOptions
from flask_ember.resource.fields import FieldBase
from flask_ember.util.collection import filter_dict_values
from flask_ember.util.meta import has_attribute


class ResourceMeta(DeclarativeMeta):

    def __new__(mcs, name, bases, attrs):
        print("Generating %s" % name)
        is_base_class = not has_attribute(bases, attrs, '_ember')
        mcs.prepare_attributes(is_base_class, name, attrs)
        klass = super().__new__(mcs, name, bases, attrs)
        if not is_base_class:
            # This works, as the generated Resource base class has no _ember object
            # field, because it is set after constructing the declarative base and
            # thus after the metaclass is executed.
            ember = getattr(klass, '_ember')
            ember.register_resource(klass)
        return klass

    @classmethod
    def prepare_attributes(mcs, is_base_class, name, attrs):
        # A resource base class has no _ember attribute set and needs no
        # meta generation except from fields.
        if is_base_class:
            attrs['__abstract__'] = True
        else:
            # TODO how to handle recursive meta definitions from parent
            options = ResourceOptions(attrs.get('Meta'))
            attrs['_options'] = options

            attrs['__abstract__'] = options.abstract
            if not options.abstract:
                attrs['__tablename__'] = mcs.get_table_name(name, options)

        # TODO should fields be possibly in a base class
        fields = filter_dict_values(attrs, mcs.is_field)
        for field_name, field in fields.items():
            attrs[field_name] = field.create_sql_column()
        attrs['_fields'] = fields

    @classmethod
    def get_table_name(mcs, name, options):
        tablename = options.tablename
        if tablename is None:
            # this is save as tablename_function has a default value
            tablename_generator = options.tablename_generator
            tablename = tablename_generator(name)
        return tablename

    @classmethod
    def is_field(mcs, name, field):
        return isinstance(field, FieldBase)
