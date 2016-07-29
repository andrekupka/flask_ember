from sqlalchemy.sql.expression import and_
from sqlalchemy.sql.schema import Table

from flask_ember.util.string import underscore
from .association_table_builder_proxy import AssociationTableBuilderProxy
from .relationship_builder_base import RelationshipBuilderBase


class ManyToManyRelationshipBuilder(RelationshipBuilderBase):
    def __init__(self, **kwargs):
        self._association_builder_proxy = None
        super().__init__(use_list=True, **kwargs)

    @property
    def association_table(self):
        return self.resource_property.association_table

    @association_table.setter
    def association_table(self, association_table):
        assert self.association_table is None, 'There is already an ' \
                                               'association table.'
        self.resource_property.association_table = association_table
        self._association_builder_proxy = AssociationTableBuilderProxy(
            association_table)

    @property
    def foreign_key_builder(self):
        assert self._association_builder_proxy is not None, 'There is no ' \
                                                            'association ' \
                                                            'table yet.'
        return self._association_builder_proxy

    def create_association_tables(self):
        # If the inverse relation has already created the association table
        # this step is obsolete.
        if self.association_table is not None:
            return

        source_name = underscore(self.resource_name)
        target_name = underscore(self.inverse.resource_name)
        table_name = ('{}_{}_{}_{}_association'.format(source_name,
                                                       self.name,
                                                       target_name,
                                                       self.inverse.name))
        table = Table(table_name, self.metadata)
        self.association_table = table
        self.inverse.builder.association_table = table

    def get_relation_arguments(self):
        kwargs = super().get_relation_arguments()
        kwargs['secondary'] = self.association_table
        kwargs['primaryjoin'] = and_(
            *self.inverse.builder.join_clauses)
        kwargs['secondaryjoin'] = and_(*self.join_clauses)
        return kwargs
