import requests
import os
import time

class AmadeusClient:
    def __init__(self):
        self.client_id = os.getenv("AMADEUS_CLIENT_ID")
        self.client_secret = os.getenv("AMADEUS_CLIENT_SECRET")
        self.base_url = "https://test.api.amadeus.com"
        self.token = None
        self.token_expiry = 0

    def get_token(self):
        if self.token and time.time() < self.token_expiry:
            return self.token
        resp = requests.post(
            f"{self.base_url}/v1/security/oauth2/token",
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        self.token = data["access_token"]
        self.token_expiry = time.time() + int(data["expires_in"]) - 60
        return self.token

    def get(self, endpoint, params=None):
        token = self.get_token()
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(f"{self.base_url}{endpoint}", headers=headers, params=params)
        resp.raise_for_status()
        return resp.json()

    def get_pois(self, latitude, longitude, radius_km=20):
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "radius": radius_km,
        }
        return self.get("/v1/reference-data/locations/pois", params).get("data", [])

    def get_flights(self, origin, destination, departure_date, adults=1):
        params = {
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": departure_date,
            "adults": adults,
            "currencyCode": "USD",
            "max": 5,
        }
        return self.get("/v2/shopping/flight-offers", params).get("data", []) 