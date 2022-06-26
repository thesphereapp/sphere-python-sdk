from typing import Union

from pydantic import BaseModel, Field

from sphere.finance.currency import Currency
from sphere.wise.models.account_details import EurAccountDetails, GbpAccountDetails, UsdAccountDetails


# TODO: unit test
class BusinessProfilePayoutDetails(BaseModel):
    account_details: Union[EurAccountDetails, GbpAccountDetails, UsdAccountDetails] = Field(alias="accountDetails")
    currency: Currency = Field(alias="currency")
    wise_recipient_id: int = Field(alias="wiseRecipientId")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        schema_extra = {
            "example":
                {
                    "accountDetails": {
                        "legalType": "PRIVATE",
                        "sortCode": "40-30-20",
                        "accountNumber": "12345678"
                    },
                    "currency": "EUR",
                    "wiseRecipientId": 5,
                }
        }
