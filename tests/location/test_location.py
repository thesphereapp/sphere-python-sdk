import unittest
from typing import Dict

from sphere.location.location import Location
from sphere.location.location_state import LocationState


class LocationTest(unittest.TestCase):

    def test_building_from_dict(self):
        # given
        my_dict = self.location_dict()
        # when
        resp = Location(**my_dict)
        # then
        self.assertEqual("456", resp.userId)
        self.assertEqual(True, resp.is_active())
        self.assertEqual("ACTIVE", resp.state.name)
        self.assertEqual(1, len(resp.stateChangeLog))

    def test_state_change(self):
        my_dict = self.location_dict()
        location = Location(**my_dict)
        self.assertEqual("ACTIVE", location.state.name)
        self.assertEqual(1, len(location.stateChangeLog))
        location.change_state(LocationState.ACTIVE)
        self.assertEqual("ACTIVE", location.state.name)
        self.assertEqual(1, len(location.stateChangeLog))
        location.change_state(LocationState.DELETED)
        self.assertEqual("DELETED", location.state.name)
        self.assertEqual(2, len(location.stateChangeLog))
        location.change_state(LocationState.ACTIVE)
        self.assertEqual("ACTIVE", location.state.name)
        self.assertEqual(3, len(location.stateChangeLog))

    @staticmethod
    def location_dict() -> Dict[str, any]:
        return {
            "_id": "123",
            "userId": "456",
            "profileId": "999",
            "name": "My location"
        }
