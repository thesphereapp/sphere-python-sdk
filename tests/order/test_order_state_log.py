import unittest
from typing import Dict

from sphere.order.order_state import OrderState
from sphere.order.order_state_log import OrderStateLog


class OrderStateLogTest(unittest.TestCase):

    def test_building_from_dict(self):
        # given
        my_dict = self.order_dict()
        # when
        resp = OrderStateLog(**my_dict)
        # then
        self.assertEqual(resp.state, OrderState.NEW)

    @staticmethod
    def order_dict() -> Dict[str, any]:
        return {
                "state": "NEW",
                "date": "2022-03-10 07:00:00.550604",
            }
