import os
from dotenv import load_dotenv
load_dotenv()
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class CurrencyClient:
    def __init__(self):
        self.exchangerate_base = "https://api.exchangerate.host"
        self.frankfurter_base = "https://api.frankfurter.app"
        self.exchangerate_api_key = os.getenv("EXCHANGERATE_API_KEY")
        
    def get_exchange_rate(self, from_currency: str, to_currency: str, date: Optional[str] = None) -> Dict:
        """Get exchange rate using Exchangerate.host API"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
            
        url = f"{self.exchangerate_base}/latest"
        params = {
            "base": from_currency.upper(),
            "symbols": to_currency.upper()
        }
        if self.exchangerate_api_key:
            params["access_key"] = self.exchangerate_api_key
        
        print(f"Requesting exchange rate: {url}")
        print(f"Params: {params}")
        
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        return resp.json()
    
    def get_historical_rates(self, from_currency: str, to_currencies: List[str], 
                           start_date: str, end_date: str) -> Dict:
        """Get historical exchange rates using Exchangerate.host API"""
        url = f"{self.exchangerate_base}/timeseries"
        params = {
            "base": from_currency.upper(),
            "symbols": ",".join([curr.upper() for curr in to_currencies]),
            "start_date": start_date,
            "end_date": end_date
        }
        if self.exchangerate_api_key:
            params["access_key"] = self.exchangerate_api_key
        
        print(f"Requesting historical rates: {url}")
        print(f"Params: {params}")
        
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        return resp.json()
    
    def get_supported_currencies(self) -> Dict:
        """Get list of supported currencies using Exchangerate.host API"""
        url = f"{self.exchangerate_base}/symbols"
        params = {}
        if self.exchangerate_api_key:
            params["access_key"] = self.exchangerate_api_key
        
        print(f"Requesting supported currencies: {url}")
        
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        return resp.json()
    
    def get_frankfurter_rate(self, from_currency: str, to_currency: str, 
                           date: Optional[str] = None) -> Dict:
        """Get exchange rate using Frankfurter.app API"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
            
        url = f"{self.frankfurter_base}/{date}"
        params = {
            "from": from_currency.upper(),
            "to": to_currency.upper()
        }
        
        print(f"Requesting Frankfurter rate: {url}")
        print(f"Params: {params}")
        
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        return resp.json()
    
    def get_frankfurter_currencies(self) -> Dict:
        """Get list of supported currencies using Frankfurter.app API"""
        url = f"{self.frankfurter_base}/currencies"
        
        print(f"Requesting Frankfurter currencies: {url}")
        
        resp = requests.get(url)
        resp.raise_for_status()
        return resp.json()
    
    def convert_amount(self, amount: float, from_currency: str, to_currency: str, 
                      date: Optional[str] = None) -> Dict:
        """Convert amount between currencies using Exchangerate.host API"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
            
        url = f"{self.exchangerate_base}/convert"
        params = {
            "from": from_currency.upper(),
            "to": to_currency.upper(),
            "amount": amount,
            "date": date
        }
        if self.exchangerate_api_key:
            params["access_key"] = self.exchangerate_api_key
        
        print(f"Requesting conversion: {url}")
        print(f"Params: {params}")
        
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        return resp.json() 