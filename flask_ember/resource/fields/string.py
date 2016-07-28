from sqlalchemy import types

from .field_base import FieldBase


class String(FieldBase):
    __sql_type__ = types.String

    __type_options__ = ['length']

    def __init__(self, length=None, **kwargs):
        kwargs['length'] = length
        super().__init__(**kwargs)
