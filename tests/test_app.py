import unittest
import requests
import json
import os

BASE_URL = "http://localhost:8080"  # URL where the Flask app is running


class ReceiptProcessorIntegrationTest(unittest.TestCase):

    @classmethod
    def load_example_receipt(cls, filename):
        """
        Utility function to load a JSON file from the examples directory.
        """
        with open(os.path.join("examples", filename), "r") as file:
            return json.load(file)

    def test_process_receipt(self):
        receipt_data = self.load_example_receipt("simple-receipt.json")

        response = requests.post(
            f"{BASE_URL}/receipts/process",
            json=receipt_data
        )

        self.assertEqual(response.status_code, 200)

        response_data = response.json()

        self.assertIn("id", response_data)

    def test_process_invalid_receipt(self):
        receipt_data = self.load_example_receipt("invalid-receipt.json")

        response = requests.post(
            f"{BASE_URL}/receipts/process",
            json=receipt_data
        )

        self.assertEqual(response.status_code, 400)

        error_data = response.json()

        self.assertIn("error", error_data)
        self.assertEqual(error_data["error"],
                         "Missing required field: retailer")

    def test_process_already_processed_receipt(self):
        receipt_data = self.load_example_receipt("simple-receipt.json")

        response = requests.post(
            f"{BASE_URL}/receipts/process",
            json=receipt_data
        )

        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.receipt_id = response_data["id"]

        response = requests.post(
            f"{BASE_URL}/receipts/process",
            json=receipt_data
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], self.receipt_id)

    def test_get_points_receipt_processed(self):
        receipt_data = self.load_example_receipt("simple-receipt.json")

        post_response = requests.post(
            f"{BASE_URL}/receipts/process", json=receipt_data)
        post_data = post_response.json()
        receipt_id = post_data["id"]

        get_response = requests.get(f"{BASE_URL}/receipts/{receipt_id}/points")

        self.assertEqual(get_response.status_code, 200)

        points_data = get_response.json()

        self.assertIn("points", points_data)

        self.assertIsInstance(points_data["points"], int)
        # Expected points for the simple-receipt.json
        self.assertEqual(points_data["points"], 31)

    def test_get_points_receipt_not_processed(self):
        response = requests.get(f"{BASE_URL}/receipts/invalid-id/points")

        self.assertEqual(response.status_code, 404)

        error_data = response.json()

        self.assertIn("error", error_data)
        self.assertEqual(error_data["error"], "Receipt not found")
