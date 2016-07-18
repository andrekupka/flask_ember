from .field_base import FieldBase


class DataFieldBase(FieldBase):
    __sql_type__ = None

    def __init__(self, type_options=None, primary_key=False,
                 column_options=None, **kwargs):
        self.type_options = type_options
        merge_options = dict(primary_key=primary_key)
        if column_options:
            column_options.update(merge_options)
        else:
            column_options = merge_options
        super().__init__(column_options=column_options, **kwargs)

    def set_type_options(self, arguments, **kwargs):
        arguments['type_options'] = kwargs

    def create_sql_type(self):
        if self.type_options is not None:
            return self.__sql_type__(**self.type_options)
        return self.__sql_type__
