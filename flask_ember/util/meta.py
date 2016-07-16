import inspect


def get_class_fields(klass, predicate=None):
    return [(name, field) for name, field in klass.__dict__.items()
            if (predicate(name, field) if predicate else True)]


def get_fields(klass, predicate=None):
    fields = list()
    for base in inspect.getmro(klass)[::-1]:
        fields.extend(get_class_fields(base, predicate))
    return fields


def get_methods(klass):
    return get_fields(klass, lambda name, field: inspect.isfunction(field))
