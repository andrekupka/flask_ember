from sqlalchemy.sql.expression import and_
from sqlalchemy.sql.schema import Column, ForeignKeyConstraint

from .relationship_builder_base import RelationshipBuilderBase


class OneSidedRelationshipBuilder(RelationshipBuilderBase):
    def __init__(self, **kwargs):
        self.primary_join_clauses = list()
        super().__init__(**kwargs)

    def create_non_primary_key_columns(self):
        if not self.generate_foreign_key:
            return

        primary_columns = self.target_table.primary_key.columns
        if not primary_columns:
            raise Exception("No primary key found in table "
                            "'{}' ".format(self.target_table.fullname))

        foreign_key_names = list()
        foreign_key_ref_names = list()

        for primary_column in primary_columns:
            column_name = '{}_{}'.format(self.name,
                                         primary_column.key)
            column = Column(column_name, primary_column.type)
            self.builder.add_column(column)

            foreign_key_names.append(column.key)
            foreign_key_ref_names.append('{}.{}'.format(
                self.target_table.fullname, primary_column.key))
            self.primary_join_clauses.append(column == primary_column)

        foreign_key_name = '_'.join(foreign_key_names)
        constraint_name = '{}_{}_fk'.format(self.table.fullname,
                                            foreign_key_name)
        constraint = ForeignKeyConstraint(foreign_key_names,
                                          foreign_key_ref_names,
                                          name=constraint_name)
        self.builder.add_constraint(constraint)

    def get_relation_arguments(self):
        kwargs = super().get_relation_arguments()
        clause_source = (self if self.generate_foreign_key else
                         self.inverse.builder)
        kwargs['primaryjoin'] = and_(*clause_source.primary_join_clauses)

        if self.table == self.target_table and not self.generate_foreign_key:
            kwargs['remote_side'] = [column for column in
                                     self.table.primary_key.columns]
        return kwargs
