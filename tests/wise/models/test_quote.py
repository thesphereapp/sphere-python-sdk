import unittest
from typing import Dict

from sphere.wise.models.quote import Quote


class QuoteTest(unittest.TestCase):
    def test_building_from_dict(self):
        quote = Quote(**self.__dict())
        self.assertEqual("USD", quote.target_currency.value)

    @staticmethod
    def __dict() -> Dict[str, any]:
        return {
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
                                "label": "0.77 GBP"
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
                                "label": "3.04 GBP"
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
