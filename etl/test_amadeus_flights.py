import os
from amadeus_client import AmadeusClient

amadeus = AmadeusClient()

# Example: JFK (New York) to LHR (London) on a future date
origin = "JFK"
destination = "LHR"
departure_date = "2024-08-01"

flights = amadeus.get_flights(origin, destination, departure_date)
print("Flight Offers:")
for offer in flights:
    print(offer) 