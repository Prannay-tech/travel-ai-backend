import httpx
import logging
from typing import List
from app.core.providers import BaseHotelProvider, TrotterHotel
from app.core.config import settings

logger = logging.getLogger(__name__)

class SerperHotelProvider(BaseHotelProvider):
    """
    Adapter for Google Hotels via Serper.
    """

    def __init__(self):
        self.api_key = settings.SERPER_API_KEY
        self.base_url = "https://google.serper.dev/hotels"

    async def search(self, city: str, check_in: str, check_out: str) -> List[TrotterHotel]:
        if not self.api_key:
            return []

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.base_url,
                    headers={"X-API-KEY": self.api_key, "Content-Type": "application/json"},
                    json={"q": f"Hotels in {city}", "checkIn": check_in, "checkOut": check_out}
                )
                response.raise_for_status()
                data = response.json().get("hotels", [])

                results = []
                for h in data:
                    # MAP GOOGLE -> TROTTER
                    results.append(TrotterHotel(
                        provider_id=f"google_{h.get('cid')}",
                        name=h.get("title"),
                        price=float(h.get("price", "0").replace('$', '').replace(',', '')),
                        currency="USD",
                        rating=float(h.get("rating", 4.0)),
                        image_url=h.get("thumbnail", ""),
                        address=h.get("address", city),
                        amenities=h.get("amenities", [])
                    ))
                return results
            except Exception as e:
                logger.error(f"Google Hotels Error: {str(e)}")
                return []
