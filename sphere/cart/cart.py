from datetime import datetime, timezone
from typing import Optional, List

from bson import ObjectId
from pydantic import Field, BaseModel
from sphere.finance.money import money_sum

from sphere.cart.cart_money import CartMoney

from sphere.item.order_line_item import OrderLineItem

from sphere.cart.cart_metadata import CartMetadata


class Cart(BaseModel):
    id: Optional[str] = Field(alias="_id")
    locationId: str
    tableNr: int
    metaData: CartMetadata
    createdDate: datetime = datetime.now(timezone.utc)
    updatedDate: datetime = datetime.now(timezone.utc)
    items: List[OrderLineItem] = []
    money: Optional[CartMoney] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
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
            }
        }

    def item_in_cart(self, item_id: str) -> bool:
        for item in self.items:
            if item.id == item_id:
                return True
        return False

    def __item_id(self, item_id: str) -> Optional[int]:
        for i, item in enumerate(self.items):
            if item.id == item_id:
                return i
        return None

    def modify_item(self, new_item: OrderLineItem):
        if new_item.quantityUnit.quantity.is_zero():
            return self.remove_item(new_item)

        self.updatedDate = datetime.now(timezone.utc)
        my_item_id = self.__item_id(new_item.id)
        if my_item_id is not None:
            self.items[my_item_id].quantity_updated(new_item.quantityUnit)
        else:
            self.items.append(new_item)
        self.__update_cart_money()

    def remove_item(self, new_item: OrderLineItem):
        my_item_id = self.__item_id(new_item.id)
        if my_item_id is None:
            return None
        self.updatedDate = datetime.now(timezone.utc)
        del self.items[my_item_id]
        self.__update_cart_money()

    def __update_cart_money(self):
        if (self.items is None) or len(self.items) == 0:
            self.money = None
            return None
        total_gross_sales_moneys = []
        total_tax_moneys = []
        total_discount_moneys = []
        total_moneys = []
        for item in self.items:
            total_gross_sales_moneys.append(item.grossSalesMoney)
            total_tax_moneys.append(item.totalTaxMoney)
            total_discount_moneys.append(item.totalDiscountMoney)
            total_moneys.append(item.totalMoney)

        total_gross_sales_money = money_sum(total_gross_sales_moneys).get(self.metaData.currency)
        total_tax_money = money_sum(total_tax_moneys).get(self.metaData.currency)
        total_discount_money = money_sum(total_discount_moneys).get(self.metaData.currency)
        total_moneys = money_sum(total_moneys).get(self.metaData.currency)

        self.money = CartMoney(totalGrossSalesMoney=total_gross_sales_money,
                               totalTaxMoney=total_tax_money,
                               totalDiscountMoney=total_discount_money,
                               totalMoney=total_moneys)


def new_cart(location_id: str, table_nr: int) -> Cart:
    return Cart(id=str(ObjectId()),
                locationId=location_id,
                tableNr=table_nr,
                metaData=CartMetadata())
