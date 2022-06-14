import unittest
from sphere.payment.payment import Payment


class PaymentTest(unittest.TestCase):

    def test_building_from_dict(self):
        # given
        my_dict = {
            "_id": "123",
            "cartId": "300",
            "orderId": "456",
            "money": {
                "amount": 500,
                "currency": "GBP"
            },
            "externalReferenceId": "sp_123123123",
            "externalReference": "STRIPE",
            "createdDate": "2022-03-10 07:00:00.550604",
        }
        # when
        resp = Payment(**my_dict)
        # then
        self.assertEqual(resp.cartId, "300")
