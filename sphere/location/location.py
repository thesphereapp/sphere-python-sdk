from typing import Optional, List

from bson import ObjectId
from pydantic import Field, BaseModel

from sphere.location.location_state import LocationState
from sphere.location.location_state_log import LocationStateLog


class Location(BaseModel):
    id: str = Field(alias="_id")
    userId: str
    profileId: str
    name: Optional[str] = None
    state: LocationState = LocationState.ACTIVE
    stateChangeLog: List[LocationStateLog] = [LocationStateLog()]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "123",
                "userId": "456",
                "profileId": "999",
                "name": "My location",
                "state": "ACTIVE",
                "createdDate": "2022-03-10 07:00:00.550604"
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
