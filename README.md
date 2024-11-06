# receipt-processor-challenge

Fetch Rewards Receipt Processor Challenge

---

## Instructions

```bash
$ git clone https://github.com/vchrombie/receipt-processor-challenge
$ cd receipt-processor-challenge

$ docker build -t vchrombie-receipt-processor .
$ docker run -p 5000:5000 vchrombie-receipt-processor

$ curl -X POST http://localhost:5000/receipts/process \
    -H "Content-Type: application/json" \
    -d @examples/receipt-1.json
{"id":"785a61d2-4da6-4e6d-9572-198086bff003"}

$ curl -X GET http://localhost:5000/receipts/2ee47ba9-ac23-4fdc-96be-d3d8ea968899/points
{"points":28}
```

## Endpoints

- POST `/receipts/process`: Accepts a receipt JSON, calculates points, and
  returns a unique receipt ID.
- GET `/receipts/{id}/points`: Retrieves the points for the receipt with the
  specified ID.

## Rules for Points Calculation

- Retailer Name
  - One point for every alphanumeric character in the retailer name.
- Total Amount
  - 50 points if the total is a round dollar amount with no cents.
  - 25 points if the total is a multiple of `0.25`.
- Item Count
  - 5 points for every two items on the receipt.
- Item Description Length
  - If the trimmed length of the item description is a multiple of 3, multiply
    the price by `0.2` and round up to the nearest integer. The result is the
    number of points earned.
- Purchase Date and Time
  - 6 points if the day in the purchase date is odd.
  - 10 points if the time of purchase is after 2:00pm and before 4:00pm.
