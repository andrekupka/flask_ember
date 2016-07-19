import sqlalchemy as sql

from .field_base import FieldBase


class DataFieldBase(FieldBase):
    """Base class for data field declarations in resources. A data field
    describes a simple plain data sqlalchemy column. Therefore each data field
    generates a :class:`sqlalchemy.Column` of the type that is specified in
    :const:`__sql_type__`.

    :param sql_options: options that are directly forwarded to the generated
        sqlalchemy type
    :type sql_options: dict
    :param column_options: options that are directly forwarded to the generated
        :class:`sqlalchemy.Column`
    :type column_options: dict
    """

    #: A dictionary that specifies all column options that can be passed
    #: directly to the constructor of :class:`DataFieldBase` instead of the
    #: column_options parameter.
    DIRECT_COLUMN_OPTIONS = dict(
        primary_key=False,
        nullable=True,
        unique=False,
        default=None
    )

    #: The sqlalchemy type that is used to describe this column.
    __sql_type__ = None

    #: Set this to True to force the generation of a sqlalchemy type whose
    #: constructor is not called.
    __dont_initialize_type__ = False

    def __init__(self, sql_options=None, column_options=None, **kwargs):
        #: The options that are passed to the constructor of the created
        #: sqlalchemy type.
        self.sql_options = sql_options or dict()
        #: The options that are passed to the constructor of the created
        #: :class:`sqlalchemy.Column`.
        self.column_options = column_options or dict()
        self.add_column_options(self.column_options, kwargs)

    def add_column_options(self, column_options, arguments):
        """Adds the arguments that are defined in
        :const:`DIRECT_COLUMN_OPTIONS` and that are contained in the given
        arguments to the given column options. If an option is not contained in
        arguments its default value is set.

        :param column_options: the column options
        :type column_options: dict
        :param arguments: the arguments from where options are extracted
        :type arguments: dict
        """
        for name, default_value in DataFieldBase.DIRECT_COLUMN_OPTIONS.items():
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

    def prepare_attributes(self, field_name, attrs):
        attrs[field_name] = sql.Column(self.create_sql_type(),
                                       **self.column_options)

    def create_sql_type(self):
        """Creates the sqlalchemy type that represents this data field. The
        type that shall be returned is specified by :const:`__sql_type__` of
        subclasses. If :const:`__dont_initialize_type__` is set the type is
        directly returned, otherwise the type's constructor is called and
        :attr:`sql_options` is expanded as parameter.

        :rtype: an sqlalchemy type
        """
        if self.__dont_initialize_type__:
            return self.__sql_type__
        return self.__sql_type__(**self.sql_options)
