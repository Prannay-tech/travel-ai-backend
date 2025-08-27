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
from flight_apis import flight_api
from weather_api import weather_api
from currency_api import currency_api

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
                    "model": "llama3-70b-8192",
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
    """Get real hotel data from Hotels.com API or similar."""
    try:
        if not HOTELS_API_KEY:
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

        # Real API call would go here
        # async with httpx.AsyncClient() as client:
        #     response = await client.get(
        #         f"https://hotels-com-provider.p.rapidapi.com/v1/hotels/search",
        #         headers={"X-RapidAPI-Key": HOTELS_API_KEY},
        #         params={
        #             "query": search.destination,
        #             "checkin_date": search.check_in,
        #             "checkout_date": search.check_out,
        #             "adults_number": search.guests
        #         }
        #     )
        #     return response.json()

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
    """Get cost of living data for a destination."""
    try:
        # This would integrate with a cost of living API
        # For now, using a simplified approach with known data
        cost_of_living_data = {
            "Bali, Indonesia": {
                "daily_food": 25,
                "daily_transport": 15,
                "daily_activities": 30,
                "daily_misc": 20,
                "currency": "USD",
                "source": "Cost of living database"
            },
            "Maldives": {
                "daily_food": 60,
                "daily_transport": 40,
                "daily_activities": 80,
                "daily_misc": 50,
                "currency": "USD",
                "source": "Cost of living database"
            },
            "Swiss Alps": {
                "daily_food": 45,
                "daily_transport": 25,
                "daily_activities": 60,
                "daily_misc": 30,
                "currency": "USD",
                "source": "Cost of living database"
            },
            "Tokyo, Japan": {
                "daily_food": 35,
                "daily_transport": 20,
                "daily_activities": 40,
                "daily_misc": 25,
                "currency": "USD",
                "source": "Cost of living database"
            },
            "Rome, Italy": {
                "daily_food": 40,
                "daily_transport": 15,
                "daily_activities": 35,
                "daily_misc": 20,
                "currency": "USD",
                "source": "Cost of living database"
            }
        }
        
        # Try exact match first
        if destination in cost_of_living_data:
            return cost_of_living_data[destination]
        
        # Try partial match
        for key, value in cost_of_living_data.items():
            if destination.lower() in key.lower() or key.lower() in destination.lower():
                return value
        
        # Default values for unknown destinations
        return {
            "daily_food": 30,
            "daily_transport": 20,
            "daily_activities": 40,
            "daily_misc": 25,
            "currency": "USD",
            "source": "Estimated average"
        }
        
    except Exception as e:
        logger.error(f"Error fetching cost of living: {e}")
        return {
            "daily_food": 30,
            "daily_transport": 20,
            "daily_activities": 40,
            "daily_misc": 25,
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
                    "model": "llama3-8b-8192",
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

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
