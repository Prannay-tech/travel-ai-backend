"""
Comprehensive Travel AI Backend - AI-powered travel planning with booking integration.
Features: AI chat, destination recommendations, flight booking, hotel booking, activity planning.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import httpx
import os
from dotenv import load_dotenv
import logging
from datetime import datetime, timedelta
import json

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
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")
GROQ_BASE_URL = "https://api.groq.com/openai/v1/chat/completions"

# Real API Keys from environment variables
SKYSCANNER_API_KEY = os.getenv("SKYSCANNER_API_KEY", "")
AMADEUS_CLIENT_ID = os.getenv("AMADEUS_CLIENT_ID", "8W8ZGIcN61pNWmljxuc350cSGFUGXTCv")
AMADEUS_CLIENT_SECRET = os.getenv("AMADEUS_CLIENT_SECRET", "4d7fY8brcLFkHMcG")
HOTELS_API_KEY = os.getenv("HOTELS_API_KEY", "")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "0199245a95814f5a968202129251607")
GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY", "")
CURRENCY_API_KEY = os.getenv("CURRENCY_API_KEY", "sk-vasW68a7a30dd9e7f619")

# Import flight search API
from flight_apis import flight_api
from weather_api import weather_api
from currency_api import currency_api

# Pydantic Models
class ChatMessage(BaseModel):
    message: str
    session_id: str = "default-session"
    conversation_history: Optional[List[Dict[str, str]]] = None

# Conversation state management
conversation_states = {}

class ConversationState(BaseModel):
    session_id: str
    current_step: str = "welcome"
    collected_data: Dict = {}
    messages: List[Dict[str, str]] = []

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

# AI System Prompt for Travel Planning
AI_SYSTEM_PROMPT = """
You are an expert AI travel planner. Guide users through a structured conversation to collect their travel preferences.

CONVERSATION FLOW:
1. WELCOME: Greet and ask where they're traveling from
2. DESTINATION_TYPE: Ask about type of destination (beach, mountain, city, etc.)
3. BUDGET: Ask about budget per person
4. DATES: Ask about travel dates
5. RECOMMENDATIONS: Provide personalized recommendations

IMPORTANT RULES:
- Always acknowledge the information they provide
- Ask ONE question at a time
- Don't repeat the same question if they've already answered
- Be conversational and friendly
- If they mention multiple things, acknowledge all and focus on the next missing piece

EXAMPLE RESPONSES:
- "Great! I see you're traveling from Dallas. What type of destination are you looking for? Beach, mountain, city, or something else?"
- "Perfect! A beach destination sounds amazing. What's your budget per person for this trip?"
- "Excellent! With a $2000 budget, I can suggest some fantastic beach destinations. When are you planning to travel?"
- Travel type: "domestic" or "international"
- Destination type: "beach", "mountain", "city", "historic", "religious", "adventure", "relaxing"
- Travel dates (e.g., "next summer", "December 2024")
- Currency preference (e.g., "USD", "EUR", "GBP")
- Additional preferences (e.g., "romantic getaway", "family-friendly")

