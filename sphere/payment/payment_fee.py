from typing import List

from pydantic import BaseModel
from sphere.finance.money import Money, money_sum


class Fee(BaseModel):
    name: str
    money: Money

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        schema_extra = {
            "example": {
                "name": "Stripe card processing fee",
                "money": {
                    "amount": 500,
                    "currency": "GBP"
                },
            }
        }


def total_fees(fees: List[Fee]) -> Money:
    fee_currencies = list(set([f.money.currency for f in fees]))
    if len(fee_currencies) != 1:
        raise ValueError("Fees are in multiple currencies")
    return money_sum([f.money for f in fees])[fee_currencies[0]]
