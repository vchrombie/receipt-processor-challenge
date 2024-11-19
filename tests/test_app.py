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

    def test_bonus_points_new_users(self):

        receipt_data = self.load_example_receipt("simple-receipt.json")
        response = requests.post(
            f"{BASE_URL}/receipts/process",
            json=receipt_data,
        )

        self.assertEqual(response.status_code, 200)
        self.id1 = response.json()["id"]

        receipt_data = self.load_example_receipt("receipt-1.json")
        response = requests.post(
            f"{BASE_URL}/receipts/process",
            json=receipt_data,
        )

        self.assertEqual(response.status_code, 200)
        self.id2 = response.json()["id"]

        receipt_data = self.load_example_receipt("receipt-2.json")
        response = requests.post(
            f"{BASE_URL}/receipts/process",
            json=receipt_data,
        )

        self.assertEqual(response.status_code, 200)
        self.id3 = response.json()["id"]

        response = requests.get(f"{BASE_URL}/receipts/{self.id1}/points")
        self.points1 = response.json()["points"]

        response = requests.get(f"{BASE_URL}/receipts/{self.id2}/points")
        self.points2 = response.json()["points"]

        response = requests.get(f"{BASE_URL}/receipts/{self.id3}/points")
        self.points3 = response.json()["points"]

        self.assertEqual(self.points1, 1031)  # 1000 bonus + 31 points
        self.assertEqual(self.points2, 528)  # 500 bonus + 28 points
        self.assertEqual(self.points3, 359)  # 250 bonus + 109 points

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
        self.assertEqual(points_data["points"], 1031)

    def test_get_points_receipt_not_processed(self):
        response = requests.get(f"{BASE_URL}/receipts/invalid-id/points")

        self.assertEqual(response.status_code, 404)

        error_data = response.json()

        self.assertIn("error", error_data)
        self.assertEqual(error_data["error"], "Receipt not found")
