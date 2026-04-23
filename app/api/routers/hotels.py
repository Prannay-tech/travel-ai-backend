from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from app.models.api import HotelSearch
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# You can integrate your chosen hotel service here later (e.g. Hotelbeds/Amadeus)
# from app.services.hotel_service import HotelbedsService

@router.post("/search", response_model=List[Dict[str, Any]])
async def search_hotels(search: HotelSearch):
    """Search for hotels using the structured API model."""
    try:
        # Placeholder for real integration
        # hotels = await hotel_service.search(destination=search.destination, check_in=search.check_in...)
        
        # Temporary mock to keep the system running
        return [
            {
                "id": "hotel_1",
                "name": f"Grand Hotel in {search.destination}",
                "rating": 4.8,
                "price_per_night": {"USD": 250, "EUR": 210, "GBP": 180},
                "amenities": ["WiFi", "Pool", "Spa", "Restaurant"],
                "location": "City Center",
                "image": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800",
                "booking_link": "https://www.hotels.com"
            }
        ]
    except Exception as e:
        logger.error(f"Error serving hotel search: {e}")
        raise HTTPException(status_code=500, detail="Internal server error fetching hotels")
