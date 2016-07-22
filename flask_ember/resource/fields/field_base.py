import sqlalchemy as sql

from flask_ember.model.field_builder import FieldBuilder
from flask_ember.resource.resource_property_base import ResourcePropertyBase


class FieldBase(ResourcePropertyBase):
    """Base class for data declarations in resources. A field describes a
    simple plain data column. Therefore each field generates a
    :class:`sqlalchemy.Column` of the type that is specified in
    :const:`__sql_type__`.

    :param allowed_type_options: options that can be passed via **kwargs and
        are directly passed to the generated sqlalchemy type
    :type allowed_type_options: dict
    """

    #: A dictionary that specifies all column options that can be passed
    #: directly to the constructor of :class:`FieldBase`.
    COLUMN_OPTIONS = dict(
        primary_key=False,
        nullable=True,
        unique=False,
        default=None
    )

    #: The sqlalchemy type that is used to describe this column.
    __sql_type__ = None

    def __init__(self, allowed_type_options=None, **kwargs):
        #: The options that are passed to the constructor of the created
        #: sqlalchemy type.
        self.type_options = dict()
        #: The options that are passed to the constructor of the created
        #: :class:`sqlalchemy.Column`.
        self.column_options = dict()
        self._prepare_type_options(allowed_type_options or dict(), kwargs)
        self._prepare_column_options(kwargs)
        super().__init__()

    def do_register_at_descriptor(self, descriptor):
        descriptor.add_field(self, self.name)

    def create_property_builder(self):
        return FieldBuilder(self.__sql_type__, self.type_options,
                            self.column_options, resource_property=self)

    def _prepare_type_options(self, allowed_type_options, kwargs):
        for option, default_value in allowed_type_options.items():
            # TODO Some options might be contained or set as attribute as well,
            # e.g. the length of a string which could also be used for
            # validation purposes. Therefore simply popping options should be
            # reconsidered.
            self.type_options[option] = kwargs.pop(option, default_value)

    def _prepare_column_options(self, kwargs):
        """Adds the arguments that are defined in :const:`COLUMN_OPTIONS` and
        that are contained in the given arguments to the column options. If an
        option is not contained in arguments its default value is set.

        :param kwargs: the arguments from where options are extracted :type
        kwargs: dict
        """
        for option, default_value in FieldBase.COLUMN_OPTIONS.items():
            self.column_options[option] = kwargs.pop(option, default_value)
