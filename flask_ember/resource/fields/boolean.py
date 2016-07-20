from sqlalchemy import types

from .field_base import FieldBase


class Boolean(FieldBase):
    __sql_type__ = types.Boolean
