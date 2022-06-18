import unittest
from decimal import Decimal
from typing import Dict

from sphere.finance.currency import Currency

from sphere.payment.payment_fee import Fee
from sphere.payment.payout import Payout
from sphere.payment.payout_state import PayoutState
from sphere.payment.sphere_fee_payout import SphereFeePayout, initial_payout


class SphereFeePayoutTest(unittest.TestCase):

    def test_building_from_dict(self):
        # given
        my_dict = self.__sphere_payout()
        # when
        resp = SphereFeePayout(**my_dict)
        # then
        self.assertEqual(len(resp.payoutIds), 2)

    def test_state_change(self):
        my_dict = self.__sphere_payout()
        payout = SphereFeePayout(**my_dict)
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

    def test_adding_payouts_happy_flow(self):
        # given
        payout1, payout2, payout3 = [Payout(**self.__payout("62ae1669e573eace4cfebbfc")),
                                     Payout(**self.__payout("62ae168076004d5a60f537a1")),
                                     Payout(**self.__payout("62ae16855e23a27749c1d2ba"))]
        payout1_sphere_fees = [Fee(**self.__sphere_fee(100)),
                               Fee(**self.__sphere_fee(100)),
                               Fee(**self.__sphere_fee(100))]
        payout2_sphere_fees = [Fee(**self.__sphere_fee(200)),
                               Fee(**self.__sphere_fee(200)),
                               Fee(**self.__sphere_fee(200))]
        payout3_sphere_fees = [Fee(**self.__sphere_fee(300)),
                               Fee(**self.__sphere_fee(300)),
                               Fee(**self.__sphere_fee(300))]
        payout_fees = [Fee(**self.__sphere_fee(32))]
        # when
        sphere_payout = initial_payout(payout_fees)
        # then
        self.assertEqual(Decimal(-32), sphere_payout.netMoney.amount)
        self.assertEqual(Decimal(0), sphere_payout.baseMoney.amount)
        # when
        sphere_payout.add_payout(payout1, payout1_sphere_fees)
        # then
        self.assertEqual(Decimal(268), sphere_payout.netMoney.amount)
        self.assertEqual(300, sphere_payout.baseMoney.amount)
        self.assertEqual("GBP", sphere_payout.baseMoney.currency.value)
        # when
        sphere_payout.add_payout(payout2, payout2_sphere_fees)
        # then
        self.assertEqual(Decimal(868), sphere_payout.netMoney.amount)
        self.assertEqual(900, sphere_payout.baseMoney.amount)
        self.assertEqual("GBP", sphere_payout.baseMoney.currency.value)
        # when
        sphere_payout.add_payout(payout3, payout3_sphere_fees)
        # then
        self.assertEqual(Decimal(1768), sphere_payout.netMoney.amount)
        self.assertEqual(1800, sphere_payout.baseMoney.amount)
        self.assertEqual("GBP", sphere_payout.baseMoney.currency.value)

    def test_adding_payment_already_processed_payouts(self):
        # given
        payout1 = Payout(**self.__payout("62ae1702a223c826eeb4a317"))

        payout1_sphere_fees = [Fee(**self.__sphere_fee(100)),
                               Fee(**self.__sphere_fee(100)),
                               Fee(**self.__sphere_fee(100))]
        payout_fees = [Fee(**self.__sphere_fee(32))]
        # when
        sphere_payout = initial_payout(payout_fees)
        # then
        self.assertEqual(Decimal(-32), sphere_payout.netMoney.amount)
        self.assertEqual(Decimal(0), sphere_payout.baseMoney.amount)
        # when
        sphere_payout.add_payout(payout1, payout1_sphere_fees)
        # then
        self.assertEqual(Decimal(268), sphere_payout.netMoney.amount)
        self.assertEqual(300, sphere_payout.baseMoney.amount)
        self.assertEqual("GBP", sphere_payout.baseMoney.currency.value)
        # when
        sphere_payout.add_payout(payout1, payout1_sphere_fees)
        # then
        self.assertEqual(Decimal(268), sphere_payout.netMoney.amount)
        self.assertEqual(300, sphere_payout.baseMoney.amount)
        self.assertEqual("GBP", sphere_payout.baseMoney.currency.value)

    def test_adding_fees_with_different_currency(self):
        # given
        payout1 = Payout(**self.__payout("62ae1691f9edcbfff356bdff"))
        payout1_sphere_fees = [Fee(**self.__sphere_fee(100))]
        payout1_sphere_fees[0].money.currency = Currency.EUR

        payout_fees = [Fee(**self.__sphere_fee(32))]
        # when
        sphere_payout = initial_payout(payout_fees)
        # then
        self.assertEqual(Decimal(-32), sphere_payout.netMoney.amount)
        self.assertEqual(Decimal(0), sphere_payout.baseMoney.amount)

        error_was_raised = False
        error_message = ""
        try:
            sphere_payout.add_payout(payout1, payout1_sphere_fees)
        except ValueError as e:
            error_was_raised = True
            error_message = e.args[0]

        self.assertTrue(error_was_raised)
        self.assertEqual("Sphere payout and fee have different currencies. EUR vs GBP", error_message)
        self.assertEqual(Decimal(-32), sphere_payout.netMoney.amount)
        self.assertEqual(Decimal(0), sphere_payout.baseMoney.amount)

    def test_adding_payout_with_different_currency(self):
        # given
        payout1 = Payout(**self.__payout("62ae170a4743b4b45b3bb747"))
        payout1.baseMoney.currency = Currency.EUR
        payout1_sphere_fees = [Fee(**self.__sphere_fee(100))]

        payout_fees = [Fee(**self.__sphere_fee(32))]
        # when
        sphere_payout = initial_payout(payout_fees)
        # then
        self.assertEqual(Decimal(-32), sphere_payout.netMoney.amount)
        self.assertEqual(Decimal(0), sphere_payout.baseMoney.amount)

        error_was_raised = False
        error_message = ""
        try:
            sphere_payout.add_payout(payout1, payout1_sphere_fees)
        except ValueError as e:
            error_was_raised = True
            error_message = e.args[0]

        self.assertTrue(error_was_raised)
        self.assertEqual("Sphere payout and regular payout have different currencies. EUR vs GBP", error_message)
        self.assertEqual(Decimal(-32), sphere_payout.netMoney.amount)
        self.assertEqual(Decimal(0), sphere_payout.baseMoney.amount)

    @staticmethod
    def __payout(payout_id: str) -> Dict[str, any]:
        return {
            "_id": payout_id,
            "userId": "62ae16c032caa6507f68d61f",
            "profileId": "62ae16c539f933b4a95300b7",
            "paymentIds": [
                "62ae16d1c0e9a0515869c83a",
                "62ae16d629f459f2670f4f67",
                "62ae16dab8731383ac7b0c36",
                "62ae16e0bc063aec6aee4fbb",
                "62ae16e587d4add0064f7fa0",
                "62ae16ea05390601fb5a3cdf",
                "62ae16ef4e1173028988678a",
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
    def __sphere_payout() -> Dict[str, any]:
        return {
            "_id": "62ae1669e573eace4cfebbfc",
            "payoutIds": [
                "62ae1639799e0be01ee1482b",
                "62ae16402695cfb9581f1c6a"
            ],
            "baseMoney": {
                "amount": 8000,
                "currency": "GBP"
            },
            "netMoney": {
                "amount": 7968,
                "currency": "GBP"
            },
            "fees": [
                {
                    "name": "Wise payout",
                    "money": {
                        "amount": 32,
                        "currency": "GBP"
                    }
                },
            ],
            "state": "NEW",
            "stateChangeLog": [
                {
                    "state": "NEW",
                    "date": "2022-03-10 07:00:00.550604",
                }
            ],
        }

    @staticmethod
    def __sphere_fee(amount: int) -> Dict[str, any]:
        return {"name": "My fee",
                "money": {
                    "amount": amount,
                    "currency": "GBP"
                }}
