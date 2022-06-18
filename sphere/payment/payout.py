from typing import List, Set

import bson
import pydantic
from bson import ObjectId
from pydantic import Field, BaseModel
from sphere.finance.money import Money, money_sum
from sphere.payment.payment import Payment

from sphere.payment.payout_state import PayoutState
from sphere.payment.payout_state_log import PayoutStateLog


class Payout(BaseModel):
    id: str = Field(alias="_id")
    userId: str
    profileId: str
    paymentIds: Set[str]
    baseMoney: Money
    state: PayoutState = PayoutState.NEW
    stateChangeLog: List[PayoutStateLog] = [PayoutStateLog()]

    @pydantic.validator("id")
    @classmethod
    def id_is_valid(cls, value):
        if bson.objectid.ObjectId.is_valid(value):
            return value
        raise ValueError("Invalid id format")

    @pydantic.validator("userId")
    @classmethod
    def user_id_is_valid(cls, value):
        if bson.objectid.ObjectId.is_valid(value):
            return value
        raise ValueError("Invalid userId format")

    @pydantic.validator("profileId")
    @classmethod
    def profileId_is_valid(cls, value):
        if bson.objectid.ObjectId.is_valid(value):
            return value
        raise ValueError("Invalid profileId format")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
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
                    "amount": 850,
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
        }

    def change_state(self, new_state: PayoutState):
        if self.state == new_state:
            return None
        self.state = new_state
        log = PayoutStateLog(state=new_state)
        self.stateChangeLog.append(log)

    def add_payment(self, payment: Payment):
        for payment_id in self.paymentIds:
            if payment_id == payment.id:
                return None
        if payment.netMoney.currency != self.baseMoney.currency:
            raise ValueError(
                "Payout and payment have different currencies. " + payment.netMoney.currency.value + " vs " + self.baseMoney.currency.value)
        if bson.objectid.ObjectId.is_valid(payment.id) is False:
            raise ValueError("Invalid paymentid format")

        self.paymentIds.add(payment.id)
        self.baseMoney = money_sum([self.baseMoney, payment.netMoney])[payment.netMoney.currency]
