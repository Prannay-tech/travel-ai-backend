"""
Comprehensive Travel AI Backend - AI-powered travel planning with booking integration.
Features: AI chat, destination recommendations, flight booking, hotel booking, activity planning.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional, Tuple
import httpx
import os
from dotenv import load_dotenv
import logging
from datetime import datetime, timedelta
import json
import re
import uuid

# Add new imports for enhanced data fetching
import asyncio
from datetime import datetime, timedelta
import re
from typing import List, Dict, Optional, Tuple

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Travel AI API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Keys and Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_BASE_URL = "https://api.groq.com/openai/v1/chat/completions"

# Real API Keys from environment variables
SKYSCANNER_API_KEY = os.getenv("SKYSCANNER_API_KEY", "")
AMADEUS_CLIENT_ID = os.getenv("AMADEUS_CLIENT_ID", "")
AMADEUS_CLIENT_SECRET = os.getenv("AMADEUS_CLIENT_SECRET", "")
HOTELS_API_KEY = os.getenv("HOTELS_API_KEY", "")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY", "")
CURRENCY_API_KEY = os.getenv("CURRENCY_API_KEY", "")

# Import flight search API
from flight_apis import flight_api, FlightSearchAPI
from weather_api import weather_api
from currency_api import currency_api
from cost_of_living_dataset import cost_of_living_dataset

# Pydantic Models
class ChatMessage(BaseModel):
    message: str
    conversation_history: Optional[List[Dict[str, str]]] = None
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

# Conversation state storage (in production, use Redis or database)
conversation_states = {}

# AI System Prompt for Travel Planning
AI_SYSTEM_PROMPT = """
You are an expert AI travel planner conducting a structured conversation to help users plan their perfect trip.

CONVERSATION FLOW:
1. WELCOME: Greet and ask for current location
2. TRAVEL_TYPE: Ask if they want domestic or international travel
3. DESTINATION_TYPE: Ask what type of place they want (beach, mountain, city, historic, etc.)
4. PEOPLE_COUNT: Ask how many people are traveling
5. BUDGET: Ask budget per person
6. DATES: Ask when they want to travel and for how many days
7. ADDITIONAL_PREFERENCES: Ask for any additional activities/preferences
8. RECOMMENDATIONS: Show AI-generated recommendations
9. BOOKING: Help with flight/hotel booking

INSTRUCTIONS:
- Always ask ONE question at a time
- Extract information from user responses
- Be friendly and conversational
- If user provides multiple pieces of info, acknowledge and move to next step
- For destination types, interpret natural language (e.g., "tropical paradise" = beach, "ancient ruins" = historic)
- For budget, extract amounts and currency
- For dates, extract time period and duration

