from typing import List

import bson
import pydantic
from bson import ObjectId
from pydantic import Field, BaseModel

from sphere.location.location_state import LocationState
from sphere.location.location_state_log import LocationStateLog


class Location(BaseModel):
    id: str = Field(alias="_id")
    userId: str
    profileId: str
    name: str = Field(title='Name', description='name of the location')
    state: LocationState = LocationState.ACTIVE
    stateChangeLog: List[LocationStateLog] = [LocationStateLog()]

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
    def profile_id_is_valid(cls, value):
        if bson.objectid.ObjectId.is_valid(value):
            return value
        raise ValueError("Invalid profileId format")

    @pydantic.validator("name")
    @classmethod
    def name_is_valid(cls, value):
        if value is None or len(value) == 0:
            raise ValueError("Location name can not be empty")
        value = value.strip()
        if len(value) == 0:
            raise ValueError("Location name can not be empty")
        if len(value) > 512:
            raise ValueError("Location name needs to be smaller than 512 characters")

        return value

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "62ae4576d77070ad862b62fa",
                "userId": "62ae2adee2e3a21a46d70468",
                "profileId": "62ae3f2cd77070ad862b62f9",
                "name": "Strand street cafe",
                "state": "ACTIVE",
                "stateChangeLog": [
                    {
                        "state": "ACTIVE",
                        "date": "2022-03-10 07:00:00.550604",
                    }
                ]
            }
        }

    def is_active(self) -> bool:
        return self.state == LocationState.ACTIVE

    def change_state(self, new_state: LocationState):
        if self.state == new_state:
            return None
        self.state = new_state
        log = LocationStateLog(state=new_state)
        self.stateChangeLog.append(log)
