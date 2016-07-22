from copy import deepcopy

from .resource_descriptor import ResourceDescriptor
from .resource_property_base import ResourcePropertyBase
from flask_ember.util.meta import (get_class_attributes,
                                   get_inherited_attributes)


class ResourceMeta(type):

    def __init__(cls, name, bases, attrs):
        print("\nGenerating %s\n" % name)
        # TODO this check is a dirty hack and should be improved
        if not hasattr(cls._ember, 'Resource'):
            # if this is the resource base class ignore instrumentation, this
            # works because when the resource base is generated, it is not set
            # in the ember object
            return

        ResourceMeta.instrument_resource(cls)

    @staticmethod
    def instrument_resource(cls):
        descriptor = cls._descriptor = ResourceDescriptor(cls)

        # TODO if this is an abstract class really abort here?
        if descriptor.options.abstract:
            return

        cls._table = None
        cls._mapper = None

        cls._model_generated = False

        properties = ResourceMeta.collect_and_copy_properties(cls)
        for name, prop in properties:
            prop.register_at_descriptor(cls, name)

        cls._ember.register_resource(cls)

    @staticmethod
    def collect_and_copy_properties(cls):
        # TODO filter properties from base classes that are no resources and
        # thus are no instance from ResourceMeta
        inherited_properties = get_inherited_attributes(
            cls, ResourceMeta.is_property)
        base_properties = map(lambda prop: (prop[0], deepcopy(prop[1])),
                              inherited_properties)
        properties = get_class_attributes(cls, ResourceMeta.is_property)
        return list(base_properties) + properties

    @staticmethod
    def is_property(name, field):
        return isinstance(field, ResourcePropertyBase)
