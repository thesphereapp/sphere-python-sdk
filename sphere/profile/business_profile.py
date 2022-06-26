from typing import List
import validators
import bson
import pydantic
from bson import ObjectId
from pydantic import Field, BaseModel

from sphere.profile.business_profile_payout_details import BusinessProfilePayoutDetails
from sphere.profile.profile_state import ProfileState
from sphere.profile.profile_state_log import ProfileStateLog


class BusinessProfile(BaseModel):
    id: str = Field(alias="_id")
    userId: str
    webpage: str
    avatar: str
    payout_details: BusinessProfilePayoutDetails = Field(alias="payoutDetails")

    state: ProfileState = ProfileState.ACTIVE
    stateChangeLog: List[ProfileStateLog] = [ProfileStateLog()]

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

    @pydantic.validator("webpage")
    @classmethod
    def webpage_is_valid(cls, value):
        if validators.url(value):
            return value
        raise ValueError("Invalid webpage url")

    @pydantic.validator("avatar")
    @classmethod
    def avatar_is_valid(cls, value):
        if validators.url(value):
            return value
        raise ValueError("Invalid avatar url")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "62ae3f2cd77070ad862b62f9",
                "userId": "62ae2adee2e3a21a46d70468",
                "webpage": "https://example.com",
                "avatar": "https://example.com/logo.png",
                "payoutDetails": {
                    "accountDetails": {
                        "legalType": "PRIVATE",
                        "sortCode": "40-30-20",
                        "accountNumber": "12345678"
                    },
                    "currency": "EUR",
                    "wiseRecipientId": 5,
                },
                "state": "ACTIVE",
                "stateChangeLog": [
                    {
                        "state": "ACTIVE",
                        "date": "2022-03-10 07:00:00"
                    }
                ],
            }
        }

    def change_state(self, new_state: ProfileState):
        if self.state == new_state:
            return None
        self.state = new_state
        log = ProfileStateLog(state=new_state)
        self.stateChangeLog.append(log)
