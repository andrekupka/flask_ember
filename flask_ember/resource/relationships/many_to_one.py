from sqlalchemy import and_, Column, ForeignKeyConstraint
from sqlalchemy.orm import backref

from .relationship_base import RelationshipBase
from flask_ember.util.string import underscore


class ManyToOne(RelationshipBase):

    def create_non_primary_key_columns(self, primary_key):
        # TODO consolidate with OneToMany
        # create the target primary keys if they don't exist yet
        self.target._descriptor.create_primary_key_columns()
        target_columns = self.target_table.primary_key.columns

        if not target_columns:
            raise Exception("No primary key found in target table "
                            "'{}' ".format(self.target_table.fullname))

        foreign_key_names = list()
        foreign_key_ref_names = list()

        for target_column in target_columns:
            column_name = '{}_{}'.format(self.name, target_column.key)
            column = Column(column_name, target_column.type)
            self.descriptor.add_column(column)

            foreign_key_names.append(column.key)
            foreign_key_ref_names.append(
                '{}.{}'.format(self.target_table.fullname, target_column.key))
            self.primary_join_clauses.append(column == target_column)

        foreign_key_name = '_'.join(foreign_key_names)
        constraint_name = '{}_{}_fk'.format(self.table.fullname,
                                            foreign_key_name)
        constraint = ForeignKeyConstraint(foreign_key_names,
                                          foreign_key_ref_names,
                                          name=constraint_name)
        self.descriptor.add_constraint(constraint)

    def get_relation_kwargs(self):
        kwargs = dict()
        if self.backref:
            kwargs['backref'] = backref(self.backref, lazy='dynamic')
        kwargs['lazy'] = 'select'
        kwargs['primaryjoin'] = and_(*self.primary_join_clauses)

        if self.target_table == self.table:
            # If there is a self reference the remote side of the relation must
            # be specified. The remote side consists of the primary key columns
            # of this resource.
            kwargs['remote_side'] = [column for column in
                                     self.table.primary_key.columns]
        return kwargs