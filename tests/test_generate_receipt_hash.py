import unittest
from src.utils import generate_receipt_hash


class TestGenerateReceiptHash(unittest.TestCase):
    def test_generate_receipt_hash(self):
        data = {
            "retailer": "Walgreens",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "15:00",
            "items": [
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Pepsi", "price": "1.25"}
            ],
            "total": "9.25"
        }
        # Expected hash generated from the data
        self.assertEqual(generate_receipt_hash(
            data), "27edd4bcda59a5bab33e2266ab2876c5ffebebc4c7de12c93806eb8357f56870")
