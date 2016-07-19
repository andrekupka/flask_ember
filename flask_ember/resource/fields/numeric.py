from sqlalchemy import types

from .data_field_base import DataFieldBase


class Numeric(DataFieldBase):
    __sql_type__ = types.Numeric
