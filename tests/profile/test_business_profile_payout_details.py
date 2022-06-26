import unittest
from typing import Dict

from sphere.profile.business_profile_payout_details import BusinessProfilePayoutDetails


class BusinessProfilePayoutDetailsTest(unittest.TestCase):

    def test_building_gbp_from_dict(self):
        # given-when
        details = BusinessProfilePayoutDetails(**self.__gbp_dict())
        # then
        self.assertEqual("GBP", details.currency.value)
        self.assertEqual(5, details.wise_recipient_id)
        self.assertEqual("40-30-20", details.account_details.sort_code)
        self.assertEqual("12345678", details.account_details.account_number)

    def test_building_eur_from_dict(self):
        # given-when
        details = BusinessProfilePayoutDetails(**self.__eur_dict())
        # then
        self.assertEqual("EUR", details.currency.value)
        self.assertEqual(5, details.wise_recipient_id)
        self.assertEqual("PRIVATE", details.account_details.legal_type.value)
        self.assertEqual("DE89370400440532013000", details.account_details.iban)

    def test_building_usd_from_dict(self):
        # given-when
        details = BusinessProfilePayoutDetails(**self.__usd_dict())
        # then
        self.assertEqual("USD", details.currency.value)
        self.assertEqual(5, details.wise_recipient_id)
        self.assertEqual("CHECKING", details.account_details.account_type.value)
        self.assertEqual("50 Branson Ave", details.account_details.address.first_line)

    @staticmethod
    def __eur_dict() -> Dict[str, any]:
        return {
            "accountDetails": {
                "legalType": "PRIVATE",
                "IBAN": "DE89370400440532013000"
            },
            "currency": "EUR",
            "wiseRecipientId": 5,
        }

    @staticmethod
    def __usd_dict() -> Dict[str, any]:
        return {
            "accountDetails": {
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
                },
            "currency": "USD",
            "wiseRecipientId": 5,
        }

    @staticmethod
    def __gbp_dict() -> Dict[str, any]:
        return {
            "accountDetails": {
                "legalType": "PRIVATE",
                "sortCode": "40-30-20",
                "accountNumber": "12345678"
            },
            "currency": "GBP",
            "wiseRecipientId": 5,
        }
