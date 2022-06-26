import pydantic
from pydantic import BaseModel, Field
from sphere.finance.currency import Currency
from sphere.wise.models.account_type import AccountType
from sphere.wise.models.legal_type import LegalType
import string

LETTERS = {ord(d): str(i) for i, d in enumerate(string.digits + string.ascii_uppercase)}


def _number_iban(iban):
    return (iban[4:] + iban[:4]).translate(LETTERS)


def valid_iban(iban):
    return int(_number_iban(iban)) % 97 == 1


def generate_iban_check_digits(iban):
    number_iban = _number_iban(iban[:2] + '00' + iban[4:])
    return '{:0>2}'.format(98 - (int(number_iban) % 97))


def is_valid_iban(value: str) -> bool:
    if generate_iban_check_digits(value) == value[2:4] and valid_iban(value):
        return True
    return False


class EurRecipientRequestDetails(BaseModel):
    legal_type: LegalType = Field(alias="legalType")
    iban: str = Field(alias="IBAN")

    @pydantic.validator("iban")
    @classmethod
    def iban_is_valid(cls, value):
        if is_valid_iban(value):
            return value
        raise ValueError("Invalid iban for eur recipient request")

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


class GbpRecipientRequestDetails(BaseModel):
    legal_type: LegalType = Field(alias="legalType")
    # TODO: add sort code valdiator
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


class UsdRecipientRequestDetails(BaseModel):
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


class EurRecipientRequest(BaseModel):
    profile: int = Field(alias="profile")
    account_holder_name: str = Field(alias="accountHolderName")
    currency: Currency = Field(Currency.EUR, alias="currency")
    type: str = Field(alias="type")
    details: EurRecipientRequestDetails = Field(alias="details")

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
    details: GbpRecipientRequestDetails = Field(alias="details")

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
    details: UsdRecipientRequestDetails = Field(alias="details")

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
