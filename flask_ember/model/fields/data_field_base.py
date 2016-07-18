import sqlalchemy as sql

from .field_base import FieldBase


DIRECT_COLUMN_OPTIONS = [
    ('primary_key', False),
    ('nullable', True),
    ('unique', False),
    ('default', None)
]


class DataFieldBase(FieldBase):
    __sql_type__ = None
    __dont_initialize_type__ = False

    def __init__(self, sql_options=None, column_options=None, **kwargs):
        self.sql_options = sql_options
        column_options = column_options or dict()
        self.add_column_options(column_options, kwargs)
        super().__init__(column_options=column_options, **kwargs)

    def add_column_options(self, column_options, arguments):
        """Adds the arguments that are defined in
        :const:`DIRECT_COLUMN_OPTIONS` and that are contained in the given
        arguments to the given column_options. If an option is not contained in
        arguments its default value is set.

        :param column_options: the column options
        :type column_options: dict
        :param arguments: the arguments from where options are extracted
        :type arguments: dict
        """
        for name, default_value in DIRECT_COLUMN_OPTIONS:
            column_options[name] = arguments.pop(name, default_value)

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
        if self.__dont_initialize_type__:
            return self.__sql_type__
        elif self.sql_options is not None:
            return self.__sql_type__(**self.sql_options)
        return self.__sql_type__()

    def create_sql_column(self):
        return sql.Column(self.create_sql_type(), **self.column_options)

