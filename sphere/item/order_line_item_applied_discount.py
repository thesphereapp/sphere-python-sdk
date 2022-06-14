from pydantic import Field, BaseModel
from sphere.finance.money import Money


class OrderLineItemAppliedDiscount(BaseModel):
    # TODO: use name field validator
    #  name: str = Field( lt=512, title='Name',description='name of the discount')
    name: str = Field(title='Name', description='name of the discount')
    money: Money = Field(
        title='Discount finance',
        description='how much discount is applied',
    )

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        schema_extra = {
            "example": {
                "name": "Frequent buyer",
                "finance": {
                    "amount": 100,
                    "currency": "USD"
                }
            }
        }
