from sqlalchemy import types

from .field_base import FieldBase


class Integer(FieldBase):
    __sql_type__ = types.Integer
