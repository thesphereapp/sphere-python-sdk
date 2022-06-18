import unittest
from typing import Dict

from sphere.profile.business_profile import BusinessProfile
from sphere.profile.profile_state import ProfileState


class BusinessProfileTest(unittest.TestCase):

    def test_building_from_dict(self):
        # given
        my_dict = self.profile_dict()
        # when
        resp = BusinessProfile(**my_dict)
        # then
        self.assertEqual("456", resp.userId)
        self.assertTrue(resp.wiseRecipientId is None)
        self.assertEqual("ACTIVE", resp.state.name)
        self.assertEqual(1, len(resp.stateChangeLog))

    def test_state_change(self):
        my_dict = self.profile_dict()
        business_profile = BusinessProfile(**my_dict)
        self.assertEqual("ACTIVE", business_profile.state.name)
        self.assertEqual(1, len(business_profile.stateChangeLog))
        business_profile.change_state(ProfileState.ACTIVE)
        self.assertEqual("ACTIVE", business_profile.state.name)
        self.assertEqual(1, len(business_profile.stateChangeLog))
        business_profile.change_state(ProfileState.DELETED)
        self.assertEqual("DELETED", business_profile.state.name)
        self.assertEqual(2, len(business_profile.stateChangeLog))
        business_profile.change_state(ProfileState.ACTIVE)
        self.assertEqual("ACTIVE", business_profile.state.name)
        self.assertEqual(3, len(business_profile.stateChangeLog))

    @staticmethod
    def profile_dict() -> Dict[str, any]:
        return {
            "_id": "123",
            "userId": "456",
            "webpage": "https://example.com",
            "avatar": "https://example.com/logo.png"
        }
