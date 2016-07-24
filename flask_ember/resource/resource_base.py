from .resource_meta import ResourceMeta


class ResourceBase:
    """ The base class for a resource. This class must not be used directly.
    Instead the generated :attr:`flask_ember.FlaskEmber.Resource` field
    must be used as base class for resources.
    """
    pass
