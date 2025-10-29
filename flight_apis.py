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

# Load environment variables first
load_dotenv()

# API Keys
SKYSCANNER_API_KEY = os.getenv("SKYSCANNER_API_KEY", "")
AMADEUS_CLIENT_ID = os.getenv("AMADEUS_CLIENT_ID", "")
AMADEUS_CLIENT_SECRET = os.getenv("AMADEUS_CLIENT_SECRET", "")

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
    
    async def _get_place_id(self, query: str) -> str:
        """Get place ID from airport code or city name using auto-complete"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://flights-sky.p.rapidapi.com/flights/auto-complete",
                    params={"query": query},
                    headers={
                        "X-RapidAPI-Key": SKYSCANNER_API_KEY,
                        "X-RapidAPI-Host": "flights-sky.p.rapidapi.com"
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("data") and len(data["data"]) > 0:
                        # Return the first result's skyId
                        return data["data"][0]["presentation"]["skyId"]
        except Exception as e:
            logger.error(f"Error getting place ID for {query}: {e}")
        
        return query  # Fallback to original query

    async def search_flights_skyscanner(self, origin: str, destination: str, 
                                      departure_date: str, passengers: int = 1,
                                      return_date: str = None, search_type: str = "one-way") -> List[Dict]:
        """Search flights using RapidAPI Skyscanner API with optimal endpoint selection"""
        if not self.skyscanner_available:
            return []
            
        try:
            # Convert airport codes to place IDs
            origin_id = await self._get_place_id(origin)
            destination_id = await self._get_place_id(destination)
            
            async with httpx.AsyncClient() as client:
                # Select optimal endpoint based on search type
                if search_type == "roundtrip" and return_date:
                    # Use roundtrip search for complete trips
                    response = await client.get(
                        "https://flights-sky.p.rapidapi.com/flights/search-roundtrip",
                        params={
                            "fromEntityId": origin_id,
                            "toEntityId": destination_id,
                            "departDate": departure_date,
                            "returnDate": return_date
                        },
                        headers={
                            "X-RapidAPI-Key": SKYSCANNER_API_KEY,
                            "X-RapidAPI-Host": "flights-sky.p.rapidapi.com"
                        }
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        return self._parse_roundtrip_results(data, origin, destination, departure_date, return_date)
                else:
                    # Use cheapest-one-way for price comparison
                    response = await client.get(
                        "https://flights-sky.p.rapidapi.com/flights/cheapest-one-way",
                        params={
                            "fromEntityId": origin_id,
                            "toEntityId": destination_id,
                            "departDate": departure_date
                        },
                        headers={
                            "X-RapidAPI-Key": SKYSCANNER_API_KEY,
                            "X-RapidAPI-Host": "flights-sky.p.rapidapi.com"
                        }
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        return self._parse_cheapest_one_way_results(data, origin, destination, departure_date)
                
                logger.error(f"RapidAPI Skyscanner error: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error in RapidAPI Skyscanner search: {e}")
            return []
    
    async def _poll_for_complete_results(self, client: httpx.AsyncClient, initial_data: Dict) -> Optional[Dict]:
        """Poll for complete results when status is incomplete"""
        try:
            # Extract session token or search ID from initial response
            session_token = initial_data.get('data', {}).get('context', {}).get('sessionToken')
            if not session_token:
                logger.error("No session token found for polling")
                return None
            
            # Poll for complete results (max 10 attempts, 2 seconds between)
            max_attempts = 10
            for attempt in range(max_attempts):
                await asyncio.sleep(2)  # Wait 2 seconds between polls
                
                try:
                    # Use the search-incomplete endpoint
                    poll_response = await client.get(
                        "https://flights-sky.p.rapidapi.com/web/flights/search-incomplete",
                        params={"sessionToken": session_token},
                        headers={
                            "X-RapidAPI-Key": SKYSCANNER_API_KEY,
                            "X-RapidAPI-Host": "flights-sky.p.rapidapi.com"
                        }
                    )
                    
                    if poll_response.status_code == 200:
                        poll_data = poll_response.json()
                        context = poll_data.get('data', {}).get('context', {})
                        status = context.get('status', 'unknown')
                        
                        if status == 'complete':
                            logger.info(f"Results complete after {attempt + 1} attempts")
                            return poll_data
                        elif status == 'incomplete':
                            logger.info(f"Still incomplete, attempt {attempt + 1}/{max_attempts}")
                            continue
                        else:
                            logger.warning(f"Unknown status: {status}")
                            return poll_data
                    else:
                        logger.error(f"Polling error: {poll_response.status_code}")
                        return None
                        
                except Exception as e:
                    logger.error(f"Error during polling attempt {attempt + 1}: {e}")
                    continue
            
            logger.warning("Max polling attempts reached, returning partial results")
            return None
            
        except Exception as e:
            logger.error(f"Error in polling for complete results: {e}")
            return None
    
    def _get_skyscanner_endpoint(self, search_type: str, origin: str, destination: str, 
                                departure_date: str, return_date: str = None) -> str:
        """Get the appropriate Skyscanner endpoint based on search type"""
        base_url = "https://flights-sky.p.rapidapi.com"
        
        if search_type == "roundtrip" and return_date:
            # Roundtrip search
            return f"{base_url}/web/flights/search-roundtrip"
        elif search_type == "multi-city":
            # Multi-city search
            return f"{base_url}/web/flights/search-multi-city"
        else:
            # One-way search (default)
            return f"{base_url}/web/flights/search-one-way"
    
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
    
    def _parse_cheapest_one_way_results(self, results: Dict, origin: str, destination: str, departure_date: str) -> List[Dict]:
        """Parse cheapest-one-way results from RapidAPI Skyscanner"""
        flights = []
        
        try:
            data = results.get("data", [])
            
            if not data:
                logger.warning("No flight data returned from cheapest-one-way endpoint")
                return []
            
            # Take the first few results (cheapest prices)
            for i, flight_data in enumerate(data[:5]):  # Limit to 5 results
                day = flight_data.get("day", departure_date)
                price = flight_data.get("price", 0)
                group = flight_data.get("group", "unknown")
                
                # Create flight entry
                flights.append({
                    "id": f"rapidapi_cheapest_{i}",
                    "airline": "Multiple Airlines",
                    "flight_number": f"Cheapest {group.title()}",
                    "departure_time": f"{day}T09:00:00",  # Default morning departure
                    "arrival_time": f"{day}T15:00:00",    # Default afternoon arrival
                    "duration": "6h 00m",  # Default duration
                    "price": {"USD": price},
                    "stops": 0 if group == "low" else 1,  # Assume direct for low prices
                    "aircraft": "Commercial Aircraft",
                    "booking_link": f"https://www.skyscanner.com/transport/flights/{origin}/{destination}/{day}/",
                    "source": "RapidAPI Skyscanner Cheapest",
                    "departure_date": day,
                    "price_category": group
                })
            
            logger.info(f"Parsed {len(flights)} flights from cheapest-one-way endpoint")
            return flights
            
        except Exception as e:
            logger.error(f"Error parsing cheapest-one-way results: {e}")
            return []

    def _parse_roundtrip_results(self, results: Dict, origin: str, destination: str, departure_date: str, return_date: str) -> List[Dict]:
        """Parse roundtrip search results from RapidAPI Skyscanner"""
        flights = []
        
        try:
            data = results.get("data", {})
            itineraries = data.get("itineraries", {})
            results_data = itineraries.get("results", {})
            
            if not results_data:
                logger.warning("No roundtrip data returned from search-roundtrip endpoint")
                return []
            
            # Parse roundtrip results
            for i, (itinerary_id, itinerary) in enumerate(list(results_data.items())[:3]):  # Limit to 3 results
                pricing_options = itinerary.get("pricingOptions", [])
                
                for j, option in enumerate(pricing_options[:2]):  # Limit to 2 pricing options per itinerary
                    price = option.get("price", {})
                    agent = option.get("agentIds", [""])[0]
                    
                    # Get leg details for outbound and return
                    leg_ids = itinerary.get("legIds", [])
                    outbound_leg = itineraries.get("legs", {}).get(leg_ids[0], {}) if len(leg_ids) > 0 else {}
                    return_leg = itineraries.get("legs", {}).get(leg_ids[1], {}) if len(leg_ids) > 1 else {}
                    
                    # Calculate total duration
                    outbound_duration = self._calculate_leg_duration(outbound_leg, itineraries)
                    return_duration = self._calculate_leg_duration(return_leg, itineraries)
                    
                    flights.append({
                        "id": f"rapidapi_roundtrip_{i}_{j}",
                        "airline": agent or "Multiple Airlines",
                        "flight_number": f"Roundtrip {agent or 'Flight'}",
                        "departure_time": f"{departure_date}T09:00:00",
                        "arrival_time": f"{return_date}T18:00:00",
                        "duration": f"{outbound_duration} + {return_duration}",
                        "price": {"USD": price.get("amount", 0)},
                        "stops": len(outbound_leg.get("segmentIds", [])) - 1,
                        "aircraft": "Commercial Aircraft",
                        "booking_link": option.get("url", ""),
                        "source": "RapidAPI Skyscanner Roundtrip",
                        "departure_date": departure_date,
                        "return_date": return_date,
                        "trip_type": "roundtrip"
                    })
            
            logger.info(f"Parsed {len(flights)} roundtrip flights")
            return flights
            
        except Exception as e:
            logger.error(f"Error parsing roundtrip results: {e}")
            return []

    def _calculate_leg_duration(self, leg: Dict, itineraries: Dict) -> str:
        """Calculate duration for a flight leg"""
        try:
            segments = leg.get("segmentIds", [])
            if not segments:
                return "6h 00m"
            
            # Get first and last segment times
            first_segment = itineraries.get("segments", {}).get(segments[0], {})
            last_segment = itineraries.get("segments", {}).get(segments[-1], {})
            
            departure = first_segment.get("departureDateTime", "")
            arrival = last_segment.get("arrivalDateTime", "")
            
            if departure and arrival:
                # Simple duration calculation (in real implementation, parse datetime)
                return "6h 00m"  # Placeholder
            
            return "6h 00m"
        except:
            return "6h 00m"

    async def get_price_calendar(self, origin: str, destination: str) -> List[Dict]:
        """Get price calendar for flexible date searches"""
        if not self.skyscanner_available:
            return []
            
        try:
            # Convert airport codes to place IDs
            origin_id = await self._get_place_id(origin)
            destination_id = await self._get_place_id(destination)
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://flights-sky.p.rapidapi.com/flights/price-calendar",
                    params={
                        "fromEntityId": origin_id,
                        "toEntityId": destination_id
                    },
                    headers={
                        "X-RapidAPI-Key": SKYSCANNER_API_KEY,
                        "X-RapidAPI-Host": "flights-sky.p.rapidapi.com"
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_price_calendar_results(data, origin, destination)
                else:
                    logger.error(f"Price calendar error: {response.status_code}")
                    return []
                
        except Exception as e:
            logger.error(f"Error getting price calendar: {e}")
            return []

    def _parse_price_calendar_results(self, results: Dict, origin: str, destination: str) -> List[Dict]:
        """Parse price calendar results"""
        calendar_data = []
        
        try:
            data = results.get("data", [])
            
            if not data:
                logger.warning("No price calendar data returned")
                return []
            
            # Parse price calendar data
            for entry in data[:30]:  # Limit to 30 days
                day = entry.get("day", "")
                price = entry.get("price", 0)
                group = entry.get("group", "unknown")
                
                calendar_data.append({
                    "date": day,
                    "price": price,
                    "price_category": group,
                    "origin": origin,
                    "destination": destination,
                    "currency": "USD"
                })
            
            logger.info(f"Parsed {len(calendar_data)} price calendar entries")
            return calendar_data
            
        except Exception as e:
            logger.error(f"Error parsing price calendar results: {e}")
            return []

    async def validate_airport_code(self, airport_code: str) -> Dict:
        """Validate airport code using the airports database"""
        if not self.skyscanner_available:
            return {"valid": False, "error": "API not available"}
            
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://flights-sky.p.rapidapi.com/flights/airports",
                    headers={
                        "X-RapidAPI-Key": SKYSCANNER_API_KEY,
                        "X-RapidAPI-Host": "flights-sky.p.rapidapi.com"
                    }
                )
                
                if response.status_code == 200:
                    airports = response.json()
                    
                    # Search for the airport code
                    for airport in airports:
                        if isinstance(airport, dict) and airport.get("iata", "").upper() == airport_code.upper():
                            return {
                                "valid": True,
                                "airport": {
                                    "iata": airport.get("iata"),
                                    "icao": airport.get("icao"),
                                    "name": airport.get("name"),
                                    "location": airport.get("location"),
                                    "skyId": airport.get("skyId")
                                }
                            }
                    
                    return {"valid": False, "error": "Airport code not found"}
                else:
                    return {"valid": False, "error": f"API error: {response.status_code}"}
                
        except Exception as e:
            return {"valid": False, "error": str(e)}

    def _parse_rapidapi_skyscanner_results(self, results: Dict) -> List[Dict]:
        """Parse RapidAPI Skyscanner results from web endpoints"""
        flights = []
        
        try:
            # Extract data from the new web API structure
            data = results.get("data", {})
            itineraries = data.get("itineraries", {})
            results_data = itineraries.get("results", {})
            
            # Extract flight results
            for itinerary_id, itinerary in results_data.items():
                # Get pricing options
                pricing_options = itinerary.get("pricingOptions", [])
                
                for option in pricing_options:
                    price = option.get("price", {})
                    agent = option.get("agentIds", [""])[0]
                    
                    # Get leg details
                    leg_id = itinerary.get("legIds", [""])[0]
                    leg = itineraries.get("legs", {}).get(leg_id, {})
                    
                    # Get segment details
                    segments = []
                    for segment_id in leg.get("segmentIds", []):
                        segment = itineraries.get("segments", {}).get(segment_id, {})
                        segments.append({
                            "departure": segment.get("departureDateTime"),
                            "arrival": segment.get("arrivalDateTime"),
                            "origin": segment.get("originPlaceId"),
                            "destination": segment.get("destinationPlaceId"),
                            "carrier": segment.get("marketingCarrierId")
                        })
                    
                    # Calculate duration
                    duration = self._calculate_duration(segments)
                    
                    flights.append({
                        "id": f"rapidapi_skyscanner_{itinerary_id}_{agent}",
                        "airline": agent,
                        "flight_number": f"{agent} Flight",
                        "departure_time": segments[0].get("departure") if segments else "",
                        "arrival_time": segments[-1].get("arrival") if segments else "",
                        "duration": duration,
                        "price": {"USD": price.get("amount", 0)},
                        "stops": len(segments) - 1,
                        "aircraft": "Commercial Aircraft",
                        "booking_link": option.get("url", ""),
                        "source": "RapidAPI Skyscanner Web",
                        "origin": segments[0].get("origin", "") if segments else "",
                        "destination": segments[-1].get("destination", "") if segments else ""
                    })
                    
        except Exception as e:
            logger.error(f"Error parsing RapidAPI Skyscanner results: {e}")
            
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
                           departure_date: str, passengers: int = 1, 
                           return_date: str = None, search_type: str = "one-way") -> List[Dict]:
        """Search flights using all available APIs with support for different search types"""
        all_flights = []
        
        # Search with Skyscanner
        if self.skyscanner_available:
            skyscanner_flights = await self.search_flights_skyscanner(
                origin, destination, departure_date, passengers, return_date, search_type
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
