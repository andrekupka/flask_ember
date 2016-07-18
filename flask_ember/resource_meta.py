import inspect

from flask_ember.model.fields.field_base import FieldBase
from flask_ember.util.meta import (get_class_fields, get_fields,
                                   get_class_methods)
from flask_ember.resource_options import ResourceOptions


class ResourceMeta(type):

    def __new__(mcs, name, bases, attrs):
        klass = super().__new__(mcs, name, bases, attrs)
        meta = attrs.get('Meta')
        klass._options = ResourceOptions(meta)
        klass._fields = get_class_fields(klass, mcs.is_field)
        klass._methods = get_class_methods(klass)
        print("\nMETA: %s with %s" % (name, mcs.__name__))
        print(bases)
        print(attrs)
        print(klass._options)
        print(klass._fields)
        print(klass._methods)
        return klass

    @classmethod
    def is_field(mcs, name, field):
        return isinstance(field, FieldBase)
