from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from pydantic import BaseModel

# ─── STANDARD TROTTER SCHEMAS ────────────────────────────────
# These are the only objects the AI brain will ever see.
# No matter which vendor we use, they must return these formats.

class TrotterFlight(BaseModel):
    provider_id: str
    airline: str
    airline_logo: str
    price: float
    currency: str
    departure_time: str
    arrival_time: str
    origin: str
    destination: str
    booking_url: Optional[str] = None

class TrotterHotel(BaseModel):
    provider_id: str
    name: str
    price: float
    currency: str
    rating: float
    image_url: str
    address: str
    amenities: List[str]
    booking_url: Optional[str] = None

class TrotterActivity(BaseModel):
    id: str
    name: str
    description: str
    location: str
    neighborhood: str
    best_time: str # 'Morning', 'Afternoon', 'Sunset', 'Evening'
    intensity: str # 'Low', 'Medium', 'High'
    age_suitability: str # 'All', 'Adults', 'Families'
    coordinates: Optional[Dict[str, float]] = None

# ─── BASE PROVIDER INTERFACES ────────────────────────────────

class BaseFlightProvider(ABC):
    @abstractmethod
    async def search(self, origin: str, destination: str, date: str) -> List[TrotterFlight]:
        pass

    @abstractmethod
    async def book(self, offer_id: str, passengers: List[Dict]) -> Dict:
        """Executes a real flight booking/ticketing."""
        pass

class BaseHotelProvider(ABC):
    @abstractmethod
    async def search(self, city: str, check_in: str, check_out: str) -> List[TrotterHotel]:
        pass

    @abstractmethod
    async def book(self, offer_id: str, guests: List[Dict]) -> Dict:
        """Executes a real hotel reservation."""
        pass
