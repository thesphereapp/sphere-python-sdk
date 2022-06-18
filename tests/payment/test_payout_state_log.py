import unittest
from typing import Dict

from sphere.payment.payout_state_log import PayoutStateLog


class PayoutStateLogTest(unittest.TestCase):

    def test_building_from_dict(self):
        # given
        my_dict = self.__dict_value()
        # when
        resp = PayoutStateLog(**my_dict)
        # then
        self.assertEqual(resp.state.name, "COMPLETED")

    def test_default(self):
        # when
        resp = PayoutStateLog()
        # then
        self.assertEqual(resp.state.name, "NEW")

    @staticmethod
    def __dict_value() -> Dict[str, any]:
        return {
            "state": "COMPLETED",
            "date": "2022-03-10 07:00:00.550604",
        }
