from sqlalchemy.ext.declarative import DeclarativeMeta

from flask_ember.resource_meta import ResourceMeta


class DeclarativeModelMeta(DeclarativeMeta, ResourceMeta):

    def __new__(mcs, name, bases, attrs):
        print("\n" + (80 * '-') + "\nDECLARATIVE MODEL META: %s" % name)
        print(bases)
        print(attrs)
        # TODO We set this class to abstract if it is a resource and not a
        # model class in order to avoid sqlalchemy table generation. This is
        # kind of a dirty hack as a resource should not inherit from any model
        # class. Nevertheless this is currently not possible as the parent
        # resource class is replaced by a model class with the abstractresource
        # decorator.
        if not attrs.get('_is_model', False):
            attrs['__abstract__'] = True
        klass = super().__new__(mcs, name, bases, attrs)
        return klass
