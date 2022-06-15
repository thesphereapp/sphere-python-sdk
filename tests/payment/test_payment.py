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
            "fee": {
                "paymentProcessioningFee": {
                    "name": "Stripe payment processing fee",
                    "money": {
                        "amount": 32,
                        "currency": "GBP"
                    }
                },
                "sphereFee": {
                    "name": "Sphere platform fee",
                    "money": {
                        "amount": 85,
                        "currency": "GBP"
                    }
                },
                "payoutProcessingFee": {
                    "name": "Wise payout fee",
                    "money": {
                        "amount": 28,
                        "currency": "GBP"
                    }
                },
            },
            "externalReferenceId": "sp_123123123",
            "externalReference": "STRIPE_CHARGE_ID"
        }
        # when
        resp = Payment(**my_dict)
        # then
        self.assertEqual(resp.cartId, "300")
