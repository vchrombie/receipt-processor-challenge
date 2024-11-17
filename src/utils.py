import math

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
