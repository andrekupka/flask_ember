from sqlalchemy.ext.declarative import DeclarativeMeta

from flask_ember.resource_meta import ResourceMeta


class DeclarativeResourceMeta(DeclarativeMeta, ResourceMeta):

    def __new__(mcs, name, bases, attrs):
        print("\n" + (80 * '-') + "\nMODEL RESOURCE META: %s" % name)
        print(bases)
        if not name.startswith('New'):
            attrs['__abstract__'] = True
        klass = super().__new__(mcs, name, bases, attrs)
        return klass
