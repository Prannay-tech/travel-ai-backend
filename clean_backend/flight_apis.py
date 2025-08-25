"""
Flight Search APIs Integration
Supports multiple flight search providers for comprehensive results.
"""

import httpx
import os
import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import json
import asyncio
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# API Keys
SKYSCANNER_API_KEY = os.getenv("SKYSCANNER_API_KEY", "")
AMADEUS_CLIENT_ID = os.getenv("AMADEUS_CLIENT_ID", "")
AMADEUS_CLIENT_SECRET = os.getenv("AMADEUS_CLIENT_SECRET", "")

# Load environment variables
load_dotenv()

class FlightSearchAPI:
    """Comprehensive flight search using multiple APIs"""
    
    def __init__(self):
        self.skyscanner_available = bool(SKYSCANNER_API_KEY)
        self.amadeus_available = bool(AMADEUS_CLIENT_ID and AMADEUS_CLIENT_SECRET)
        self.amadeus_token = None
        
    async def get_amadeus_token(self) -> Optional[str]:
        """Get Amadeus API access token"""
        if not self.amadeus_available:
            return None
            
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://test.api.amadeus.com/v1/security/oauth2/token",
                    data={
                        "grant_type": "client_credentials",
                        "client_id": AMADEUS_CLIENT_ID,
                        "client_secret": AMADEUS_CLIENT_SECRET
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    self.amadeus_token = data.get("access_token")
                    return self.amadeus_token
                else:
                    logger.error(f"Amadeus token error: {response.status_code}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error getting Amadeus token: {e}")
            return None
    
    async def search_flights_skyscanner(self, origin: str, destination: str, 
                                      departure_date: str, passengers: int = 1) -> List[Dict]:
        """Search flights using Skyscanner API"""
        if not self.skyscanner_available:
            return []
            
        try:
            # Step 1: Create search session
            async with httpx.AsyncClient() as client:
                create_response = await client.post(
                    "https://partners.api.skyscanner.net/apiservices/v3/flights/live/search/create",
                    headers={
                        "x-api-key": SKYSCANNER_API_KEY,
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                    data={
                        "queryLegs": json.dumps([{
                            "originPlaceId": origin,
                            "destinationPlaceId": destination,
                            "date": departure_date
                        }]),
                        "adults": passengers,
                        "children": 0,
                        "infants": 0,
                        "cabinClass": "CABIN_CLASS_ECONOMY",
                        "currencyCode": "USD"
                    }
                )
                
                if create_response.status_code != 200:
                    logger.error(f"Skyscanner create search error: {create_response.status_code}")
                    return []
                
                search_data = create_response.json()
                session_token = search_data.get("sessionToken")
                
                if not session_token:
                    return []
                
                # Step 2: Poll for results
                max_attempts = 10
                for attempt in range(max_attempts):
                    await asyncio.sleep(2)  # Wait between polls
                    
                    poll_response = await client.get(
                        f"https://partners.api.skyscanner.net/apiservices/v3/flights/live/search/poll/{session_token}",
                        headers={"x-api-key": SKYSCANNER_API_KEY}
                    )
                    
                    if poll_response.status_code == 200:
                        results = poll_response.json()
                        return self._parse_skyscanner_results(results)
                    elif poll_response.status_code == 202:
                        # Still processing, continue polling
                        continue
                    else:
                        logger.error(f"Skyscanner poll error: {poll_response.status_code}")
                        break
                
                return []
                
        except Exception as e:
            logger.error(f"Error in Skyscanner search: {e}")
            return []
    
    async def search_flights_amadeus(self, origin: str, destination: str, 
                                   departure_date: str, passengers: int = 1) -> List[Dict]:
        """Search flights using Amadeus API"""
        if not self.amadeus_available:
            return []
            
        try:
            # Get token if needed
            if not self.amadeus_token:
                await self.get_amadeus_token()
                
            if not self.amadeus_token:
                return []
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://test.api.amadeus.com/v2/shopping/flight-offers",
                    headers={
                        "Authorization": f"Bearer {self.amadeus_token}",
                        "Content-Type": "application/json"
                    },
                    params={
                        "originLocationCode": origin,
                        "destinationLocationCode": destination,
                        "departureDate": departure_date,
                        "adults": passengers,
                        "max": 20,
                        "currencyCode": "USD"
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_amadeus_results(data)
                else:
                    logger.error(f"Amadeus search error: {response.status_code}")
                    return []
                    
        except Exception as e:
            logger.error(f"Error in Amadeus search: {e}")
            return []
    
    def _parse_skyscanner_results(self, results: Dict) -> List[Dict]:
        """Parse Skyscanner API results"""
        flights = []
        
        try:
            content = results.get("content", {})
            results_data = content.get("results", {})
            
            # Extract itineraries
            itineraries = results_data.get("itineraries", {})
            
            for itinerary_id, itinerary in itineraries.items():
                pricing_options = itinerary.get("pricingOptions", [])
                
                for option in pricing_options:
                    price = option.get("price", {})
                    agent = option.get("agentIds", [""])[0]
                    
                    # Get leg details
                    leg_id = itinerary.get("legIds", [""])[0]
                    leg = results_data.get("legs", {}).get(leg_id, {})
                    
                    # Get segment details
                    segments = []
                    for segment_id in leg.get("segmentIds", []):
                        segment = results_data.get("segments", {}).get(segment_id, {})
                        segments.append({
                            "departure": segment.get("departureDateTime"),
                            "arrival": segment.get("arrivalDateTime"),
                            "origin": segment.get("originPlaceId"),
                            "destination": segment.get("destinationPlaceId"),
                            "carrier": segment.get("marketingCarrierId")
                        })
                    
                    flights.append({
                        "id": f"skyscanner_{itinerary_id}_{agent}",
                        "airline": agent,
                        "flight_number": f"{agent} Flight",
                        "departure_time": segments[0].get("departure") if segments else "",
                        "arrival_time": segments[-1].get("arrival") if segments else "",
                        "duration": self._calculate_duration(segments),
                        "price": {"USD": price.get("amount", 0)},
                        "stops": len(segments) - 1,
                        "aircraft": "Commercial Aircraft",
                        "booking_link": option.get("url", ""),
                        "source": "Skyscanner"
                    })
                    
        except Exception as e:
            logger.error(f"Error parsing Skyscanner results: {e}")
            
        return flights[:10]  # Return top 10 results
    
    def _parse_amadeus_results(self, results: Dict) -> List[Dict]:
        """Parse Amadeus API results"""
        flights = []
        
        try:
            data = results.get("data", [])
            
            for flight in data:
                itineraries = flight.get("itineraries", [])
                if not itineraries:
                    continue
                    
                itinerary = itineraries[0]
                segments = itinerary.get("segments", [])
                
                if not segments:
                    continue
                
                # Calculate duration
                duration = flight.get("itineraries", [{}])[0].get("duration", "")
                
                # Get price
                price = flight.get("price", {})
                total_price = price.get("total", "0")
                
                flights.append({
                    "id": f"amadeus_{flight.get('id', 'unknown')}",
                    "airline": segments[0].get("carrierCode", "Unknown"),
                    "flight_number": f"{segments[0].get('carrierCode', '')} {segments[0].get('number', '')}",
                    "departure_time": segments[0].get("departure", {}).get("at", ""),
                    "arrival_time": segments[-1].get("arrival", {}).get("at", ""),
                    "duration": duration,
                    "price": {"USD": float(total_price) if total_price else 0},
                    "stops": len(segments) - 1,
                    "aircraft": "Commercial Aircraft",
                    "booking_link": f"https://www.amadeus.com/flights/{flight.get('id', '')}",
                    "source": "Amadeus"
                })
                
        except Exception as e:
            logger.error(f"Error parsing Amadeus results: {e}")
            
        return flights[:10]  # Return top 10 results
    
    def _calculate_duration(self, segments: List[Dict]) -> str:
        """Calculate total flight duration from segments"""
        if not segments:
            return "Unknown"
            
        try:
            first_departure = datetime.fromisoformat(segments[0].get("departure", "").replace("Z", "+00:00"))
            last_arrival = datetime.fromisoformat(segments[-1].get("arrival", "").replace("Z", "+00:00"))
            
            duration = last_arrival - first_departure
            hours = int(duration.total_seconds() // 3600)
            minutes = int((duration.total_seconds() % 3600) // 60)
            
            return f"{hours}h {minutes}m"
            
        except Exception:
            return "Unknown"
    
    async def search_flights(self, origin: str, destination: str, 
                           departure_date: str, passengers: int = 1) -> List[Dict]:
        """Search flights using all available APIs"""
        all_flights = []
        
        # Search with Skyscanner
        if self.skyscanner_available:
            skyscanner_flights = await self.search_flights_skyscanner(
                origin, destination, departure_date, passengers
            )
            all_flights.extend(skyscanner_flights)
        
        # Search with Amadeus
        if self.amadeus_available:
            amadeus_flights = await self.search_flights_amadeus(
                origin, destination, departure_date, passengers
            )
            all_flights.extend(amadeus_flights)
        
        # If no real APIs available, return mock data
        if not all_flights:
            all_flights = self._get_mock_flights(origin, destination, departure_date, passengers)
        
        # Sort by price and remove duplicates
        unique_flights = self._remove_duplicates(all_flights)
        sorted_flights = sorted(unique_flights, key=lambda x: x["price"]["USD"])
        
        return sorted_flights[:15]  # Return top 15 results
    
    def _get_mock_flights(self, origin: str, destination: str, 
                         departure_date: str, passengers: int) -> List[Dict]:
        """Return mock flight data when no APIs are available"""
        return [
            {
                "id": "mock_1",
                "airline": "Delta Airlines",
                "flight_number": "DL123",
                "departure_time": f"{departure_date}T09:00:00",
                "arrival_time": f"{departure_date}T11:30:00",
                "duration": "2h 30m",
                "price": {"USD": 450, "EUR": 380, "GBP": 330},
                "stops": 0,
                "aircraft": "Boeing 737",
                "booking_link": "https://www.delta.com",
                "source": "Mock Data"
            },
            {
                "id": "mock_2",
                "airline": "American Airlines",
                "flight_number": "AA456",
                "departure_time": f"{departure_date}T14:15:00",
                "arrival_time": f"{departure_date}T16:45:00",
                "duration": "2h 30m",
                "price": {"USD": 380, "EUR": 320, "GBP": 280},
                "stops": 1,
                "aircraft": "Airbus A320",
                "booking_link": "https://www.aa.com",
                "source": "Mock Data"
            },
            {
                "id": "mock_3",
                "airline": "United Airlines",
                "flight_number": "UA789",
                "departure_time": f"{departure_date}T07:30:00",
                "arrival_time": f"{departure_date}T10:15:00",
                "duration": "2h 45m",
                "price": {"USD": 520, "EUR": 440, "GBP": 380},
                "stops": 0,
                "aircraft": "Boeing 787",
                "booking_link": "https://www.united.com",
                "source": "Mock Data"
            }
        ]
    
    def _remove_duplicates(self, flights: List[Dict]) -> List[Dict]:
        """Remove duplicate flights based on airline and flight number"""
        seen = set()
        unique_flights = []
        
        for flight in flights:
            key = f"{flight['airline']}_{flight['flight_number']}"
            if key not in seen:
                seen.add(key)
                unique_flights.append(flight)
        
        return unique_flights

# Global instance
flight_api = FlightSearchAPI()
