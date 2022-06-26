from typing import Optional
from uuid import UUID

import pydantic
from pydantic import BaseModel, Field

from datetime import datetime

from sphere.wise.models.quote import Quote


class Details(BaseModel):
    reference: str = Field(alias="reference")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        schema_extra = {
            "example": {
                "reference": "to my friend"
            }
        }


class Transfer(BaseModel):
    id: int = Field(alias="id")
    user: int = Field(alias="user")
    target_account: int = Field(alias="targetAccount")
    source_account: Optional[int] = Field(alias="sourceAccount")
    quote: Optional[Quote] = Field(alias="quote")
    quote_uuid: str = Field(alias="quoteUuid")
    status: str = Field(alias="status")
    reference: str = Field(alias="reference")
    rate: float = Field(alias="rate")
    created: datetime = Field(alias="created")
    business: int = Field(alias="business")
    transfer_request: None = Field(alias="transferRequest")
    details: Details = Field(alias="details")
    has_active_issues: bool = Field(alias="hasActiveIssues")
    source_currency: str = Field(alias="sourceCurrency")
    source_value: float = Field(alias="sourceValue")
    target_currency: str = Field(alias="targetCurrency")
    target_value: int = Field(alias="targetValue")
    customer_transaction_id: str = Field(alias="customerTransactionId")

    @pydantic.validator("quote_uuid")
    @classmethod
    def quote_uuid_is_uuid_is_valid(cls, value):
        uuid_obj = UUID(value, version=4)
        if str(uuid_obj) == value:
            return value
        raise ValueError("Quote uuid is not valid v4 uuid")

    @pydantic.validator("customer_transaction_id")
    @classmethod
    def customer_transaction_id_is_valid(cls, value):
        uuid_obj = UUID(value, version=4)
        if str(uuid_obj) == value:
            return value
        raise ValueError("Customer transaction id is not valid uuid")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        schema_extra = {
            "example": {
                "id": 468956,
                "user": 123,
                "targetAccount": 333,
                "sourceAccount": None,
                "quote": None,
                "quoteUuid": "bd244a95-dcf8-4c31-aac8-bf5e2f3e54c0",
                "status": "incoming_payment_waiting",
                "reference": "to my friend",
                "rate": 0.9065,
                "created": "2018-08-28 07:43:55",
                "business": 999,
                "transferRequest": None,
                "details": {
                    "reference": "to my friend"
                },
                "hasActiveIssues": False,
                "sourceCurrency": "EUR",
                "sourceValue": 661.89,
                "targetCurrency": "GBP",
                "targetValue": 600,
                "customerTransactionId": "bd244a95-dcf8-4c31-aac8-bf5e2f3e54c0"
            }
        }
