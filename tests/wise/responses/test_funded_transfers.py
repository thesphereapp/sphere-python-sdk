import unittest
from typing import Dict

from sphere.wise.responses.funded_transfer import FundedTransferResponse


class FundedTransfersTest(unittest.TestCase):
    def test_building_from_dict(self):
        resp = FundedTransferResponse(**self.__dict())
        self.assertEqual("COMPLETED", resp.status.value)

    @staticmethod
    def __dict() -> Dict[str, any]:
        return {
            "type": "BALANCE",
            "status": "COMPLETED",
            "errorCode": None
        }
