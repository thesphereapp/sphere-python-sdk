import unittest
from typing import Dict

from sphere.payment.payment_fee import Fee


class FeeTest(unittest.TestCase):

    def test_building_from_dict(self):
        # given
        my_dict = self.__dict_value()
        # when
        resp = Fee(**my_dict)
        # then
        self.assertEqual(resp.name, "Stripe card processing fee")

    @staticmethod
    def __dict_value() -> Dict[str, any]:
        return {
            "name": "Stripe card processing fee",
            "money": {
                "amount": 500,
                "currency": "GBP"
            }
        }
