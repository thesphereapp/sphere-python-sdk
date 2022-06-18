from decimal import Decimal
from typing import List, Set

from bson import ObjectId
from pydantic import Field, BaseModel

from sphere.finance.money import Money, money_sum, money_subtract
from sphere.payment.payment_fee import Fee, total_fees
from sphere.payment.payout import Payout

from sphere.payment.payout_state import PayoutState
from sphere.payment.payout_state_log import PayoutStateLog


class SphereFeePayout(BaseModel):
    id: str = Field(alias="_id")
    payoutIds: Set[str]
    baseMoney: Money
    netMoney: Money
    fees: List[Fee]
    state: PayoutState = PayoutState.NEW
    stateChangeLog: List[PayoutStateLog] = [PayoutStateLog()]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "123",
                "payoutIds": [
                    "1",
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "9",
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
        }

    def change_state(self, new_state: PayoutState):
        if self.state == new_state:
            return None
        self.state = new_state
        log = PayoutStateLog(state=new_state)
        self.stateChangeLog.append(log)

    def add_payout(self, payout: Payout, sphere_fees: List[Fee]):
        for payout_id in self.payoutIds:
            if payout_id == payout.id:
                return None
        for fee in sphere_fees:
            if fee.money.currency != self.baseMoney.currency:
                raise ValueError(
                    "Sphere payout and fee have different currencies. " + fee.money.currency.value + " vs " + self.baseMoney.currency.value)
        if payout.baseMoney.currency != self.baseMoney.currency:
            raise ValueError(
                "Sphere payout and regular payout have different currencies. " + payout.baseMoney.currency.value + " vs " + self.baseMoney.currency.value)
        self.payoutIds.add(payout.id)
        fee_sum = total_fees(sphere_fees)
        self.baseMoney = money_sum([self.baseMoney, fee_sum])[self.baseMoney.currency]
        self.netMoney = money_sum([self.netMoney, fee_sum])[self.netMoney.currency]

    def calculate_net_money(self, payout_fees: List[Fee]):
        self.fees = payout_fees
        fee_sum = total_fees(payout_fees)
        self.netMoney = money_subtract(self.baseMoney, fee_sum)


def initial_payout(payout_fees: List[Fee]) -> SphereFeePayout:
    currency = payout_fees[0].money.currency
    base_money = Money(amount=Decimal(0), currency=currency)
    fee_sum = total_fees(payout_fees)
    net_money = money_subtract(base_money, fee_sum)
    payload = {
        "_id": str(ObjectId()),
        "payoutIds": [],
        "baseMoney": base_money,
        "netMoney": net_money,
        "fees":payout_fees,
    }
    return SphereFeePayout(**payload)
