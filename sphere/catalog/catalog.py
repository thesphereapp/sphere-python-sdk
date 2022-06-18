from typing import Optional, List

from bson import ObjectId
from pydantic import Field, BaseModel


class Catalog(BaseModel):
    id: str = Field(str(ObjectId()), alias="_id")
    # TODO: use name field validator
    # name: str = Field( lt=512,title='Name',description='name of the catalog')
    name: str = Field(title='Name', description='name of the catalog')
    userId: str = Field(title='UserId', description='The userId of the merchant who owns it', )
    presentAtAllLocations: bool = Field(True, title="Present at all locations",
                                        description='Boolean flag that indicates if this catalog is present at all '
                                                    'merchant locations')
    allowedLocations: Optional[List[str]] = Field(None, title='Allowed locations',
                                                  description='Ids of locations where this catalog is allowed')

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "123",
                "name": "Ice cream",
                "userId": "456",
                "presentAtAllLocations": False,
                "allowedLocations": ["789", "101112", "456789"]
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
