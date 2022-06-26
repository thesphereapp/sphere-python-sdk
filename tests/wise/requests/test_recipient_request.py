import unittest
from typing import Dict

from sphere.wise.requests.recipient_requests import UsdRecipientRequest, EurRecipientRequest, GbpRecipientRequest


class RecipientRequestTest(unittest.TestCase):

    def test_building_usd(self):
        resp = UsdRecipientRequest(**self.__dict_usd())
        self.assertEqual("London", resp.details.address.city)

    def test_building_eur(self):
        resp = EurRecipientRequest(**self.__dict_eur())
        self.assertEqual("BUSINESS", resp.details.legal_type.value)
        self.assertEqual("DE89370400440532013000", resp.details.iban)

    def test_building_gbp(self):
        resp = GbpRecipientRequest(**self.__dict_gbp())
        self.assertEqual("40-30-20", resp.details.sort_code)

    @staticmethod
    def __dict_usd() -> Dict[str, any]:
        return {
            "profile": 999,
            "accountHolderName": "<recipient name>",
            "currency": "USD",
            "type": "aba",
            "details": {
                "legalType": "PRIVATE",
                "abartn": "111000025",
                "accountNumber": "12345678",
                "accountType": "CHECKING",
                "address": {
                    "country": "GB",
                    "city": "London",
                    "postCode": "10025",
                    "firstLine": "50 Branson Ave"
                }
            }
        }

    @staticmethod
    def __dict_gbp() -> Dict[str, any]:
        return {
            "profile": 999,
            "accountHolderName": "Jon's Bakerly Plc",
            "currency": "GBP",
            "type": "sort_code",
            "details": {
                "legalType": "PRIVATE",
                "sortCode": "40-30-20",
                "accountNumber": "12345678"
            }
        }

    @staticmethod
    def __dict_eur() -> Dict[str, any]:
        return {
            "profile": 111,
            "accountHolderName": "My Bakery Oü",
            "currency": "EUR",
            "type": "iban",
            "details": {
                "legalType": "BUSINESS",
                "IBAN": "DE89370400440532013000"
            }
        }
