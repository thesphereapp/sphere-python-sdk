import unittest
from typing import Dict

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
        self.assertEqual(7, len(payout.paymentIds))
        payment.id = "62ae15a076b93f1e308f4a2f"
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
            "_id": "62ae157fb0bddbccd414e896",
            "userId": "62ae15853fb296d960e908e9",
            "profileId": "62ae158ba68815182544ea56",
            "paymentIds": [
                "62ae15903dc86aab32abbc2f",
                "62ae15953a2a4982c7bfa1e6",
                "62ae159af995d8864d91a644",
                "62ae15a076b93f1e308f4a2f",
                "62ae15a56fe7dd1a2f56b3b8",
                "62ae15abbbfeb5ed9eed9078",
                "62ae15b0696255a29f4fca99",
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
            "_id": "62ae15beb1d0b7c8631de115",
            "cartId": "62ae15c4ec4e07d7d19067f1",
            "orderId": "62ae15c93c0e1bdf7066fe66",
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
