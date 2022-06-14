from unittest import TestCase

from fastapi.testclient import TestClient

from app import app


class TestApp(TestCase):
    client = TestClient(app=app)

    def test_heath_endpoint(self):
        # given
        endpoint = "/health"
        # when
        result = self.client.get(endpoint)
        # then
        self.assertEqual(200, result.status_code)
        self.assertEqual({"Hello": "World"}, result.json())