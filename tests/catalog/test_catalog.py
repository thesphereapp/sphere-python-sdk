import unittest
from typing import Dict

from sphere.catalog.catalog import Catalog


class CatalogTest(unittest.TestCase):

    def test_building_from_dict(self):
        catalog = Catalog(**self.catalog_dict())
        self.assertEqual(24, len(catalog.id))
        self.assertEqual(len(catalog.allowedLocations), 3)
        self.assertEqual("62ae0ea285976d54f1e3ffa6", catalog.userId)

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
        self.assertTrue(catalog4.allowed_in_location("62ae1404e694145e58696d50"))

    @staticmethod
    def catalog_dict() -> Dict[str, any]:
        return {
            "_id": "62ae0e9814bf33d7f9d010c3",
            "name": "Ice cream",
            "userId": "62ae0ea285976d54f1e3ffa6",
            "presentAtAllLocations": False,
            "allowedLocations": ["62ae13f741613f993baead1a", "62ae13fe2ef3d4f322d475c6", "62ae1404e694145e58696d50"]
        }
