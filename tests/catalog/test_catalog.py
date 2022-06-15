import unittest
from typing import Dict

from sphere.catalog.catalog import Catalog


class CatalogTest(unittest.TestCase):

    def test_building_from_dict(self):
        # given
        my_dict = self.catalog_dict()
        # when
        resp = Catalog(**my_dict)
        # then
        self.assertEqual(len(resp.allowedLocations),3)

    @staticmethod
    def catalog_dict() -> Dict[str, any]:
        return {
                "_id": "123",
                "name": "Ice cream",
                "userId": "456",
                "presentAtAllLocations": False,
                "allowedLocations": ["789", "101112", "456789"]
            }
