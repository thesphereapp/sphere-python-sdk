import unittest
from typing import Dict

from sphere.wise.models.transfer import Transfer


class TransferTest(unittest.TestCase):

    def test_building_from_dict(self):
        transfer = Transfer(**self.__dict())
        self.assertEqual(333, transfer.target_account)

    @staticmethod
    def __dict() -> Dict[str, any]:
        return {
            "id": 468956,
            "user": 123,
            "targetAccount": 333,
            "sourceAccount": None,
            "quote": None,
            "quoteUuid": "bd244a95-dcf8-4c31-aac8-bf5e2f3e54c0",
            "status": "incoming_payment_waiting",
            "reference": "to my friend",
            "rate": 0.9065,
            "created": "2018-08-28 07:43:55",
            "business": 999,
            "transferRequest": None,
            "details": {
                "reference": "to my friend"
            },
            "hasActiveIssues": False,
            "sourceCurrency": "EUR",
            "sourceValue": 661.89,
            "targetCurrency": "GBP",
            "targetValue": 600,
            "customerTransactionId": "bd244a95-dcf8-4c31-aac8-bf5e2f3e54c0"
        }
