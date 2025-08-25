import os
from amadeus_client import AmadeusClient

amadeus = AmadeusClient()

# Example: Car rental at LAX airport for 2 days
params = {
    "pickupLocationCode": "LAX",
    "pickupDate": "2024-08-01T10:00:00",
    "returnDate": "2024-08-03T10:00:00"
}
cars = amadeus.get("/v1/shopping/car-rental-offers", params).get("data", [])
print("Car Rental Offers:")
for car in cars:
    print(car) 