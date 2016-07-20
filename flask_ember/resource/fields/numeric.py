from sqlalchemy import types

from .field_base import FieldBase


class Numeric(FieldBase):
    __sql_type__ = types.Numeric
