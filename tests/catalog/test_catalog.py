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
        self.assertEqual(len(resp.allowedLocations), 3)

    def test_present_in_location(self):
        catalog1 = Catalog(**self.catalog_dict())
        catalog1.presentAtAllLocations = True
        self.assertTrue(catalog1.allowed_in_location("123"))
        self.assertTrue(catalog1.allowed_in_location("789"))

        catalog2 = Catalog(**self.catalog_dict())
        catalog2.allowedLocations = None
        self.assertFalse(catalog2.allowed_in_location("123"))
        self.assertFalse(catalog2.allowed_in_location("789"))

        catalog3 = Catalog(**self.catalog_dict())
        catalog3.allowedLocations = []
        self.assertFalse(catalog3.allowed_in_location("123"))
        self.assertFalse(catalog3.allowed_in_location("789"))

        catalog4 = Catalog(**self.catalog_dict())
        self.assertFalse(catalog4.allowed_in_location("123"))
        self.assertTrue(catalog4.allowed_in_location("789"))

    @staticmethod
    def catalog_dict() -> Dict[str, any]:
        return {
            "_id": "123",
            "name": "Ice cream",
            "userId": "456",
            "presentAtAllLocations": False,
            "allowedLocations": ["789", "101112", "456789"]
        }
