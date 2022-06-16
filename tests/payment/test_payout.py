import unittest

from dns.immutable import Dict

from sphere.payment.payout import Payout


class PayoutTest(unittest.TestCase):

    def test_building_from_dict(self):
        # given
        my_dict = self.__dict_value()
        # when
        resp = Payout(**my_dict)
        # then
        self.assertEqual(resp.paymentIds[0], "1")

    @staticmethod
    def __dict_value() -> Dict[str, any]:
        return {
                "_id": "123",
                "userId": "456",
                "profileId": "789",
                "paymentIds": [
                    "1",
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "9",
                ],
                "amount": {
                    "amount": 850,
                    "currency": "GBP"
                },
                "state": "NEW",
                "stateChangeLog": [
                    {
                        "state": "NEW",
                        "date": "2022-03-10 07:00:00.550604",
                    }
                ],
            }
