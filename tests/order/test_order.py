import unittest
from typing import Dict

from sphere.order.order import Order


class OrderTest(unittest.TestCase):

    def test_building_from_dict(self):
        # given
        my_dict = self.order_dict()
        # when
        resp = Order(**my_dict)
        # then
        self.assertEqual(resp.cart.metaData.currency.value, "GBP")

    @staticmethod
    def order_dict() -> Dict[str, any]:
        return {
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
