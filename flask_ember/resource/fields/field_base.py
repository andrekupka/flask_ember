from flask_ember.model.field_builder import FieldBuilder
from flask_ember.resource.resource_property_base import ResourcePropertyBase


class FieldBase(ResourcePropertyBase):
    """ Base class for data declarations in resources. A field describes a
    simple plain data column. Therefore each field generates a
    :class:`sqlalchemy.Column` of the type that is specified in
    :const:`__sql_type__`.

    :param allowed_type_options: options that can be passed via **kwargs and
                                 are directly passed to the generated
                                 sqlalchemy type
    :type allowed_type_options: dict
    """

    #: A list that specifies all column options that can be passed directly to
    #: the constructor of :class:`FieldBase`.
    COLUMN_OPTIONS = [
        'primary_key',
        'nullable',
        'unique',
        'default'
    ]

    #: A list that specifies type options that are allowed for this field
    #: type. Subclasses can override this field to allow type options.
    __type_options__ = []

    #: The sqlalchemy type that is used to describe this column.
    __sql_type__ = None

    def __init__(self, **kwargs):
        #: The options that are passed to the constructor of the created
        #: sqlalchemy type.
        self.type_options = dict()
        #: The options that are passed to the constructor of the created
        #: :class:`sqlalchemy.Column`.
        self.column_options = dict()
        self._incorporate_options(self.__type_options__,
                                  self.type_options,
                                  kwargs)
        self._incorporate_options(FieldBase.COLUMN_OPTIONS,
                                  self.column_options,
                                  kwargs)
        super().__init__()

    def register_at_descriptor(self, descriptor):
        descriptor.add_field(self, self.name)

    def create_builder(self):
        return FieldBuilder(self.__sql_type__, self.type_options,
                            self.column_options, resource_property=self)

    def _incorporate_options(self, allowed_options, target_options, kwargs):
        """ Extracts all given allowed options from kwargs and sets them in
        the given target options. If an allowed option is not found in
        kwargs it will not be set. All allowed options will be popped from
        kwargs.

        :param allowed_options: The list of allowed options.
        :type allowed_options: list
        :param target_options: The dict where the allowed options are to be
                               incorporated into.
        :type target_options: dict
        :param kwargs: The arguments where allowed options are popped from.
        :type kwargs: dict
        """
        for option in allowed_options:
            # TODO some options may be preserved as attribute because they
            # might be used later by the api or validation generation (e.g.
            # nullable)
            value = kwargs.pop(option, None)
            if value is not None:
                target_options[option] = value
