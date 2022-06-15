from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import Field, BaseModel
from sphere.finance.money import Money
from sphere.payment.external_reference import ExternalReference


class Fee(BaseModel):
    name: str
    money: Money

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        schema_extra = {
            "example": {
                "name": "Stripe payment processing fee",
                "money": {
                    "amount": 500,
                    "currency": "GBP"
                },
            }
        }


class PaymentFee(BaseModel):
    paymentProcessioningFee: Fee
    sphereFee: Fee
    payoutProcessingFee: Fee

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
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
                }
            }
        }
