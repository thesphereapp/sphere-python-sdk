import unittest
from typing import Dict

from sphere.user.user import User
from sphere.user.user_state import UserState


class UserTest(unittest.TestCase):

    def test_building_from_dict(self):
        # given
        my_dict = self.user_dict()
        # when
        resp = User(**my_dict)
        # then
        self.assertEqual("62ae173adab723d7f0bdf42f", resp.id)
        self.assertEqual("ACTIVE", resp.state.name)
        self.assertEqual(1, len(resp.stateChangeLog))

    def test_state_change(self):
        my_dict = self.user_dict()
        user = User(**my_dict)
        self.assertEqual("ACTIVE", user.state.name)
        self.assertEqual(1, len(user.stateChangeLog))
        user.change_state(UserState.ACTIVE)
        self.assertEqual("ACTIVE", user.state.name)
        self.assertEqual(1, len(user.stateChangeLog))
        user.change_state(UserState.DELETED)
        self.assertEqual("DELETED", user.state.name)
        self.assertEqual(2, len(user.stateChangeLog))
        user.change_state(UserState.ACTIVE)
        self.assertEqual("ACTIVE", user.state.name)
        self.assertEqual(3, len(user.stateChangeLog))

    @staticmethod
    def user_dict() -> Dict[str, any]:
        return {
            "_id": "62ae173adab723d7f0bdf42f",
            "email": "example@gmail.com",
            "password": "xxx"
        }
