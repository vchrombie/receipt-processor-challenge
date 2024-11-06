package main

import (
	"testing"
)

func TestPointsForRetailerName(t *testing.T) {
	tests := []struct {
		name     string
		retailer string
		expected int
	}{
		{"All alphanumeric", "Walgreens", 9},
		{"Non-alphanumeric characters", "7-Eleven", 7},
		{"Empty retailer name", "", 0},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			points := pointsForRetailerName(tt.retailer)
			if points != tt.expected {
				t.Errorf("Expected %d points, got %d", tt.expected, points)
			}
		})
	}
}

func TestPointsForTotalAmount(t *testing.T) {
	tests := []struct {
		name     string
		total    string
		expected int
	}{
		{"Multiple of 0.25", "9.25", 25},
		{"Round dollar amount", "10.00", 75},
		{"Neither round nor multiple of 0.25", "9.99", 0},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			points := pointsForTotalAmount(tt.total)
			if points != tt.expected {
				t.Errorf("Expected %d points, got %d", tt.expected, points)
			}
		})
	}
}

func TestPointsForItemCount(t *testing.T) {
	tests := []struct {
		name      string
		itemCount int
		expected  int
	}{
		{"Four items", 4, 10},
		{"Five items", 5, 10},
		{"One item", 1, 0},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			points := pointsForItemCount(tt.itemCount)
			if points != tt.expected {
				t.Errorf("Expected %d points, got %d", tt.expected, points)
			}
		})
	}
}

func TestPointsForItemDescriptions(t *testing.T) {
	tests := []struct {
		name     string
		items    []Item
		expected int
	}{
		{
			"Description length multiple of 3",
			[]Item{{ShortDescription: "Dasani", Price: "3.00"}},
			1, // 3.00 * 0.2 = 0.6, rounded up = 1
		},
		{
			"Description length not multiple of 3",
			[]Item{{ShortDescription: "Pepsi", Price: "2.50"}},
			0,
		},
		{
			"Multiple items with mixed description lengths",
			[]Item{
				{ShortDescription: "Dasani", Price: "3.00"},
				{ShortDescription: "Pepsi", Price: "5.00"},
			},
			1, // 1 point for "Dasani", 0 point for "Pepsi"
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			points := pointsForItemDescriptions(tt.items)
			if points != tt.expected {
				t.Errorf("Expected %d points, got %d", tt.expected, points)
			}
		})
	}
}

func TestPointsForPurchaseDate(t *testing.T) {
	tests := []struct {
		name         string
		purchaseDate string
		expected     int
	}{
		{"Odd day", "2022-01-01", 6},
		{"Even day", "2022-01-02", 0},
		{"Invalid date", "invalid-date", 0},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			points := pointsForPurchaseDate(tt.purchaseDate)
			if points != tt.expected {
				t.Errorf("Expected %d points, got %d", tt.expected, points)
			}
		})
	}
}

func TestPointsForPurchaseTime(t *testing.T) {
	tests := []struct {
		name         string
		purchaseTime string
		expected     int
	}{
		{"Between 2:00pm and 4:00pm", "15:00", 10},
		{"At 1:00pm", "13:00", 0},
		{"At 2:00pm", "14:00", 10},
		{"At 4:00pm", "16:00", 0},
		{"Invalid time", "invalid-time", 0},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			points := pointsForPurchaseTime(tt.purchaseTime)
			if points != tt.expected {
				t.Errorf("Expected %d points, got %d", tt.expected, points)
			}
		})
	}
}