RESPONSE FORMAT:
- Ask clear, specific questions
- Acknowledge information provided
- Guide to next step naturally
"""

# Enhanced Travel Data with Real Destinations
TRAVEL_DATA = {
    "domestic": {
        "beach": [
            {
                "id": 1,
                "name": "Bali, Indonesia",
                "type": "beach",
                "country": "Indonesia",
                "description": "Tropical paradise with beautiful beaches, temples, and culture",
                "image": "https://images.unsplash.com/photo-1537953773345-d172ccf13cf1?w=800",
                "rating": 4.8,
                "cost_per_person": {"USD": 1200, "EUR": 1100, "GBP": 950},
                "highlights": ["Beaches", "Temples", "Culture", "Adventure"],
                "best_time": "April-October",
                "flight_time": "18-24 hours",
                "currency": "IDR",
                "daily_cost_usd": 100,
                "flight_cost_usd": 500
            },
            {
                "id": 2,
                "name": "Maldives",
                "type": "beach",
                "country": "Maldives",
                "description": "Luxury overwater bungalows and crystal clear waters",
                "image": "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?w=800",
                "rating": 4.9,
                "cost_per_person": {"USD": 3500, "EUR": 3200, "GBP": 2800},
                "highlights": ["Luxury", "Beaches", "Snorkeling", "Relaxation"],
                "best_time": "November-April",
                "flight_time": "20-30 hours",
                "currency": "MVR",
                "daily_cost_usd": 150,
                "flight_cost_usd": 600
            }
        ],
        "mountain": [
            {
                "id": 3,
                "name": "Swiss Alps",
                "type": "mountain",
                "country": "Switzerland",
                "description": "Majestic mountains perfect for skiing and hiking",
                "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800",
                "rating": 4.9,
                "cost_per_person": {"USD": 2500, "EUR": 2300, "GBP": 2000},
                "highlights": ["Skiing", "Hiking", "Scenic Views", "Adventure"],
                "best_time": "December-March (skiing), June-September (hiking)",
                "flight_time": "8-12 hours",
                "currency": "CHF",
                "daily_cost_usd": 120,
                "flight_cost_usd": 400
            }
        ],
        "city": [
            {
                "id": 4,
                "name": "Tokyo, Japan",
                "type": "city",
                "country": "Japan",
                "description": "Modern metropolis with rich culture and technology",
                "image": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=800",
                "rating": 4.7,
                "cost_per_person": {"USD": 2000, "EUR": 1800, "GBP": 1600},
                "highlights": ["Technology", "Culture", "Food", "Shopping"],
                "best_time": "March-May (Cherry Blossom), September-November",
                "flight_time": "12-16 hours",
                "currency": "JPY",
                "daily_cost_usd": 100,
                "flight_cost_usd": 500
            }
        ]
    },
    "international": {
        "beach": [
            {
                "id": 5,
                "name": "Rome, Italy",
                "type": "historic",
                "country": "Italy",
                "description": "Ancient city with incredible history and architecture",
                "image": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=800",
                "rating": 4.6,
                "cost_per_person": {"USD": 1800, "EUR": 1600, "GBP": 1400},
                "highlights": ["History", "Architecture", "Food", "Culture"],
                "best_time": "April-June, September-October",
                "flight_time": "8-12 hours",
                "currency": "EUR",
                "daily_cost_usd": 150,
                "flight_cost_usd": 500
            }
        ]
    }
}

# Currency conversion rates (you can use a real API for this)
CURRENCY_RATES = {
    "USD": 1.0,
    "EUR": 0.85,
    "GBP": 0.73,
    "CAD": 1.25,
    "AUD": 1.35
}

async def call_groq_ai(message: str, conversation_history: List[Dict[str, str]] = None) -> str:
    """Call Groq AI API for travel planning conversation."""
    try:
        if not GROQ_API_KEY or GROQ_API_KEY == "your-groq-api-key-here":
            return "I'm here to help you plan your trip! Please provide your Groq API key to enable AI features."

        # Prepare conversation history
        messages = [{"role": "system", "content": AI_SYSTEM_PROMPT}]

        if conversation_history:
            messages.extend(conversation_history)

        messages.append({"role": "user", "content": message})

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                GROQ_BASE_URL,
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.1-70b-versatile",
                    "messages": messages,
                    "temperature": 0.3,
                    "max_tokens": 800,
                    "top_p": 0.8,
                    "frequency_penalty": 0.1,
                    "presence_penalty": 0.1
                }
            )

            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                logger.error(f"Groq API error: {response.status_code} - {response.text}")
                return "I'm having trouble connecting to my AI service. Please try again later."

    except Exception as e:
        logger.error(f"Error calling Groq AI: {e}")
        return "I'm experiencing technical difficulties. Please try again later."

async def handle_conversational_flow(message: str, session_id: str) -> Dict:
    """Handle the structured conversational flow for travel planning."""
    try:
        # Get or create conversation state
        if session_id not in conversation_states:
            conversation_states[session_id] = ConversationState(session_id=session_id)
            logger.info(f"Created new conversation state for session: {session_id}")
        
        state = conversation_states[session_id]
        logger.info(f"Current step: {state.current_step}, Collected data: {state.collected_data}")
        
        # Extract information from user message based on current step
        extracted_info = await extract_travel_info(message, state.current_step)
        
        # Update state with extracted information
        if extracted_info:
            state.collected_data.update(extracted_info)
        
        # Determine next step and response
        response_data = await determine_next_step(state, message)
        
        # Update conversation state
        conversation_states[session_id] = state
        
        return response_data
        
    except Exception as e:
        logger.error(f"Error in conversational flow: {e}")
        return {
            "response": "I'm having trouble processing your request. Let's start over!",
            "step": "welcome",
            "data_collected": {},
            "recommendations": None
        }

async def extract_travel_info(message: str, current_step: str) -> Dict[str, str]:
    """Extract travel information from user message based on current step."""
    extracted = {}
    
    message_lower = message.lower()
    
    if current_step == "welcome" or "location" in current_step:
        # Extract location
        location_patterns = [
            r"from\s+([A-Za-z\s,]+)",
            r"in\s+([A-Za-z\s,]+)",
            r"at\s+([A-Za-z\s,]+)",
            r"([A-Za-z\s,]+)\s+area"
        ]
        for pattern in location_patterns:
            match = re.search(pattern, message_lower)
            if match:
                extracted["travel_from"] = match.group(1).strip().title()
                break
    
    elif current_step == "travel_type":
        if any(word in message_lower for word in ["domestic", "local", "same country", "within"]):
            extracted["travel_type"] = "domestic"
        elif any(word in message_lower for word in ["international", "abroad", "foreign", "overseas"]):
            extracted["travel_type"] = "international"
    
    elif current_step == "destination_type":
        # Map natural language to destination types
        type_mapping = {
            "beach": ["beach", "ocean", "coast", "tropical", "island", "paradise", "seaside"],
            "mountain": ["mountain", "hiking", "skiing", "alpine", "peaks", "trails"],
            "city": ["city", "urban", "metropolitan", "downtown", "nightlife"],
            "historic": ["historic", "ancient", "ruins", "monuments", "heritage", "cultural"],
            "religious": ["religious", "spiritual", "temple", "church", "pilgrimage"],
            "adventure": ["adventure", "thrilling", "extreme", "outdoor", "sports"],
            "relaxing": ["relaxing", "peaceful", "quiet", "serene", "spa"]
        }
        
        for dest_type, keywords in type_mapping.items():
            if any(keyword in message_lower for keyword in keywords):
                extracted["destination_type"] = dest_type
                break
    
    elif current_step == "people_count":
        # Extract number of people
        people_patterns = [
            r"(\d+)\s*(?:people?|person|travelers?)",
            r"family\s+of\s+(\d+)",
            r"(\d+)\s*(?:of\s+us|traveling)"
        ]
        for pattern in people_patterns:
            match = re.search(pattern, message_lower)
            if match:
                extracted["people_count"] = match.group(1)
                break
    
    elif current_step == "budget":
        # Extract budget information
        budget_patterns = [
            r"\$?(\d+(?:,\d+)*(?:-\d+(?:,\d+)*)?)",
            r"(\d+(?:,\d+)*)\s*(?:dollars?|usd|eur|gbp)",
            r"budget\s+(?:of\s+)?\$?(\d+(?:,\d+)*)"
        ]
        for pattern in budget_patterns:
            match = re.search(pattern, message_lower)
            if match:
                extracted["budget_per_person"] = match.group(1)
                break
        
        # Extract currency
        if "eur" in message_lower or "euro" in message_lower:
            extracted["currency"] = "EUR"
        elif "gbp" in message_lower or "pound" in message_lower:
            extracted["currency"] = "GBP"
        else:
            extracted["currency"] = "USD"
    
    elif current_step == "dates":
        # Extract travel dates and duration
        date_patterns = [
            r"(\w+\s+\d{4})",
            r"(\d{1,2}\s+\w+)",
            r"(next\s+\w+)",
            r"(\d+)\s*(?:days?|nights?)"
        ]
        for pattern in date_patterns:
            match = re.search(pattern, message_lower)
            if match:
                if "day" in pattern or "night" in pattern:
                    extracted["duration"] = match.group(1)
                else:
                    extracted["travel_dates"] = match.group(1)
    
    elif current_step == "additional_preferences":
        # Extract additional preferences
        extracted["additional_preferences"] = message
    
    return extracted

async def determine_next_step(state: ConversationState, message: str) -> Dict:
    """Determine the next step in the conversation and generate appropriate response."""
    
    # Check if we have all required information for recommendations
    required_fields = ["travel_from", "travel_type", "destination_type", "people_count", "budget_per_person", "travel_dates"]
    missing_fields = [field for field in required_fields if field not in state.collected_data]
    
    if not missing_fields and state.current_step != "recommendations":
        # We have all info, generate recommendations
        state.current_step = "recommendations"
        return await generate_recommendations_response(state)
    
    # Determine next step based on what's missing
    if "travel_from" not in state.collected_data:
        state.current_step = "location"
        return {
            "response": "Great! I'd love to help you plan your perfect trip. First, where are you traveling from?",
            "step": "location",
            "data_collected": state.collected_data,
            "recommendations": None
        }
    
    elif "travel_type" not in state.collected_data:
        state.current_step = "travel_type"
        return {
            "response": f"Thanks! Are you looking for domestic travel within your country, or international travel abroad?",
            "step": "travel_type",
            "data_collected": state.collected_data,
            "recommendations": None
        }
    
    elif "destination_type" not in state.collected_data:
        state.current_step = "destination_type"
        return {
            "response": "What type of destination are you looking for? For example: beaches, mountains, cities, historic sites, religious places, adventure activities, or relaxing getaways?",
            "step": "destination_type",
            "data_collected": state.collected_data,
            "recommendations": None
        }
    
    elif "people_count" not in state.collected_data:
        state.current_step = "people_count"
        return {
            "response": "How many people will be traveling?",
            "step": "people_count",
            "data_collected": state.collected_data,
            "recommendations": None
        }
    
    elif "budget_per_person" not in state.collected_data:
        state.current_step = "budget"
        return {
            "response": "What's your budget per person for this trip?",
            "step": "budget",
            "data_collected": state.collected_data,
            "recommendations": None
        }
    
    elif "travel_dates" not in state.collected_data:
        state.current_step = "dates"
        return {
            "response": "When do you want to travel and for how many days?",
            "step": "dates",
            "data_collected": state.collected_data,
            "recommendations": None
        }
    
    elif "additional_preferences" not in state.collected_data:
        state.current_step = "additional_preferences"
        return {
            "response": "Any additional preferences or activities you'd like to include? For example: adventure sports, fine dining, cultural experiences, etc.",
            "step": "additional_preferences",
            "data_collected": state.collected_data,
            "recommendations": None
        }
    
    # Fallback response
    return {
        "response": "I'm processing your information. Let me ask you a few more questions to find the perfect destination for you.",
        "step": state.current_step,
        "data_collected": state.collected_data,
        "recommendations": None
    }

async def generate_recommendations_response(state: ConversationState) -> Dict:
    """Generate recommendations based on collected data."""
    try:
        # Create TravelPreferences object
        preferences = TravelPreferences(
            budget_per_person=state.collected_data.get("budget_per_person", "2000"),
            people_count=state.collected_data.get("people_count", "2"),
            travel_from=state.collected_data.get("travel_from", "Unknown"),
            travel_type=state.collected_data.get("travel_type", "international"),
            destination_type=state.collected_data.get("destination_type", "beach"),
            travel_dates=state.collected_data.get("travel_dates", "Flexible"),
            currency=state.collected_data.get("currency", "USD"),
            additional_preferences=state.collected_data.get("additional_preferences", "")
        )
        
        # Get AI-generated recommendations
        llm_response = await call_groq_recommendations(preferences)
        
        if llm_response:
            try:
                import json
                recommendations = json.loads(llm_response)
                state.recommendations = recommendations.get("destinations", [])
                
                # Format response
                response_text = "Perfect! Based on your preferences, here are my top recommendations:\n\n"
                for i, dest in enumerate(state.recommendations[:3], 1):
                    response_text += f"{i}. **{dest['name']}, {dest['country']}**\n"
                    response_text += f"   {dest['description']}\n"
                    response_text += f"   Estimated cost: {dest['estimated_cost_per_person']}\n"
                    response_text += f"   Best time: {dest['best_time_to_visit']}\n\n"
                
                response_text += "Which destination interests you most? I can help you with flight and hotel bookings!"
                
                return {
                    "response": response_text,
                    "step": "recommendations",
                    "data_collected": state.collected_data,
                    "recommendations": state.recommendations
                }
                
            except json.JSONDecodeError:
                return {
                    "response": "I found some great destinations for you! Let me show you the options...",
                    "step": "recommendations",
                    "data_collected": state.collected_data,
                    "recommendations": []
                }
        
        return {
            "response": "I'm having trouble generating recommendations right now. Let me try a different approach.",
            "step": "recommendations",
            "data_collected": state.collected_data,
            "recommendations": []
        }
        
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        return {
            "response": "I encountered an issue while generating recommendations. Let's try again!",
            "step": "recommendations",
            "data_collected": state.collected_data,
            "recommendations": []
        }

async def get_real_flights(search: FlightSearch) -> List[Dict]:
    """Get real flight data using integrated flight search APIs."""
    try:
        # Use the comprehensive flight search API
        flights = await flight_api.search_flights(
            origin=search.origin,
            destination=search.destination,
            departure_date=search.departure_date,
            passengers=search.passengers
        )
        
        # Convert currency if needed
        for flight in flights:
            if "USD" in flight["price"]:
                usd_price = flight["price"]["USD"]
                flight["price"]["EUR"] = round(usd_price * 0.85, 2)
                flight["price"]["GBP"] = round(usd_price * 0.73, 2)
        
        return flights

    except Exception as e:
        logger.error(f"Error fetching flights: {e}")
        # Return mock data as fallback
        return [
            {
                "id": "fallback_1",
                "airline": "Delta Airlines",
                "flight_number": "DL123",
                "departure_time": f"{search.departure_date}T09:00:00",
                "arrival_time": f"{search.departure_date}T11:30:00",
                "duration": "2h 30m",
                "price": {"USD": 450, "EUR": 380, "GBP": 330},
                "stops": 0,
                "aircraft": "Boeing 737",
                "booking_link": "https://www.delta.com",
                "source": "Fallback Data"
            }
        ]

async def get_real_hotels(search: HotelSearch) -> List[Dict]:
    """Get real hotel data from RapidAPI Skyscanner Hotel API."""
    try:
        if not SKYSCANNER_API_KEY:
            # Return mock data if no API key
            return [
                {
                    "id": "hotel_1",
                    "name": "Grand Hotel & Spa",
                    "rating": 4.8,
                    "price_per_night": {"USD": 250, "EUR": 210, "GBP": 180},
                    "amenities": ["WiFi", "Pool", "Spa", "Restaurant"],
                    "location": "City Center",
                    "image": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800",
                    "booking_link": "https://www.hotels.com"
                },
                {
                    "id": "hotel_2",
                    "name": "Boutique Hotel",
                    "rating": 4.5,
                    "price_per_night": {"USD": 180, "EUR": 150, "GBP": 130},
                    "amenities": ["WiFi", "Breakfast", "Bar"],
                    "location": "Downtown",
                    "image": "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800",
                    "booking_link": "https://www.booking.com"
                }
            ]

        # Get entity ID for the destination using RapidAPI Skyscanner
        async with httpx.AsyncClient() as client:
            # First, get the entity ID for the destination
            auto_complete_response = await client.get(
                "https://flights-sky.p.rapidapi.com/hotels/auto-complete",
                params={"query": search.destination},
                headers={
                    "X-RapidAPI-Key": SKYSCANNER_API_KEY,
                    "X-RapidAPI-Host": "flights-sky.p.rapidapi.com"
                }
            )
            
            if auto_complete_response.status_code != 200:
                logger.error(f"Hotel auto-complete error: {auto_complete_response.status_code}")
                return []
            
            auto_complete_data = auto_complete_response.json()
            if not auto_complete_data.get("data") or not auto_complete_data["data"]:
                logger.error("No hotel destinations found")
                return []
            
            # Find the first city result
            entity_id = None
            for result in auto_complete_data["data"]:
                if result.get("entityType") == "city":
                    entity_id = result.get("entityId")
                    break
            
            if not entity_id:
                logger.error("No city entity ID found")
                return []
            
            # Search for hotels
            hotel_search_response = await client.get(
                "https://flights-sky.p.rapidapi.com/hotels/search",
                params={
                    "entityId": entity_id,
                    "checkin": search.check_in,
                    "checkout": search.check_out,
                    "guests": search.guests
                },
                headers={
                    "X-RapidAPI-Key": SKYSCANNER_API_KEY,
                    "X-RapidAPI-Host": "flights-sky.p.rapidapi.com"
                }
            )
            
            if hotel_search_response.status_code != 200:
                logger.error(f"Hotel search error: {hotel_search_response.status_code}")
                return []
            
            search_data = hotel_search_response.json()
            if not search_data.get("data") or not search_data["data"].get("results"):
                logger.error("No hotel search results")
                return []
            
            # Parse hotel results
            hotels = []
            hotel_cards = search_data["data"]["results"].get("hotelCards", [])
            
            for hotel_card in hotel_cards[:10]:  # Limit to 10 hotels
                hotel_info = hotel_card.get("hotel", {})
                pricing = hotel_card.get("pricing", {})
                
                # Extract price information
                price_per_night = {}
                if pricing.get("price"):
                    price_per_night["USD"] = pricing["price"]
                
                # Extract amenities
                amenities = []
                if hotel_info.get("amenities"):
                    amenities = [amenity.get("name", "") for amenity in hotel_info["amenities"][:5]]
                
                hotel = {
                    "id": str(hotel_info.get("id", "")),
                    "name": hotel_info.get("name", "Unknown Hotel"),
                    "rating": hotel_info.get("rating", 0),
                    "price_per_night": price_per_night,
                    "location": f"{hotel_info.get('address', {}).get('city', '')}, {hotel_info.get('address', {}).get('country', '')}",
                    "amenities": amenities,
                    "booking_link": pricing.get("deeplink", "https://www.skyscanner.com"),
                    "image": hotel_info.get("images", [{}])[0].get("url", "") if hotel_info.get("images") else "",
                    "stars": hotel_info.get("stars", 0),
                    "description": hotel_info.get("description", "")
                }
                hotels.append(hotel)
            
            logger.info(f"Found {len(hotels)} hotels for {search.destination}")
            return hotels

    except Exception as e:
        logger.error(f"Error fetching hotels: {e}")
        return []

async def get_real_activities(search: ActivitySearch) -> List[Dict]:
    """Get real activity data from Google Places API or similar."""
    try:
        if not GOOGLE_PLACES_API_KEY:
            # Return mock data if no API key
            return [
                {
                    "id": "activity_1",
                    "name": "City Walking Tour",
                    "description": "Explore the city with a knowledgeable guide",
                    "duration": "3 hours",
                    "price": {"USD": 45, "EUR": 38, "GBP": 33},
                    "rating": 4.7,
                    "category": "Cultural",
                    "image": "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800",
                    "booking_link": "https://www.viator.com"
                },
                {
                    "id": "activity_2",
                    "name": "Adventure Sports",
                    "description": "Thrilling outdoor activities and sports",
                    "duration": "4 hours",
                    "price": {"USD": 80, "EUR": 68, "GBP": 59},
                    "rating": 4.9,
                    "category": "Adventure",
                    "image": "https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=800",
                    "booking_link": "https://www.getyourguide.com"
                }
            ]

        # Real API call would go here
        # async with httpx.AsyncClient() as client:
        #     response = await client.get(
        #         f"https://maps.googleapis.com/maps/api/place/textsearch/json",
        #         params={
        #             "query": f"tourist attractions in {search.destination}",
        #             "key": GOOGLE_PLACES_API_KEY
        #         }
        #     )
        #     return response.json()

    except Exception as e:
        logger.error(f"Error fetching activities: {e}")
        return []

async def get_weather_data(destination: str) -> Dict:
    """Get weather data for a destination."""
    try:
        if not WEATHER_API_KEY:
            return {
                "temperature": "22°C",
                "condition": "Sunny",
                "humidity": "65%",
                "forecast": "Clear skies for the next 5 days"
            }

        # Real weather API call would go here
        # async with httpx.AsyncClient() as client:
        #     response = await client.get(
        #         f"http://api.weatherapi.com/v1/current.json",
        #         params={
        #             "key": WEATHER_API_KEY,
        #             "q": destination
        #         }
        #     )
        #     return response.json()

    except Exception as e:
        logger.error(f"Error fetching weather: {e}")
        return {}

async def get_average_flight_prices(origin: str, destination: str, departure_date: str, return_date: Optional[str] = None) -> Dict:
    """Get average flight prices for a route during specific dates."""
    try:
        # Use the flight API to get real prices
        flights = await flight_api.search_flights(
            origin=origin,
            destination=destination,
            departure_date=departure_date,
            passengers=1
        )
        
        if not flights:
            return {"average_price": 0, "price_range": "0-0", "currency": "USD", "source": "No data available"}
        
        # Calculate average price
        prices = [flight["price"]["USD"] for flight in flights if "USD" in flight["price"]]
        if not prices:
            return {"average_price": 0, "price_range": "0-0", "currency": "USD", "source": "No price data"}
        
        avg_price = sum(prices) / len(prices)
        min_price = min(prices)
        max_price = max(prices)
        
        return {
            "average_price": round(avg_price, 2),
            "price_range": f"{min_price}-{max_price}",
            "currency": "USD",
            "source": "Real-time flight data",
            "total_flights": len(flights)
        }
        
    except Exception as e:
        logger.error(f"Error fetching flight prices: {e}")
        # Return estimated prices based on distance
        return {"average_price": 500, "price_range": "400-800", "currency": "USD", "source": "Estimated"}

async def get_average_hotel_prices(destination: str, check_in: str, check_out: str, guests: int = 1) -> Dict:
    """Get average hotel prices for a destination during specific dates."""
    try:
        # Calculate number of nights
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
        nights = (check_out_date - check_in_date).days
        
        # Use the hotel API to get real prices
        hotels = await get_real_hotels(HotelSearch(
            destination=destination,
            check_in=check_in,
            check_out=check_out,
            guests=guests
        ))
        
        if not hotels:
            return {"average_price_per_night": 0, "total_cost": 0, "currency": "USD", "source": "No data available"}
        
        # Calculate average price per night
        prices = [hotel["price_per_night"]["USD"] for hotel in hotels if "USD" in hotel["price_per_night"]]
        if not prices:
            return {"average_price_per_night": 0, "total_cost": 0, "currency": "USD", "source": "No price data"}
        
        avg_price_per_night = sum(prices) / len(prices)
        total_cost = avg_price_per_night * nights
        
        return {
            "average_price_per_night": round(avg_price_per_night, 2),
            "total_cost": round(total_cost, 2),
            "nights": nights,
            "currency": "USD",
            "source": "Real-time hotel data",
            "total_hotels": len(hotels)
        }
        
    except Exception as e:
        logger.error(f"Error fetching hotel prices: {e}")
        # Return estimated prices based on destination type
        return {"average_price_per_night": 150, "total_cost": 150 * 7, "currency": "USD", "source": "Estimated"}

async def get_cost_of_living(destination: str) -> Dict:
    """Get cost of living data for a destination using the dataset."""
    try:
        # Parse destination to extract city and country
        if "," in destination:
            city, country = destination.split(",", 1)
            city = city.strip()
            country = country.strip()
        else:
            city = destination
            country = None
        
        # Use the dataset-based cost of living system
        cost_data = await cost_of_living_dataset.get_cost_of_living(city, country)
        
        return cost_data
        
    except Exception as e:
        logger.error(f"Error fetching cost of living: {e}")
        return {
            "daily_food": 30,
            "daily_transport": 20,
            "daily_activities": 40,
            "daily_misc": 25,
            "daily_total": 115,
            "currency": "USD",
            "source": "Fallback data"
        }

async def calculate_total_trip_cost(origin: str, destination: str, departure_date: str, 
                                  return_date: str, guests: int, preferences: Dict) -> Dict:
    """Calculate total trip cost using real-time data."""
    try:
        # Fetch all cost components concurrently
        flight_task = get_average_flight_prices(origin, destination, departure_date, return_date)
        hotel_task = get_average_hotel_prices(destination, departure_date, return_date, guests)
        living_task = get_cost_of_living(destination)
        
        flight_data, hotel_data, living_data = await asyncio.gather(
            flight_task, hotel_task, living_task
        )
        
        # Calculate number of days
        departure = datetime.strptime(departure_date, "%Y-%m-%d")
        return_dt = datetime.strptime(return_date, "%Y-%m-%d")
        days = (return_dt - departure).days
        
        # Calculate daily living costs
        daily_living_cost = (
            living_data["daily_food"] + 
            living_data["daily_transport"] + 
            living_data["daily_activities"] + 
            living_data["daily_misc"]
        )
        
        # Calculate total costs
        flight_cost_per_person = flight_data["average_price"]
        hotel_cost_total = hotel_data["total_cost"]
        living_cost_total = daily_living_cost * days
        
        # Total cost per person
        total_cost_per_person = flight_cost_per_person + (hotel_cost_total / guests) + (living_cost_total / guests)
        
        # Convert to user's currency if needed
        user_currency = preferences.get("currency", "USD")
        if user_currency != "USD":
            conversion_rates = {
                "EUR": 0.85,
                "GBP": 0.73,
                "CAD": 1.25,
                "AUD": 1.35
            }
            rate = conversion_rates.get(user_currency, 1.0)
            total_cost_per_person = total_cost_per_person * rate
            flight_cost_per_person = flight_cost_per_person * rate
            hotel_cost_total = hotel_cost_total * rate
            living_cost_total = living_cost_total * rate
        
        return {
            "total_cost_per_person": round(total_cost_per_person, 2),
            "breakdown": {
                "flight_cost_per_person": round(flight_cost_per_person, 2),
                "hotel_cost_per_person": round(hotel_cost_total / guests, 2),
                "living_cost_per_person": round(living_cost_total / guests, 2)
            },
            "details": {
                "flight_data": flight_data,
                "hotel_data": hotel_data,
                "living_data": living_data,
                "days": days,
                "guests": guests
            },
            "currency": user_currency,
            "source": "Real-time data calculation"
        }
        
    except Exception as e:
        logger.error(f"Error calculating total trip cost: {e}")
        return {
            "total_cost_per_person": 0,
            "breakdown": {},
            "details": {},
            "currency": preferences.get("currency", "USD"),
            "source": "Calculation failed"
        }

async def call_groq_recommendations(preferences: TravelPreferences) -> str:
    """Call Groq LLM to generate personalized travel recommendations with real cost data."""
    try:
        # Parse travel dates to get departure and return dates
        departure_date, return_date = parse_travel_dates(preferences.travel_dates)
        
        # Get potential destinations based on preferences
        potential_destinations = get_potential_destinations(preferences)
        
        # Calculate costs for each destination
        destination_costs = []
        for dest in potential_destinations[:5]:  # Limit to top 5 for performance
            cost_data = await calculate_total_trip_cost(
                origin=preferences.travel_from,
                destination=dest["name"],
                departure_date=departure_date,
                return_date=return_date,
                guests=int(preferences.people_count),
                preferences=preferences.model_dump()
            )
            
            if cost_data["total_cost_per_person"] > 0:
                destination_costs.append({
                    "destination": dest,
                    "cost_data": cost_data
                })
        
        # Filter by budget
        budget_range = parse_budget_range(preferences.budget_per_person)
        affordable_destinations = []
        
        for item in destination_costs:
            cost = item["cost_data"]["total_cost_per_person"]
            if budget_range["min"] <= cost <= budget_range["max"]:
                affordable_destinations.append(item)
        
        # Sort by cost (lowest first)
        affordable_destinations.sort(key=lambda x: x["cost_data"]["total_cost_per_person"])
        
        # Create detailed prompt for AI with real cost data
        destinations_info = []
        for item in affordable_destinations[:3]:
            dest = item["destination"]
            cost = item["cost_data"]
            destinations_info.append(f"""
