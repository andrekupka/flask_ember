from .declarative_model_meta import DeclarativeModelMeta


class ModelBase(metaclass=DeclarativeModelMeta):
    __abstract__ = True

    def parent_init(self, *args, **kwargs):
        return self.parent().__init__(*args, **kwargs)

    def parent(self):
        return super(self.__class__, self)
