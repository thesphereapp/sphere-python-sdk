import uuid
from datetime import datetime
from typing import Optional, List

import bson
import pydantic
from bson import ObjectId
from pydantic import Field, BaseModel
from sphere.finance.currency import Currency


class Notice(BaseModel):
    text: str = Field(alias="text")
    link: Optional[str] = Field(alias="link")
    type: str = Field(alias="type")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        schema_extra = {
            "example":
                {
                    "text": "You can have a maximum of 3 open transfers with a guaranteed rate. After that, they'll be transferred using the live rate. Complete or cancel your other transfers to regain the use of guaranteed rate.",
                    "link": None,
                    "type": "WARNING"
                }
        }


class Fee(BaseModel):
    transferwise: float = Field(alias="transferwise")
    pay_in: int = Field(alias="payIn")
    discount: float = Field(alias="discount")
    partner: int = Field(alias="partner")
    total: float = Field(alias="total")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        schema_extra = {
            "example":
                {
                    "transferwise": 3.04,
                    "payIn": 0,
                    "discount": 2.27,
                    "partner": 0,
                    "total": 0.77
                }
        }


class MoneyValue(BaseModel):
    amount: float = Field(alias="amount")
    currency: Currency = Field(alias="currency")
    label: str = Field(alias="label")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        schema_extra = {
            "example":
                {
                    "amount": 0.77,
                    "currency": "GBP",
                    "label:": "0.77 GBP"
                }
        }


class Total(BaseModel):
    type: str = Field(alias="type")
    label: str = Field(alias="label")
    value: MoneyValue = Field(alias="value")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        schema_extra = {
            "example":
                {
                    "type": "TOTAL",
                    "label": "Total fees",
                    "value": {
                        "amount": 0.77,
                        "currency": "GBP",
                        "label:": "0.77 GBP"
                    }
                }
        }


class Explanation(BaseModel):
    plain_text: str = Field(alias="plainText")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        schema_extra = {
            "example":
                {
                    "plainText": "You can have a discount for a number of reasons..."
                }
        }


class Item(BaseModel):
    type: str = Field(alias="type")
    label: str = Field(alias="label")
    value: MoneyValue = Field(alias="value")
    id: Optional[int] = Field(alias="id")
    explanation: Optional[Explanation] = Field(alias="explanation")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        schema_extra = {
            "example":
                {
                    "id": 123,
                    "type": "DISCOUNT",
                    "value": {
                        "amount": -2.27,
                        "currency": "GBP",
                        "label": "2.27 GBP"
                    },
                    "label": "Discount applied",
                    "explanation": {
                        "plainText": "You can have a discount for a number of reasons..."
                    }
                }
        }


class Price(BaseModel):
    price_set_id: int = Field(alias="priceSetId")
    total: Total = Field(alias="total")
    items: List[Item] = Field(alias="item")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        schema_extra = {
            "example":
                {
                    "priceSetId": 238,
                    "total": {
                        "type": "TOTAL",
                        "label": "Total fees",
                        "value": {
                            "amount": 0.77,
                            "currency": "GBP",
                            "label:": "0.77 GBP"
                        }
                    },
                    "items": [
                        {
                            "type": "FEE",
                            "label": "fee",
                            "value": {
                                "amount": 0,
                                "currency": "GBP",
                                "label": "0 GBP"
                            }
                        },
                        {
                            "type": "TRANSFERWISE",
                            "label": "Our fee",
                            "value": {
                                "amount": 3.04,
                                "currency": "GBP",
                                "label": "3.04 GBP"
                            }
                        },
                        {
                            "id": 123,
                            "type": "DISCOUNT",
                            "value": {
                                "amount": -2.27,
                                "currency": "GBP",
                                "label": "2.27 GBP"
                            },
                            "label": "Discount applied",
                            "explanation": {
                                "plainText": "You can have a discount for a number of reasons..."
                            }
                        }
                    ]
                }
        }


class DisabledReason(BaseModel):
    code: str = Field(alias="code")
    message: str = Field(alias="message")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        schema_extra = {
            "example":
                {
                    "code": "error.payInmethod.disabled",
                    "message": "Open a multi-currency account and add funds to instantly pay for your transfers."
                }
        }


