from sqlalchemy import types

from .data_field_base import DataFieldBase


class Boolean(DataFieldBase):
    __sql_type__ = types.Boolean

    def __init__(self, create_constraint=True, name=None, *args, **kwargs):
        self.set_type_options(kwargs, create_constraint=create_constraint,
                              name=name)
        super().__init__(*args, **kwargs)
