from bson import ObjectId
from pydantic import BaseModel


class RandomForm(BaseModel):
    email: str
    password: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "email": "example@gmail.com",
                "password": "hello world",
            }
        }
