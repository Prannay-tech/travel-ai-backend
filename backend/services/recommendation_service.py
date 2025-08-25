"""
Enhanced recommendation service integrating real-world data sources.
"""

import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging
from ..clients.currency_client import currency_client
from ..clients.weather_client import weather_client
from ..clients.holiday_client import holiday_client
from ..config import settings

logger = logging.getLogger(__name__)

class RecommendationService:
    """Service for generating comprehensive travel recommendations."""
    
    def __init__(self):
        # Real-world destination data
        self.domestic_destinations = self._load_domestic_destinations()
        self.international_destinations = self._load_international_destinations()
    
    async def generate_recommendations(self, travel_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive travel recommendations."""
        try:
            # Extract travel preferences
            destination_type = travel_data.get("destination", "").lower()
            budget = travel_data.get("budget")
            travel_dates = travel_data.get("travelDates", "")
            current_location = travel_data.get("currentLocation", "")
            preferences = travel_data.get("preferences", "")
            currency = travel_data.get("currency", "USD")
            travel_type = travel_data.get("travelType", "international")
            
            # Select destinations based on preferences
            selected_destinations = await self._select_destinations(
                destination_type, travel_type, budget, currency
            )
            
            # Get weather data for first destination
            weather_info = None
            if selected_destinations:
                first_destination = selected_destinations[0]
                weather_info = await weather_client.get_weather_summary(
                    first_destination["name"]
                )
            
            # Get holiday data for first destination
            holidays = []
            if selected_destinations:
                first_destination = selected_destinations[0]
                country = first_destination.get("country", first_destination.get("state", "USA"))
                holidays = await holiday_client.get_upcoming_holidays(country, 90)
            
            # Generate travel tips
            travel_tips = self._generate_travel_tips(
                destination_type, budget, preferences, travel_type
            )
            
            # Calculate summary statistics
            summary = self._calculate_summary(
                selected_destinations, currency, travel_type, destination_type
            )
            
            return {
                "places": selected_destinations,
                "weather": weather_info,
                "holidays": holidays,
                "summary": summary
            }
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return self._get_fallback_recommendations()
    
    async def _select_destinations(
        self, 
        destination_type: str, 
        travel_type: str, 
        budget: Optional[str], 
        currency: str
    ) -> List[Dict]:
        """Select destinations based on criteria."""
        # Choose destination pool
        if travel_type == "domestic":
            destination_pool = self.domestic_destinations
        else:
            destination_pool = self.international_destinations
        
        # Filter by destination type
        if "beach" in destination_type:
            selected = destination_pool.get("beach", [])
        elif "mountain" in destination_type:
            selected = destination_pool.get("mountain", [])
        elif "city" in destination_type:
            selected = destination_pool.get("city", [])
        else:
            # Mix of destinations
            selected = []
            for category in destination_pool.values():
                selected.extend(category[:2])  # Take 2 from each category
        
        # Filter by budget if specified
        if budget:
            budget_usd = self._parse_budget(budget, currency)
            if budget_usd:
                selected = [
                    dest for dest in selected 
                    if (dest["cost_day_usd"] * 7 + dest["avg_flight_cost"]) <= budget_usd
                ]
        
        # Convert costs to selected currency
        selected = await self._convert_destination_costs(selected, currency)
        
        # Limit results
        return selected[:6]
    
    async def _convert_destination_costs(
        self, 
        destinations: List[Dict], 
        target_currency: str
    ) -> List[Dict]:
        """Convert destination costs to target currency."""
        converted_destinations = []
        
        for dest in destinations:
            converted_dest = dest.copy()
            
            # Convert daily cost
            daily_cost_converted = await currency_client.convert_currency(
                dest["cost_day_usd"], "USD", target_currency
            )
            converted_dest["cost_day_converted"] = daily_cost_converted or dest["cost_day_usd"]
            
            # Convert flight cost
            flight_cost_converted = await currency_client.convert_currency(
                dest["avg_flight_cost"], "USD", target_currency
            )
            converted_dest["flight_cost_converted"] = flight_cost_converted or dest["avg_flight_cost"]
            
            converted_dest["currency"] = target_currency
            converted_destinations.append(converted_dest)
        
        return converted_destinations
    
    def _parse_budget(self, budget: str, currency: str) -> Optional[float]:
        """Parse budget string to USD amount."""
        try:
            # Extract numbers from budget string
            import re
            numbers = re.findall(r'\d+', budget)
            if numbers:
                amount = int(numbers[0]) * 1000  # Assume first number is in thousands
                # Convert to USD for comparison
                if currency != "USD":
                    # Use fallback rates for budget parsing
                    fallback_rates = {
                        "EUR": 0.85, "GBP": 0.73, "JPY": 110.0,
                        "CAD": 1.25, "AUD": 1.35, "CHF": 0.92, "SGD": 1.35
                    }
                    rate = fallback_rates.get(currency, 1.0)
                    amount = amount / rate
                return amount
        except Exception as e:
            logger.error(f"Error parsing budget: {e}")
        return None
    
    def _generate_travel_tips(
        self, 
        destination_type: str, 
        budget: Optional[str], 
        preferences: str, 
        travel_type: str
    ) -> List[str]:
        """Generate personalized travel tips."""
        tips = []
        
        # Travel type tips
        if travel_type == "domestic":
            tips.extend([
                "Consider booking flights 2-3 months in advance for best prices",
                "Check for local events and festivals during your visit"
            ])
        else:
            tips.extend([
                "Book international flights 3-6 months in advance",
                "Check visa requirements and passport validity",
                "Consider travel insurance for international trips"
            ])
        
        # Destination type tips
        if "beach" in destination_type:
            tips.extend([
                "Pack sunscreen and beach essentials",
                "Book accommodations early during peak season"
            ])
        elif "mountain" in destination_type:
            tips.extend([
                "Check weather conditions before hiking",
                "Pack appropriate gear for altitude changes"
            ])
        elif "city" in destination_type:
            tips.extend([
                "Research public transportation options",
                "Book popular attractions in advance"
            ])
        
        # Budget tips
        if budget and "budget" in budget.lower():
            tips.extend([
                "Consider staying in hostels or budget accommodations",
                "Eat at local restaurants for authentic and affordable meals"
            ])
        
        # Preference-based tips
        if "family" in preferences.lower():
            tips.extend([
                "Look for family-friendly activities and accommodations",
                "Plan activities suitable for all ages"
            ])
        
        return tips[:5]  # Limit to 5 tips
    
    def _calculate_summary(
        self, 
        destinations: List[Dict], 
        currency: str, 
        travel_type: str, 
        destination_type: str
    ) -> Dict[str, Any]:
        """Calculate summary statistics."""
        if not destinations:
            return {
                "totalDestinations": 0,
                "averageCost": 0,
                "averageFlightCost": 0,
                "bestTimeToVisit": "Year-round",
                "travelTips": [],
                "currency": currency,
                "travelType": travel_type
            }
        
        # Calculate averages
        total_cost = sum(dest.get("cost_day_converted", dest["cost_day_usd"]) for dest in destinations)
        total_flight_cost = sum(dest.get("flight_cost_converted", dest["avg_flight_cost"]) for dest in destinations)
        
        avg_cost = total_cost / len(destinations)
        avg_flight_cost = total_flight_cost / len(destinations)
        
        # Determine best time to visit
        best_time = self._get_best_time_to_visit(destination_type, travel_type)
        
        return {
            "totalDestinations": len(destinations),
            "averageCost": round(avg_cost, 2),
            "averageFlightCost": round(avg_flight_cost, 2),
            "bestTimeToVisit": best_time,
            "travelTips": self._generate_travel_tips(destination_type, None, "", travel_type),
            "currency": currency,
            "travelType": travel_type
        }
    
    def _get_best_time_to_visit(self, destination_type: str, travel_type: str) -> str:
        """Get best time to visit based on destination type and travel type."""
        if travel_type == "domestic":
            if "beach" in destination_type:
                return "March to October for best beach weather"
            elif "mountain" in destination_type:
                return "June to September for hiking, December to March for skiing"
            elif "city" in destination_type:
                return "Spring (March to May) or Fall (September to November)"
        else:
            if "beach" in destination_type:
                return "April to October for best weather (avoid monsoon seasons)"
            elif "mountain" in destination_type:
                return "June to September for hiking, December to March for skiing"
            elif "city" in destination_type:
                return "Spring (March to May) or Fall (September to November)"
        
        return "Year-round, but check specific destination for best times"
    
    def _load_domestic_destinations(self) -> Dict[str, List[Dict]]:
        """Load domestic US destinations."""
        return {
            "beach": [
                {
                    "name": "Miami Beach, Florida",
                    "state": "FL",
                    "description": "Famous for its Art Deco architecture, white sand beaches, and vibrant nightlife",
                    "image": "https://images.unsplash.com/photo-1514214246283-d427a95c5d2f?w=400",
                    "rating": 8.7,
                    "cost_day_usd": 180,
                    "weather": "Tropical, 20-32°C year-round",
                    "highlights": ["South Beach", "Art Deco District", "Cuban cuisine", "Water sports"],
                    "best_time": "March to May, October to December",
                    "airport": "MIA",
                    "avg_flight_cost": 250
                },
                {
                    "name": "San Diego, California",
                    "state": "CA",
                    "description": "Perfect weather year-round with beautiful beaches and laid-back vibe",
                    "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400",
                    "rating": 8.9,
                    "cost_day_usd": 200,
                    "weather": "Mediterranean, 15-25°C year-round",
                    "highlights": ["La Jolla", "Gaslamp Quarter", "Zoo", "Craft beer"],
                    "best_time": "March to November",
                    "airport": "SAN",
                    "avg_flight_cost": 300
                }
            ],
            "mountain": [
                {
                    "name": "Denver, Colorado",
                    "state": "CO",
                    "description": "Gateway to the Rockies with outdoor adventures and craft beer scene",
                    "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400",
                    "rating": 8.5,
                    "cost_day_usd": 150,
                    "weather": "Mountain, -5 to 30°C",
                    "highlights": ["Rocky Mountains", "Craft breweries", "Skiing", "Hiking"],
                    "best_time": "June to September, December to March",
                    "airport": "DEN",
                    "avg_flight_cost": 280
                }
            ],
            "city": [
                {
                    "name": "New York City",
                    "state": "NY",
                    "description": "The city that never sleeps with endless entertainment and culture",
                    "image": "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=400",
                    "rating": 8.5,
                    "cost_day_usd": 300,
                    "weather": "Temperate, -5 to 30°C",
                    "highlights": ["Times Square", "Central Park", "Broadway", "Museums"],
                    "best_time": "April to June, September to November",
                    "airport": "JFK/LGA",
                    "avg_flight_cost": 350
                }
            ]
        }
    
    def _load_international_destinations(self) -> Dict[str, List[Dict]]:
        """Load international destinations."""
        return {
            "beach": [
                {
                    "name": "Bali, Indonesia",
                    "country": "Indonesia",
                    "description": "Tropical paradise with stunning beaches, rich culture, and affordable luxury",
                    "image": "https://images.unsplash.com/photo-1537953773345-d172ccf13cf1?w=400",
                    "rating": 9.2,
                    "cost_day_usd": 80,
                    "weather": "Tropical, 25-32°C year-round",
                    "highlights": ["Beach resorts", "Cultural temples", "Rice terraces", "Water sports"],
                    "best_time": "April to October",
                    "airport": "DPS",
                    "avg_flight_cost": 1200
                }
            ],
            "mountain": [
                {
                    "name": "Swiss Alps",
                    "country": "Switzerland",
                    "description": "Majestic mountains with world-class skiing and hiking",
                    "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400",
                    "rating": 9.3,
                    "cost_day_usd": 250,
                    "weather": "Alpine, varies by season",
                    "highlights": ["Skiing", "Hiking", "Chocolate", "Scenic trains"],
                    "best_time": "December to March (skiing), June to September (hiking)",
                    "airport": "ZRH/GVA",
                    "avg_flight_cost": 1000
                }
            ],
            "city": [
                {
                    "name": "Tokyo, Japan",
                    "country": "Japan",
                    "description": "Futuristic metropolis blending tradition with innovation",
                    "image": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=400",
                    "rating": 9.0,
                    "cost_day_usd": 180,
                    "weather": "Temperate, 10-30°C",
                    "highlights": ["Technology", "Sushi", "Cherry blossoms", "Efficient transport"],
                    "best_time": "March to May, October to November",
                    "airport": "NRT/HND",
                    "avg_flight_cost": 1200
                }
            ]
        }
    
    def _get_fallback_recommendations(self) -> Dict[str, Any]:
        """Get fallback recommendations when errors occur."""
        return {
            "places": [],
            "weather": {
                "current": {"temperature": "22°C", "condition": "Sunny", "humidity": "65%"},
                "forecast": [
                    {"day": "Today", "temp": "22°C", "condition": "Sunny"},
                    {"day": "Tomorrow", "temp": "24°C", "condition": "Partly Cloudy"},
                    {"day": "Day 3", "temp": "21°C", "condition": "Light Rain"}
                ]
            },
            "holidays": [
                {"name": "Local Festival", "date": "2024-08-15", "description": "Annual cultural celebration"}
            ],
            "summary": {
                "totalDestinations": 0,
                "averageCost": 0,
                "averageFlightCost": 0,
                "bestTimeToVisit": "Year-round",
                "travelTips": ["Check local weather before traveling", "Book accommodations in advance"],
                "currency": "USD",
                "travelType": "international"
            }
        }

# Global recommendation service instance
recommendation_service = RecommendationService() 