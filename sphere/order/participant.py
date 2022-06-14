from typing import Optional
from pydantic import BaseModel


class Participant(BaseModel):
    name: Optional[str] = None
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
