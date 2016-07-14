class ResourceMeta(type):
    def __new__(mcs, name, bases, attrs):
        klass = super().__new__(mcs, name, bases, attrs)
        meta = attrs.get('Meta')
        klass._options = klass.OPTIONS_CLASS(meta)
        return klass

