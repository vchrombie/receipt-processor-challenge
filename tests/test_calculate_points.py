import unittest
from src.utils import (
    calculate_retailer_points,
    calculate_total_amount_points,
    calculate_item_count_points,
    calculate_item_description_points,
    calculate_date_points,
    calculate_time_points,
    calculate_points,
)


class TestCalculatePoints(unittest.TestCase):

    def test_calculate_retailer_points(self):
        self.assertEqual(calculate_retailer_points("Walgreens"), 9)
        self.assertEqual(calculate_retailer_points("7-Eleven"), 7)
        self.assertEqual(calculate_retailer_points(""), 0)

    def test_calculate_total_amount_points(self):
        self.assertEqual(calculate_total_amount_points("9.25"), 25)
        self.assertEqual(calculate_total_amount_points("10.00"), 75)  # 50 + 25
        self.assertEqual(calculate_total_amount_points("9.99"), 0)

    def test_calculate_item_count_points(self):
        self.assertEqual(calculate_item_count_points(4), 10)  # 5 * 2 pairs
        self.assertEqual(calculate_item_count_points(5), 10)  # 5 * 2 pairs
        self.assertEqual(calculate_item_count_points(1), 0)

    def test_calculate_item_description_points(self):
        items = [
            {"shortDescription": "Gatorade", "price": "2.25"},  # 8 characters
            {"shortDescription": "Pepsi", "price": "1.25"}  # 5 characters
        ]
        self.assertEqual(calculate_item_description_points(
            items), 0)

        items = [
            {"shortDescription": "Dasani", "price": "1.25"},  # 6 characters
            {"shortDescription": "Sprite", "price": "1.50"}  # 6 characters
        ]
        self.assertEqual(calculate_item_description_points(
            items), 2)  # (1.25 * 0.2 = [0.25] = 1) + (1.50 * 0.2 = [0.30] = 1)

    def test_calculate_date_points(self):
        self.assertEqual(calculate_date_points("2022-01-01"), 6)
        self.assertEqual(calculate_date_points("2022-01-02"), 0)

    def test_calculate_time_points(self):
        self.assertEqual(calculate_time_points("15:00"), 10)
        self.assertEqual(calculate_time_points("13:00"), 0)
        self.assertEqual(calculate_time_points("14:00"), 10)  # 2:00pm included
        self.assertEqual(calculate_time_points("16:00"), 0)  # 4:00pm excluded

    def test_calculate_points(self):
        self.assertEqual(calculate_points({
            "retailer": "Walgreens",
            "total": "9.25",
            "items": [
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Pepsi", "price": "1.25"}
            ],
            "purchaseDate": "2022-01-01",
            "purchaseTime": "15:00"
        }), 55)
