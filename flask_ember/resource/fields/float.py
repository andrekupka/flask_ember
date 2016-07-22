from sqlalchemy import types

from .field_base import FieldBase


class Float(FieldBase):
    __sql_type__ = types.Float
