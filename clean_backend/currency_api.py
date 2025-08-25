"""
Currency API Integration
Supports real-time currency conversion and exchange rates.
"""

import httpx
import os
import logging
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

# API Keys
CURRENCY_API_KEY = os.getenv("CURRENCY_API_KEY", "")

class CurrencyAPI:
    """Currency conversion using ExchangeRate-API"""
    
    def __init__(self):
        self.api_key = CURRENCY_API_KEY
        self.base_url = "https://api.exchangerate.host"
        self.available = bool(self.api_key)
        
    async def get_exchange_rates(self, base_currency: str = "USD") -> Optional[Dict]:
        """Get current exchange rates for a base currency"""
        if not self.available:
            return self._get_mock_rates(base_currency)
            
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/latest",
                    params={
                        "base": base_currency,
                        "apikey": self.api_key
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_rates_data(data)
                else:
                    logger.error(f"Currency API error: {response.status_code}")
                    return self._get_mock_rates(base_currency)
                    
        except Exception as e:
            logger.error(f"Error fetching exchange rates: {e}")
            return self._get_mock_rates(base_currency)
    
    async def convert_currency(self, amount: float, from_currency: str, to_currency: str) -> Optional[Dict]:
        """Convert amount from one currency to another"""
        if not self.available:
            return self._get_mock_conversion(amount, from_currency, to_currency)
            
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/convert",
                    params={
                        "from": from_currency,
                        "to": to_currency,
                        "amount": amount,
                        "apikey": self.api_key
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_conversion_data(data)
                else:
                    logger.error(f"Currency conversion API error: {response.status_code}")
                    return self._get_mock_conversion(amount, from_currency, to_currency)
                    
        except Exception as e:
            logger.error(f"Error converting currency: {e}")
            return self._get_mock_conversion(amount, from_currency, to_currency)
    
    async def get_historical_rates(self, date: str, base_currency: str = "USD") -> Optional[Dict]:
        """Get historical exchange rates for a specific date"""
        if not self.available:
            return self._get_mock_historical_rates(date, base_currency)
            
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/{date}",
                    params={
                        "base": base_currency,
                        "apikey": self.api_key
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_rates_data(data)
                else:
                    logger.error(f"Historical rates API error: {response.status_code}")
                    return self._get_mock_historical_rates(date, base_currency)
                    
        except Exception as e:
            logger.error(f"Error fetching historical rates: {e}")
            return self._get_mock_historical_rates(date, base_currency)
    
    def _parse_rates_data(self, data: Dict) -> Dict:
        """Parse exchange rates API response"""
        try:
            return {
                "base_currency": data.get("base", "USD"),
                "date": data.get("date", datetime.now().date().isoformat()),
                "rates": data.get("rates", {}),
                "success": data.get("success", True),
                "source": "ExchangeRate-API"
            }
        except Exception as e:
            logger.error(f"Error parsing rates data: {e}")
            return self._get_mock_rates("USD")
    
    def _parse_conversion_data(self, data: Dict) -> Dict:
        """Parse currency conversion API response"""
        try:
            return {
                "from_currency": data.get("query", {}).get("from", "USD"),
                "to_currency": data.get("query", {}).get("to", "EUR"),
                "amount": data.get("query", {}).get("amount", 1),
                "result": data.get("result", 0),
                "rate": data.get("info", {}).get("rate", 1),
                "date": data.get("date", datetime.now().date().isoformat()),
                "success": data.get("success", True),
                "source": "ExchangeRate-API"
            }
        except Exception as e:
            logger.error(f"Error parsing conversion data: {e}")
            return self._get_mock_conversion(1, "USD", "EUR")
    
    def _get_mock_rates(self, base_currency: str) -> Dict:
        """Return mock exchange rates"""
        mock_rates = {
            "USD": 1.0,
            "EUR": 0.85,
            "GBP": 0.73,
            "CAD": 1.25,
            "AUD": 1.35,
            "JPY": 110.0,
            "CHF": 0.92,
            "CNY": 6.45,
            "INR": 75.0,
            "BRL": 5.2
        }
        
        # Adjust rates based on base currency
        if base_currency != "USD":
            base_rate = mock_rates.get(base_currency, 1.0)
            adjusted_rates = {}
            for currency, rate in mock_rates.items():
                adjusted_rates[currency] = rate / base_rate
            mock_rates = adjusted_rates
        
        return {
            "base_currency": base_currency,
            "date": datetime.now().date().isoformat(),
            "rates": mock_rates,
            "success": True,
            "source": "Mock Data"
        }
    
    def _get_mock_conversion(self, amount: float, from_currency: str, to_currency: str) -> Dict:
        """Return mock currency conversion"""
        mock_rates = {
            "USD": 1.0,
            "EUR": 0.85,
            "GBP": 0.73,
            "CAD": 1.25,
            "AUD": 1.35,
            "JPY": 110.0,
            "CHF": 0.92,
            "CNY": 6.45,
            "INR": 75.0,
            "BRL": 5.2
        }
        
        from_rate = mock_rates.get(from_currency, 1.0)
        to_rate = mock_rates.get(to_currency, 1.0)
        conversion_rate = to_rate / from_rate
        result = amount * conversion_rate
        
        return {
            "from_currency": from_currency,
            "to_currency": to_currency,
            "amount": amount,
            "result": round(result, 2),
            "rate": round(conversion_rate, 4),
            "date": datetime.now().date().isoformat(),
            "success": True,
            "source": "Mock Data"
        }
    
    def _get_mock_historical_rates(self, date: str, base_currency: str) -> Dict:
        """Return mock historical rates"""
        return self._get_mock_rates(base_currency)

# Global instance
currency_api = CurrencyAPI()
