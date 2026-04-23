import httpx
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class DuffelService:
    """Service to interact with Duffel API for real-time flight data."""
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://api.duffel.com/air"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Duffel-Version": "v1",
            "Content-Type": "application/json"
        }

    async def search_flights(self, origin: str, destination: str, date: str, passengers: int = 1) -> List[Dict[str, Any]]:
        """
        Creates an Offer Request in Duffel and returns flight offers.
        """
        if not self.api_token:
            logger.warning("No Duffel API Key provided.")
            return []

        payload = {
            "data": {
                "slices": [
                    {
                        "origin": origin,
                        "destination": destination,
                        "departure_date": date
                    }
                ],
                "passengers": [{"type": "adult"} for _ in range(passengers)],
                "return_offers": True
            }
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/offer_requests",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code != 201:
                logger.error(f"Duffel API Error: {response.text}")
                return []
            
            data = response.json()["data"]
            offers = data.get("offers", [])
            
            # Parse down to a cleaner format for the LLM
            parsed_offers = []
            for offer in offers[:5]: # Top 5 to not overflow LLM context
                parsed_offers.append({
                    "id": offer["id"],
                    "total_amount": offer["total_amount"],
                    "total_currency": offer["total_currency"],
                    "owner": offer["owner"]["name"],
                    "duration": offer["slices"][0]["duration"]
                })
                
            return parsed_offers
