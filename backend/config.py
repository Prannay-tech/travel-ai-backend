"""
Configuration settings for the Travel AI backend.
"""

import os
from typing import Optional

class Settings:
    """Application settings loaded from environment variables."""
    
    # Database
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    
    # API Keys
    OPENTRIPMAP_API_KEY: str = os.getenv("OPENTRIPMAP_API_KEY", "")
    AMADEUS_CLIENT_ID: str = os.getenv("AMADEUS_CLIENT_ID", "")
    AMADEUS_CLIENT_SECRET: str = os.getenv("AMADEUS_CLIENT_SECRET", "")
    TOMTOM_API_KEY: str = os.getenv("TOMTOM_API_KEY", "")
    WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY", "")
    CALENDARIFIC_API_KEY: str = os.getenv("CALENDARIFIC_API_KEY", "")
    EXCHANGERATE_API_KEY: str = os.getenv("EXCHANGERATE_API_KEY", "")
    
    # Currency API (Exchangerate.host)
    EXCHANGERATE_BASE_URL: str = "https://api.exchangerate.host"
    
    # Weather API
    WEATHER_BASE_URL: str = "https://api.weatherapi.com/v1"
    
    # Calendarific API
    CALENDARIFIC_BASE_URL: str = "https://calendarific.com/api/v2"
    
    # TomTom API
    TOMTOM_BASE_URL: str = "https://api.tomtom.com/search/2"
    
    # Amadeus API
    AMADEUS_BASE_URL: str = "https://test.api.amadeus.com/v1"
    
    # OpenTripMap API
    OPENTRIPMAP_BASE_URL: str = "https://api.opentripmap.com/0.1/en/places"
    
    # Application Settings
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    
    # Cache Settings
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "3600"))  # 1 hour default
    
    @classmethod
    def validate_required_keys(cls) -> list:
        """Validate that required API keys are present."""
        missing_keys = []
        
        # Optional keys (can work without them)
        optional_keys = [
            "OPENTRIPMAP_API_KEY",
            "AMADEUS_CLIENT_ID", 
            "AMADEUS_CLIENT_SECRET",
            "TOMTOM_API_KEY",
            "WEATHER_API_KEY",
            "CALENDARIFIC_API_KEY",
            "EXCHANGERATE_API_KEY"
        ]
        
        # Required keys
        required_keys = [
            "SUPABASE_URL",
            "SUPABASE_KEY"
        ]
        
        for key in required_keys:
            if not getattr(cls, key):
                missing_keys.append(key)
        
        return missing_keys

# Global settings instance
settings = Settings() 