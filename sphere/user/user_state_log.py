from datetime import datetime, timezone
from pydantic import BaseModel

from sphere.user.user_state import UserState


class UserStateLog(BaseModel):
    state: UserState = UserState.ACTIVE
    date: datetime = datetime.now(timezone.utc)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        schema_extra = {
            "example": {
                "state": "ACTIVE",
                "date": "2022-03-10 07:00:00.550604",
            }
        }
