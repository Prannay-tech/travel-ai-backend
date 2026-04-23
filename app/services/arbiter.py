import asyncio
from typing import List
from app.services.providers.duffel_flight import DuffelProvider
from app.services.providers.serper_hotels import SerperHotelProvider
from app.core.providers import TrotterFlight, TrotterHotel

class ArbiterEngine:
    def __init__(self):
        # We can now add/remove providers here without breaking the core logic
        self.flight_providers = [DuffelProvider()]
        self.hotel_providers = [SerperHotelProvider()]

    async def find_best_hotel(self, city: str, check_in: str, check_out: str) -> List[TrotterHotel]:
        """Runs all hotel providers in parallel and consolidates results."""
        tasks = [p.search(city, check_in, check_out) for p in self.hotel_providers]
        results = await asyncio.gather(*tasks)
        
        # Flatten and deduplicate
        all_hotels = [hotel for sublist in results for hotel in sublist]
        return sorted(all_hotels, key=lambda x: x.rating, reverse=True)

    async def find_best_flight(self, origin: str, destination: str, date: str) -> List[TrotterFlight]:
        """Runs all flight providers in parallel."""
        tasks = [p.search(origin, destination, date) for p in self.flight_providers]
        results = await asyncio.gather(*tasks)
        
        all_flights = [flight for sublist in results for flight in sublist]
        return sorted(all_flights, key=lambda x: x.price)

arbiter = ArbiterEngine()
