from sqlalchemy import Column, ForeignKeyConstraint, and_
from sqlalchemy.orm import backref, relationship

from .property_builder_base import PropertyBuilderBase


class RelationshipBuilder(PropertyBuilderBase):

    def __init__(self, backref, is_self_single_side, has_many_side=True, *args,
                 **kwargs):
        self.backref = backref
        self.is_self_single_side = is_self_single_side
        self.has_many_side = has_many_side
        self.primary_join_clauses = list()
        super().__init__(*args, **kwargs)

    @property
    def target(self):
        return self.resource_property.target

    @property
    def target_table(self):
        return self.target._table

    def _get_one_and_many_table(self):
        if self.is_self_single_side:
            return self.table, self.target_table
        return self.target_table, self.table

    def _get_many_model_builder(self):
        if self.is_self_single_side:
            return self.target._descriptor.model_builder
        return self.builder

    def create_non_primary_key_columns(self):
        one_table, many_table = self._get_one_and_many_table()
        builder = self._get_many_model_builder()

        primary_columns = one_table.primary_key.columns
        if not primary_columns:
            raise Exception("No primary key found in table "
                            "'{}' ".format(one_table.fullname))

        foreign_key_names = list()
        foreign_key_ref_names = list()

        for primary_column in primary_columns:
            column_name = '{}_{}'.format(one_table.fullname,
                                         primary_column.key)
            column = Column(column_name, primary_column.type)
            builder.add_column(column)

            foreign_key_names.append(column.key)
            foreign_key_ref_names.append(
                '{}.{}'.format(one_table.fullname,
                               primary_column.key))
            self.primary_join_clauses.append(column == primary_column)

        foreign_key_name = '_'.join(foreign_key_names)
        constraint_name = '{}_{}_fk'.format(many_table.fullname,
                                            foreign_key_name)
        constraint = ForeignKeyConstraint(foreign_key_names,
                                          foreign_key_ref_names,
                                          name=constraint_name)
        builder.add_constraint(constraint)

    def _get_lazy_options(self):
        if not self.has_many_side:
            return 'select', 'select'
        elif self.is_self_single_side:
            return 'select', 'dynamic'
        return 'dynamic', 'select'

    def _get_uselist_option(self):
        if not self.has_many_side:
            return False, False
        elif self.is_self_single_side:
            return False, True
        return True, False

    def _get_relation_kwargs(self):
        backref_lazy, lazy = self._get_lazy_options()
        backref_uselist, uselist = self._get_uselist_option()

        kwargs = {
            'lazy': lazy,
            'uselist': uselist,
            'primaryjoin': and_(*self.primary_join_clauses)
        }
        if self.backref:
            kwargs['backref'] = backref(self.backref, lazy=backref_lazy,
                                        uselist=backref_uselist)
        if self.table == self.target_table:
            kwargs['remote_side'] = [column for column in
                                     self.table.primary_key.columns]
        return kwargs

    def create_properties(self):
        relation_kwargs = self._get_relation_kwargs()
        relation = relationship(self.target, **relation_kwargs)
        self.add_mapper_property(self.name, relation)
