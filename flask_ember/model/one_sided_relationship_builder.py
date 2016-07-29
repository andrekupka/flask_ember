from sqlalchemy.sql.expression import and_

from .relationship_builder_base import RelationshipBuilderBase


class OneSidedRelationshipBuilder(RelationshipBuilderBase):
    def __init__(self, **kwargs):
        super().__init__(force_primary_key=False, **kwargs)

    def get_relation_arguments(self):
        kwargs = super().get_relation_arguments()
        clause_source = (self if self.generate_foreign_key else
                         self.inverse.builder)
        kwargs['primaryjoin'] = and_(*clause_source.join_clauses)

        if self.table == self.target_table and not self.generate_foreign_key:
            kwargs['remote_side'] = [column for column in
                                     self.table.primary_key.columns]
        return kwargs
