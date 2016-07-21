import sqlalchemy as sql

from flask_ember.model.field_builder import FieldBuilder
from flask_ember.resource.resource_property_base import ResourcePropertyBase


class FieldBase(ResourcePropertyBase):
    """Base class for data declarations in resources. A field describes a
    simple plain data sqlalchemy column. Therefore each field generates a
    :class:`sqlalchemy.Column` of the type that is specified in
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
        self._prepare_column_options(kwargs)
        super().__init__()

    def do_register_at_descriptor(self, descriptor):
        descriptor.add_field(self, self.name)

    def create_property_builder(self):
        return FieldBuilder(self.__sql_type__, not
                            self.__dont_initialize_type__, self.sql_options,
                            self.column_options, resource_property=self)

    def _prepare_column_options(self, arguments):
        """Adds the arguments that are defined in
        :const:`DIRECT_COLUMN_OPTIONS` and that are contained in the given
        arguments to the column options. If an option is not contained in
        arguments its default value is set. Removes the name options from the
        column options and sets it as column_name attribute

        :param arguments: the arguments from where options are extracted
        :type arguments: dict
        """
        for name, default_value in FieldBase.DIRECT_COLUMN_OPTIONS.items():
            self.column_options[name] = arguments.pop(name, default_value)
        self.column_name = self.column_options.pop('name', None)

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
