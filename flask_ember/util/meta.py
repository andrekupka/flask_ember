import inspect


def get_class_fields(klass, predicate=None):
    # TODO generalize searching in nested class
    if '_resource_class' in klass.__dict__:
        klass = klass._resource_class
    return [(name, field) for name, field in klass.__dict__.items()
            if (predicate(name, field) if predicate else True)]


def get_inherited_fields(klass, predicate):
    return get_fields(klass, predicate, exclude_self=True)


def get_fields(klass, predicate=None, exclude_self=False):
    mro = klass.mro()[::-1]
    if exclude_self:
        mro = mro[:-1]

    fields = list()
    for base in mro:
        fields.extend(get_class_fields(base, predicate))
    return fields


def is_method(name, field):
    return inspect.isfunction(field)


def get_class_methods(klass):
    return get_class_fields(klass, is_method)


def get_inherited_methods(klass):
    return get_inherited_fields(klass, is_method)


def get_methods(klass):
    return get_fields(klass, is_method)
