from pydantic import Field, BaseModel
from sphere.finance.currency import Currency


class QuoteRequest(BaseModel):
    profile_id: int = Field(alias="profileId")
    source_currency: Currency = Field(alias="sourceCurrency")
    source_amount: int = Field(alias="sourceAmount")
    target_currency: Currency = Field(alias="targetCurrency")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        schema_extra = {
            "example":
                {
                    "profileId": 123,
                    "sourceCurrency": "EUR",
                    "sourceAmount": 10,
                    "targetCurrency": "GBP"
                }
        }
