import uuid

from flask import Flask, request, jsonify
from utils import (
    validate_receipt,
    generate_receipt_hash,
    calculate_points,
)

app = Flask(__name__)

# In-memory storage for receipts and points
receipts = {}
receipt_hashes = {}


@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    data = request.json

    # Validate the receipt
    is_valid, error_message = validate_receipt(data)
    if not is_valid:
        app.logger.error(f"Invalid receipt: {error_message}")
        return jsonify({"error": error_message}), 400

    # Check if the receipt has already been processed
    receipt_hash = generate_receipt_hash(data)
    if receipt_hash in receipt_hashes:
        app.logger.info(
            f"Receipt already processed with ID: {receipt_hashes[receipt_hash]}")
        return jsonify({"id": receipt_hashes[receipt_hash]})

    # Process the valid receipt
    receipt_id = str(uuid.uuid4())
    points = calculate_points(data)

    # Store the receipt and points
    receipts[receipt_id] = points
    receipt_hashes[receipt_hash] = receipt_id

    app.logger.info(f"Stored receipt with ID: {receipt_id}")
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
