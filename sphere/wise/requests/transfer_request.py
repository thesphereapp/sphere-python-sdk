from uuid import UUID

import pydantic
from pydantic import Field, BaseModel

from sphere.wise.models.source_of_funds import SourceOfFunds
from sphere.wise.models.transfer_purpose import TransferPurpose, TransferPurposeSubTransferPurpose


class TransferRequest(BaseModel):
    source_account: int = Field(alias="sourceAccount")
    target_account: int = Field(alias="targetAccount")
    quote_uuid: str = Field(alias="quoteUuid")
    customer_transaction_id: str = Field(alias="customerTransactionId")
    reference: str = Field(alias="reference")
    transfer_purpose: str = Field(alias="transferPurpose")
    transfer_purpose_sub_transfer_purpose: str = Field(alias="transferPurposeSubTransferPurpose")
    source_of_funds: str = Field(alias="sourceOfFunds")

    @pydantic.validator("quote_uuid")
    @classmethod
    def quote_uuid_is_uuid_is_valid(cls, value):
        uuid_obj = UUID(value, version=4)
        if str(uuid_obj) == value:
            return value
        raise ValueError("Quote uuid is not valid v4 uuid")

    @pydantic.validator("transfer_purpose")
    @classmethod
    def transfer_purpose_is_valid(cls, value):
        for el in TransferPurpose:
            if el.value == value:
                return value
        raise ValueError("Invalid transfer purpose")

    @pydantic.validator("transfer_purpose_sub_transfer_purpose")
    @classmethod
    def transfer_sub_purpose_is_valid(cls, value):
        for el in TransferPurposeSubTransferPurpose:
            if el.value == value:
                return value
        raise ValueError("Invalid transfer purpose")

    @pydantic.validator("source_of_funds")
    @classmethod
    def source_of_funds_is_valid(cls, value):
        for el in SourceOfFunds:
            if el.value == value:
                return value
        raise ValueError("Invalid source of funds")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        schema_extra = {
            "example":
                {
                    "sourceAccount": 900,
                    "targetAccount": 200,
                    "quoteUuid": "e5ca48ea-90a4-4207-9759-34712121384a",
                    "customerTransactionId": "9226ad17-37dd-4659-aaad-fb89d300a408",
                    "reference": "Sphere",
                    "transferPurpose": "verification.transfers.purpose.pay.bills",
                    "transferPurposeSubTransferPurpose": "verification.sub.transfers.purpose.pay.interpretation.service",
                    "sourceOfFunds": "verification.source.of.funds.other"
                }
        }
