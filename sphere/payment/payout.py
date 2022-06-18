from typing import List, Set

from bson import ObjectId
from pydantic import Field, BaseModel
from sphere.finance.money import Money

from sphere.payment.payout_state import PayoutState
from sphere.payment.payout_state_log import PayoutStateLog


class Payout(BaseModel):
    id: str = Field(alias="_id")
    userId: str
    profileId: str
    paymentIds: Set[str]
    amount: Money
    state: PayoutState = PayoutState.NEW
    stateChangeLog: List[PayoutStateLog] = [PayoutStateLog()]

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
                "amount": {
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