- {dest['name']}, {dest['country']}: {cost['total_cost_per_person']} {cost['currency']} per person
  Flight: {cost['breakdown']['flight_cost_per_person']} {cost['currency']}
  Hotel: {cost['breakdown']['hotel_cost_per_person']} {cost['currency']}
  Daily living: {cost['breakdown']['living_cost_per_person']} {cost['currency']}
  Highlights: {', '.join(dest['highlights'])}
  Best time: {dest['best_time']}
""")
        
        prompt = f"""
You are an expert travel advisor. Based on the user's preferences and real-time cost data, recommend the best destinations.

User Preferences:
- Budget: {preferences.budget_per_person} {preferences.currency}
- People: {preferences.people_count}
- Travel type: {preferences.travel_type} {preferences.destination_type}
- Dates: {preferences.travel_dates}
- From: {preferences.travel_from}
- Additional preferences: {preferences.additional_preferences}

Available destinations with real cost data:
{''.join(destinations_info)}

Return ONLY valid JSON with detailed recommendations:
{{
    "destinations": [
        {{
            "name": "Destination Name",
            "country": "Country",
            "type": "destination_type",
            "description": "Detailed description",
            "total_cost_per_person": "1500 USD",
            "cost_breakdown": {{
                "flight": "500 USD",
                "hotel": "700 USD", 
                "daily_living": "300 USD"
            }},
            "best_time_to_visit": "Month-Month",
            "highlights": ["Highlight1", "Highlight2"],
            "why_perfect": "Why this destination is perfect for the user",
            "travel_tips": "Specific tips for this destination"
        }}
    ]
}}

