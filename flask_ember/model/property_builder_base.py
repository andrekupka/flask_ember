from abc import ABCMeta


class PropertyBuilderBase(metaclass=ABCMeta):
    """ Base class for property builders. A property builder is responsible
    for generate the sqlalchemy columns and relations out of a property. The
    adding of those is delegated to and centrally managed by a
    :class:`ModelBuilder` which is part of the resource's descriptor.

    :param resource_property: The property of the resource that is to be
                              constructed.
    :type resource_property: ResourcePropertyBase
    """

    def __init__(self, resource_property):
        #: The property of the resource for which a sqlalchemy model is
        #: generated.
        self.resource_property = resource_property

    @property
    def name(self):
        """ The name of the underlying property in the resource.
        """
        return self.resource_property.name

    @property
    def resource(self):
        """ The underlying resource.
        """
        return self.resource_property.resource

    @property
    def resource_name(self):
        return self.resource.__name__

    @property
    def table(self):
        """ The generated sqlalchemy table that maps the resource.
        """
        return self.resource._table

    @property
    def metadata(self):
        """ The sqlalchemy metadata.
        """
        return self.resource._metadata

    @property
    def builder(self):
        """ The central model builder.
        """
        return self.resource._descriptor.model_builder

    def add_table_column(self, column):
        self.builder.add_column(column)

    def add_mapper_property(self, name, prop):
        self.builder.add_property(name, prop)

    def create_association_tables(self):
        """ Creates association tables for a property (mainly
        relationships). Can be overridden by subclasses.
        """
        pass

    def create_primary_key_columns(self):
        """ Creates primary key columns for a property. Can be overridden by
        subclasses.
        """
        pass

    def create_non_primary_key_columns(self):
        """ Creates non-primary key columns for a property. Can be
        overridden by subclasses.
        """
        pass

    def create_properties(self):
        """ Creates additional properties in the sqlalchemy mapper for a
        property. Can be overridden by subclasses.
        """
        pass
