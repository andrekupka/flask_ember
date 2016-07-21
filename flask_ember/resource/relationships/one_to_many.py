from sqlalchemy import and_, Column, ForeignKeyConstraint
from sqlalchemy.orm import backref

from .relationship_base import RelationshipBase
from flask_ember.util.string import underscore


class OneToMany(RelationshipBase):

    def create_non_primary_key_columns(self):
        # TODO consolidate with ManyToOne
        primary_key_columns = self.table.primary_key.columns
        if not primary_key_columns:
            raise Exception("No primary key found in table "
                            "'{}'.".format(self.table.fullname))

        target_descriptor = self.target._descriptor

        foreign_key_names = list()
        foreign_key_ref_names = list()

        for primary_key_column in primary_key_columns:
            column_name = '{}_{}'.format(self.table.fullname,
                                         primary_key_column.key)
            column = Column(column_name, primary_key_column.type)
            target_descriptor.add_column(column)

            foreign_key_names.append(column.key)
            foreign_key_ref_names.append(
                '{}.{}'.format(self.table.fullname, primary_key_column.key))
            self.primary_join_clauses.append(column == primary_key_column)

        foreign_key_name = '_'.join(foreign_key_names)
        constraint_name = '{}_{}_fk'.format(self.target_table.fullname,
                                            foreign_key_name)
        constraint = ForeignKeyConstraint(foreign_key_names,
                                          foreign_key_ref_names,
                                          name=constraint_name)
        target_descriptor.add_constraint(constraint)

    def get_relation_kwargs(self):
        kwargs = dict()
        if self.backref:
            kwargs['backref'] = backref(self.backref, lazy='select')
        kwargs['lazy'] = 'dynamic'
        kwargs['primaryjoin'] = and_(*self.primary_join_clauses)

        if self.target_table == self.table:
            # If there is a self reference the remote side of the relation must
            # be specified. The remote side consists of the primary key columns
            # of this resource.
            kwargs['remote_side'] = [column for column in
                                     self.table.primary_key.columns]
        return kwargs
