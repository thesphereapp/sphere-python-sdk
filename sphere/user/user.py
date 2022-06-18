from typing import List

import bson
import pydantic
from bson import ObjectId
from pydantic import Field, BaseModel

from sphere.user.user_state import UserState
from sphere.user.user_state_log import UserStateLog


class User(BaseModel):
    id: str = Field(alias="_id")
    # TODO: add validator
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

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "62ae2adee2e3a21a46d70468",
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
