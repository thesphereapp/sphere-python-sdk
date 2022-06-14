from decimal import Decimal

from pydantic import BaseModel, Field

from item.measurement_unit import MeasurementUnit


class OrderQuantityUnit(BaseModel):
    measurementUnit: MeasurementUnit = MeasurementUnit.AMOUNT
    # TODO: use lte and ge
    # precision: int = Field(0,lte=5,ge=0)
    precision: int = Field(0, title="Precision", description="Number of places after comma we're going to show")
    quantity: Decimal = Field(Decimal(0.0), title="Quantity", description="The quantity of the product")

    class Config:
        schema_extra = {
            "example": {
                "quantity": 5.0,
                "measurementUnit": "METER",
                "precision": 3
            }
        }
