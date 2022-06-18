from typing import Optional, List, Set

import bson
import pydantic
from bson import ObjectId
from pydantic import Field, BaseModel
from sphere.cart.cart import Cart

from sphere.order.order_state import OrderState
from sphere.order.order_state_log import OrderStateLog
from sphere.order.participant import Participant


class Order(BaseModel):
    id: str = Field(alias="_id")
    state: OrderState = OrderState.NEW
    stateChangeLog: List[OrderStateLog] = [OrderStateLog()]
    cartId: str
    cart: Cart
    profileId: str
    participants: Optional[List[Participant]] = None
    paymentIds: Set[str] = set()

    @pydantic.validator("id")
    @classmethod
    def id_is_valid(cls, value):
        if bson.objectid.ObjectId.is_valid(value):
            return value
        raise ValueError("Invalid id format")

    @pydantic.validator("cartId")
    @classmethod
    def cart_id_is_valid(cls, value):
        if bson.objectid.ObjectId.is_valid(value):
            return value
        raise ValueError("Invalid cartId format")

    @pydantic.validator("profileId")
    @classmethod
    def profile_id_is_valid(cls, value):
        if bson.objectid.ObjectId.is_valid(value):
            return value
        raise ValueError("Invalid profileId format")

    @pydantic.validator("paymentIds")
    @classmethod
    def payment_id_is_valid(cls, value):
        for p in value:
            if not bson.objectid.ObjectId.is_valid(p):
                raise ValueError("Invalid paymentId format")
        return value

    def change_state(self, new_state: OrderState):
        if self.state == new_state:
            return None
        self.state = new_state
        log = OrderStateLog(state=new_state)
        self.stateChangeLog.append(log)

    def add_payment_id(self, payment_id: str):
        self.paymentIds.add(payment_id)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "123",
                "state": "COMPLETED",
                "stateChangeLog": [
                    {
                        "state": "NEW",
                        "date": "2022-03-10 07:00:00"
                    },
                    {
                        "state": "PAYMENT_IN_PROGRESS",
                        "date": "2022-03-10 07:02:00"
                    },
                    {
                        "state": "PAYMENT_COMPLETED",
                        "date": "2022-03-10 07:03:00"
                    }
                ],
                "cartId": "123",
                "cart": {
                    "_id": "123",
                    "locationId": "456789",
                    "tableNr": 1,
                    "metaData": {
                        "cartCurrency": "GBP"
                    },
                    "createdDate": "2022-06-05 07:00:00.550604",
                    "updatedDate": "2022-06-05 07:05:00.550604",
                    "items": [
                        {
                            "id": "123",
                            "name": "Vanilla ice cream",
                            "quantityUnit": {
                                "quantity": 2,
                                "measurementUnit": "AMOUNT",
                                "precision": 0
                            },
                            "note": None,
                            "catalogId": "999",
                            "metaData": {
                                "brand": "Ben and Jerry's"
                            },
                            "basePriceMoney": {
                                "amount": 100,
                                "currency": "GBP"
                            },
                            "grossSalesMoney": {
                                "amount": 200,
                                "currency": "GBP"
                            },
                            "appliedTaxes": [
                                {
                                    "name": "Value added tax",
                                    "money": {
                                        "amount": 30,
                                        "currency": "GBP"
                                    }
                                },
                                {
                                    "name": "Sugar tax",
                                    "money": {
                                        "amount": 10,
                                        "currency": "GBP"
                                    }
                                }
                            ],
                            "appliedDiscounts": [
                                {
                                    "name": "Frequent buyer",
                                    "money": {
                                        "amount": 40,
                                        "currency": "GBP"
                                    }
                                }
                            ],
                            "totalTaxMoney": {
                                "amount": 30,
                                "currency": "GBP"
                            },
                            "totalDiscountMoney": {
                                "amount": 40,
                                "currency": "GBP"
                            },
                            "totalMoney": {
                                "amount": 190,
                                "currency": "GBP"
                            }
                        },
                        {
                            "id": "123",
                            "name": "Chocolate ice cream",
                            "quantityUnit": {
                                "quantity": 1,
                                "measurementUnit": "AMOUNT",
                                "precision": 0
                            },
                            "note": "Make it nice",
                            "catalogId": "999",
                            "metaData": {
                                "brand": "Ben and Jerry's"
                            },
                            "basePriceMoney": {
                                "amount": 100,
                                "currency": "GBP"
                            },
                            "grossSalesMoney": {
                                "amount": 100,
                                "currency": "GBP"
                            },
                            "appliedTaxes": [
                                {
                                    "name": "Value added tax",
                                    "money": {
                                        "amount": 15,
                                        "currency": "GBP"
                                    }
                                },
                                {
                                    "name": "Sugar tax",
                                    "money": {
                                        "amount": 5,
                                        "currency": "GBP"
                                    }
                                }
                            ],
                            "appliedDiscounts": None,
                            "totalTaxMoney": {
                                "amount": 20,
                                "currency": "GBP"
                            },
                            "totalDiscountMoney": None,
                            "totalMoney": {
                                "amount": 120,
                                "currency": "GBP"
                            }
                        },
                    ],
                    "money": {
                        "totalGrossSalesMoney": {
                            "amount": 300,
                            "currency": "GBP"
                        },
                        "totalTaxMoney": {
                            "amount": 50,
                            "currency": "GBP"
                        },
                        "totalDiscountMoney": {
                            "amount": 40,
                            "currency": "GBP"
                        },
                        "totalMoney": {
                            "amount": 310,
                            "currency": "GBP"
                        },
                    }
                },
                "profileId": "459",
                "participants": [
                    {
                        "name": "James Clark",
                        "email": "james.clark@example.com",
                    }
                ],
                "paymentIds": ["999"]
            }
        }
