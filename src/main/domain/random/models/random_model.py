from datetime import datetime, timezone
from typing import Optional

from bson import ObjectId
from pydantic import Field, BaseModel


class RandomModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    name: str
    createdDateUtc: Optional[datetime] = datetime.now(timezone.utc)
    isFixed: bool = False

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "123",
                "name": "random",
                "createdDateUtc": "2022-03-10 07:00:00.550604",
                "isFixed": False
            }
        }