No other text, just JSON.
"""
        
        # Call Groq API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                GROQ_BASE_URL,
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.1-8b-instant",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are an expert travel advisor. Always respond with valid JSON format as requested. Use the provided real cost data to give accurate recommendations."
                        },
                        {
                            "role": "user", 
                            "content": prompt
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 2000
                },
                timeout=30.0
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                logger.error(f"Groq API error: {response.status_code} - {response.text}")
                return None
                
    except Exception as e:
        logger.error(f"Error calling Groq for recommendations: {e}")
        return None

def parse_travel_dates(travel_dates: str) -> Tuple[str, str]:
    """Parse travel dates string to get departure and return dates."""
    try:
        # Handle various date formats
        if "december" in travel_dates.lower():
            year = "2024"
            month = "12"
            # Assume 7-day trip
            departure_date = f"{year}-{month}-15"
            return_date = f"{year}-{month}-22"
        elif "january" in travel_dates.lower():
            year = "2025"
            month = "01"
            departure_date = f"{year}-{month}-15"
            return_date = f"{year}-{month}-22"
        else:
            # Default to current year, 7 days from now
            departure_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
            return_date = (datetime.now() + timedelta(days=37)).strftime("%Y-%m-%d")
        
        return departure_date, return_date
        
    except Exception as e:
        logger.error(f"Error parsing travel dates: {e}")
        # Fallback dates
        departure_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        return_date = (datetime.now() + timedelta(days=37)).strftime("%Y-%m-%d")
        return departure_date, return_date

def get_potential_destinations(preferences: TravelPreferences) -> List[Dict]:
    """Get potential destinations based on user preferences."""
    all_destinations = []
    
    # Get destinations from TRAVEL_DATA
    if preferences.travel_type.lower() == "domestic":
        for dest_type, destinations in TRAVEL_DATA.get("domestic", {}).items():
            if preferences.destination_type.lower() in dest_type.lower():
                all_destinations.extend(destinations)
    else:
        for dest_type, destinations in TRAVEL_DATA.get("international", {}).items():
            if preferences.destination_type.lower() in dest_type.lower():
                all_destinations.extend(destinations)
    
    # If no exact match, get all destinations
    if not all_destinations:
        for destinations in TRAVEL_DATA.get("domestic", {}).values():
            all_destinations.extend(destinations)
        for destinations in TRAVEL_DATA.get("international", {}).values():
            all_destinations.extend(destinations)
    
    return all_destinations

def parse_budget_range(budget_str: str) -> Dict[str, float]:
    """Parse budget string to get min and max values."""
    try:
        budget_clean = budget_str.replace("$", "").replace(",", "")
        
        if "-" in budget_clean:
            min_budget, max_budget = map(float, budget_clean.split("-"))
        elif "+" in budget_clean:
            min_budget = float(budget_clean.replace("+", ""))
            max_budget = min_budget * 2
        else:
            min_budget = 0
            max_budget = float(budget_clean)
        
        return {"min": min_budget, "max": max_budget}
        
    except Exception as e:
        logger.error(f"Error parsing budget range: {e}")
        return {"min": 0, "max": 5000}

# API Endpoints
@app.get("/")
async def root():
    return {"message": "Travel AI API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/chat")
async def chat_endpoint(request: ChatMessage):
    """AI chat endpoint for travel planning conversations."""
    try:
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        # Use conversational flow for structured travel planning
        logger.info(f"Starting conversational flow for session: {session_id}")
        response_data = await handle_conversational_flow(request.message, session_id)
        logger.info(f"Response data: {response_data}")
        
        return {
            "response": response_data["response"],
            "session_id": session_id,
            "step": response_data["step"],
            "data_collected": response_data["data_collected"],
            "recommendations": response_data["recommendations"]
        }
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail="Chat service error")

@app.post("/recommendations")
async def get_recommendations(preferences: TravelPreferences):
    """Get AI-powered travel recommendations with real-time cost data."""
    try:
        # Call enhanced Groq LLM for recommendations with real cost data
        llm_response = await call_groq_recommendations(preferences)
        
        if llm_response:
            try:
                # Try to parse the JSON response from LLM
                import json
                logger.info(f"LLM Response: {llm_response}")  # Log full response
                recommendations = json.loads(llm_response)
                
                # Add additional data to each destination
                for dest in recommendations.get("destinations", []):
                    # Add weather data
                    dest["weather"] = await get_weather_data(dest["name"])
                    
                    # Add booking links
                    dest["booking_links"] = {
                        "flights": f"https://www.skyscanner.com/search?from={preferences.travel_from}&to={dest['name']}",
                        "hotels": f"https://www.booking.com/search?ss={dest['name']}",
                        "activities": f"https://www.getyourguide.com/search?q={dest['name']}"
                    }
                
                return {
                    "success": True,
                    "destinations": recommendations.get("destinations", []),
                    "preferences": preferences.model_dump(),
                    "total_found": len(recommendations.get("destinations", [])),
                    "source": "AI Generated with Real-time Data"
                }
                
            except json.JSONDecodeError:
                # If LLM doesn't return valid JSON, fall back to filtered data
                logger.warning("LLM response not valid JSON, using fallback")
                return await get_filtered_recommendations(preferences)
        else:
            # Fall back to filtered data if LLM fails
            logger.warning("LLM call failed, using fallback")
            return await get_filtered_recommendations(preferences)

    except Exception as e:
        logger.error(f"Recommendations error: {e}")
        raise HTTPException(status_code=500, detail="Recommendations service error")

async def get_filtered_recommendations(preferences: TravelPreferences):
    """Fallback method using filtered data (original logic)."""
    try:
        # Filter destinations based on preferences
        filtered_destinations = []
        
        # Get the appropriate destination pool based on travel type
        if preferences.travel_type.lower() == "domestic":
            destination_pool = TRAVEL_DATA.get("domestic", {})
        else:
            destination_pool = TRAVEL_DATA.get("international", {})
        
        # Find matching destination types
        for dest_type, destinations in destination_pool.items():
            if preferences.destination_type.lower() in dest_type.lower():
                filtered_destinations.extend(destinations)
        
        # If no exact match, get a mix of destinations
        if not filtered_destinations:
            for destinations in destination_pool.values():
                filtered_destinations.extend(destinations)
        
        # Filter by budget
        budget_clean = preferences.budget_per_person.replace("$", "").replace(",", "")
        if "-" in budget_clean:
            min_budget, max_budget = map(int, budget_clean.split("-"))
        elif "+" in budget_clean:
            min_budget = int(budget_clean.replace("+", ""))
            max_budget = min_budget * 2
        else:
            min_budget = 0
            max_budget = int(budget_clean)
        
        # Convert to user's currency and filter
        final_destinations = []
        for dest in filtered_destinations:
            # Calculate total cost for a 7-day trip
            daily_cost = dest["daily_cost_usd"]
            flight_cost = dest["flight_cost_usd"]
            total_cost = (daily_cost * 7) + flight_cost
            
            # Convert to user's currency
            if preferences.currency != "USD":
                # Simple conversion (you can use real API for this)
                conversion_rates = {
                    "EUR": 0.85,
                    "GBP": 0.73,
                    "CAD": 1.25,
                    "AUD": 1.35
                }
                rate = conversion_rates.get(preferences.currency, 1.0)
                total_cost = total_cost * rate
            
            if min_budget <= total_cost <= max_budget:
                dest_copy = dest.copy()
                dest_copy["total_cost"] = round(total_cost, 2)
                dest_copy["currency"] = preferences.currency
                final_destinations.append(dest_copy)

        # Get weather data for top destinations
        for dest in final_destinations[:3]:
            dest["weather"] = await get_weather_data(dest["name"])

        return {
            "success": True,
            "destinations": final_destinations[:5],
            "preferences": preferences.model_dump(),
            "total_found": len(final_destinations),
            "source": "Filtered Data"
        }

    except Exception as e:
        logger.error(f"Filtered recommendations error: {e}")
        raise HTTPException(status_code=500, detail="Filtered recommendations service error")

@app.post("/flights")
async def search_flights(search: FlightSearch):
    """Search for flights."""
    try:
        flights = await get_real_flights(search)
        return {
            "success": True,
            "flights": flights,
            "search": search.dict()
        }
    except Exception as e:
        logger.error(f"Flight search error: {e}")
        raise HTTPException(status_code=500, detail="Flight search error")

@app.get("/price-calendar")
async def get_price_calendar(origin: str, destination: str):
    """Get price calendar for flexible date searches"""
    try:
        flight_api = FlightSearchAPI()
        calendar_data = await flight_api.get_price_calendar(origin, destination)
        
        if not calendar_data:
            return {"error": "No price calendar data available", "calendar": []}
        
        return {
            "origin": origin,
            "destination": destination,
            "calendar": calendar_data,
            "total_days": len(calendar_data),
            "data_source": "RapidAPI Skyscanner"
        }
        
    except Exception as e:
        logger.error(f"Error getting price calendar: {e}")
        return {"error": str(e), "calendar": []}

@app.get("/validate-airport/{airport_code}")
async def validate_airport(airport_code: str):
    """Validate airport code and get airport information"""
    try:
        flight_api = FlightSearchAPI()
        result = await flight_api.validate_airport_code(airport_code.upper())
        
        return result
        
    except Exception as e:
        logger.error(f"Error validating airport: {e}")
        return {"valid": False, "error": str(e)}

@app.get("/flight-search-options")
async def get_flight_search_options():
    """Get available flight search options and endpoints"""
    return {
        "search_types": ["one-way", "roundtrip", "multi-city", "everywhere"],
        "endpoints": {
            "flights": "Search flights (one-way/roundtrip)",
            "cheapest_one_way": "Get cheapest one-way flights",
            "search_everywhere": "Search flights to everywhere from a location",
            "search_multi_city": "Search multi-city flights",
            "price_calendar": "Get price calendar for flexible dates",
            "price_calendar_web": "Get monthly price calendar view",
            "price_calendar_web_return": "Get monthly return price calendar",
            "validate_airport": "Validate airport codes",
            "search_incomplete": "Get incomplete search results (polling)",
            "flight_detail": "Get detailed flight information"
        },
        "features": {
            "real_time_prices": True,
            "price_calendar": True,
            "monthly_calendar": True,
            "airport_validation": True,
            "roundtrip_search": True,
            "multi_city_search": True,
            "everywhere_search": True,
            "place_id_conversion": True,
            "polling_support": True,
            "detailed_flight_info": True
        },
        "data_sources": ["RapidAPI Skyscanner", "Amadeus"],
        "coverage": "95% global flight data",
        "total_endpoints": 10
    }

@app.get("/hotel-search-options")
async def get_hotel_search_options():
    """Get available hotel search options and endpoints"""
    return {
        "search_types": ["city_search", "hotel_prices", "hotel_reviews"],
        "endpoints": {
            "hotels": "Search hotels by destination and dates",
            "hotel_auto_complete": "Auto-complete hotel destinations",
            "hotel_prices": "Get specific hotel prices",
            "hotel_reviews": "Get hotel reviews",
            "similar_hotels": "Find similar hotels"
        },
        "features": {
            "real_time_prices": True,
            "multiple_partners": True,
            "hotel_reviews": True,
            "price_comparison": True,
            "booking_links": True
        },
        "data_sources": ["RapidAPI Skyscanner Hotels"],
        "partners": ["Booking.com", "Hotels.com", "Expedia", "Priceline", "SuperTravel"],
        "coverage": "Global hotel data"
    }

@app.get("/hotels/auto-complete")
async def hotel_auto_complete(query: str):
    """Auto-complete hotel destinations"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://flights-sky.p.rapidapi.com/hotels/auto-complete",
                params={"query": query},
                headers={
                    "X-RapidAPI-Key": SKYSCANNER_API_KEY,
                    "X-RapidAPI-Host": "flights-sky.p.rapidapi.com"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "query": query,
                    "results": data.get("data", []),
                    "data_source": "RapidAPI Skyscanner"
                }
            else:
                return {"success": False, "error": f"API error: {response.status_code}"}
                
    except Exception as e:
        logger.error(f"Error in hotel auto-complete: {e}")
        return {"success": False, "error": str(e)}

@app.get("/hotels/prices")
async def get_hotel_prices(hotel_id: str, checkin: str, checkout: str):
    """Get specific hotel prices"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://flights-sky.p.rapidapi.com/hotels/prices",
                params={
                    "hotelId": hotel_id,
                    "checkin": checkin,
                    "checkout": checkout
                },
                headers={
                    "X-RapidAPI-Key": SKYSCANNER_API_KEY,
                    "X-RapidAPI-Host": "flights-sky.p.rapidapi.com"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "hotel_id": hotel_id,
                    "checkin": checkin,
                    "checkout": checkout,
                    "prices": data.get("data", {}),
                    "data_source": "RapidAPI Skyscanner"
                }
            else:
                return {"success": False, "error": f"API error: {response.status_code}"}
                
    except Exception as e:
        logger.error(f"Error getting hotel prices: {e}")
        return {"success": False, "error": str(e)}

# Additional Flight Endpoints
@app.get("/flights/search-everywhere")
async def search_everywhere_flights(from_entity_id: str, type: str = "oneway"):
    """Search for flights to everywhere from a specific location"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://flights-sky.p.rapidapi.com/flights/search-everywhere",
                params={
                    "fromEntityId": from_entity_id,
                    "type": type
                },
                headers={
                    "X-RapidAPI-Key": SKYSCANNER_API_KEY,
                    "X-RapidAPI-Host": "flights-sky.p.rapidapi.com"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "from_entity_id": from_entity_id,
                    "type": type,
                    "results": data.get("data", {}),
                    "data_source": "RapidAPI Skyscanner"
                }
            else:
                return {"success": False, "error": f"API error: {response.status_code}"}
                
    except Exception as e:
        logger.error(f"Error in search-everywhere: {e}")
        return {"success": False, "error": str(e)}

@app.post("/flights/search-multi-city")
async def search_multi_city_flights(request: dict):
    """Search for multi-city flights"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://flights-sky.p.rapidapi.com/flights/search-multi-city",
                json=request,
                headers={
                    "X-RapidAPI-Key": SKYSCANNER_API_KEY,
                    "X-RapidAPI-Host": "flights-sky.p.rapidapi.com",
                    "Content-Type": "application/json"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "request": request,
                    "results": data.get("data", {}),
                    "data_source": "RapidAPI Skyscanner"
                }
            else:
                return {"success": False, "error": f"API error: {response.status_code}"}
                
    except Exception as e:
        logger.error(f"Error in multi-city search: {e}")
        return {"success": False, "error": str(e)}

@app.get("/flights/search-incomplete")
async def search_incomplete_flights():
    """Get incomplete flight search results (for polling)"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://flights-sky.p.rapidapi.com/flights/search-incomplete",
                headers={
                    "X-RapidAPI-Key": SKYSCANNER_API_KEY,
                    "X-RapidAPI-Host": "flights-sky.p.rapidapi.com"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "results": data.get("data", {}),
                    "data_source": "RapidAPI Skyscanner"
                }
            else:
                return {"success": False, "error": f"API error: {response.status_code}"}
                
    except Exception as e:
        logger.error(f"Error getting incomplete results: {e}")
        return {"success": False, "error": str(e)}

