import os
from amadeus_client import AmadeusClient

amadeus = AmadeusClient()

# Example: Search hotels in Paris (city code PAR) for 2 nights
params = {
    "cityCode": "PAR",
    "checkInDate": "2024-08-01",
    "checkOutDate": "2024-08-03",
    "adults": 1,
    "roomQuantity": 1,
    "radius": 5,
    "radiusUnit": "KM",
    "paymentPolicy": "NONE",
    "includeClosed": False,
    "bestRateOnly": True,
    "view": "FULL",
    "sort": "PRICE"
}
hotels = amadeus.get("/v2/shopping/hotel-offers", params).get("data", [])
print("Hotel Offers:")
for hotel in hotels:
    print(hotel) 