Always respond in a friendly, helpful manner. If you need more information, ask specific questions.
"""

# Enhanced Travel Data with Real Destinations
TRAVEL_DATA = {
    "domestic": {
        "beach": [
            {
                "id": 1,
                "name": "Miami Beach, Florida",
                "type": "beach",
                "country": "USA",
                "description": "Sunny beaches with vibrant nightlife and culture",
                "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800",
                "rating": 4.6,
                "cost_per_person": {"USD": 800, "EUR": 680, "GBP": 584},
                "highlights": ["Beaches", "Nightlife", "Culture", "Shopping"],
                "best_time": "March-May, September-November",
                "flight_time": "2-4 hours",
                "currency": "USD",
                "daily_cost_usd": 80,
                "flight_cost_usd": 200
            },
            {
                "id": 2,
                "name": "Hawaii, USA",
                "type": "beach",
                "country": "USA",
                "description": "Paradise islands with stunning beaches and volcanoes",
                "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800",
                "rating": 4.8,
                "cost_per_person": {"USD": 1500, "EUR": 1275, "GBP": 1095},
                "highlights": ["Beaches", "Volcanoes", "Culture", "Adventure"],
                "best_time": "April-October",
                "flight_time": "8-12 hours",
                "currency": "USD",
                "daily_cost_usd": 120,
                "flight_cost_usd": 400
            }
        ],
        "mountain": [
            {
                "id": 3,
                "name": "Rocky Mountains, Colorado",
                "type": "mountain",
                "country": "USA",
                "description": "Majestic mountains perfect for skiing and hiking",
                "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800",
                "rating": 4.7,
                "cost_per_person": {"USD": 1000, "EUR": 850, "GBP": 730},
                "highlights": ["Skiing", "Hiking", "Scenic Views", "Adventure"],
                "best_time": "December-March (skiing), June-September (hiking)",
                "flight_time": "3-6 hours",
                "currency": "USD",
                "daily_cost_usd": 100,
                "flight_cost_usd": 300
            }
        ],
        "city": [
            {
                "id": 4,
                "name": "New York City",
                "type": "city",
                "country": "USA",
                "description": "The city that never sleeps with endless entertainment",
                "image": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=800",
                "rating": 4.5,
                "cost_per_person": {"USD": 1200, "EUR": 1020, "GBP": 876},
                "highlights": ["Culture", "Food", "Shopping", "Entertainment"],
                "best_time": "April-June, September-November",
                "flight_time": "0-2 hours",
                "currency": "USD",
                "daily_cost_usd": 150,
                "flight_cost_usd": 100
            }
        ]
    },
    "international": {
        "beach": [
            {
                "id": 5,
                "name": "Bali, Indonesia",
                "type": "beach",
                "country": "Indonesia",
                "description": "Tropical paradise with beautiful beaches, temples, and culture",
                "image": "https://images.unsplash.com/photo-1537953773345-d172ccf13cf1?w=800",
                "rating": 4.8,
                "cost_per_person": {"USD": 1200, "EUR": 1020, "GBP": 876},
                "highlights": ["Beaches", "Temples", "Culture", "Adventure"],
                "best_time": "April-October",
                "flight_time": "18-24 hours",
                "currency": "IDR",
                "daily_cost_usd": 100,
                "flight_cost_usd": 500
            },
            {
                "id": 6,
                "name": "Maldives",
                "type": "beach",
                "country": "Maldives",
                "description": "Luxury overwater bungalows and crystal clear waters",
                "image": "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?w=800",
                "rating": 4.9,
                "cost_per_person": {"USD": 3500, "EUR": 2975, "GBP": 2555},
                "highlights": ["Luxury", "Beaches", "Snorkeling", "Relaxation"],
                "best_time": "November-April",
                "flight_time": "20-30 hours",
                "currency": "MVR",
                "daily_cost_usd": 150,
                "flight_cost_usd": 600
            },
            {
                "id": 7,
                "name": "Santorini, Greece",
                "type": "beach",
                "country": "Greece",
                "description": "Stunning white buildings and blue waters",
                "image": "https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?w=800",
                "rating": 4.7,
                "cost_per_person": {"USD": 1800, "EUR": 1530, "GBP": 1314},
                "highlights": ["Beaches", "Architecture", "Sunsets", "Romance"],
                "best_time": "June-September",
                "flight_time": "12-16 hours",
                "currency": "EUR",
                "daily_cost_usd": 120,
                "flight_cost_usd": 500
            }
        ],
        "historic": [
            {
                "id": 8,
                "name": "Rome, Italy",
                "type": "historic",
                "country": "Italy",
                "description": "Ancient city with incredible history and architecture",
                "image": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=800",
                "rating": 4.6,
                "cost_per_person": {"USD": 1800, "EUR": 1530, "GBP": 1314},
                "highlights": ["History", "Architecture", "Food", "Culture"],
                "best_time": "April-June, September-October",
                "flight_time": "8-12 hours",
                "currency": "EUR",
                "daily_cost_usd": 150,
                "flight_cost_usd": 500
            },
            {
                "id": 9,
                "name": "Paris, France",
                "type": "historic",
                "country": "France",
                "description": "City of love with iconic landmarks and culture",
                "image": "https://images.unsplash.com/photo-1502602898536-47ad22581b52?w=800",
                "rating": 4.5,
                "cost_per_person": {"USD": 2000, "EUR": 1700, "GBP": 1460},
                "highlights": ["History", "Architecture", "Food", "Culture"],
                "best_time": "April-June, September-October",
                "flight_time": "7-10 hours",
                "currency": "EUR",
                "daily_cost_usd": 180,
                "flight_cost_usd": 600
            }
        ],
        "city": [
            {
                "id": 10,
                "name": "Tokyo, Japan",
                "type": "city",
                "country": "Japan",
                "description": "Modern metropolis with rich culture and technology",
                "image": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=800",
                "rating": 4.7,
                "cost_per_person": {"USD": 2000, "EUR": 1700, "GBP": 1460},
                "highlights": ["Technology", "Culture", "Food", "Shopping"],
                "best_time": "March-May (Cherry Blossom), September-November",
                "flight_time": "12-16 hours",
                "currency": "JPY",
                "daily_cost_usd": 100,
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

# API Endpoints
@app.get("/")
async def root():
    return {"message": "Travel AI API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/chat")
async def chat_endpoint(request: ChatMessage):
    """AI chat endpoint for travel planning conversations with state management."""
    try:
        # Get or create conversation state
        if request.session_id not in conversation_states:
            conversation_states[request.session_id] = ConversationState(session_id=request.session_id)
        
        state = conversation_states[request.session_id]
        
        # Add user message to history
        state.messages.append({"role": "user", "content": request.message})
        
        # Create conversation context
        conversation_context = [
            {"role": "system", "content": AI_SYSTEM_PROMPT + "\n\nCurrent conversation step: " + state.current_step + "\nCollected data: " + str(state.collected_data)}
        ] + state.messages[-10:]  # Keep last 10 messages for context
        
        # Get AI response
        response = await call_groq_ai(request.message, conversation_context)
        
        # Add AI response to history
        state.messages.append({"role": "assistant", "content": response})
        
        # Update conversation state based on user input
        await update_conversation_state(state, request.message)
        
        return {
            "response": response,
            "session_id": request.session_id,
            "step": state.current_step,
            "data_collected": state.collected_data
        }
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail="Chat service error")

async def update_conversation_state(state: ConversationState, user_message: str):
    """Update conversation state based on user input."""
    user_message_lower = user_message.lower()
    
    # Extract location if mentioned
    if "from" in user_message_lower or "traveling from" in user_message_lower:
        # Simple location extraction (you can make this more sophisticated)
        words = user_message.split()
        for i, word in enumerate(words):
            if word.lower() in ["from", "traveling", "leaving"] and i + 1 < len(words):
                location = words[i + 1]
                if location.lower() not in ["to", "and", "or", "the", "a", "an"]:
                    state.collected_data["travel_from"] = location
                    state.current_step = "destination_type"
                    break
    
    # Extract destination type
    destination_keywords = ["beach", "mountain", "city", "historic", "adventure", "relaxing", "cultural"]
    for keyword in destination_keywords:
        if keyword in user_message_lower:
            state.collected_data["destination_type"] = keyword
            state.current_step = "budget"
            break
    
    # Extract budget information
    if any(word in user_message_lower for word in ["budget", "cost", "price", "$", "dollar"]):
        state.current_step = "dates"
    
    # Extract travel dates
    if any(word in user_message_lower for word in ["december", "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november"]):
        state.current_step = "recommendations"

async def call_groq_recommendations(preferences: TravelPreferences) -> str:
    """Call Groq LLM to generate personalized travel recommendations."""
    try:
        # Create a detailed prompt for the LLM
        prompt = f"""