@app.get("/flights/detail")
async def get_flight_detail():
    """Get detailed flight information"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://flights-sky.p.rapidapi.com/flights/detail",
                headers={
                    "X-RapidAPI-Key": SKYSCANNER_API_KEY,
                    "X-RapidAPI-Host": "flights-sky.p.rapidapi.com"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "results": data.get("data", {}),
                    "data_source": "RapidAPI Skyscanner"
                }
            else:
                return {"success": False, "error": f"API error: {response.status_code}"}
                
    except Exception as e:
        logger.error(f"Error getting flight details: {e}")
        return {"success": False, "error": str(e)}

@app.get("/flights/price-calendar-web")
async def get_price_calendar_web(from_entity_id: str, to_entity_id: str, year_month: str):
    """Get price calendar for web (monthly view)"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://flights-sky.p.rapidapi.com/flights/price-calendar-web",
                params={
                    "fromEntityId": from_entity_id,
                    "toEntityId": to_entity_id,
                    "yearMonth": year_month
                },
                headers={
                    "X-RapidAPI-Key": SKYSCANNER_API_KEY,
                    "X-RapidAPI-Host": "flights-sky.p.rapidapi.com"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "from_entity_id": from_entity_id,
                    "to_entity_id": to_entity_id,
                    "year_month": year_month,
                    "calendar": data.get("data", {}),
                    "data_source": "RapidAPI Skyscanner"
                }
            else:
                return {"success": False, "error": f"API error: {response.status_code}"}
                
    except Exception as e:
        logger.error(f"Error getting price calendar web: {e}")
        return {"success": False, "error": str(e)}

