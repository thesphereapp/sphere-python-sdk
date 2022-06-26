import unittest
from typing import Dict

from sphere.wise.models.account_details import UsdAccountDetails, EurAccountDetails, GbpAccountDetails


class AccountDetailsTest(unittest.TestCase):
    def test_building_usd_from_dict(self):
        details = UsdAccountDetails(**self.__usd_dict())
        self.assertEqual("50 Branson Ave", details.address.first_line)

    def test_building_eur_from_dict(self):
        details = EurAccountDetails(**self.__eur_dict())
        self.assertEqual("DE89370400440532013000", details.iban)

    def test_building_gbp_from_dict(self):
        details = GbpAccountDetails(**self.__gbp_dict())
        self.assertEqual("12345678", details.account_number)

    @staticmethod
    def __usd_dict() -> Dict[str, any]:
        return {
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

    @staticmethod
    def __eur_dict() -> Dict[str, any]:
        return {
            "legalType": "PRIVATE",
            "IBAN": "DE89370400440532013000"
        }

    @staticmethod
    def __gbp_dict() -> Dict[str, any]:
        return {
            "legalType": "PRIVATE",
            "sortCode": "40-30-20",
            "accountNumber": "12345678"
        }
