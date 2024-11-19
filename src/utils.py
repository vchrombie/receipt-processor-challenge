import re
import math
import hashlib

from datetime import datetime


def calculate_retailer_points(retailer_name):
    """
    Calculate points based on the retailer name.

    - One point for every alphanumeric character in the retailer name.
    """
    return sum(c.isalnum() for c in retailer_name)


def calculate_total_amount_points(total):
    """
    Calculate points based on total amount.

    - 50 points if the total is a round dollar amount with no cents.
    - 25 points if the total is a multiple of `0.25`.
    """
    points = 0
    total = float(total)

    # 50 points if the total is a round dollar amount
    if total.is_integer():
        points += 50

    # 25 points if the total is a multiple of 0.25
    if total % 0.25 == 0:
        points += 25

    return points


def calculate_item_count_points(item_count):
    """
    Calculate points based on the item count.

    - 5 points for every two items.
    """
    return (item_count // 2) * 5


def calculate_item_description_points(items):
    """
    Calculate points based on item description length.

    - If the trimmed length of the item description is a multiple of 3, multiply
    the price by `0.2` and round up to the nearest integer. The result is the
    number of points earned.
    """
    points = 0
    for item in items:
        description_length = len(item["shortDescription"].strip())

        # Check if length is a multiple of 3
        if description_length % 3 == 0:
            item_price = float(item["price"])
            points += math.ceil(item_price * 0.2)

    return points


def calculate_date_points(purchase_date):
    """
    Calculate points based on the purchase date's day.

    - 6 points if the day in the purchase date is odd.    
    """
    day = datetime.strptime(purchase_date, "%Y-%m-%d").day
    return 6 if day % 2 == 1 else 0


def calculate_time_points(purchase_time):
    """
    Calculate points based on the purchase date's time.

    - 10 points if the time of purchase is after 2:00pm and before 4:00pm.
    """
    time = datetime.strptime(purchase_time, "%H:%M").time()
    afternoon_start = datetime.strptime("14:00", "%H:%M").time()
    afternoon_end = datetime.strptime("16:00", "%H:%M").time()

    if afternoon_start <= time < afternoon_end:
        return 10
    return 0


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


def validate_receipt_retailer(retailer_name):
    """
    Validate the retailer field in the receipt data.
    """
    if not re.match(r"^[\w\s\-&]+$", retailer_name):
        return False, f"Invalid retailer format"

    return True, ""


def validate_receipt_purchase_date(purchase_date):
    """
    Validate the purchaseDate field in the receipt data.
    """
    try:
        datetime.strptime(purchase_date, "%Y-%m-%d")
    except ValueError:
        return False, "Invalid purchaseDate format"

    return True, ""


def validate_receipt_purchase_time(purchase_time):
    """
    Validate the purchaseTime field in the receipt data.
    """
    try:
        datetime.strptime(purchase_time, "%H:%M")
    except ValueError:
        return False, "Invalid purchaseTime format"

    return True, ""


def validate_receipt_total(total):
    """
    Validate the total field in the receipt data.
    """
    if not re.match(r"^\d+\.\d{2}$", total):
        return False, "Invalid total format"

    return True, ""


def validate_receipt_items(items):
    """
    Validate the items field in the receipt data.
    """
    if not isinstance(items, list) or len(items) == 0:
        return False, "Items must be a non-empty list"

    for item in items:
        if not isinstance(item, dict):
            return False, "Each item must be a dictionary"

        if "shortDescription" not in item or "price" not in item:
            return False, "Each item must have shortDescription and price"

        # Validate shortDescription
        if not re.match(r"^[\w\s\-]+$", item["shortDescription"]):
            return False, f"Invalid shortDescription format in items"

        # Validate price
        if not re.match(r"^\d+\.\d{2}$", item["price"]):
            return False, "Invalid price format in items"

    return True, ""


def validate_receipt(data):
    """
    Validate the receipt data against the required schema.
    """
    required_fields = ["retailer", "purchaseDate",
                       "purchaseTime", "items", "total"]
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"

    validations = [
        validate_receipt_retailer(data["retailer"]),
        validate_receipt_purchase_date(data["purchaseDate"]),
        validate_receipt_purchase_time(data["purchaseTime"]),
        validate_receipt_total(data["total"]),
        validate_receipt_items(data["items"]),
    ]

    for is_valid, error_message in validations:
        if not is_valid:
            return is_valid, error_message

    return True, ""


def generate_receipt_hash(data):
    """
    Generate a hash for the receipt data.
    """
    receipt_string = f"{data['retailer']}_{data['purchaseDate']}_{data['purchaseTime']}_{data['total']}"
    item_strings = [
        f"{item['shortDescription']}_{item['price']}" for item in data["items"]
    ]
    receipt_string += "_".join(item_strings)
    return hashlib.sha256(receipt_string.encode('utf-8')).hexdigest()
