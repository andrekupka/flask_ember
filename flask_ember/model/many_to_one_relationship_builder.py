from .one_sided_relationship_builder import OneSidedRelationshipBuilder


class ManyToOneRelationshipBuilder(OneSidedRelationshipBuilder):
    def get_foreign_key_arguments(self):
        kwargs = super().get_foreign_key_arguments()
        if self.resource_property.weak:
            kwargs['ondelete'] = 'CASCADE'
        elif self.resource_property.strong:
            kwargs['ondelete'] = 'SET NULL'
        return kwargs
