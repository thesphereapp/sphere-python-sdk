from typing import Optional, List

import bson
import pydantic
from bson import ObjectId
from pydantic import Field, BaseModel


class Catalog(BaseModel):
    id: str = Field(alias="_id")
    name: str = Field(title='Name', description='name of the catalog')
    userId: str = Field(title='UserId', description='The userId of the merchant who owns it', )
    presentAtAllLocations: bool = Field(True, title="Present at all locations",
                                        description='Boolean flag that indicates if this catalog is present at all '
                                                    'merchant locations')
    allowedLocations: Optional[List[str]] = Field(None, title='Allowed locations',
                                                  description='Ids of locations where this catalog is allowed')

    @pydantic.validator("id")
    @classmethod
    def id_is_valid(cls, value):
        if bson.objectid.ObjectId.is_valid(value):
            return value
        raise ValueError("Invalid id format")

    @pydantic.validator("name")
    @classmethod
    def name_is_valid(cls, value):
        if value is None or len(value) == 0:
            raise ValueError("Category name can not be empty")
        value = value.strip()
        if len(value) == 0:
            raise ValueError("Category name can not be empty")
        if len(value) > 512:
            raise ValueError("Category name needs to be smaller than 512 characters")

        return value

    @pydantic.validator("userId")
    @classmethod
    def userid_is_valid(cls, value):
        if bson.objectid.ObjectId.is_valid(value):
            return value
        raise ValueError("Invalid userId format")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "62ae0e9814bf33d7f9d010c3",
                "name": "Ice cream",
                "userId": "62ae0ea285976d54f1e3ffa6",
                "presentAtAllLocations": False,
                "allowedLocations": ["62ae13f741613f993baead1a", "62ae13fe2ef3d4f322d475c6", "62ae1404e694145e58696d50"]
            }
        }

    def allowed_in_location(self, location_id: str) -> bool:
        if self.presentAtAllLocations is True:
            return True
        if self.allowedLocations is None:
            return False
        for _id in self.allowedLocations:
            if _id == location_id:
                return True
        return False
