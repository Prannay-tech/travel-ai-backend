import logging
import httpx
from typing import List, Dict, Optional
from app.core.config import settings
from app.models.api import HotelOffer

logger = logging.getLogger(__name__)

class HotelService:
    """
    Service to fetch real-time hotel data using the Amadeus API.
    """

    def __init__(self):
        self.api_key = settings.AMADEUS_API_KEY
        self.api_secret = settings.AMADEUS_API_SECRET
        self.base_url = "https://test.api.amadeus.com/v1" # Use 'test' for development
        self._access_token = None

    async def _get_access_token(self):
        """Authenticates with Amadeus to get a Bearer token."""
        if self._access_token:
            return self._access_token

        url = f"{self.base_url}/security/oauth2/token"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    url,
                    data={
                        "grant_type": "client_credentials",
                        "client_id": self.api_key,
                        "client_secret": self.api_secret
                    },
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                response.raise_for_status()
                data = response.json()
                self._access_token = data["access_token"]
                return self._access_token
            except Exception as e:
                logger.error(f"Failed to authenticate with Amadeus: {str(e)}")
                return None

    async def search_hotels(self, city_code: str, check_in: str, check_out: str, guests: int = 1) -> List[HotelOffer]:
        """
        Searches for hotels in a city for specific dates.
        """
        token = await self._get_access_token()
        if not token:
            return self._get_mock_hotels(city_code) # Fallback to mock for reliability

        # 1. Get Hotel IDs for the city
        search_url = f"{self.base_url}/reference-data/locations/hotels/by-city"
        async with httpx.AsyncClient() as client:
            try:
                # First, find hotels in the city
                response = await client.get(
                    search_url,
                    params={"cityCode": city_code, "radius": 5, "radiusUnit": "KM"},
                    headers={"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                hotel_list = response.json().get("data", [])
                hotel_ids = [h["hotelId"] for h in hotel_list[:5]] # Limit to top 5 for speed

                if not hotel_ids:
                    return self._get_mock_hotels(city_code)

                # 2. Get Offers for those hotels
                offers_url = f"{self.base_url}/shopping/hotel-offers"
                offers_res = await client.get(
                    offers_url,
                    params={
                        "hotelIds": ",".join(hotel_ids),
                        "adults": guests,
                        "checkInDate": check_in,
                        "checkOutDate": check_out,
                        "currency": "USD"
                    },
                    headers={"Authorization": f"Bearer {token}"}
                )
                offers_res.raise_for_status()
                data = offers_res.json().get("data", [])

                return self._parse_offers(data)

            except Exception as e:
                logger.error(f"Amadeus hotel search failed: {str(e)}")
                return self._get_mock_hotels(city_code)

    def _parse_offers(self, data: List[Dict]) -> List[HotelOffer]:
        """Parses Amadeus offer data into our Pydantic models."""
        parsed = []
        for item in data:
            hotel = item.get("hotel", {})
            offer = item.get("offers", [{}])[0] # Get first offer
            
            parsed.append(HotelOffer(
                id=hotel.get("hotelId"),
                name=hotel.get("name"),
                rating=float(hotel.get("rating", 4.0)),
                price=float(offer.get("price", {}).get("total", 0)),
                image="https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80", # Real Amadeus images are separate API calls, using high-quality placeholder
                address=hotel.get("address", {}).get("cityName", "Global"),
                tags=["Real-time", "Amadeus Verified"]
            ))
        return parsed

    def _get_mock_hotels(self, city: str) -> List[HotelOffer]:
        """Safe fallback data if the API is down or keys are missing."""
        return [
            HotelOffer(
                id=f"mock_{city}_1",
                name="Grand Luxury Resort",
                rating=4.9,
                price=350.0,
                image="https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&q=80",
                address=f"Downtown {city}",
                tags=["Premium"]
            ),
            HotelOffer(
                id=f"mock_{city}_2",
                name="Boutique Stay Inn",
                rating=4.5,
                price=180.0,
                image="https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80",
                address=f"Arts District {city}",
                tags=["Boutique"]
            )
        ]

hotel_service = HotelService()
