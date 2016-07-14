from .resource_meta import ResourceMeta
from .resource_options  import ResourceOptions


class Resource(metaclass=ResourceMeta):
    OPTIONS_CLASS = ResourceOptions
