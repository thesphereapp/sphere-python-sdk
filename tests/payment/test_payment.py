import unittest
from typing import Dict

from sphere.payment.payment import Payment


class PaymentTest(unittest.TestCase):

    def test_building_from_dict(self):
        # given
        my_dict = self.__dict_value()
        # when
        resp = Payment(**my_dict)
        # then
        self.assertEqual("62ae1547e32e5edcd494aa39",resp.cartId)

    @staticmethod
    def __dict_value() -> Dict[str, any]:
        return {
            "_id": "62ae1550abbc8ba71b6ecf09",
            "cartId": "62ae1547e32e5edcd494aa39",
            "orderId": "62ae1557393af9c2ae86a5b2",
            "baseMoney": {
                "amount": 850,
                "currency": "GBP"
            },
            "netMoney": {
                "amount": 701,
                "currency": "GBP"
            },
            "fees": [
                {
                    "name": "Stripe card processing",
                    "money": {
                        "amount": 32,
                        "currency": "GBP"
                    }
                },
                {
                    "name": "Sphere platform",
                    "money": {
                        "amount": 85,
                        "currency": "GBP"
                    }
                },
                {
                    "name": "Wise payout",
                    "money": {
                        "amount": 32,
                        "currency": "GBP"
                    }
                },
            ],
            "externalReferenceId": "sp_123123123",
            "externalReference": "STRIPE_CHARGE_ID",
            "createdDate": "2022-03-10 07:00:00.550604",
        }
