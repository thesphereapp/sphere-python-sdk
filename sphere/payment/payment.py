from datetime import datetime, timezone
from typing import Optional, List

from bson import ObjectId
from pydantic import Field, BaseModel
from sphere.finance.money import Money
from sphere.payment.external_reference import ExternalReference
from sphere.payment.payment_fee import Fee


class Payment(BaseModel):
    id: Optional[str] = Field(alias="_id")
    cartId: str
    baseMoney: Money
    netMoney: Money
    fees: List[Fee] = []
    externalReferenceId: str
    externalReference: ExternalReference
    createdDate: datetime = datetime.now(timezone.utc)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "123",
                "cartId": "300",
                "orderId": "456",
                "baseMoney": {
                    "amount": 850,
                    "currency": "GBP"
                },
                "netMoney": {
                    "amount": 701,
                    "currency": "GBP"
                },
                "fees": [
                    {
                        "name": "Stripe card processing",
                        "money": {
                            "amount": 32,
                            "currency": "GBP"
                        }
                    },
                    {
                        "name": "Sphere platform",
                        "money": {
                            "amount": 85,
                            "currency": "GBP"
                        }
                    }
                ],
                "externalReferenceId": "sp_123123123",
                "externalReference": "STRIPE_CHARGE_ID",
                "createdDate": "2022-03-10 07:00:00.550604",
            }
        }
