import decimal
from decimal import Decimal
from unittest import TestCase

from sphere.finance.currency import Currency

from sphere.item.order_quantity_unit import OrderQuantityUnit

from sphere.finance.money import money_sum, Money, money_multiply, money_divide, money_subtract


class MoneyTest(TestCase):
    def test_empty_money_list_is_empty_dict(self):
        # given
        moneys = []
        # when
        result = money_sum(moneys)
        # then
        self.assertEqual({}, result)

    def test_sum_works_with_one_currency(self):
        # given
        money1 = Money(amount=Decimal(5), currency=Currency.EUR)
        money2 = Money(amount=Decimal(4), currency=Currency.EUR)
        money3 = Money(amount=Decimal(1), currency=Currency.EUR)
        moneys = [money1, money2, money3]
        # when
        result = money_sum(moneys, precision=2)
        # then
        self.assertEqual(Decimal(10), result.get(Currency.EUR).amount)

    def test_sum_works_with_none(self):
        # given
        money1 = Money(amount=Decimal(5), currency=Currency.EUR)
        money2 = Money(amount=Decimal(4), currency=Currency.EUR)
        moneys = [money1, None, money2]
        # when
        result = money_sum(moneys, precision=2)
        # then
        self.assertEqual(Decimal(9), result.get(Currency.EUR).amount)

    def test_sum_works_with_precision(self):
        # given
        money1 = Money(amount=Decimal(5), currency=Currency.EUR)
        money2 = Money(amount=Decimal(4), currency=Currency.EUR)
        money3 = Money(amount=Decimal(1.351), currency=Currency.EUR)
        moneys = [money1, money2, money3]
        # when
        result = money_sum(moneys, precision=2)
        # then
        ctx = decimal.getcontext()
        ctx.prec = 2
        self.assertEqual(True, Decimal(10.35) - result.get(Currency.EUR).amount < Decimal(0.01))

    def test_sum_works_with_multiple_currencies(self):
        # given
        money1 = Money(amount=Decimal(5), currency=Currency.EUR)
        money2 = Money(amount=Decimal(4), currency=Currency.EUR)
        money3 = Money(amount=Decimal(1), currency=Currency.EUR)
        money4 = Money(amount=Decimal(3), currency=Currency.USD)
        money5 = Money(amount=Decimal(-2), currency=Currency.USD)
        moneys = [money1, money2, money3, money4, money5]
        # when
        result = money_sum(moneys)
        # then
        self.assertEqual(Decimal(10), result.get(Currency.EUR).amount)
        self.assertEqual(Decimal(1), result.get(Currency.USD).amount)

    def test_money_multiplication_works_with_zero(self):
        # given
        money = Money(amount=Decimal(5), currency=Currency.EUR)
        quantity = OrderQuantityUnit()
        # when
        result = money_multiply(quantity, money)
        # then
        self.assertEqual(Decimal(0), result.amount)
        self.assertEqual(Currency.EUR, result.currency)

    def test_money_multiplication_works_with_non_zero(self):
        # given
        money = Money(amount=Decimal(5), currency=Currency.EUR)
        quantity = OrderQuantityUnit(quantity=Decimal(5))
        # when
        result = money_multiply(quantity, money)
        # then
        self.assertEqual(Decimal(25), result.amount)
        self.assertEqual(Currency.EUR, result.currency)

    def test_money_multiplication_takes_precision_into_account(self):
        # given
        money = Money(amount=Decimal(2.253), currency=Currency.EUR)
        quantity = OrderQuantityUnit(quantity=Decimal(4), precision=1)
        # when
        result = money_multiply(quantity, money)
        # then
        self.assertEqual(Decimal(9), result.amount)
        self.assertEqual(Currency.EUR, result.currency)

    def test_can_not_divide_with_zero(self):
        # given
        money = Money(amount=Decimal(5), currency=Currency.EUR)
        quantity = OrderQuantityUnit()
        # when-then
        self.assertRaises(ValueError, money_divide, money, quantity)

    def test_can_divide_zero(self):
        # given
        money = Money(amount=Decimal(0), currency=Currency.EUR)
        quantity = OrderQuantityUnit(quantity=Decimal(5))
        # when
        result = money_divide(money, quantity)
        # then
        self.assertEqual(Decimal(0), result.amount)
        self.assertEqual(Currency.EUR, result.currency)

    def test_money_division_works_with_non_zero(self):
        # given
        money = Money(amount=Decimal(5), currency=Currency.EUR)
        quantity = OrderQuantityUnit(quantity=Decimal(1.25))
        # when
        result = money_divide(money, quantity)
        # then
        self.assertEqual(True, Decimal(4) - result.amount < Decimal(0.01))
        self.assertEqual(Currency.EUR, result.currency)

    def test_money_division_takes_precision_into_account(self):
        # given
        money = Money(amount=Decimal(4), currency=Currency.EUR)
        quantity = OrderQuantityUnit(quantity=Decimal(2.253), precision=2)
        # when
        result = money_divide(money, quantity)
        # then
        self.assertEqual(True, Decimal(1.78) - result.amount < Decimal(0.01))
        self.assertEqual(Currency.EUR, result.currency)

    def test_subtraction_with_same_currency(self):
        # given
        money1 = Money(amount=Decimal(4.25), currency=Currency.EUR)
        money2 = Money(amount=Decimal(0.34), currency=Currency.EUR)
        # when
        result = money_subtract(money1, money2)
        # then
        self.assertEqual(True, Decimal(3.91) - result.amount < Decimal(0.01))
        self.assertEqual(Currency.EUR, result.currency)

    def test_subtraction_with_different_currency(self):
        money1 = Money(amount=Decimal(1), currency=Currency.GBP)
        money2 = Money(amount=Decimal(0.5), currency=Currency.EUR)
        error_was_raised = False
        error_message = ""
        try:
            money_subtract(money1, money2)
        except ValueError as e:
            error_was_raised = True
            error_message = e.args[0]

        self.assertTrue(error_was_raised)
        self.assertEqual("Subtraction only allowed for moneys in the same currency. GBP vs EUR", error_message)
