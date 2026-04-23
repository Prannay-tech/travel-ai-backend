import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Travel AI API"
    VERSION: str = "1.0.0"
    
    # AI Keys and Configuration
    LLM_MODEL: str = os.getenv("LLM_MODEL", "groq/llama-3.3-70b-versatile")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # 3rd Party APIs
    SKYSCANNER_API_KEY: str = os.getenv("SKYSCANNER_API_KEY", "")
    AMADEUS_CLIENT_ID: str = os.getenv("AMADEUS_CLIENT_ID", "")
    AMADEUS_CLIENT_SECRET: str = os.getenv("AMADEUS_CLIENT_SECRET", "")
    HOTELS_API_KEY: str = os.getenv("HOTELS_API_KEY", "")
    WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY", "")
    GOOGLE_PLACES_API_KEY: str = os.getenv("GOOGLE_PLACES_API_KEY", "")
    CURRENCY_API_KEY: str = os.getenv("CURRENCY_API_KEY", "")
    
    # Security / Auth
    SECRET_KEY: str = os.getenv("SECRET_KEY", "fallback_secret_key_change_in_prod")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

settings = Settings()
