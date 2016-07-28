from sqlalchemy import types

from .field_base import FieldBase


class DateTime(FieldBase):
    __sql_type__ = types.DateTime

    __type_options__ = ['timezone']

    def __init__(self, timezone=None, **kwargs):
        kwargs['timezone'] = timezone
        super().__init__(**kwargs)
