from .field_base import FieldBase


class DataFieldBase(FieldBase):
    __sql_type__ = None

    def __init__(self, sql_options=None, primary_key=False,
                 column_options=None, **kwargs):
        self.sql_options = sql_options
        merge_options = dict(primary_key=primary_key)
        if column_options:
            column_options.update(merge_options)
        else:
            column_options = merge_options
        super().__init__(column_options=column_options, **kwargs)

    def add_sql_options(self, arguments, **sql_options):
        """Adds the given sql options to the given arguments. If no sql options
        are set yet the given options are set directly.

        :param arguments: the arguments to which the sql options are added
        :type arguments: dict
        :param sql_options: the sql options that are to be added
        :type sql_options: dict
        """
        if 'sql_options' in arguments:
            arguments['sql_options'].update(sql_options)
        else:
            arguments['sql_options'] = sql_options

    def create_sql_type(self):
        if self.sql_options is not None:
            return self.__sql_type__(**self.sql_options)
        return self.__sql_type__