class PaymentOption(BaseModel):
    disabled: bool = Field(alias="disabled")
    estimated_delivery: Optional[datetime] = Field(alias="estimatedDelivery")
    formatted_estimated_delivery: Optional[str] = Field(alias="formattedEstimatedDelivery")
    estimated_delivery_delays: List[str] = Field(alias="estimatedDeliveryDelays")
    fee: Fee = Field(alias="fee")
    price: Price = Field(alias="price")
    source_amount: int = Field(alias="sourceAmount")
    target_amount: float = Field(alias="targetAmount")
    source_currency: str = Field(alias="sourceCurrency")
    target_currency: str = Field(alias="targetCurrency")
    pay_in: str = Field(alias="payIn")
    pay_out: str = Field(alias="pay_out")
    allowed_profile_types: List[str] = Field(alias="allowedProfileTypes")
    pay_in_product: str = Field(alias="payInProduct")
    fee_percentage: float = Field(alias="feePercentage")
    disabled_reason: Optional[DisabledReason] = Field(alias="disabledReason")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example":
                {
                    "disabled": False,
                    "estimatedDelivery": "2019-04-08T12:30:00Z",
                    "formattedEstimatedDelivery": "by Apr 8",
                    "estimatedDeliveryDelays": [],
                    "fee": {
                        "transferwise": 3.04,
                        "payIn": 0,
                        "discount": 2.27,
                        "partner": 0,
                        "total": 0.77
                    },
                    "price": {
                        "priceSetId": 238,
                        "total": {
                            "type": "TOTAL",
                            "label": "Total fees",
                            "value": {
                                "amount": 0.77,
                                "currency": "GBP",
                                "label:": "0.77 GBP"
                            }
                        },
                        "items": [
                            {
                                "type": "FEE",
                                "label": "fee",
                                "value": {
                                    "amount": 0,
                                    "currency": "GBP",
                                    "label": "0 GBP"
                                }
                            },
                            {
                                "type": "TRANSFERWISE",
                                "label": "Our fee",
                                "value": {
                                    "amount": 3.04,
                                    "currency": "GBP",
                                    "label": "3.04 GBP"
                                }
                            },
                            {
                                "id": 123,
                                "type": "DISCOUNT",
                                "value": {
                                    "amount": -2.27,
                                    "currency": "GBP",
                                    "label": "2.27 GBP"
                                },
                                "label": "Discount applied",
                                "explanation": {
                                    "plainText": "You can have a discount for a number of reasons..."
                                }
                            }
                        ]
                    },
                    "sourceAmount": 100,
                    "targetAmount": 129.24,
                    "sourceCurrency": "GBP",
                    "targetCurrency": "USD",
                    "payIn": "BANK_TRANSFER",
                    "pay_out": "BANK_TRANSFER",
                    "allowedProfileTypes": [
                        "PERSONAL",
                        "BUSINESS"
                    ],
                    "payInProduct": "CHEAP",
                    "feePercentage": 0.0092
                }

        }


