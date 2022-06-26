from typing import List

import bson
import pydantic
import validators
from bson import ObjectId
from pydantic import Field, BaseModel

from sphere.user.user_state import UserState
from sphere.user.user_state_log import UserStateLog


class User(BaseModel):
    id: str = Field(alias="_id")
    name: str
    email: str
    # TODO: add validator
    password: str
    state: UserState = UserState.ACTIVE
    stateChangeLog: List[UserStateLog] = [UserStateLog()]

    @pydantic.validator("id")
    @classmethod
    def id_is_valid(cls, value):
        if bson.objectid.ObjectId.is_valid(value):
            return value
        raise ValueError("Invalid id format")

    @pydantic.validator("email")
    @classmethod
    def email_is_valid(cls, value):
        if validators.email(value):
            return value
        raise ValueError("Invalid email")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "62ae2adee2e3a21a46d70468",
                "name": "Little Bakehouse Llc",
                "email": "example@gmail.com",
                "password": "xxx",
                "state": "ACTIVE",
                "stateChangeLog": [
                    {
                        "state": "ACTIVE",
                        "date": "2022-03-10 07:00:00"
                    }
                ],
            }
        }

    def change_state(self, new_state: UserState):
        if self.state == new_state:
            return None
        self.state = new_state
        log = UserStateLog(state=new_state)
        self.stateChangeLog.append(log)
