import unittest
from typing import Dict

from sphere.order.order_state import OrderState
from sphere.order.order_state_log import OrderStateLog
from sphere.order.participant import Participant


class ParticipantTest(unittest.TestCase):

    def test_building_from_dict(self):
        # given
        my_dict = self.order_dict()
        # when
        resp = Participant(**my_dict)
        # then
        self.assertEqual(resp.email, "james.clark@example.com")

    @staticmethod
    def order_dict() -> Dict[str, any]:
        return  {
                "name": "James Clark",
                "email": "james.clark@example.com",
            }
