import os
from dotenv import load_dotenv
load_dotenv()
from tomtom_client import TomTomClient

print("TOMTOM_API_KEY:", os.getenv("TOMTOM_API_KEY"))

tomtom = TomTomClient()

# Example: Search for museums in Paris
query = "museum"
lat = 48.8566
lon = 2.3522

pois = tomtom.search_pois(query, lat, lon)
print("TomTom POIs (Museums in Paris):")
for poi in pois:
    name = poi["poi"]["name"]
    address = poi["address"]["freeformAddress"]
    print(f"{name} - {address}") 