class Quote(BaseModel):
    id: str = Field(alias="id")
    source_currency: Currency = Field(alias="sourceCurrency")
    target_currency: Currency = Field(alias="targetCurrency")
    source_amount: int = Field(alias="sourceAmount")
    pay_out: str = Field(alias="pay_out")
    preferred_pay_in: str = Field(alias="preferredPayIn")
    rate: float = Field(alias="rate")
    created_time: datetime = Field(alias="createdTime")
    user: int = Field(alias="user")
    profile: int = Field(alias="profile")
    rate_type: str = Field(alias="rateType")
    rate_expiration_time: datetime = Field(alias="rateExpirationTime")
    guaranteed_target_amount_allowed: bool = Field(alias="guaranteedTargetAmountAllowed")
    target_amount_allowed: bool = Field(alias="targetAmountAllowed")
    guaranteed_target_amount: bool = Field(alias="guaranteedTargetAmount")
    provided_amount_type: str = Field(alias="providedAmountType")
    payment_options: List[PaymentOption] = Field(alias="paymentOptions")
    status: str = Field(alias="status")
    expiration_time: datetime = Field(alias="expirationTime")
    notices: List[Notice]

    @pydantic.validator("id")
    @classmethod
    def id_is_valid_uuid(cls, value):
        uuid_obj = uuid.UUID(value, version=4)
        if str(uuid_obj) == value:
            return value
        raise ValueError("Id is not valid uuid 4")

    # TODO: write unit test
    def find_cheapest_payment_option(self) -> PaymentOption:
        raise NotImplementedError("finding cheapest payment option")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        schema_extra = {
            "example": {
                "id": "11144c35-9fe8-4c32-b7fd-d05c2a7734bf",
                "sourceCurrency": "GBP",
                "targetCurrency": "USD",
                "sourceAmount": 100,
                "pay_out": "BANK_TRANSFER",
                "preferredPayIn": "BANK_TRANSFER",
                "rate": 1.30445,
                "createdTime": "2019-04-05T13:18:58Z",
                "user": 55,
                "profile": 101,
                "rateType": "FIXED",
                "rateExpirationTime": "2019-04-08T13:18:57Z",
                "guaranteedTargetAmountAllowed": True,
                "targetAmountAllowed": True,
                "guaranteedTargetAmount": False,
                "providedAmountType": "SOURCE",
                "paymentOptions": [
                    {
                        "disabled": False,
                        "estimatedDelivery": "2019-04-08T12:30:00Z",
                        "formattedEstimatedDelivery": "by Apr 8",
                        "estimatedDeliveryDelays": [],
                        "fee": {
                            "transferwise": 3.04,
                            "payIn": 0,
                            "discount": 2.27,
                            "partner": 0,
                            "total": 0.77
                        },
                        "price": {
                            "priceSetId": 238,
                            "total": {
                                "type": "TOTAL",
                                "label": "Total fees",
                                "value": {
                                    "amount": 0.77,
                                    "currency": "GBP",
                                    "label:": "0.77 GBP"
                                }
                            },
                            "items": [
                                {
                                    "type": "FEE",
                                    "label": "fee",
                                    "value": {
                                        "amount": 0,
                                        "currency": "GBP",
                                        "label": "0 GBP"
                                    }
                                },
                                {
                                    "type": "TRANSFERWISE",
                                    "label": "Our fee",
                                    "value": {
                                        "amount": 3.04,
                                        "currency": "GBP",
                                        "label": "3.04 GBP"
                                    }
                                },
                                {
                                    "id": 123,
                                    "type": "DISCOUNT",
                                    "value": {
                                        "amount": -2.27,
                                        "currency": "GBP",
                                        "label": "2.27 GBP"
                                    },
                                    "label": "Discount applied",
                                    "explanation": {
                                        "plainText": "You can have a discount for a number of reasons..."
                                    }
                                }
                            ]
                        },
                        "sourceAmount": 100,
                        "targetAmount": 129.24,
                        "sourceCurrency": "GBP",
                        "targetCurrency": "USD",
                        "payIn": "BANK_TRANSFER",
                        "pay_out": "BANK_TRANSFER",
                        "allowedProfileTypes": [
                            "PERSONAL",
                            "BUSINESS"
                        ],
                        "payInProduct": "CHEAP",
                        "feePercentage": 0.0092
                    },
                    {
                        "disabled": True,
                        "estimatedDelivery": None,
                        "formattedEstimatedDelivery": None,
                        "estimatedDeliveryDelays": [],
                        "fee": {
                            "transferwise": 3.04,
                            "payIn": 0,
                            "discount": 0,
                            "partner": 0,
                            "total": 3.04
                        },
                        "price": {
                            "priceSetId": 238,
                            "total": {
                                "type": "TOTAL",
                                "label": "Total fees",
                                "value": {
                                    "amount": 3.04,
                                    "currency": "GBP",
                                    "label:": "3.04 GBP"
                                }
                            },
                            "items": [
                                {
                                    "type": "FEE",
                                    "label": "fee",
                                    "value": {
                                        "amount": 0,
                                        "currency": "GBP",
                                        "label": "0 GBP"
                                    }
                                },
                                {
                                    "type": "TRANSFERWISE",
                                    "label": "Our fee",
                                    "value": {
                                        "amount": 3.04,
                                        "currency": "GBP",
                                        "label": "3.04 GBP"
                                    }
                                }
                            ]
                        },
                        "sourceAmount": 100,
                        "targetAmount": 129,
                        "sourceCurrency": "GBP",
                        "targetCurrency": "USD",
                        "payIn": "BALANCE",
                        "pay_out": "BANK_TRANSFER",
                        "allowedProfileTypes": [
                            "PERSONAL",
                            "BUSINESS"
                        ],
                        "disabledReason": {
                            "code": "error.payInmethod.disabled",
                            "message": "Open a multi-currency account and add funds to instantly pay for your transfers."
                        },
                        "payInProduct": "BALANCE",
                        "feePercentage": 0.0111
                    }
                ],
                "status": "PENDING",
                "expirationTime": "2019-04-05T13:48:58Z",
                "notices": [
                    {
                        "text": "You can have a maximum of 3 open transfers with a guaranteed rate. After that, they'll be transferred using the live rate. Complete or cancel your other transfers to regain the use of guaranteed rate.",
                        "link": None,
                        "type": "WARNING"
                    }
                ]
            }
        }
