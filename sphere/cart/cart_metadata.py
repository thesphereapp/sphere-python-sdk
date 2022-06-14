from bson import ObjectId
from pydantic import BaseModel
from sphere.finance.currency import Currency


class CartMetadata(BaseModel):
    currency: Currency = Currency.GBP

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "currency": "GBP"
            }
        }