import unittest

from dns.immutable import Dict
from sphere.finance.currency import Currency

from sphere.payment.payment import Payment
from sphere.payment.payout import Payout
from sphere.payment.payout_state import PayoutState


class PayoutTest(unittest.TestCase):

    def test_building_from_dict(self):
        # given
        my_dict = self.__dict_value()
        # when
        resp = Payout(**my_dict)
        # then
        self.assertEqual(len(resp.paymentIds), 7)

    def test_adding_payment_happy_flow(self):
        payout = Payout(**self.__dict_value())
        payment = Payment(**self.__payment_dict())
        self.assertEqual(7, len(payout.paymentIds))
        payout.add_payment(payment)
        self.assertEqual(8, len(payout.paymentIds))
        self.assertEqual("GBP", payout.baseMoney.currency.value)
        self.assertEqual(1050, payout.baseMoney.amount)

    def test_adding_payment_already_processed(self):
        payout = Payout(**self.__dict_value())
        payment = Payment(**self.__payment_dict())
        payment.id = "1"
        self.assertEqual(7, len(payout.paymentIds))
        payout.add_payment(payment)
        self.assertEqual(7, len(payout.paymentIds))
        self.assertEqual("GBP", payout.baseMoney.currency.value)
        self.assertEqual(1000, payout.baseMoney.amount)

    def test_adding_payment_with_different_currency(self):
        payout = Payout(**self.__dict_value())
        payment = Payment(**self.__payment_dict())
        payment.netMoney.currency = Currency.EUR
        self.assertEqual(7, len(payout.paymentIds))

        error_was_raised = False
        error_message = ""
        try:
            payout.add_payment(payment)
        except ValueError as e:
            error_was_raised = True
            error_message = e.args[0]

        self.assertTrue(error_was_raised)
        self.assertEqual("Payout and payment have different currencies. EUR vs GBP", error_message)
        self.assertEqual(7, len(payout.paymentIds))
        self.assertEqual("GBP", payout.baseMoney.currency.value)
        self.assertEqual(1000, payout.baseMoney.amount)

    def test_state_change(self):
        my_dict = self.__dict_value()
        payout = Payout(**my_dict)
        self.assertEqual("NEW", payout.state.name)
        self.assertEqual(1, len(payout.stateChangeLog))
        payout.change_state(PayoutState.NEW)
        self.assertEqual("NEW", payout.state.name)
        self.assertEqual(1, len(payout.stateChangeLog))
        payout.change_state(PayoutState.IN_PROGRESS)
        self.assertEqual("IN_PROGRESS", payout.state.name)
        self.assertEqual(2, len(payout.stateChangeLog))
        payout.change_state(PayoutState.NEW)
        self.assertEqual("NEW", payout.state.name)
        self.assertEqual(3, len(payout.stateChangeLog))

    @staticmethod
    def __dict_value() -> Dict[str, any]:
        return {
            "_id": "123",
            "userId": "456",
            "profileId": "789",
            "paymentIds": [
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "9",
            ],
            "baseMoney": {
                "amount": 1000,
                "currency": "GBP"
            },
            "state": "NEW",
            "stateChangeLog": [
                {
                    "state": "NEW",
                    "date": "2022-03-10 07:00:00.550604",
                }
            ],
        }

    @staticmethod
    def __payment_dict() -> Dict[str, any]:
        return {
            "_id": "123",
            "cartId": "300",
            "orderId": "456",
            "baseMoney": {
                "amount": 1000,
                "currency": "GBP"
            },
            "netMoney": {
                "amount": 50,
                "currency": "GBP"
            },
            "fees": [
                {
                    "name": "Stripe card processing",
                    "money": {
                        "amount": 500,
                        "currency": "GBP"
                    }
                },
                {
                    "name": "Sphere platform",
                    "money": {
                        "amount": 400,
                        "currency": "GBP"
                    }
                },
                {
                    "name": "Wise payout",
                    "money": {
                        "amount": 50,
                        "currency": "GBP"
                    }
                },
            ],
            "externalReferenceId": "sp_123123123",
            "externalReference": "STRIPE_CHARGE_ID",
            "createdDate": "2022-03-10 07:00:00.550604",
        }
