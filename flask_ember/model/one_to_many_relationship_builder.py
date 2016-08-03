from .one_sided_relationship_builder import OneSidedRelationshipBuilder


class OneToManyRelationshipBuilder(OneSidedRelationshipBuilder):
    def get_relation_arguments(self):
        kwargs = super().get_relation_arguments()
        if self.inverse.weak:
            kwargs['cascade'] = 'all, delete-orphan'
            # As the foreign key cascades are configured for weak
            # relationships, we can use passive deletes and let the database
            # engine do the rest.
            kwargs['passive_deletes'] = True
        return kwargs
