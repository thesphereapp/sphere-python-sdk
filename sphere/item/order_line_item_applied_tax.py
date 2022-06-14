from pydantic import Field, BaseModel
from sphere.finance.money import Money


class OrderLineItemAppliedTax(BaseModel):
    # TODO: use name field validator
    #  name: str = Field( lt=512, title='Name',description='name of the tax')
    name: str = Field(title='Name', description='name of the tax')
    money: Money = Field(
        title='Tax finance',
        description='how much tax needs to be paid',
    )

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        schema_extra = {
            "example": {
                "name": "Value added tax",
                "finance": {
                    "amount": 500,
                    "currency": "USD"
                }
            }
        }