You are an expert travel advisor. Based on these preferences, suggest 5 destinations in valid JSON format only.

Preferences: Budget {preferences.budget_per_person} {preferences.currency}, {preferences.people_count} people, from {preferences.travel_from}, {preferences.travel_type} {preferences.destination_type} trip, {preferences.travel_dates}, {preferences.additional_preferences}

Respond ONLY with this exact JSON format (no other text):
{{
    "destinations": [
        {{
            "name": "Destination Name",
            "country": "Country",
            "type": "{preferences.destination_type}",
            "description": "Why this destination is perfect",
            "estimated_cost_per_person": "2000 USD",
            "best_time_to_visit": "June-September",
            "highlights": ["Beach", "Culture", "Food"],
            "why_perfect": "Matches your preferences perfectly"
        }}
    ]
}}
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
                            "content": "You are an expert travel advisor. Always respond with valid JSON format as requested."
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

@app.post("/recommendations")
async def get_recommendations(preferences: TravelPreferences):
    """Get AI-powered travel recommendations using Groq LLM."""
    try:
        # Call Groq LLM for recommendations
        llm_response = await call_groq_recommendations(preferences)
        
        if llm_response:
            try:
                # Try to parse the JSON response from LLM
                import json
                logger.info(f"LLM Response: {llm_response[:500]}...")  # Log first 500 chars
                recommendations = json.loads(llm_response)
                
                # Add additional data to each destination
                for dest in recommendations.get("destinations", []):
                    # Add weather data
                    dest["weather"] = await get_weather_data(dest["name"])
                    
                    # Add estimated flight cost (mock data for now)
                    dest["estimated_flight_cost"] = f"500-800 {preferences.currency}"
                    
                    # Add booking links (mock data for now)
                    dest["booking_links"] = {
                        "flights": f"https://www.skyscanner.com/search?from={preferences.travel_from}&to={dest['name']}",
                        "hotels": f"https://www.booking.com/search?ss={dest['name']}",
                        "activities": f"https://www.getyourguide.com/search?q={dest['name']}"
                    }
                
                return {
                    "success": True,
                    "destinations": recommendations.get("destinations", []),
                    "preferences": preferences.dict(),
                    "total_found": len(recommendations.get("destinations", [])),
                    "source": "AI Generated"
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
        
        # If no exact match, try partial matches or similar types
        if not filtered_destinations:
            # Try to find similar destination types
            similar_types = {
                "beach": ["beach"],
                "mountain": ["mountain"],
                "city": ["city"],
                "historic": ["historic"],
                "religious": ["historic", "city"],  # Religious sites often in historic cities
                "adventure": ["mountain", "beach"],  # Adventure can be in mountains or beaches
                "relaxing": ["beach", "mountain"]    # Relaxing can be beach or mountain
            }
            
            requested_type = preferences.destination_type.lower()
            if requested_type in similar_types:
                for similar_type in similar_types[requested_type]:
                    if similar_type in destination_pool:
                        filtered_destinations.extend(destination_pool[similar_type])
        
        # If still no matches, return a small selection of popular destinations
        if not filtered_destinations:
            # Return top 3 destinations from the pool
            all_destinations = []
            for destinations in destination_pool.values():
                all_destinations.extend(destinations)
            filtered_destinations = all_destinations[:3]
        
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
            "preferences": preferences.dict(),
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

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
