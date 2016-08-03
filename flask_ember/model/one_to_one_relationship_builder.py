from .one_sided_relationship_builder import OneSidedRelationshipBuilder


class OneToOneRelationshipBuilder(OneSidedRelationshipBuilder):
    def __init__(self, **kwargs):
        super().__init__(use_list=False, **kwargs)

    def get_foreign_key_arguments(self):
        kwargs = super().get_foreign_key_arguments()
        if self.generate_foreign_key:
            if self.resource_property.strong:
                kwargs['ondelete'] = 'CASCADE'
            elif self.resource_property.weak:
                kwargs['ondelete'] = 'SET NULL'
        return kwargs

    def get_relation_arguments(self):
        kwargs = super().get_relation_arguments()
        if not self.generate_foreign_key and self.resource_property.strong:
            kwargs['cascade'] = 'all, delete-orphan'
            kwargs['passive_deletes'] = True
        return kwargs
