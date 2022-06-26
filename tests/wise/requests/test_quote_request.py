import unittest
from typing import Dict

from sphere.wise.requests.quote_requests import QuoteRequest


class QuoteRequestTest(unittest.TestCase):

    def test_building_from_dict(self):
        quote = QuoteRequest(**self.__dict())
        self.assertEqual(123, quote.profile_id)

    @staticmethod
    def __dict() -> Dict[str, any]:
        return {
            "profileId": 123,
            "sourceCurrency": "EUR",
            "sourceAmount": 10,
            "targetCurrency": "GBP"
        }
