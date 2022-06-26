import unittest
from typing import Dict

from sphere.wise.requests.transfer_request import TransferRequest


class QuoteTest(unittest.TestCase):

    def test_building_from_dict(self):
        transfer = TransferRequest(**self.__dict())
        self.assertEqual(900, transfer.source_account)

    @staticmethod
    def __dict() -> Dict[str, any]:
        return {
            "sourceAccount": 900,
            "targetAccount": 200,
            "quoteUuid": "e5ca48ea-90a4-4207-9759-34712121384a",
            "customerTransactionId": "9226ad17-37dd-4659-aaad-fb89d300a408",
            "reference": "Sphere",
            "transferPurpose": "verification.transfers.purpose.pay.bills",
            "transferPurposeSubTransferPurpose": "verification.sub.transfers.purpose.pay.interpretation.service",
            "sourceOfFunds": "verification.source.of.funds.other"
        }
