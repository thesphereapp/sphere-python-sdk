from typing import Optional
from pydantic import BaseModel
from finance.money import Money
from item.order_line_item import OrderLineItem


class CartMoney(BaseModel):
    totalGrossSalesMoney: Money
    totalTaxMoney: Optional[Money] = None
    totalDiscountMoney: Optional[Money] = None
    totalMoney: Money

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        schema_extra = {
            "example": {
                "totalGrossSalesMoney": {
                    "amount": 500,
                    "currency": "GBP"
                },
                "totalTaxMoney": {
                    "amount": 100,
                    "currency": "GBP"
                },
                "totalDiscountMoney": None,
                "totalMoney": {
                    "amount": 500,
                    "currency": "GBP"
                },
            }
        }


def initial_cart_money(item: OrderLineItem) -> CartMoney:
    return CartMoney(totalGrossSalesMoney=item.grossSalesMoney,
                     totalTaxMoney=item.totalTaxMoney,
                     totalDiscountMoney=item.totalDiscountMoney,
                     totalMoney=item.totalMoney)