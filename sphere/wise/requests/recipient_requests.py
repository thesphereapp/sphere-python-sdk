import pydantic
from pydantic import BaseModel, Field
from sphere.finance.currency import Currency
from sphere.wise.models.account_details import EurAccountDetails, GbpAccountDetails, UsdAccountDetails






class EurRecipientRequest(BaseModel):
    profile: int = Field(alias="profile")
    account_holder_name: str = Field(alias="accountHolderName")
    currency: Currency = Field(Currency.EUR, alias="currency")
    type: str = Field(alias="type")
    details: EurAccountDetails = Field(alias="details")

    @pydantic.validator("currency")
    @classmethod
    def currency_is_valid(cls, value):
        if Currency.EUR == value:
            return value
        message = "Invalid currency argument for eur recipient request. {}".format(value)
        raise ValueError(message)

    @pydantic.validator("type")
    @classmethod
    def type_is_valid(cls, value):
        if "iban" == value:
            return value
        raise ValueError("Invalid type argument for eur recipient request")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        schema_extra = {
            "example":
                {
                    "profile": 111,
                    "accountHolderName": "My Bakery Oü",
                    "currency": "EUR",
                    "type": "iban",
                    "details": {
                        "legalType": "PRIVATE",
                        "IBAN": "DE89370400440532013000"
                    }
                }
        }


class GbpRecipientRequest(BaseModel):
    profile: int = Field(alias="profile")
    account_holder_name: str = Field(alias="accountHolderName")
    currency: Currency = Field(Currency.GBP, alias="currency")
    type: str = Field(alias="type")
    details: GbpAccountDetails = Field(alias="details")

    @pydantic.validator("currency")
    @classmethod
    def currency_is_valid(cls, value):
        if Currency.GBP == value:
            return value
        message = "Invalid currency argument for gbp recipient request. {}".format(value)
        raise ValueError(message)

    @pydantic.validator("type")
    @classmethod
    def type_is_valid(cls, value):
        if value in ["sort_code"]:
            return value
        raise ValueError("Invalid type argument for gbp recipient request")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        schema_extra = {
            "example":
                {
                    "profile": 999,
                    "accountHolderName": "Jon's Bakerly Plc",
                    "currency": "GBP",
                    "type": "sort_code",
                    "details": {
                        "legalType": "PRIVATE",
                        "sortCode": "40-30-20",
                        "accountNumber": "12345678"
                    }
                }
        }


class UsdRecipientRequest(BaseModel):
    profile: int = Field(alias="profile")
    account_holder_name: str = Field(alias="accountHolderName")
    currency: Currency = Field(Currency.USD, alias="currency")
    type: str = Field(alias="type")
    details: UsdAccountDetails = Field(alias="details")

    @pydantic.validator("currency")
    @classmethod
    def currency_is_valid(cls, value):
        if Currency.USD == value:
            return value
        message = "Invalid currency argument for usd recipient request. {}".format(value)
        raise ValueError(message)

    @pydantic.validator("type")
    @classmethod
    def type_is_valid(cls, value):
        if value == "aba":
            return value
        raise ValueError("Invalid type argument for usd recipient request")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        schema_extra = {
            "example":
                {
                    "profile": 999,
                    "accountHolderName": "<recipient name>",
                    "currency": "USD",
                    "type": "aba",
                    "details": {
                        "legalType": "PRIVATE",
                        "abartn": "111000025",
                        "accountNumber": "12345678",
                        "accountType": "CHECKING",
                        "address": {
                            "country": "GB",
                            "city": "London",
                            "postCode": "10025",
                            "firstLine": "50 Branson Ave"
                        }
                    }
                }
        }
