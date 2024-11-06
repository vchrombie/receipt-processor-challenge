package main

import (
	"encoding/json"
	"fmt"
	"log"
	"math"
	"net/http"
	"regexp"
	"strconv"
	"strings"
	"time"

	"github.com/google/uuid"
)

type Receipt struct {
	Retailer     string `json:"retailer"`
	PurchaseDate string `json:"purchaseDate"`
	PurchaseTime string `json:"purchaseTime"`
	Total        string `json:"total"`
	Items        []Item `json:"items"`
}

type Item struct {
	ShortDescription string `json:"shortDescription"`
	Price            string `json:"price"`
}

// In-memory storage for receipts and points
var receipts = make(map[string]int)

// Calculate points for a receipt based on the rules
func CalculatePoints(receipt Receipt) int {
	points := 0

	points += pointsForRetailerName(receipt.Retailer)
	points += pointsForTotalAmount(receipt.Total)
	points += pointsForItemCount(len(receipt.Items))
	points += pointsForItemDescriptions(receipt.Items)
	points += pointsForPurchaseDate(receipt.PurchaseDate)
	points += pointsForPurchaseTime(receipt.PurchaseTime)

	return points
}

// Points for retailer name
// One point for every alphanumeric character in the retailer name
func pointsForRetailerName(retailer string) int {
	reg := regexp.MustCompile(`[a-zA-Z0-9]`)
	return len(reg.FindAllString(retailer, -1))
}

// Points for total amount
// 50 points if the total is a round dollar amount with no cents
// 25 points if the total is a multiple of `0.25`
func pointsForTotalAmount(total string) int {
	points := 0
	value, err := strconv.ParseFloat(total, 64)
	if err != nil {
		return points
	}

	if value == float64(int(value)) {
		points += 50
	}
	if math.Mod(value, 0.25) == 0 {
		points += 25
	}
	return points
}

// Points for item count
// 5 points for every two items on the receipt
func pointsForItemCount(itemCount int) int {
	return (itemCount / 2) * 5
}

// Points for item descriptions
// If the trimmed length of the item description is a multiple of 3,
// multiply the price by `0.2` and round up to the nearest integer
func pointsForItemDescriptions(items []Item) int {
	points := 0
	for _, item := range items {
		description := strings.TrimSpace(item.ShortDescription)
		if len(description)%3 == 0 {
			price, err := strconv.ParseFloat(item.Price, 64)
			if err == nil {
				points += int(math.Ceil(price * 0.2))
			}
		}
	}
	return points
}

// Points for purchase date
// 6 points if the day in the purchase date is odd
func pointsForPurchaseDate(purchaseDate string) int {
	date, err := time.Parse("2006-01-02", purchaseDate)
	if err != nil || date.Day()%2 == 0 {
		return 0
	}
	return 6
}

// Points for purchase time
// 10 points if the time of purchase is after 2:00pm and before 4:00pm
func pointsForPurchaseTime(purchaseTime string) int {
	t, err := time.Parse("15:04", purchaseTime)
	if err != nil || t.Hour() < 14 || t.Hour() >= 16 {
		return 0
	}
	return 10
}

func ProcessReceipt(w http.ResponseWriter, r *http.Request) {
	/*
		POST /receipts/process
		Process a receipt, calculates points, generates an ID, and stores the points
	*/

	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var receipt Receipt
	if err := json.NewDecoder(r.Body).Decode(&receipt); err != nil {
		http.Error(w, "Invalid request payload", http.StatusBadRequest)
		return
	}

	id := uuid.New().String()
	points := CalculatePoints(receipt)

	receipts[id] = points

	log.Printf("Stored receipt with ID: %s, Points: %d", id, points)

	response := map[string]string{"id": id}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func GetPoints(w http.ResponseWriter, r *http.Request) {
	/*
		GET /receipts/{id}
		Retrieve the points for a receipt with the given ID
	*/

	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	pathParts := strings.Split(r.URL.Path, "/")
	if len(pathParts) < 3 {
		http.Error(w, "Invalid URL path", http.StatusBadRequest)
		return
	}
	id := pathParts[2]
	log.Printf("Retrieving points for ID: %s", id)

	points, exists := receipts[id]
	if !exists {
		log.Printf("Receipt not found for ID: %s", id)
		http.Error(w, "Receipt not found", http.StatusNotFound)
		return
	}

	response := map[string]int{"points": points}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func main() {
	// Route setup
	http.HandleFunc("/receipts/process", ProcessReceipt)
	http.HandleFunc("/receipts/", GetPoints)

	// Start the server
	fmt.Println("Starting server on port 8080...")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatalf("Server failed to start: %v", err)
	}
}
