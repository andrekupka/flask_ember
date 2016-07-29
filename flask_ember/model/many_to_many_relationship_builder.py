from sqlalchemy.sql.expression import and_
from sqlalchemy.sql.schema import Column, ForeignKeyConstraint, Table

from flask_ember.util.string import underscore
from .relationship_builder_base import RelationshipBuilderBase


class ManyToManyRelationshipBuilder(RelationshipBuilderBase):
    def __init__(self, **kwargs):
        self.secondary_join_clauses = list()
        super().__init__(use_list=True, **kwargs)

    @property
    def association_table(self):
        return self.resource_property.association_table

    @association_table.setter
    def association_table(self, association_table):
        assert self.association_table is None, 'There is already an ' \
                                               'association table.'
        self.resource_property.association_table = association_table

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
        table = Table(table_name, self.resource._metadata)
        self.association_table = table
        self.inverse.builder.association_table = table

    def create_non_primary_key_columns(self):
        # TODO this is obsolete as a many-to-many relationship always
        # generates a foreign key.
        if not self.generate_foreign_key:
            pass

        primary_columns = self.target_table.primary_key.columns
        if not primary_columns:
            raise Exception("No primary key found in table "
                            "'{}'.".format(self.target_table.fullname))

        foreign_key_names = list()
        foreign_key_ref_names = list()

        for primary_column in primary_columns:
            column_name = '{}_{}'.format(self.name,
                                         primary_column.key)
            column = Column(column_name, primary_column.type, primary_key=True)
            self.association_table.append_column(column)

            foreign_key_names.append(column.key)
            foreign_key_ref_names.append('{}.{}'.format(
                self.target_table.fullname, primary_column.key))
            self.secondary_join_clauses.append(column == primary_column)

        foreign_key_name = '_'.join(foreign_key_names)
        constraint_name = '{}_{}_fk'.format(self.association_table.fullname,
                                            foreign_key_name)
        constraint = ForeignKeyConstraint(foreign_key_names,
                                          foreign_key_ref_names,
                                          name=constraint_name)
        self.association_table.append_constraint(constraint)

    def get_relation_arguments(self):
        kwargs = super().get_relation_arguments()
        kwargs['secondary'] = self.association_table
        kwargs['primaryjoin'] = and_(
           *self.inverse.builder.secondary_join_clauses)
        kwargs['secondaryjoin'] = and_(*self.secondary_join_clauses)
        return kwargs
