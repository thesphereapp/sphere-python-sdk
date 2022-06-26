import pydantic
import validators
from pydantic import BaseModel, Field
from sphere.wise.models.account_type import AccountType
from sphere.wise.models.legal_type import LegalType


class EurAccountDetails(BaseModel):
    legal_type: LegalType = Field(alias="legalType")
    iban: str = Field(alias="IBAN")

    @pydantic.validator("iban")
    @classmethod
    def iban_is_valid(cls, value):
        if validators.iban(value):
            return value
        raise ValueError("Invalid iban")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        schema_extra = {
            "example":
                {
                    "legalType": "PRIVATE",
                    "IBAN": "DE89370400440532013000"
                }
        }


class GbpAccountDetails(BaseModel):
    legal_type: LegalType = Field(alias="legalType")
    # TODO: add sort code validator
    sort_code: str = Field(alias="sortCode")
    # TODO: add account nr validation
    account_number: str = Field(alias="accountNumber")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        schema_extra = {
            "example":
                {
                    "legalType": "PRIVATE",
                    "sortCode": "40-30-20",
                    "accountNumber": "12345678"
                }
        }

# TODO: add validation
class Address(BaseModel):
    country: str = Field(alias="country")
    city: str = Field(alias="city")
    post_code: str = Field(alias="postCode")
    first_line: str = Field(alias="firstLine")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        schema_extra = {
            "example":
                {
                    "country": "GB",
                    "city": "London",
                    "postCode": "10025",
                    "firstLine": "50 Branson Ave"
                }
        }


class UsdAccountDetails(BaseModel):
    legal_type: LegalType = Field(alias="legalType")
    # TODO: add validation
    abartn: str = Field(alias="abartn")
    # TODO: add validation
    account_number: str = Field(alias="accountNumber")
    account_type: AccountType = Field(alias="accountType")
    address: Address = Field(alias="address")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        schema_extra = {
            "example":
                {
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