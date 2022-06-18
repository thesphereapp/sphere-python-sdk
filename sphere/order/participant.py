from typing import Optional
from pydantic import BaseModel


class Participant(BaseModel):
    # TODO: both values can not be null
    name: Optional[str] = None
    # TODO: add regex check
    email: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        schema_extra = {
            "example": {
                "name": "James Clark",
                "email": "james.clark@example.com",
            }
        }
