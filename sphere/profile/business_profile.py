from typing import Optional, List

from bson import ObjectId
from pydantic import Field, BaseModel

from sphere.profile.profile_state import ProfileState
from sphere.profile.profile_state_log import ProfileStateLog


class BusinessProfile(BaseModel):
    id: str = Field(alias="_id")
    userId: str
    webpage: str
    avatar: str
    wiseRecipientId: Optional[int] = None
    state: ProfileState = ProfileState.ACTIVE
    stateChangeLog: List[ProfileStateLog] = [ProfileStateLog()]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "123",
                "userId": "456",
                "webpage": "https://example.com",
                "avatar": "https://example.com/logo.png",
                "wiseRecipientId": 900,
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