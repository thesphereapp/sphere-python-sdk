from decimal import Decimal
from typing import List, Dict

from pydantic import BaseModel, Field
from sphere.item.order_quantity_unit import OrderQuantityUnit

from sphere.finance.currency import Currency


class Money(BaseModel):
    amount: Decimal = Field(Decimal(0), title='Amount', description='finance amount in cents')
    currency: Currency = Field(Currency.EUR, title='Currency', description='the currency the amount maps to')

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        schema_extra = {
            "example": {
                "amount": 500,
                "currency": "GBP"
            }
        }


def money_sum(moneys: List[Money], precision=3) -> Dict[Currency, Money]:
    moneys_not_null = [m for m in moneys if m is not None]
    if len(moneys_not_null) == 0:
        return {}
    if len(moneys_not_null) == 1:
        return {moneys_not_null[0].currency: moneys_not_null[0]}
    currency_sum = {}
    for m in moneys_not_null:
        if (m is not None) and (not m.amount.is_zero()):
            current_amount = currency_sum.get(m.currency, Decimal(0.0))
            current_amount = current_amount.__add__(m.amount)
            currency_sum[m.currency] = current_amount

    if precision == 0:
        return {currency: Money(currency=currency, amount=amount) for currency, amount in currency_sum.items()}
    currency_money = {}
    for currency, amount in currency_sum.items():
        amount = round(amount, precision)
        amount = Decimal(amount)
        currency_money[currency] = Money(currency=currency, amount=amount)
    return currency_money


def money_multiply(quantity_unit: OrderQuantityUnit, money: Money) -> Money:
    if money is None:
        raise ValueError("None value can not be multiplied")
    quantity = quantity_unit.quantity
    amount = quantity.__mul__(money.amount)
    amount = Decimal(round(amount, quantity_unit.precision))
    return Money(amount=amount, currency=money.currency)


def money_divide(money: Money, quantity_unit: OrderQuantityUnit) -> Money:
    if quantity_unit.quantity.is_zero():
        raise ValueError("Can not divide with zero")
    if money is None:
        raise ValueError("None value can not be divided")
    amount = money.amount / quantity_unit.quantity
    amount = Decimal(round(amount, quantity_unit.precision))
    return Money(amount=amount, currency=money.currency)
