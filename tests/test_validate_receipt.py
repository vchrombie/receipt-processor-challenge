import unittest
from src.utils import (
    validate_receipt_retailer,
    validate_receipt_purchase_date,
    validate_receipt_purchase_time,
    validate_receipt_total,
    validate_receipt_items,
    validate_receipt,
)


class TestValidateReceipt(unittest.TestCase):

    def test_validate_receipt_retailer(self):
        self.assertTrue(validate_receipt_retailer("7 - Eleven")[0])
        self.assertFalse(validate_receipt_retailer("test!@#$")[0])
        self.assertFalse(validate_receipt_retailer("")[0])
        assert validate_receipt_retailer("")[1] == "Invalid retailer format"

    def test_validate_receipt_purchase_date(self):
        self.assertTrue(validate_receipt_purchase_date("2022-01-01")[0])
        self.assertFalse(validate_receipt_purchase_date("01-01-2022")[0])
        assert validate_receipt_purchase_date(
            "01-01-2022")[1] == "Invalid purchaseDate format"

    def test_validate_receipt_purchase_time(self):
        self.assertTrue(validate_receipt_purchase_time("15:00")[0])
        self.assertFalse(validate_receipt_purchase_time(":")[0])
        assert validate_receipt_purchase_time(
            ":")[1] == "Invalid purchaseTime format"

    def test_validate_receipt_total(self):
        self.assertTrue(validate_receipt_total("9.25")[0])
        self.assertFalse(validate_receipt_total("9.2")[0])
        assert validate_receipt_total("9.2")[1] == "Invalid total format"

    def test_validate_receipt_items(self):
        self.assertTrue(validate_receipt_items([
            {"shortDescription": "Gatorade", "price": "2.25"},
            {"shortDescription": "Pepsi", "price": "1.25"}
        ])[0])

        result, message = validate_receipt_items([[]])
        self.assertFalse(result)
        assert message == "Each item must be a dictionary"

        result, message = validate_receipt_items([
            {"price": "2.25"},
        ])
        self.assertFalse(result)
        assert message == "Each item must have shortDescription and price"

        result, message = validate_receipt_items([
            {"shortDescription": "", "price": "2.25"}
        ])
        self.assertFalse(result)
        assert message == "Invalid shortDescription format in items"

        result, message = validate_receipt_items([
            {"shortDescription": "Gatorade", "price": "2.2"}
        ])
        self.assertFalse(result)
        assert message == "Invalid price format in items"

        result, message = validate_receipt_items([])
        self.assertFalse(result)
        assert message == "Items must be a non-empty list"

    def test_validate_receipt(self):
        self.assertTrue(validate_receipt({
            "retailer": "7 - Eleven",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "15:00",
            "total": "9.25",
            "items": [
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Pepsi", "price": "1.25"}
            ]
        }))
        self.assertFalse(validate_receipt({
            "retailer": "7 - Eleven",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "15:00",
            "total": "9.2",
            "items": [
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Pepsi", "price": "1.25"}
            ]
        })[0])
        self.assertFalse(validate_receipt({})[0])
