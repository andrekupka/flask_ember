def get_class_attributes(cls, predicate=None):
    """ Returns all attributes from the given class without its base classes
    that match the given predicate. If no predicate is given all attributes are
    returned.

    :param cls: The class to fetch attributes from.
    :type cls: type
    :param predicate: The predicate an attribute must fulfill.
    :type predicate: callable(name: str, attribute)
    :rtype: list
    """
    return [(name, attr) for name, attr in cls.__dict__.items()
            if (predicate(name, attr) if predicate else True)]


def get_inherited_attributes(cls, predicate):
    """ Returns all attributes from the given class' base classes that match
    the given predicate. If no predicate is given all attributes are returned.

    :param cls: The class to fetch attributes from.
    :type cls: type
    :param predicate: The predicate an attribute must fulfill.
    :type predicate: callable(name: str, attribute)
    :rtype: list
    """
    return get_attributes(cls, predicate, exclude_self=True)


def get_attributes(cls, predicate=None, exclude_self=False):
    """ Returns all attributes from the given class (and its base classes)
    that match the given prediate. If no predicate is given all attributes are
    returned. If exclude_self is set to True attributes from the class itself
    are excluded from the result.

    :param cls: The class to fetch attributes from.
    :type cls: type
    :param predicate: The prediate an attribute must fulfill.
    :type predicate: callable(name: str, attribute)
    :param explude_self: Whether to exclude the class itself and only consider
        parents.
    :type exclude_self: bool
    :rtype: list
    """
    mro = cls.mro()[::-1]
    if exclude_self:
        mro = mro[:-1]

    attrs = list()
    for base in mro:
        attrs.extend(get_class_attributes(base, predicate))
    return attrs
