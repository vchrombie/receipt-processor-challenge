import uuid

from flask import Flask, request, jsonify
from utils import (
    calculate_points,
    validate_receipt,
)

app = Flask(__name__)

# In-memory storage for receipts and points
receipts = {}


@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    data = request.json

    # Validate the receipt
    is_valid, error_message = validate_receipt(data)
    if not is_valid:
        app.logger.error(f"Invalid receipt: {error_message}")
        return jsonify({"error": error_message}), 400

    # Process the valid receipt
    receipt_id = str(uuid.uuid4())
    points = calculate_points(data)
    receipts[receipt_id] = points
    app.logger.info(f"Stored receipt with ID: {receipt_id}, Points: {points}")
    return jsonify({"id": receipt_id})


@app.route('/receipts/<receipt_id>/points', methods=['GET'])
def get_points(receipt_id):
    if receipt_id in receipts:
        app.logger.info(f"Retrieving points for ID: {receipt_id}")
        return jsonify({"points": receipts[receipt_id]})
    else:
        app.logger.error(f"Receipt not found for ID: {receipt_id}")
        return jsonify({"error": "Receipt not found"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
