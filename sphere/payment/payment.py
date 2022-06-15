from datetime import datetime, timezone
from typing import Optional

from bson import ObjectId
from pydantic import Field, BaseModel
from sphere.finance.money import Money
from sphere.payment.external_reference import ExternalReference
from sphere.payment.payment_fee import PaymentFee


class Payment(BaseModel):
    id: Optional[str] = Field(alias="_id")
    cartId: str
    baseMoney: Money
    netoMoney: Money
    fee: PaymentFee
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
                "cartId": "456",
                "orderId": "456",
                "baseMoney": {
                    "amount": 850,
                    "currency": "GBP"
                },
                "netoMoney": {
                    "amount": 705,
                    "currency": "GBP"
                },
                "fee": {
                    "paymentProcessioningFee": {
                        "name": "Stripe payment processing fee",
                        "money": {
                            "amount": 32,
                            "currency": "GBP"
                        }
                    },
                    "sphereFee": {
                        "name": "Sphere platform fee",
                        "money": {
                            "amount": 85,
                            "currency": "GBP"
                        }
                    },
                    "payoutProcessingFee": {
                        "name": "Wise payout fee",
                        "money": {
                            "amount": 28,
                            "currency": "GBP"
                        }
                    },
                },
                "externalReferenceId": "sp_123123123",
                "externalReference": "STRIPE_CHARGE_ID",
                "createdDate": "2022-03-10 07:00:00.550604",
            }
        }
