from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import Field, BaseModel
from sphere.finance.money import Money
from sphere.payment.external_reference import ExternalReference


class Payment(BaseModel):
    id: Optional[str] = Field(alias="_id")
    cartId: str
    money: Money
    externalReferenceId: str
    externalReference: ExternalReference
    createdDate: datetime

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "123",
                "cartId": "456",
                "orderId": "456",
                "money": {
                    "amount": 500,
                    "currency": "GBP"
                },
                "externalReferenceId": "sp_123123123",
                "externalReference": "STRIPE",
                "createdDate": "2022-03-10 07:00:00.550604",
            }
        }
