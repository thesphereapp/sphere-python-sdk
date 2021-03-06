import unittest
from decimal import Decimal
from typing import List, Union

from sphere.cart.cart_money import CartMoney

from sphere.finance.currency import Currency

from sphere.finance.money import Money

from sphere.item.order_quantity_unit import OrderQuantityUnit

from sphere.cart.cart_metadata import CartMetadata

from sphere.cart.cart import Cart

from sphere.item.order_line_item import OrderLineItem


class CartTest(unittest.TestCase):
    def test_remove_element_from_single_element_cart(self):
        # given
        old_item = self.__aItem("62ae180ffbcf07a17980643e", Decimal(5), Decimal(100), Decimal(500), Decimal(600))
        changed_item = self.__aItem("62ae180ffbcf07a17980643e", Decimal(0), Decimal(100), Decimal(500), Decimal(600))
        # when
        cart = self.__aCart([old_item])
        cart.modify_item(changed_item)
        # then
        self.assertEqual(0, len(cart.items))
        self.assertEqual(None, cart.money)

    def test_remove_element_from_multi_element_cart(self):
        # given
        random_item = self.__aItem("62ae18319bb4b7940a2f05eb", Decimal(5), Decimal(100), Decimal(500), Decimal(600))
        old_item = self.__aItem("62ae180ffbcf07a17980643e", Decimal(5), Decimal(100), Decimal(500), Decimal(600))
        changed_item = self.__aItem("62ae180ffbcf07a17980643e", Decimal(0), Decimal(100), Decimal(500), Decimal(600))
        expected_money = self.__aCartMoney(Decimal(500), None, None, Decimal(600))
        # when
        cart = self.__aCart([random_item, old_item])
        cart.modify_item(changed_item)
        # then
        self.assertEqual(1, len(cart.items))
        self.assertEqual(expected_money, cart.money)

    def test_modify_existing_element(self):
        # given
        random_item = self.__aItem("62ae18319bb4b7940a2f05eb", Decimal(5), Decimal(100), Decimal(500), Decimal(600))
        old_item = self.__aItem("62ae180ffbcf07a17980643e", Decimal(5), Decimal(100), Decimal(500), Decimal(500))
        changed_item = self.__aItem("62ae180ffbcf07a17980643e", Decimal(6), Decimal(100), Decimal(600), Decimal(625))
        expected_money = self.__aCartMoney(Decimal(1100), None, None, Decimal(1200))
        # when
        cart = self.__aCart([random_item, old_item])
        cart.modify_item(changed_item)
        # then
        self.assertEqual(2, len(cart.items))
        self.assertEqual(expected_money, cart.money)

    def test_adding_a_new_element(self):
        # given
        old_item = self.__aItem("62ae18319bb4b7940a2f05eb", Decimal(5), Decimal(100), Decimal(500), Decimal(500))
        new_item = self.__aItem("62ae180ffbcf07a17980643e", Decimal(1), Decimal(100), Decimal(500), Decimal(525))
        expected_money = self.__aCartMoney(Decimal(1000), None, None, Decimal(1025))
        # when
        cart = self.__aCart([old_item])
        cart.modify_item(new_item)
        # then
        self.assertEqual(2, len(cart.items))
        self.assertEqual(expected_money, cart.money)

    def test_remove_element_that_does_not_exist(self):
        # given
        old_item = self.__aItem("62ae180ffbcf07a17980643e", Decimal(5), Decimal(100), Decimal(500), Decimal(600))
        remove_item = self.__aItem("62ae18319bb4b7940a2f05eb", Decimal(0), Decimal(100), Decimal(500), Decimal(600))
        expected_money = self.__aCartMoney(Decimal(500), None, None, Decimal(600))
        # when
        cart = self.__aCart([old_item])
        cart.money = CartMoney(totalGrossSalesMoney=old_item.grossSalesMoney,
                               totalMoney=old_item.totalMoney)
        cart.remove_item(remove_item)
        # then
        self.assertEqual(1, len(cart.items))
        self.assertEqual(expected_money, cart.money)

    def test_emting_a_cart(self):
        # given
        old_item = self.__aItem("62ae180ffbcf07a17980643e", Decimal(5), Decimal(100), Decimal(500), Decimal(600))
        remove_item = self.__aItem("62ae180ffbcf07a17980643e", Decimal(0), Decimal(100), Decimal(500), Decimal(600))
        # when
        cart = self.__aCart([old_item])
        cart.money = None
        cart.remove_item(remove_item)
        # then
        self.assertEqual(0, len(cart.items))
        self.assertEqual(None, cart.money)

    def test_remove_existing_element(self):
        # given
        old_item = self.__aItem("62ae180ffbcf07a17980643e", Decimal(5), Decimal(100), Decimal(500), Decimal(600))
        remove_item = self.__aItem("62ae180ffbcf07a17980643e", Decimal(4), Decimal(100), Decimal(400), Decimal(500))
        # when
        cart = self.__aCart([old_item])
        cart.remove_item(remove_item)
        # then
        self.assertEqual(0, len(cart.items))
        self.assertEqual(None, cart.money)

    @staticmethod
    def __aCart(items: List[OrderLineItem]) -> Cart:
        return Cart(id="62ae0ea285976d54f1e3ffa6",
                    locationId="62ae135fd90f92ef119d5c82",
                    tableNr=1,
                    items=items,
                    metaData=CartMetadata())

    @staticmethod
    def __aItem(item_id: str, quantity: Decimal, base: Decimal, gross: Decimal, total: Decimal) -> OrderLineItem:
        return OrderLineItem(id=item_id,
                             name="item",
                             quantityUnit=OrderQuantityUnit(quantity=quantity),
                             catalogId="100",
                             basePriceMoney=Money(amount=base, currency=Currency.GBP),
                             grossSalesMoney=Money(amount=gross, currency=Currency.GBP),
                             totalMoney=Money(amount=total, currency=Currency.GBP))

    @staticmethod
    def __aCartMoney(gross: Decimal, tax: Union[Decimal, None], discount: Union[Decimal, None],
                     total: Decimal) -> CartMoney:
        money = CartMoney(totalGrossSalesMoney=Money(amount=gross, currency=Currency.GBP),
                          totalMoney=Money(amount=total, currency=Currency.GBP))
        if tax is not None:
            money.totalTaxMoney = Money(amount=tax, currency=Currency.GBP)
        if discount is not None:
            money.totalDiscountMoney = Money(amount=discount, currency=Currency.GBP)
        return money
