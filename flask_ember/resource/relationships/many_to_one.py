from sqlalchemy import and_, Column, ForeignKeyConstraint

from .relationship_base import RelationshipBase


class ManyToOne(RelationshipBase):

    def __init__(self, target_kind, *args, **kwargs):
        super().__init__(target_kind, *args, **kwargs)
        # TODO options for relationship and foreign keys
        self.column_options = dict()
        self.primary_join_clauses = []

    def create_keys(self, primary_key):
        if self.column_options.get('primary_key', False) != primary_key:
            return

        # create the target primary keys if they don't exist yet
        self.target._descriptor.create_primary_key_columns()
        target_table = self.target._table
        target_columns = target_table.primary_key.columns

        if not target_columns:
            raise Exception("No primary key found in target table "
                            "'{}' ".format(target_table.fullname))

        foreign_key_names = list()
        foreign_key_ref_names = list()

        for target_column in target_columns:
            column_name = '{}_{}'.format(self.name, target_column.key)
            column = Column(column_name, target_column.type)
            self.descriptor.add_column(column)

            foreign_key_names.append(column.key)
            foreign_key_ref_names.append('{}.{}'.format(target_table.fullname,
                                                        target_column.key))
            self.primary_join_clauses.append(column == target_column)

        constraint = ForeignKeyConstraint(foreign_key_names,
                                          foreign_key_ref_names)
        self.descriptor.add_constraint(constraint)

    def get_relation_kwargs(self):
        relation_kwargs = super().get_relation_kwargs()
        relation_kwargs.update(dict(
            primaryjoin=and_(*self.primary_join_clauses),
            lazy='select'
        ))
        return relation_kwargs
