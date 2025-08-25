import os
from dotenv import load_dotenv
load_dotenv()
import requests

class TomTomClient:
    def __init__(self):
        self.api_key = os.getenv("TOMTOM_API_KEY")
        self.base_url = "https://api.tomtom.com/search/2/poiSearch"

    def search_pois(self, query, lat, lon, radius=10000, limit=20):
        url = f"{self.base_url}/{query}.json"
        params = {
            "key": self.api_key,
            "lat": lat,
            "lon": lon,
            "radius": radius,
            "limit": limit
        }
        print("Requesting:", url)
        print("Params:", params)
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        return resp.json().get("results", []) 