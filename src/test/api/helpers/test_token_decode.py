from datetime import  timedelta
from unittest import TestCase
from datetime import datetime
import jwt

from main.api.helpers.token_decode import SecurityHelper


class TestJwtService(TestCase):
    jwt_secret = "oMMUNvjsCBa3MZefqDjYwID8H9UgktsmDta2fZvv2dO6SfMXLQJaG81rHyJo"
    service = SecurityHelper()

    def test_encode_decode(self):
        # given
        payload = {
            "userId": "123",
            "expiryTimeStampUtc": str(datetime.utcnow() + timedelta(minutes=15))
        }
        encoded_payload = jwt.encode(payload, self.jwt_secret)
        # when
        result = self.service.decode_token(encoded_payload)
        # then
        self.assertEqual("123", result["userId"])