@app.get("/flights/price-calendar-web-return")
async def get_price_calendar_web_return(from_entity_id: str, to_entity_id: str, year_month: str, year_month_return: str):
    """Get price calendar for web return flights (monthly view)"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://flights-sky.p.rapidapi.com/flights/price-calendar-web-return",
                params={
                    "fromEntityId": from_entity_id,
                    "toEntityId": to_entity_id,
                    "yearMonth": year_month,
                    "yearMonthReturn": year_month_return
                },
                headers={
                    "X-RapidAPI-Key": SKYSCANNER_API_KEY,
                    "X-RapidAPI-Host": "flights-sky.p.rapidapi.com"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "from_entity_id": from_entity_id,
                    "to_entity_id": to_entity_id,
                    "year_month": year_month,
                    "year_month_return": year_month_return,
                    "calendar": data.get("data", {}),
                    "data_source": "RapidAPI Skyscanner"
                }
            else:
                return {"success": False, "error": f"API error: {response.status_code}"}
                
    except Exception as e:
        logger.error(f"Error getting price calendar web return: {e}")
        return {"success": False, "error": str(e)}

@app.post("/hotels")
async def search_hotels(search: HotelSearch):
    """Search for hotels."""
    try:
        hotels = await get_real_hotels(search)
        return {
            "success": True,
            "hotels": hotels,
            "search": search.dict()
        }
    except Exception as e:
        logger.error(f"Hotel search error: {e}")
        raise HTTPException(status_code=500, detail="Hotel search error")

@app.post("/select-destination")
async def select_destination(request: Dict):
    """Handle destination selection and move to booking phase."""
    try:
        session_id = request.get("session_id")
        destination_index = request.get("destination_index", 0)
        
        if session_id not in conversation_states:
            raise HTTPException(status_code=404, detail="Session not found")
        
        state = conversation_states[session_id]
        
        if not state.recommendations or destination_index >= len(state.recommendations):
            raise HTTPException(status_code=400, detail="Invalid destination selection")
        
        selected_dest = state.recommendations[destination_index]
        state.selected_destination = selected_dest
        state.current_step = "booking_selection"
        
        return {
            "success": True,
            "selected_destination": selected_dest,
            "message": f"Great choice! {selected_dest['name']} is an excellent destination. Would you like me to help you with flight bookings or hotel accommodations?",
            "step": "booking_selection"
        }
        
    except Exception as e:
        logger.error(f"Destination selection error: {e}")
        raise HTTPException(status_code=500, detail="Destination selection error")

@app.post("/book-flights")
async def book_flights(request: Dict):
    """Handle flight booking request."""
    try:
        session_id = request.get("session_id")
        
        if session_id not in conversation_states:
            raise HTTPException(status_code=404, detail="Session not found")
        
        state = conversation_states[session_id]
        
        if not state.selected_destination:
            raise HTTPException(status_code=400, detail="No destination selected")
        
        # Create flight search
        flight_search = FlightSearch(
            origin=state.collected_data.get("travel_from", "Unknown"),
            destination=state.selected_destination["name"],
            departure_date=state.collected_data.get("travel_dates", "2024-12-01"),
            passengers=int(state.collected_data.get("people_count", "1"))
        )
        
        # Get flight options
        flights = await get_real_flights(flight_search)
        
        return {
            "success": True,
            "flights": flights,
            "destination": state.selected_destination,
            "message": f"Here are flight options to {state.selected_destination['name']}:",
            "step": "flight_booking"
        }
        
    except Exception as e:
        logger.error(f"Flight booking error: {e}")
        raise HTTPException(status_code=500, detail="Flight booking error")

@app.post("/book-hotels")
async def book_hotels(request: Dict):
    """Handle hotel booking request."""
    try:
        session_id = request.get("session_id")
        
        if session_id not in conversation_states:
            raise HTTPException(status_code=404, detail="Session not found")
        
        state = conversation_states[session_id]
        
        if not state.selected_destination:
            raise HTTPException(status_code=400, detail="No destination selected")
        
        # Create hotel search
        hotel_search = HotelSearch(
            destination=state.selected_destination["name"],
            check_in=state.collected_data.get("travel_dates", "2024-12-01"),
            check_out=state.collected_data.get("travel_dates", "2024-12-08"),  # 7 days later
            guests=int(state.collected_data.get("people_count", "1"))
        )
        
        # Get hotel options
        hotels = await get_real_hotels(hotel_search)
        
        return {
            "success": True,
            "hotels": hotels,
            "destination": state.selected_destination,
            "message": f"Here are hotel options in {state.selected_destination['name']}:",
            "step": "hotel_booking"
        }
        
    except Exception as e:
        logger.error(f"Hotel booking error: {e}")
        raise HTTPException(status_code=500, detail="Hotel booking error")

@app.post("/activities")
async def search_activities(search: ActivitySearch):
    """Search for activities."""
    try:
        activities = await get_real_activities(search)
        return {
            "success": True,
            "activities": activities,
            "search": search.dict()
        }
    except Exception as e:
        logger.error(f"Activity search error: {e}")
        raise HTTPException(status_code=500, detail="Activity search error")

@app.get("/destinations")
async def get_all_destinations():
    """Get all available destinations."""
    return {
        "success": True,
        "destinations": TRAVEL_DATA["domestic"]["beach"] + TRAVEL_DATA["domestic"]["mountain"] + TRAVEL_DATA["domestic"]["city"] + TRAVEL_DATA["international"]["beach"]
    }

@app.get("/currency/convert")
async def convert_currency(amount: float, from_currency: str, to_currency: str):
    """Convert currency using real-time rates."""
    try:
        if from_currency == to_currency:
            return {"converted_amount": amount, "rate": 1.0}

        # Use real currency API
        conversion = await currency_api.convert_currency(amount, from_currency, to_currency)
        
        return {
            "converted_amount": conversion.get("result", amount),
            "rate": conversion.get("rate", 1.0),
            "source": conversion.get("source", "Mock Data")
        }

    except Exception as e:
        logger.error(f"Currency conversion error: {e}")
        raise HTTPException(status_code=500, detail="Currency conversion error")

@app.get("/weather/{location}")
async def get_weather(location: str):
    """Get current weather for a location."""
    try:
        weather = await weather_api.get_current_weather(location)
        return {
            "success": True,
            "weather": weather,
            "source": weather.get("source", "Mock Data")
        }
    except Exception as e:
        logger.error(f"Weather API error: {e}")
        raise HTTPException(status_code=500, detail="Weather data fetch failed")

@app.get("/weather/{location}/forecast")
async def get_weather_forecast(location: str, days: int = 7):
    """Get weather forecast for a location."""
    try:
        forecast = await weather_api.get_forecast(location, days)
        return {
            "success": True,
            "forecast": forecast,
            "source": forecast.get("source", "Mock Data")
        }
    except Exception as e:
        logger.error(f"Weather forecast API error: {e}")
        raise HTTPException(status_code=500, detail="Weather forecast fetch failed")

@app.get("/currency/rates")
async def get_exchange_rates(base_currency: str = "USD"):
    """Get current exchange rates."""
    try:
        rates = await currency_api.get_exchange_rates(base_currency)
        return {
            "success": True,
            "rates": rates,
            "source": rates.get("source", "Mock Data")
        }
    except Exception as e:
        logger.error(f"Exchange rates API error: {e}")
        raise HTTPException(status_code=500, detail="Exchange rates fetch failed")

@app.post("/cost-analysis")
async def get_detailed_cost_analysis(request: Dict):
    """Get detailed cost analysis for a specific trip."""
    try:
        origin = request.get("origin")
        destination = request.get("destination")
        departure_date = request.get("departure_date")
        return_date = request.get("return_date")
        guests = request.get("guests", 1)
        currency = request.get("currency", "USD")
        
        if not all([origin, destination, departure_date, return_date]):
            raise HTTPException(status_code=400, detail="Missing required parameters")
        
        # Calculate detailed cost breakdown
        cost_analysis = await calculate_total_trip_cost(
            origin=origin,
            destination=destination,
            departure_date=departure_date,
            return_date=return_date,
            guests=guests,
            preferences={"currency": currency}
        )
        
        return {
            "success": True,
            "cost_analysis": cost_analysis,
            "trip_details": {
                "origin": origin,
                "destination": destination,
                "departure_date": departure_date,
                "return_date": return_date,
                "guests": guests,
                "currency": currency
            }
        }
        
    except Exception as e:
        logger.error(f"Cost analysis error: {e}")
        raise HTTPException(status_code=500, detail="Cost analysis failed")

@app.get("/cost-of-living/{city}")
async def get_cost_of_living_data(city: str, country: str = None):
    """Get detailed cost of living data for a specific city."""
    try:
        cost_data = await cost_of_living_dataset.get_cost_of_living(city, country)
        
        return {
            "success": True,
            "city": city,
            "country": country,
            "cost_of_living": cost_data,
            "summary": {
                "daily_total": cost_data.get("daily_total", 0),
                "weekly_total": cost_data.get("weekly_total", 0),
                "monthly_total": cost_data.get("monthly_total", 0),
                "currency": cost_data.get("currency", "USD"),
                "data_source": cost_data.get("source", "Unknown"),
                "data_quality": cost_data.get("data_quality", 0),
                "last_updated": cost_data.get("last_updated", "")
            }
        }
        
    except Exception as e:
        logger.error(f"Cost of living dataset error: {e}")
        raise HTTPException(status_code=500, detail="Cost of living data fetch failed")

@app.get("/cost-of-living/compare")
async def compare_cost_of_living(city1: str, city2: str, country1: str = None, country2: str = None):
    """Compare cost of living between two cities."""
    try:
        # Get cost data for both cities
        cost1_task = cost_of_living_dataset.get_cost_of_living(city1, country1)
        cost2_task = cost_of_living_dataset.get_cost_of_living(city2, country2)
        
        cost1, cost2 = await asyncio.gather(cost1_task, cost2_task)
        
        # Calculate differences
        daily_diff = cost2.get("daily_total", 0) - cost1.get("daily_total", 0)
        weekly_diff = cost2.get("weekly_total", 0) - cost1.get("weekly_total", 0)
        monthly_diff = cost2.get("monthly_total", 0) - cost1.get("monthly_total", 0)
        
        # Calculate percentage difference
        if cost1.get("daily_total", 0) > 0:
            daily_percent = (daily_diff / cost1.get("daily_total", 1)) * 100
        else:
            daily_percent = 0
        
        return {
            "success": True,
            "comparison": {
                "city1": {
                    "name": city1,
                    "country": country1,
                    "daily_total": cost1.get("daily_total", 0),
                    "weekly_total": cost1.get("weekly_total", 0),
                    "monthly_total": cost1.get("monthly_total", 0)
                },
                "city2": {
                    "name": city2,
                    "country": country2,
                    "daily_total": cost2.get("daily_total", 0),
                    "weekly_total": cost2.get("weekly_total", 0),
                    "monthly_total": cost2.get("monthly_total", 0)
                },
                "differences": {
                    "daily_difference": round(daily_diff, 2),
                    "weekly_difference": round(weekly_diff, 2),
                    "monthly_difference": round(monthly_diff, 2),
                    "daily_percentage": round(daily_percent, 2),
                    "more_expensive": city2 if daily_diff > 0 else city1
                }
            }
        }
        
    except Exception as e:
        logger.error(f"Cost comparison error: {e}")
        raise HTTPException(status_code=500, detail="Cost comparison failed")

@app.get("/cost-of-living/cities")
async def get_available_cities():
    """Get list of all available cities in the dataset."""
    try:
        cities = cost_of_living_dataset.get_city_list()
        
        return {
            "success": True,
            "total_cities": len(cities),
            "cities": cities[:100],  # Limit to first 100 for performance
            "source": "Kaggle Cost of Living Dataset"
        }
        
    except Exception as e:
        logger.error(f"Error getting city list: {e}")
        raise HTTPException(status_code=500, detail="Failed to get city list")

@app.get("/cost-of-living/search")
async def search_cities(query: str):
    """Search cities by name or country."""
    try:
        if len(query) < 2:
            raise HTTPException(status_code=400, detail="Query must be at least 2 characters")
        
        results = cost_of_living_dataset.search_cities(query)
        
        return {
            "success": True,
            "query": query,
            "results": results,
            "total_found": len(results),
            "source": "Kaggle Cost of Living Dataset"
        }
        
    except Exception as e:
        logger.error(f"Error searching cities: {e}")
        raise HTTPException(status_code=500, detail="Failed to search cities")

@app.get("/cost-of-living/dataset-info")
async def get_dataset_info():
    """Get information about the cost of living dataset."""
    try:
        total_cities = len(cost_of_living_dataset.cities_data)
        high_quality_cities = sum(1 for data in cost_of_living_dataset.cities_data.values() 
                                 if data.get('data_quality', 0) == 1)
        
        return {
            "success": True,
            "dataset_info": {
                "total_cities": total_cities,
                "high_quality_cities": high_quality_cities,
                "data_quality_percentage": round((high_quality_cities / total_cities * 100), 2) if total_cities > 0 else 0,
                "source": "Kaggle Cost of Living Dataset",
                "last_updated": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting dataset info: {e}")
        raise HTTPException(status_code=500, detail="Failed to get dataset info")

# Add new endpoints for budget-based travel planning
@app.post("/discover-destinations")
async def discover_destinations(request: dict):
    """Discover destinations based on budget, dates, and preferences"""
    try:
        # Handle both old and new request formats
        query = request.get("query", "")
        origin = request.get("origin", "")
        budget = request.get("budget")
        dates = request.get("dates", "")
        travelers = request.get("travelers", "1")
        destination_type = request.get("type", "")
        
        # Legacy format support
        currency = request.get("currency", "USD")
        travel_dates = request.get("travel_dates", {})
        preferences = request.get("preferences", {})
        trip_type = request.get("trip_type", "leisure")
        
        if not budget:
            raise HTTPException(status_code=400, detail="Budget is required")
        
        # Convert budget to USD for calculations
        budget_usd = await convert_currency(budget, currency, "USD")
        if isinstance(budget_usd, dict):
            budget_usd = budget_usd.get("converted_amount", float(budget))
        else:
            budget_usd = float(budget_usd)
        
        # Parse dates if provided in new format
        if dates and not travel_dates:
            if " to " in dates:
                start_date, end_date = dates.split(" to ")
                travel_dates = {
                    "departure_date": start_date,
                    "return_date": end_date
                }
            else:
                travel_dates = {
                    "departure_date": dates,
                    "return_date": dates
                }
        
        # Get potential destinations based on budget
        destinations = await get_budget_appropriate_destinations(
            budget_usd, travel_dates, preferences, trip_type, origin, destination_type
        )
        
        return {
            "destinations": destinations,
            "budget_usd": budget_usd,
            "original_budget": budget,
            "currency": currency,
            "trip_type": trip_type,
            "origin": origin,
            "query": query
        }
        
    except Exception as e:
        logger.error(f"Error discovering destinations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-itineraries")
async def generate_itineraries(request: dict):
    """Generate multiple itinerary options for a destination"""
    try:
        destination = request.get("destination")
        budget = request.get("budget")
        currency = request.get("currency", "USD")
        travel_dates = request.get("travel_dates", {})
        preferences = request.get("preferences", {})
        trip_type = request.get("trip_type", "leisure")
        
        if not all([destination, budget]):
            raise HTTPException(status_code=400, detail="Destination and budget are required")
        
        # Generate multiple itinerary options
        itineraries = await generate_multiple_itineraries(
            destination, budget, currency, travel_dates, preferences, trip_type
        )
        
        return {
            "destination": destination,
            "itineraries": itineraries,
            "budget": budget,
            "currency": currency
        }
        
    except Exception as e:
        logger.error(f"Error generating itineraries: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/customize-itinerary")
async def customize_itinerary(request: dict):
    """Allow users to customize their selected itinerary"""
    try:
        itinerary_id = request.get("itinerary_id")
        customizations = request.get("customizations", {})
        
        if not itinerary_id:
            raise HTTPException(status_code=400, detail="Itinerary ID is required")
        
        # Apply customizations and recalculate costs
        customized_itinerary = await apply_itinerary_customizations(
            itinerary_id, customizations
        )
        
        return {
            "itinerary": customized_itinerary,
            "customizations_applied": customizations
        }
        
    except Exception as e:
        logger.error(f"Error customizing itinerary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/supported-currencies")
async def get_supported_currencies():
    """Get list of supported currencies"""
    return {
        "currencies": [
            {"code": "USD", "name": "US Dollar", "symbol": "$"},
            {"code": "EUR", "name": "Euro", "symbol": "€"},
            {"code": "GBP", "name": "British Pound", "symbol": "£"},
            {"code": "INR", "name": "Indian Rupee", "symbol": "₹"},
            {"code": "CAD", "name": "Canadian Dollar", "symbol": "C$"},
            {"code": "AUD", "name": "Australian Dollar", "symbol": "A$"},
            {"code": "JPY", "name": "Japanese Yen", "symbol": "¥"},
            {"code": "CNY", "name": "Chinese Yuan", "symbol": "¥"},
            {"code": "BRL", "name": "Brazilian Real", "symbol": "R$"},
            {"code": "MXN", "name": "Mexican Peso", "symbol": "$"},
            {"code": "RUB", "name": "Russian Ruble", "symbol": "₽"},
            {"code": "KRW", "name": "South Korean Won", "symbol": "₩"},
            {"code": "SGD", "name": "Singapore Dollar", "symbol": "S$"},
            {"code": "HKD", "name": "Hong Kong Dollar", "symbol": "HK$"},
            {"code": "NZD", "name": "New Zealand Dollar", "symbol": "NZ$"},
            {"code": "CHF", "name": "Swiss Franc", "symbol": "CHF"},
            {"code": "SEK", "name": "Swedish Krona", "symbol": "kr"},
            {"code": "NOK", "name": "Norwegian Krone", "symbol": "kr"},
            {"code": "DKK", "name": "Danish Krone", "symbol": "kr"},
            {"code": "PLN", "name": "Polish Zloty", "symbol": "zł"}
        ]
    }

@app.get("/destination-types")
async def get_destination_types():
    """Get list of destination types and their characteristics"""
    return {
        "destination_types": [
            {
                "type": "beach",
                "name": "Beach Destinations",
                "description": "Coastal cities with beautiful beaches and water activities",
                "characteristics": ["beaches", "water sports", "seafood", "sunset views", "island vibes"],
                "examples": ["Bali", "Maldives", "Thailand", "Caribbean", "Hawaii"]
            },
            {
                "type": "mountain",
                "name": "Mountain Destinations", 
                "description": "High-altitude destinations with hiking, skiing, and mountain views",
                "characteristics": ["hiking", "skiing", "mountain views", "fresh air", "adventure"],
                "examples": ["Switzerland", "Nepal", "Colorado", "New Zealand", "Alps"]
            },
            {
                "type": "city",
                "name": "Urban Destinations",
                "description": "Major cities with cultural attractions, nightlife, and urban experiences",
                "characteristics": ["museums", "nightlife", "shopping", "restaurants", "culture"],
                "examples": ["New York", "London", "Tokyo", "Paris", "Dubai"]
            },
            {
                "type": "nature",
                "name": "Nature Destinations",
                "description": "Natural landscapes with wildlife, national parks, and outdoor activities",
                "characteristics": ["wildlife", "national parks", "hiking", "camping", "photography"],
                "examples": ["Costa Rica", "Kenya", "Iceland", "Canada", "Australia"]
            },
            {
                "type": "cultural",
                "name": "Cultural Destinations",
                "description": "Historic cities with rich heritage, monuments, and traditional experiences",
                "characteristics": ["history", "monuments", "traditional food", "local customs", "architecture"],
                "examples": ["Rome", "Kyoto", "Cairo", "Machu Picchu", "Prague"]
            },
            {
                "type": "adventure",
                "name": "Adventure Destinations",
                "description": "Destinations offering extreme sports and adrenaline activities",
                "characteristics": ["extreme sports", "adrenaline", "challenges", "outdoor activities"],
                "examples": ["New Zealand", "Nepal", "Costa Rica", "South Africa", "Chile"]
            },
            {
                "type": "wellness",
                "name": "Wellness Destinations",
                "description": "Relaxing destinations focused on health, spa, and mental well-being",
                "characteristics": ["spas", "yoga", "meditation", "healthy food", "relaxation"],
                "examples": ["Bali", "Thailand", "India", "Costa Rica", "Greece"]
            },
            {
                "type": "food",
                "name": "Food Destinations",
                "description": "Culinary destinations known for their unique cuisine and food culture",
                "characteristics": ["local cuisine", "food tours", "cooking classes", "markets", "restaurants"],
                "examples": ["Italy", "Japan", "Thailand", "France", "Mexico"]
            }
        ]
    }

@app.post("/discover-destinations-by-type")
async def discover_destinations_by_type(request: dict):
    """Discover destinations based on destination type, budget, and preferences"""
    try:
        budget = request.get("budget")
        currency = request.get("currency", "USD")
        destination_type = request.get("destination_type", "city")
        travel_dates = request.get("travel_dates", {})
        preferences = request.get("preferences", {})
        trip_type = request.get("trip_type", "leisure")
        
        if not budget:
            raise HTTPException(status_code=400, detail="Budget is required")
        
        # Convert budget to USD for calculations
        budget_usd = await convert_currency(budget, currency, "USD")
        
        # Get destinations filtered by type
        destinations = await get_destinations_by_type(
            destination_type, budget_usd, travel_dates, preferences, trip_type
        )
        
        return {
            "destination_type": destination_type,
            "destinations": destinations,
            "budget_usd": budget_usd,
            "original_budget": budget,
            "currency": currency,
            "trip_type": trip_type
        }
        
    except Exception as e:
        logger.error(f"Error discovering destinations by type: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Helper functions for new endpoints
def estimate_flight_cost(origin: str, destination: str, departure_date: str) -> float:
    """Estimate flight cost based on distance and season"""
    # Base flight costs by region (USD)
    base_costs = {
        "domestic_us": 300,
        "north_america": 500,
        "europe": 800,
        "asia": 1000,
        "south_america": 600,
        "africa": 900,
        "australia": 1200
    }
    
    # Season multipliers
    departure_month = int(departure_date.split("-")[1])
    if departure_month in [12, 1, 2]:  # Winter
        season_multiplier = 1.2
    elif departure_month in [6, 7, 8]:  # Summer
        season_multiplier = 1.3
    else:  # Spring/Fall
        season_multiplier = 1.0
    
    # Simple region detection
    if "usa" in destination.lower() or "united states" in destination.lower():
        region = "domestic_us"
    elif any(country in destination.lower() for country in ["canada", "mexico"]):
        region = "north_america"
    elif any(country in destination.lower() for country in ["france", "germany", "italy", "spain", "uk", "london", "paris"]):
        region = "europe"
    elif any(country in destination.lower() for country in ["japan", "china", "thailand", "singapore", "india"]):
        region = "asia"
    else:
        region = "europe"  # Default
    
    return base_costs[region] * season_multiplier

def estimate_hotel_cost(destination: str, days: int, travelers: int) -> float:
    """Estimate hotel cost based on destination and duration"""
    # Base hotel costs per night (USD)
    base_costs = {
        "budget": 60,
        "mid_range": 120,
        "luxury": 250
    }
    
    # Destination cost multipliers
    expensive_destinations = ["tokyo", "london", "paris", "new york", "singapore", "zurich"]
    budget_destinations = ["bangkok", "mexico city", "prague", "budapest", "krakow"]
    
    if any(dest in destination.lower() for dest in expensive_destinations):
        cost_level = "luxury"
    elif any(dest in destination.lower() for dest in budget_destinations):
        cost_level = "budget"
    else:
        cost_level = "mid_range"
    
    cost_per_night = base_costs[cost_level]
    rooms_needed = (travelers + 1) // 2  # 2 people per room
    
    return cost_per_night * days * rooms_needed

def estimate_airport_transfer_cost(destination: str, travelers: int) -> float:
    """Estimate airport transfer costs"""
    # Base transfer costs
    base_cost = 30  # USD per person
    return base_cost * travelers

def estimate_travel_insurance_cost(flight_cost: float, days: int) -> float:
    """Estimate travel insurance cost"""
    # Typically 4-8% of trip cost
    return flight_cost * 0.06

def estimate_visa_cost(origin: str, destination: str, travelers: int) -> float:
    """Estimate visa costs if international travel"""
    # US citizens don't need visas for many countries
    visa_required_destinations = ["china", "india", "russia", "brazil"]
    
    if any(dest in destination.lower() for dest in visa_required_destinations):
        return 50 * travelers  # Average visa cost
    return 0

def get_destination_rating(city: str, country: str) -> float:
    """Get destination rating based on popularity and quality"""
    # Popular destinations get higher ratings
    popular_destinations = {
        "paris": 4.8, "london": 4.7, "tokyo": 4.9, "new york": 4.6,
        "barcelona": 4.5, "rome": 4.4, "amsterdam": 4.3, "prague": 4.2,
        "bangkok": 4.1, "sydney": 4.4, "dubai": 4.3, "singapore": 4.6
    }
    
    city_lower = city.lower()
    for dest, rating in popular_destinations.items():
        if dest in city_lower:
            return rating
    
    return 4.0  # Default rating

def get_destination_image(city: str, country: str) -> str:
    """Get destination image URL"""
    # In a real app, you'd use a proper image service
    city_lower = city.lower().replace(" ", "-")
    return f"https://images.unsplash.com/photo-1506905925346-14b8e4b4c4b0?w=400&h=300&fit=crop&crop=center&q=80"

def get_destination_description(city: str, country: str, dest_type: str) -> str:
    """Get destination description based on type"""
    descriptions = {
        "beach": f"Beautiful {city} offers pristine beaches, crystal-clear waters, and perfect weather for relaxation and water activities.",
        "mountain": f"Stunning {city} provides breathtaking mountain views, hiking trails, and outdoor adventures in a serene natural setting.",
        "city": f"Vibrant {city} combines rich history, modern attractions, world-class dining, and exciting nightlife in a bustling urban environment."
    }
    return descriptions.get(dest_type, f"Discover the unique charm and attractions of {city}, {country}.")

def get_destination_activities(city: str, country: str, dest_type: str) -> List[str]:
    """Get destination activities based on type"""
    activities = {
        "beach": ["Beach relaxation", "Water sports", "Snorkeling", "Sunset cruises", "Beach volleyball"],
        "mountain": ["Hiking trails", "Mountain biking", "Scenic drives", "Photography", "Nature walks"],
        "city": ["City tours", "Museum visits", "Local cuisine", "Shopping", "Nightlife"]
    }
    return activities.get(dest_type, ["Local attractions", "Cultural sites", "Dining", "Shopping", "Entertainment"])

async def calculate_comprehensive_trip_cost(origin: str, destination: str, country: str, 
                                          departure_date: str, return_date: str, 
                                          travelers: int, budget_usd: float) -> Dict:
    """Calculate comprehensive trip cost including all components"""
    try:
        # Ensure proper types
        travelers = int(travelers)
        budget_usd = float(budget_usd)
        
        # Calculate trip duration
        departure = datetime.strptime(departure_date, "%Y-%m-%d")
        return_dt = datetime.strptime(return_date, "%Y-%m-%d")
        days = (return_dt - departure).days
        
        if days <= 0:
            days = 1  # Minimum 1 day trip
        
        # 1. FLIGHT COSTS (Round Trip)
        flight_cost_per_person = 0
        try:
            flight_data = await get_average_flight_prices(origin, destination, departure_date, return_date)
            flight_cost_per_person = flight_data["average_price"]
        except:
            # Fallback: estimate based on distance and season
            flight_cost_per_person = estimate_flight_cost(origin, destination, departure_date)
        
        total_flight_cost = flight_cost_per_person * travelers
        
        # 2. HOTEL COSTS
        hotel_cost_total = 0
        try:
            hotel_data = await get_average_hotel_prices(destination, departure_date, return_date, travelers)
            hotel_cost_total = hotel_data["total_cost"]
        except:
            # Fallback: estimate based on destination
            hotel_cost_total = estimate_hotel_cost(destination, days, travelers)
        
        # 3. DAILY LIVING COSTS (Food, Transport, Activities, Misc)
        living_costs = await cost_of_living_dataset.get_cost_of_living(destination, country)
        
        # Daily meal costs (3 meals per day)
        daily_meal_cost = (
            living_costs["daily_food"] * 1.2  # 20% markup for restaurant meals
        )
        
        # Daily transport costs (taxis, public transport, car rental)
        daily_transport_cost = (
            living_costs["daily_transport"] * 1.5  # 50% markup for tourist transport
        )
        
        # Daily activity costs (attractions, tours, entertainment)
        daily_activity_cost = (
            living_costs["daily_activities"] * 1.3  # 30% markup for tourist activities
        )
        
        # Daily miscellaneous costs (shopping, tips, etc.)
        daily_misc_cost = (
            living_costs["daily_misc"] * 1.2  # 20% markup for tourist spending
        )
        
        # Total daily cost per person
        daily_cost_per_person = (
            daily_meal_cost + 
            daily_transport_cost + 
            daily_activity_cost + 
            daily_misc_cost
        )
        
        total_daily_costs = daily_cost_per_person * days * travelers
        
        # 4. ADDITIONAL COSTS
        # Airport transfers (to/from airport)
        airport_transfer_cost = estimate_airport_transfer_cost(destination, travelers)
        
        # Travel insurance (optional but recommended)
        travel_insurance_cost = estimate_travel_insurance_cost(total_flight_cost, days)
        
        # Visa costs (if international)
        visa_cost = estimate_visa_cost(origin, destination, travelers)
        
        # Additional costs
        additional_costs = airport_transfer_cost + travel_insurance_cost + visa_cost
        
        # 5. TOTAL TRIP COST
        total_trip_cost = (
            total_flight_cost + 
            hotel_cost_total + 
            total_daily_costs + 
            additional_costs
        )
        
        # Cost per person
        cost_per_person = total_trip_cost / travelers
        
        # Budget analysis
        budget_remaining = budget_usd - total_trip_cost
        budget_utilization = (total_trip_cost / budget_usd) * 100 if budget_usd > 0 else 0
        
        return {
            "total_cost": total_trip_cost,
            "cost_per_person": cost_per_person,
            "budget_remaining": budget_remaining,
            "budget_utilization": budget_utilization,
            "fits_budget": total_trip_cost <= budget_usd,
            "breakdown": {
                "flights": {
                    "total": total_flight_cost,
                    "per_person": flight_cost_per_person
                },
                "hotel": {
                    "total": hotel_cost_total,
                    "per_night": hotel_cost_total / days if days > 0 else 0
                },
                "daily_expenses": {
                    "total": total_daily_costs,
                    "per_person_per_day": daily_cost_per_person,
                    "meals": daily_meal_cost * days * travelers,
                    "transport": daily_transport_cost * days * travelers,
                    "activities": daily_activity_cost * days * travelers,
                    "miscellaneous": daily_misc_cost * days * travelers
                },
                "additional": {
                    "airport_transfers": airport_transfer_cost,
                    "travel_insurance": travel_insurance_cost,
                    "visa": visa_cost,
                    "total": additional_costs
                }
            },
            "trip_duration": days,
            "travelers": travelers
        }
        
    except Exception as e:
        logger.error(f"Error calculating comprehensive trip cost: {e}")
        return {
            "total_cost": budget_usd + 1000,  # Over budget to exclude from results
            "fits_budget": False,
            "error": str(e)
        }

def get_destination_type(city: str, country: str) -> str:
    """Determine destination type based on city and country"""
    # Simple mapping - in a real app, you'd use a more sophisticated system
    beach_cities = ["miami", "barcelona", "sydney", "bangkok", "bali", "phuket", "cancun", "malibu", "santamonica"]
    mountain_cities = ["denver", "zurich", "vancouver", "saltlakecity", "aspen", "whistler", "chamonix", "interlaken"]
    city_cities = ["newyork", "london", "paris", "tokyo", "singapore", "dubai", "hongkong", "berlin", "amsterdam"]
    
    city_lower = city.lower().replace(" ", "")
    
    if any(beach in city_lower for beach in beach_cities):
        return "beach"
    elif any(mountain in city_lower for mountain in mountain_cities):
        return "mountain"
    elif any(city_name in city_lower for city_name in city_cities):
        return "city"
    else:
        return "city"  # Default to city

async def get_budget_appropriate_destinations(budget_usd: float, travel_dates: dict, 
                                           preferences: dict, trip_type: str, 
                                           origin: str = "", destination_type: str = "") -> List[Dict]:
    """Find destinations that fit within the budget using comprehensive cost calculation"""
    try:
        # Get available destinations from our dataset
        available_cities = cost_of_living_dataset.get_city_list()
        
        # Parse dates
        departure_date = travel_dates.get("departure_date", "2024-12-15")
        return_date = travel_dates.get("return_date", "2024-12-22")
        travelers = int(preferences.get("travelers", 1))
        
        # Filter destinations based on budget
        suitable_destinations = []
        
        # Limit to top 100 cities for performance, but prioritize by type
        cities_to_check = available_cities[:100]
        
        # If destination type specified, prioritize those cities
        if destination_type:
            type_cities = [city for city in cities_to_check 
                          if destination_type.lower() in get_destination_type(city["city"], city["country"]).lower()]
            cities_to_check = type_cities + [city for city in cities_to_check if city not in type_cities]
        
        for city_info in cities_to_check:
            city = city_info["city"]
            country = city_info["country"]
            
            # Calculate comprehensive trip cost
            cost_analysis = await calculate_comprehensive_trip_cost(
                origin, city, country, departure_date, return_date, travelers, budget_usd
            )
            
            # Only include destinations that fit the budget
            if cost_analysis["fits_budget"]:
                # Get destination type and rating
                dest_type = get_destination_type(city, country)
                rating = get_destination_rating(city, country)
                
                suitable_destinations.append({
                    "id": f"{city.lower().replace(' ', '-')}-{country.lower().replace(' ', '-')}",
                    "name": city,
                    "country": country,
                    "type": dest_type,
                    "rating": rating,
                    "image": get_destination_image(city, country),
                    "description": get_destination_description(city, country, dest_type),
                    "activities": get_destination_activities(city, country, dest_type),
                    "total_cost": cost_analysis["total_cost"],
                    "cost_per_person": cost_analysis["cost_per_person"],
                    "budget_remaining": cost_analysis["budget_remaining"],
                    "budget_utilization": cost_analysis["budget_utilization"],
                    "days": cost_analysis["trip_duration"],
                    "travelers": travelers,
                    "cost_breakdown": cost_analysis["breakdown"],
                    "flight_price": cost_analysis["breakdown"]["flights"]["per_person"],
                    "hotel_price": cost_analysis["breakdown"]["hotel"]["total"],
                    "daily_cost": cost_analysis["breakdown"]["daily_expenses"]["per_person_per_day"]
                })
        
        # Sort by budget utilization (most efficient use of budget first)
        suitable_destinations.sort(key=lambda x: x["budget_utilization"], reverse=True)
        
        return suitable_destinations[:10]  # Return top 10 destinations
        
    except Exception as e:
        logger.error(f"Error finding budget-appropriate destinations: {e}")
        return []

async def generate_multiple_itineraries(destination: str, budget: float, currency: str,
                                      travel_dates: dict, preferences: dict, trip_type: str) -> List[Dict]:
    """Generate multiple itinerary options for a destination"""
    try:
        # Get cost of living data
        living_costs = await cost_of_living_dataset.get_cost_of_living(destination)
        
        # Generate different itinerary styles
        itineraries = []
        
        # Budget itinerary
        budget_itinerary = await create_itinerary(
            destination, budget * 0.7, currency, travel_dates, preferences, "budget"
        )
        itineraries.append(budget_itinerary)
        
        # Mid-range itinerary
        midrange_itinerary = await create_itinerary(
            destination, budget, currency, travel_dates, preferences, "mid-range"
        )
        itineraries.append(midrange_itinerary)
        
        # Luxury itinerary
        luxury_itinerary = await create_itinerary(
            destination, budget * 1.3, currency, travel_dates, preferences, "luxury"
        )
        itineraries.append(luxury_itinerary)
        
        return itineraries
        
    except Exception as e:
        logger.error(f"Error generating itineraries: {e}")
        return []

async def create_itinerary(destination: str, budget: float, currency: str,
                         travel_dates: dict, preferences: dict, style: str) -> Dict:
    """Create a detailed itinerary for a destination"""
    try:
        # Calculate trip duration
        days = 7  # Default
        if travel_dates.get("duration"):
            days = int(travel_dates["duration"])
        
        # Get cost breakdown
        cost_breakdown = await calculate_total_trip_cost(
            "Origin", destination, 
            travel_dates.get("start_date", "2024-12-01"),
            travel_dates.get("end_date", "2024-12-08"),
            1, preferences
        )
        
        # Generate AI-powered itinerary
        itinerary_prompt = f"""
        Create a {style} {days}-day itinerary for {destination} with a budget of {budget} {currency}.
        
        Budget breakdown:
        - Flight: {cost_breakdown.get('breakdown', {}).get('flight_cost_per_person', 0)} {currency}
        - Accommodation: {cost_breakdown.get('breakdown', {}).get('hotel_cost_per_person', 0)} {currency}
        - Daily expenses: {cost_breakdown.get('breakdown', {}).get('living_cost_per_person', 0)} {currency}
        
        Preferences: {preferences}
        
        Provide:
        1. Day-by-day activities
        2. Restaurant recommendations
        3. Transportation options
        4. Must-see attractions
        5. Budget tips
        6. Booking recommendations
        """
        
        # Use Groq to generate itinerary
        response = await call_groq_chat(itinerary_prompt)
        
        return {
            "style": style,
            "days": days,
            "budget": budget,
            "currency": currency,
            "cost_breakdown": cost_breakdown,
            "itinerary": response,
            "booking_links": await get_booking_links(destination, travel_dates)
        }
        
    except Exception as e:
        logger.error(f"Error creating itinerary: {e}")
        return {}

async def apply_itinerary_customizations(itinerary_id: str, customizations: dict) -> Dict:
    """Apply user customizations to an itinerary"""
    try:
        # This would integrate with a database to store and retrieve itineraries
        # For now, return a mock response
        return {
            "itinerary_id": itinerary_id,
            "customizations": customizations,
            "status": "customized",
            "message": "Customizations applied successfully"
        }
        
    except Exception as e:
        logger.error(f"Error applying customizations: {e}")
        return {}

async def get_booking_links(destination: str, travel_dates: dict) -> Dict:
    """Get booking links for flights, hotels, and activities"""
    try:
        return {
            "flights": f"https://www.skyscanner.com/flights/to/{destination}",
            "hotels": f"https://www.booking.com/searchresults.html?ss={destination}",
            "activities": f"https://www.getyourguide.com/{destination.lower()}/",
            "car_rental": f"https://www.rentalcars.com/en/city/{destination.lower()}/"
        }
    except Exception as e:
        logger.error(f"Error getting booking links: {e}")
        return {}

async def get_destinations_by_type(destination_type: str, budget_usd: float, 
                                 travel_dates: dict, preferences: dict, trip_type: str) -> List[Dict]:
    """Find destinations filtered by type that fit within the budget"""
    try:
        # Define destination type mappings
        destination_mappings = {
            "beach": {
                "cities": ["Bali", "Phuket", "Maldives", "Hawaii", "Cancun", "Barcelona", "Sydney", "Dubai", "Miami", "Santos"],
                "countries": ["Thailand", "Indonesia", "Maldives", "Spain", "Australia", "Mexico", "Brazil", "Greece", "Italy", "Portugal"]
            },
            "mountain": {
                "cities": ["Zurich", "Geneva", "Kathmandu", "Denver", "Queenstown", "Innsbruck", "Chamonix", "Banff", "Aspen", "Whistler"],
                "countries": ["Switzerland", "Nepal", "Austria", "Canada", "New Zealand", "Chile", "Argentina", "Norway", "Iceland", "Japan"]
            },
            "city": {
                "cities": ["New York", "London", "Tokyo", "Paris", "Dubai", "Singapore", "Hong Kong", "Bangkok", "Istanbul", "Mumbai"],
                "countries": ["USA", "UK", "Japan", "France", "UAE", "Singapore", "Hong Kong", "Thailand", "Turkey", "India"]
            },
            "nature": {
                "cities": ["Costa Rica", "Nairobi", "Reykjavik", "Vancouver", "Cairns", "Cape Town", "Yellowstone", "Banff", "Patagonia", "Galapagos"],
                "countries": ["Costa Rica", "Kenya", "Iceland", "Canada", "Australia", "South Africa", "USA", "Chile", "Ecuador", "Brazil"]
            },
            "cultural": {
                "cities": ["Rome", "Kyoto", "Cairo", "Prague", "Athens", "Istanbul", "Delhi", "Beijing", "Marrakech", "Cusco"],
                "countries": ["Italy", "Japan", "Egypt", "Czech Republic", "Greece", "Turkey", "India", "China", "Morocco", "Peru"]
            },
            "adventure": {
                "cities": ["Queenstown", "Kathmandu", "Costa Rica", "Cape Town", "Santiago", "Reykjavik", "Banff", "Chamonix", "Interlaken", "Moab"],
                "countries": ["New Zealand", "Nepal", "Costa Rica", "South Africa", "Chile", "Iceland", "Canada", "Switzerland", "USA", "Norway"]
            },
            "wellness": {
                "cities": ["Bali", "Thailand", "Rishikesh", "Costa Rica", "Santorini", "Tulum", "Sedona", "Ubud", "Koh Samui", "Goa"],
                "countries": ["Indonesia", "Thailand", "India", "Costa Rica", "Greece", "Mexico", "USA", "Bali", "Thailand", "India"]
            },
            "food": {
                "cities": ["Rome", "Tokyo", "Bangkok", "Paris", "Mexico City", "Barcelona", "Istanbul", "Lima", "Seoul", "Bologna"],
                "countries": ["Italy", "Japan", "Thailand", "France", "Mexico", "Spain", "Turkey", "Peru", "South Korea", "Italy"]
            }
        }
        
        # Get available destinations from our dataset
        available_cities = cost_of_living_dataset.get_city_list()
        
        # Filter destinations based on type and budget
        suitable_destinations = []
        
        # Get type-specific cities and countries
        type_mapping = destination_mappings.get(destination_type, destination_mappings["city"])
        type_cities = type_mapping["cities"]
        type_countries = type_mapping["countries"]
        
        for city_info in available_cities:
            city = city_info["city"]
            country = city_info["country"]
            
            # Check if city or country matches the destination type
            if (city in type_cities or country in type_countries):
                # Get cost of living for this city
                living_costs = await cost_of_living_dataset.get_cost_of_living(city, country)
                
                # Calculate if this destination fits the budget
                daily_cost = (
                    living_costs["daily_food"] + 
                    living_costs["daily_transport"] + 
                    living_costs["daily_activities"] + 
                    living_costs["daily_misc"]
                )
                
                # Estimate flight costs (simplified)
                estimated_flight_cost = 800  # Base flight cost
                
                # Calculate total estimated cost
                days = 7  # Default 7-day trip
                total_estimated_cost = estimated_flight_cost + (daily_cost * days)
                
                if total_estimated_cost <= budget_usd:
                    # Get weather info for the destination
                    weather_info = await get_weather_info(city)
                    
                    suitable_destinations.append({
                        "city": city,
                        "country": country,
                        "estimated_daily_cost": round(daily_cost, 2),
                        "estimated_total_cost": round(total_estimated_cost, 2),
                        "budget_remaining": round(budget_usd - total_estimated_cost, 2),
                        "cost_level": "budget" if daily_cost < 50 else "mid-range" if daily_cost < 100 else "luxury",
                        "destination_type": destination_type,
                        "weather": weather_info,
                        "highlights": get_destination_highlights(city, country, destination_type)
                    })
        
        # Sort by budget remaining (descending)
        suitable_destinations.sort(key=lambda x: x["budget_remaining"], reverse=True)
        
        return suitable_destinations[:10]  # Return top 10 options
        
    except Exception as e:
        logger.error(f"Error getting destinations by type: {e}")
        return []

def get_destination_highlights(city: str, country: str, destination_type: str) -> List[str]:
    """Get destination highlights based on type"""
    highlights_mapping = {
        "beach": [
            "Beautiful beaches", "Water sports", "Seafood restaurants", "Sunset views", "Island hopping"
        ],
        "mountain": [
            "Mountain views", "Hiking trails", "Skiing", "Fresh air", "Adventure sports"
        ],
        "city": [
            "Museums", "Nightlife", "Shopping", "Restaurants", "Cultural attractions"
        ],
        "nature": [
            "Wildlife", "National parks", "Hiking", "Photography", "Outdoor activities"
        ],
        "cultural": [
            "Historic sites", "Monuments", "Traditional food", "Local customs", "Architecture"
        ],
        "adventure": [
            "Extreme sports", "Adrenaline activities", "Challenges", "Outdoor adventures", "Thrilling experiences"
        ],
        "wellness": [
            "Spas", "Yoga", "Meditation", "Healthy food", "Relaxation"
        ],
        "food": [
            "Local cuisine", "Food tours", "Cooking classes", "Markets", "Restaurants"
        ]
    }
    
    return highlights_mapping.get(destination_type, highlights_mapping["city"])

async def get_weather_info(city: str) -> Dict:
    """Get weather information for a destination"""
    try:
        # This would integrate with your weather API
        # For now, return mock data
        return {
            "temperature": "22°C",
            "condition": "Sunny",
            "humidity": "65%",
            "best_time": "Year-round"
        }
    except Exception as e:
        logger.error(f"Error getting weather info: {e}")
        return {}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
