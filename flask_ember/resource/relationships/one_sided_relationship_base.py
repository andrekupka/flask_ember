from .relationship_base import RelationshipBase


class OneSidedRelationshipBase(RelationshipBase):
    def __init__(self, *args, weak=None, strong=None, **kwargs):
        assert not (weak and strong), 'weak or strong but not both must be ' \
                                      'specified!'
        self.weak = weak
        self.strong = strong
        super().__init__(*args, **kwargs)

    def get_inverse_arguments(self):
        return dict(
            weak=self.weak,
            strong=self.strong
        )

    def check_compatibility(self, inverse):
        # TODO improve error messages
        # Both sides must either have the same weak/strong setting or at least
        # one of both must be None.
        weak = self.weak == inverse.weak or (self.weak is None or
                                             inverse.weak is None)
        assert weak, 'Inconsistent weak configuration!'
        strong = self.strong == inverse.strong or (self.strong is None or
                                                   inverse.strong is None)
        assert strong, 'Inconsistent strong configuration!'
        # The primary settings of both sides must be equal, thus if one side
        # is None it can be adjusted to the other one.
        assert self.primary != inverse.primary, 'Inconsistent primary ' \
                                                'configuration!.'

    def configure_inverse(self, inverse):
        self.weak = inverse.weak = self.weak or inverse.weak
        self.strong = inverse.strong = self.strong or inverse.strong
