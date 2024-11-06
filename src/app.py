from flask import Flask, request, jsonify
import uuid
from points_calculator import (
    calculate_retailer_points,
    calculate_total_amount_points,
    calculate_item_count_points,
    calculate_item_description_points,
    calculate_date_points,
    calculate_time_points,
)

app = Flask(__name__)

# in-memory storage for receipts
receipts = {}


def calculate_points(data):
    """Calculate total points based on the provided receipt data."""
    points = 0

    points += calculate_retailer_points(data["retailer"])
    points += calculate_total_amount_points(data["total"])
    points += calculate_item_count_points(len(data["items"]))
    points += calculate_item_description_points(data["items"])
    points += calculate_date_points(data["purchaseDate"])
    points += calculate_time_points(data["purchaseTime"])

    return points


@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    data = request.json
    receipt_id = str(uuid.uuid4())
    points = calculate_points(data)
    receipts[receipt_id] = points
    return jsonify({"id": receipt_id})


@app.route('/receipts/<receipt_id>/points', methods=['GET'])
def get_points(receipt_id):
    if receipt_id in receipts:
        return jsonify({"points": receipts[receipt_id]})
    else:
        return jsonify({"error": "Receipt not found"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
