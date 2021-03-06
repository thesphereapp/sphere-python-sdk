from decimal import Decimal
from typing import Optional, List, Dict, Union
import copy

import bson
import pydantic
from bson import ObjectId
from pydantic import Field, BaseModel
from sphere.finance.currency import Currency

from sphere.finance.money import Money, money_multiply, money_sum

from sphere.item.order_line_item_applied_discount import OrderLineItemAppliedDiscount

from sphere.item.order_line_item_applied_tax import OrderLineItemAppliedTax

from sphere.item.order_quantity_unit import OrderQuantityUnit


class OrderLineItem(BaseModel):
    id: str = Field(alias="_id")
    name: str = Field(title='Name', description='name of the product')
    quantityUnit: OrderQuantityUnit
    note: Optional[str] = None
    catalogId: str = Field(title="CatalogId", description="A catalog where the item belongs to")
    metadata: Optional[dict] = None
    appliedTaxes: Optional[List[OrderLineItemAppliedTax]] = None
    appliedDiscounts: Optional[List[OrderLineItemAppliedDiscount]] = None
    basePriceMoney: Money
    grossSalesMoney: Money
    totalTaxMoney: Optional[Money] = None
    totalDiscountMoney: Optional[Money] = None
    totalMoney: Money

    @pydantic.validator("id")
    @classmethod
    def id_is_valid(cls, value):
        if bson.objectid.ObjectId.is_valid(value):
            return value
        raise ValueError("Invalid id format")

    @pydantic.validator("name")
    @classmethod
    def name_is_valid(cls, value):
        if value is None or len(value) == 0:
            raise ValueError("Item name can not be empty")
        value = value.strip()
        if len(value) == 0:
            raise ValueError("Item name can not be empty")
        if len(value) > 512:
            raise ValueError("Item name needs to be smaller than 512 characters")

        return value

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "62ae145d2f7acdc7c21c1406",
                "name": "Ice cream",
                "quantityUnit": {
                    "quantity": "4",
                    "measurementUnit": "AMOUNT",
                    "precision": 0
                },
                "note": None,
                "catalogId": "62ae149488e6ced1ab75fadd",
                "metaData": {
                    "brand": "Ben and Jerry's"
                },
                "appliedTaxes": [
                    {
                        "name": "Value added tax",
                        "finance": {
                            "amount": 80,
                            "currency": "USD"
                        }
                    },
                    {
                        "name": "Sugar tax",
                        "finance": {
                            "amount": 20,
                            "currency": "USD"
                        }
                    }
                ],
                "appliedDiscounts": [
                    {
                        "name": "Frequent buyer",
                        "finance": {
                            "amount": 50,
                            "currency": "USD"
                        }
                    }
                ],
                "basePriceMoney": {
                    "amount": 100,
                    "currency": "GBP"
                },
                "grossSalesMoney": {
                    "amount": 400,
                    "currency": "GBP"
                },
                "totalTaxMoney": {
                    "amount": 100,
                    "currency": "GBP"
                },
                "totalDiscountMoney": {
                    "amount": 50,
                    "currency": "GBP"
                },
                "totalMoney": {
                    "amount": 450,
                    "currency": "GBP"
                }
            }
        }

    def calculate_total_money(self) -> Money:
        currency = self.basePriceMoney.currency
        total = self.grossSalesMoney.amount
        if self.totalTaxMoney is not None:
            total += self.totalTaxMoney.amount
        if self.totalDiscountMoney is not None:
            total -= self.totalDiscountMoney.amount
        return Money(amount=total, currency=currency)

    # TODO: unit test
    def quantity_updated(self, new_quantity: OrderQuantityUnit):
        if new_quantity.quantity.is_zero():
            self.grossSalesMoney = Money(currency=self.basePriceMoney.currency)
            self.totalTaxMoney = None
            self.totalDiscountMoney = None
            self.totalMoney = Money(currency=self.basePriceMoney.currency)
            return None
        multiplier = new_quantity.quantity / self.quantityUnit.quantity
        item_currency = self.basePriceMoney.currency

        self.quantityUnit = new_quantity
        self.grossSalesMoney = Money(amount=money_multiply(new_quantity, self.basePriceMoney).amount,
                                     currency=self.grossSalesMoney.currency)
        self.appliedTaxes = self.__apply_multiplier(multiplier, self.appliedTaxes)
        self.appliedDiscounts = self.__apply_multiplier(multiplier, self.appliedDiscounts)

        tax_money = []
        if self.appliedTaxes is not None:
            tax_money = [t.money for t in self.appliedTaxes]
        self.totalTaxMoney = money_sum(tax_money).get(item_currency)

        discount_money = []
        if self.appliedDiscounts is not None:
            discount_money = [t.money for t in self.appliedDiscounts]
        self.totalDiscountMoney = money_sum(discount_money).get(item_currency)
        self.totalMoney = self.__calculate_total_money(item_currency, copy.deepcopy(self.dict()))

    @staticmethod
    def __apply_multiplier(multiplier: Decimal, elements: Union[
        Optional[List[OrderLineItemAppliedTax]], Optional[List[OrderLineItemAppliedDiscount]]]) -> Union[
        Optional[List[OrderLineItemAppliedTax]], Optional[List[OrderLineItemAppliedDiscount]]]:
        if elements is not None and len(elements) > 0:
            modified_values = []
            multiplier_quantity = OrderQuantityUnit(quantity=multiplier, precision=3)
            for s in elements:
                s.money = money_multiply(multiplier_quantity, s.money)
                modified_values.append(s)
            return modified_values

    @staticmethod
    def __calculate_total_money(currency: Currency, item: Dict[str, any]) -> Money:
        discount_money = item.get("totalDiscountMoney", None)
        if discount_money is not None:
            discount_money = Money(**discount_money)
            discount_money.amount = -discount_money.amount
        tax_money = item.get("totalTaxMoney", None)
        if tax_money is not None:
            tax_money = Money(**tax_money)
        gross_sales_money = item.get("grossSalesMoney", None)
        if gross_sales_money is not None:
            gross_sales_money = Money(**gross_sales_money)
        calculations = [gross_sales_money, tax_money, discount_money]
        return money_sum(calculations).get(currency)
