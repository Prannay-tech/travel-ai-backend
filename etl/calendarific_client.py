import os
from dotenv import load_dotenv
load_dotenv()
import requests

class CalendarificClient:
    def __init__(self):
        self.api_key = os.getenv("CALENDARIFIC_API_KEY") or "bOuJMpGlgN6b8CNH1SdzwZXnkAi4qUQM"
        self.base_url = "https://calendarific.com/api/v2/holidays"

    def get_holidays(self, country, year, type=None):
        params = {
            "api_key": self.api_key,
            "country": country,
            "year": year
        }
        if type:
            params["type"] = type
        print("Requesting:", self.base_url)
        print("Params:", params)
        resp = requests.get(self.base_url, params=params)
        resp.raise_for_status()
        return resp.json().get("response", {}).get("holidays", []) 