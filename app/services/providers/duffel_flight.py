import logging
from typing import List
from duffel_api import Duffel
from app.core.providers import BaseFlightProvider, TrotterFlight
from app.core.config import settings

logger = logging.getLogger(__name__)

class DuffelProvider(BaseFlightProvider):
    """
    Adapter for the Duffel Flight API.
    """

    def __init__(self):
        self.client = Duffel(access_token=settings.DUFFEL_ACCESS_TOKEN)

    async def search(self, origin: str, destination: str, date: str) -> List[TrotterFlight]:
        try:
            # Note: simplified for the adapter pattern proof
            slices = [{"origin": origin, "destination": destination, "departure_date": date}]
            offer_request = self.client.offer_requests.create().slices(slices).passengers([{"type": "adult"}]).execute()
            offers = self.client.offers.list(offer_request.id)

            results = []
            for offer in offers:
                # MAP DUFFEL -> TROTTER
                results.append(TrotterFlight(
                    provider_id=f"duffel_{offer.id}",
                    airline=offer.owner.name,
                    airline_logo=offer.owner.logo_symbol_url,
                    price=float(offer.total_amount),
                    currency=offer.total_currency,
                    departure_time=offer.slices[0].segments[0].departing_at,
                    arrival_time=offer.slices[0].segments[-1].arriving_at,
                    origin=origin,
                    destination=destination
                ))
            return results
        except Exception as e:
            logger.error(f"Duffel Error: {str(e)}")
            return []

    async def book(self, offer_id: str, passengers: List[Dict]) -> Dict:
        """
        Finalizes an order for a specific offer via Duffel.
        """
        try:
            order = self.client.orders.create() \
                .selected_offers([offer_id]) \
                .passengers(passengers) \
                .type("instant") \
                .execute()
            
            return {
                "status": "success",
                "vendor_pnr": order.booking_reference,
                "raw_data": order.__dict__
            }
        except Exception as e:
            logger.error(f"Duffel Booking Error: {str(e)}")
            return {"status": "error", "message": str(e)}
