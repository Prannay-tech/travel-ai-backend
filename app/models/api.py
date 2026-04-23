from pydantic import BaseModel
from typing import List, Dict, Optional

class ChatMessage(BaseModel):
    message: str
    conversation_history: Optional[List[Dict[str, str]]] = None
    is_business: Optional[bool] = False
    metadata: Optional[Dict[str, Any]] = None
    session_id: Optional[str] = None

class ConversationState(BaseModel):
    session_id: str
    current_step: str = "welcome"
    collected_data: Dict[str, str] = {}
    recommendations: Optional[List[Dict]] = None
    selected_destination: Optional[Dict] = None
    booking_type: Optional[str] = None  # "flights" or "hotels"

class TravelPreferences(BaseModel):
    budget_per_person: str
    people_count: str
    travel_from: str
    travel_type: str
    destination_type: str
    travel_dates: str
    currency: str = "USD"
    additional_preferences: str = ""

class FlightSearch(BaseModel):
    origin: str
    destination: str
    departure_date: str
    return_date: Optional[str] = None
    passengers: int = 1

class HotelSearch(BaseModel):
    destination: str
    check_in: str
    check_out: str
    guests: int = 1
    rooms: int = 1

class ActivitySearch(BaseModel):
    destination: str
    date: str
    participants: int = 1

class RegisterRequest(BaseModel):
    name: Optional[str] = None
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    token: str
    user: Dict[str, str]
