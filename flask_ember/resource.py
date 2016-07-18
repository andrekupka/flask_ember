from .resource_meta import ResourceMeta


class Resource(metaclass=ResourceMeta):
    def parent_init(self, *args, **kwargs):
        return self.parent().__init__(*args, **kwargs)

    def parent(self):
        return super(self.__class__, self)
