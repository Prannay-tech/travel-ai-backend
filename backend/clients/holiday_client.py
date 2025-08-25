"""
Holiday client using Calendarific API.
"""

import httpx
from typing import Dict, Optional, List
from datetime import datetime, timedelta
import logging
from ..config import settings

logger = logging.getLogger(__name__)

class HolidayClient:
    """Client for holiday and event data using Calendarific API."""
    
    def __init__(self):
        self.base_url = settings.CALENDARIFIC_BASE_URL
        self.api_key = settings.CALENDARIFIC_API_KEY
    
    async def get_holidays(
        self, 
        country: str, 
        year: Optional[int] = None,
        month: Optional[int] = None
    ) -> Optional[List[Dict]]:
        """Get holidays for a specific country and year/month."""
        try:
            if not self.api_key:
                logger.warning("Calendarific API key not configured, using mock data")
                return self._get_mock_holidays(country)
            
            if year is None:
                year = datetime.now().year
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                url = f"{self.base_url}/holidays"
                params = {
                    "api_key": self.api_key,
                    "country": country,
                    "year": year
                }
                
                if month:
                    params["month"] = month
                
                response = await client.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                
                if data.get("meta", {}).get("code") != 200:
                    logger.error(f"Calendarific API error: {data.get('meta', {}).get('error_message')}")
                    return self._get_mock_holidays(country)
                
                holidays = []
                for holiday in data.get("response", {}).get("holidays", []):
                    holidays.append({
                        "name": holiday["name"],
                        "date": holiday["date"]["iso"],
                        "description": holiday.get("description", ""),
                        "type": holiday.get("type", []),
                        "country": holiday["country"]["name"]
                    })
                
                logger.info(f"Retrieved {len(holidays)} holidays for {country} in {year}")
                return holidays
                
        except httpx.RequestError as e:
            logger.error(f"Error fetching holidays: {e}")
            return self._get_mock_holidays(country)
        except Exception as e:
            logger.error(f"Unexpected error in get_holidays: {e}")
            return self._get_mock_holidays(country)
    
    async def get_upcoming_holidays(
        self, 
        country: str, 
        days_ahead: int = 90
    ) -> Optional[List[Dict]]:
        """Get upcoming holidays within the next N days."""
        try:
            today = datetime.now()
            end_date = today + timedelta(days=days_ahead)
            
            # Get holidays for current year
            current_year_holidays = await self.get_holidays(country, today.year)
            upcoming_holidays = []
            
            if current_year_holidays:
                for holiday in current_year_holidays:
                    try:
                        holiday_date = datetime.strptime(holiday["date"], "%Y-%m-%d")
                        if today <= holiday_date <= end_date:
                            upcoming_holidays.append(holiday)
                    except ValueError:
                        continue
            
            # If we need next year's holidays too
            if end_date.year > today.year:
                next_year_holidays = await self.get_holidays(country, end_date.year)
                if next_year_holidays:
                    for holiday in next_year_holidays:
                        try:
                            holiday_date = datetime.strptime(holiday["date"], "%Y-%m-%d")
                            if holiday_date <= end_date:
                                upcoming_holidays.append(holiday)
                        except ValueError:
                            continue
            
            # Sort by date
            upcoming_holidays.sort(key=lambda x: x["date"])
            
            logger.info(f"Retrieved {len(upcoming_holidays)} upcoming holidays for {country}")
            return upcoming_holidays[:10]  # Limit to 10
            
        except Exception as e:
            logger.error(f"Error getting upcoming holidays: {e}")
            return self._get_mock_upcoming_holidays(country)
    
    async def get_events(
        self, 
        country: str, 
        city: Optional[str] = None,
        year: Optional[int] = None
    ) -> Optional[List[Dict]]:
        """Get events for a specific location."""
        try:
            if not self.api_key:
                logger.warning("Calendarific API key not configured, using mock data")
                return self._get_mock_events(country, city)
            
            if year is None:
                year = datetime.now().year
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                url = f"{self.base_url}/events"
                params = {
                    "api_key": self.api_key,
                    "country": country,
                    "year": year
                }
                
                if city:
                    params["city"] = city
                
                response = await client.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                
                if data.get("meta", {}).get("code") != 200:
                    logger.error(f"Calendarific API error: {data.get('meta', {}).get('error_message')}")
                    return self._get_mock_events(country, city)
                
                events = []
                for event in data.get("response", {}).get("events", []):
                    events.append({
                        "name": event["title"],
                        "date": event["date"]["iso"],
                        "description": event.get("description", ""),
                        "venue": event.get("venue", {}).get("name", ""),
                        "country": event.get("country", {}).get("name", country)
                    })
                
                logger.info(f"Retrieved {len(events)} events for {country}")
                return events
                
        except httpx.RequestError as e:
            logger.error(f"Error fetching events: {e}")
            return self._get_mock_events(country, city)
        except Exception as e:
            logger.error(f"Unexpected error in get_events: {e}")
            return self._get_mock_events(country, city)
    
    def _get_mock_holidays(self, country: str) -> List[Dict]:
        """Mock holiday data."""
        mock_holidays = {
            "USA": [
                {"name": "Independence Day", "date": "2024-07-04", "description": "National holiday with fireworks"},
                {"name": "Labor Day", "date": "2024-09-02", "description": "End of summer celebration"},
                {"name": "Thanksgiving", "date": "2024-11-28", "description": "Family gathering and feast"}
            ],
            "Indonesia": [
                {"name": "Independence Day", "date": "2024-08-17", "description": "National independence celebration"},
                {"name": "Nyepi", "date": "2024-03-11", "description": "Balinese day of silence"}
            ],
            "Japan": [
                {"name": "Golden Week", "date": "2024-04-29", "description": "Series of national holidays"},
                {"name": "Obon", "date": "2024-08-13", "description": "Buddhist festival honoring ancestors"}
            ],
            "France": [
                {"name": "Bastille Day", "date": "2024-07-14", "description": "French National Day"},
                {"name": "Armistice Day", "date": "2024-11-11", "description": "World War I remembrance"}
            ]
        }
        
        return mock_holidays.get(country, [
            {"name": "Local Festival", "date": "2024-08-15", "description": "Annual cultural celebration"}
        ])
    
    def _get_mock_upcoming_holidays(self, country: str) -> List[Dict]:
        """Mock upcoming holidays data."""
        today = datetime.now()
        upcoming = []
        
        # Generate some upcoming holidays
        for i in range(3):
            date_obj = today + timedelta(days=30 + i * 30)
            upcoming.append({
                "name": f"Local Festival {i+1}",
                "date": date_obj.strftime("%Y-%m-%d"),
                "description": f"Annual celebration in {country}"
            })
        
        return upcoming
    
    def _get_mock_events(self, country: str, city: Optional[str] = None) -> List[Dict]:
        """Mock events data."""
        location = city if city else country
        return [
            {
                "name": f"Cultural Festival in {location}",
                "date": (datetime.now() + timedelta(days=45)).strftime("%Y-%m-%d"),
                "description": "Annual cultural celebration with music and food",
                "venue": f"Central Plaza, {location}",
                "country": country
            },
            {
                "name": f"Food & Wine Festival",
                "date": (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d"),
                "description": "Celebration of local cuisine and wines",
                "venue": f"Downtown {location}",
                "country": country
            }
        ]

# Global holiday client instance
holiday_client = HolidayClient() 