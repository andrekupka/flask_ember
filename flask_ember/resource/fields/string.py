from sqlalchemy import types

from .field_base import FieldBase


class String(FieldBase):
    __sql_type__ = types.String

    TYPE_OPTIONS = ['length']

    def __init__(self, length=None, **kwargs):
        kwargs['length'] = length
        super().__init__(allowed_type_options=String.TYPE_OPTIONS, **kwargs)
