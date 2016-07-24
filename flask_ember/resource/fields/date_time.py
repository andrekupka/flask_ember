from sqlalchemy import types

from .field_base import FieldBase


class DateTime(FieldBase):
    __sql_type__ = types.DateTime

    TYPE_OPTIONS = ['timezone']

    def __init__(self, timezone=None, **kwargs):
        kwargs['timezone'] = timezone
        super().__init__(allowed_type_options=DateTime.TYPE_OPTIONS, **kwargs)
