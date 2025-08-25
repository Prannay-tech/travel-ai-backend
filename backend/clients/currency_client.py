"""
Currency conversion client using Exchangerate.host API.
"""

import httpx
import asyncio
from typing import Dict, Optional
from datetime import datetime, date
import logging
from ..config import settings

logger = logging.getLogger(__name__)

class CurrencyClient:
    """Client for currency conversion using Exchangerate.host API."""
    
    def __init__(self):
        self.base_url = "https://api.exchangerate.host"
        self.api_key = settings.EXCHANGERATE_API_KEY
        self.supported_currencies = [
            "USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "SGD"
        ]
    
    async def get_exchange_rates(self, base_currency: str = "USD") -> Dict[str, float]:
        """Get current exchange rates for all supported currencies."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                url = f"{self.base_url}/latest"
                params = {"base": base_currency}
                
                # Add API key if available
                if self.api_key:
                    params["apikey"] = self.api_key
                
                response = await client.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                
                if not data.get("success", False):
                    logger.error(f"Exchangerate API error: {data.get('error', {}).get('info', 'Unknown error')}")
                    return self._get_fallback_rates(base_currency)
                
                rates = data.get("rates", {})
                
                # Add base currency with rate 1.0
                rates[base_currency] = 1.0
                
                logger.info(f"Retrieved exchange rates for {base_currency}")
                return rates
                
        except httpx.RequestError as e:
            logger.error(f"Error fetching exchange rates: {e}")
            # Return fallback rates
            return self._get_fallback_rates(base_currency)
        except Exception as e:
            logger.error(f"Unexpected error in get_exchange_rates: {e}")
            return self._get_fallback_rates(base_currency)
    
    async def convert_currency(
        self, 
        amount: float, 
        from_currency: str, 
        to_currency: str
    ) -> Optional[float]:
        """Convert amount from one currency to another."""
        try:
            if from_currency == to_currency:
                return amount
            
            rates = await self.get_exchange_rates(from_currency)
            if to_currency in rates:
                converted_amount = amount * rates[to_currency]
                logger.info(f"Converted {amount} {from_currency} to {converted_amount:.2f} {to_currency}")
                return round(converted_amount, 2)
            else:
                logger.error(f"Currency {to_currency} not supported")
                return None
                
        except Exception as e:
            logger.error(f"Error converting currency: {e}")
            return None
    
    async def get_historical_rates(
        self, 
        date_str: str, 
        base_currency: str = "USD"
    ) -> Optional[Dict[str, float]]:
        """Get historical exchange rates for a specific date."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                url = f"{self.base_url}/{date_str}"
                params = {"base": base_currency}
                
                # Add API key if available
                if self.api_key:
                    params["apikey"] = self.api_key
                
                response = await client.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                
                if not data.get("success", False):
                    logger.error(f"Exchangerate API error: {data.get('error', {}).get('info', 'Unknown error')}")
                    return None
                
                rates = data.get("rates", {})
                rates[base_currency] = 1.0
                
                logger.info(f"Retrieved historical rates for {date_str}")
                return rates
                
        except httpx.RequestError as e:
            logger.error(f"Error fetching historical rates: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in get_historical_rates: {e}")
            return None
    
    def _get_fallback_rates(self, base_currency: str) -> Dict[str, float]:
        """Fallback exchange rates if API is unavailable."""
        fallback_rates = {
            "USD": 1.0,
            "EUR": 0.85,
            "GBP": 0.73,
            "JPY": 110.0,
            "CAD": 1.25,
            "AUD": 1.35,
            "CHF": 0.92,
            "SGD": 1.35
        }
        
        # Adjust rates based on base currency
        if base_currency != "USD":
            base_rate = fallback_rates.get(base_currency, 1.0)
            adjusted_rates = {}
            for currency, rate in fallback_rates.items():
                adjusted_rates[currency] = rate / base_rate
            return adjusted_rates
        
        return fallback_rates
    
    def is_supported_currency(self, currency: str) -> bool:
        """Check if a currency is supported."""
        return currency.upper() in self.supported_currencies
    
    async def get_supported_currencies(self) -> list:
        """Get list of supported currencies."""
        return self.supported_currencies.copy()

# Global currency client instance
currency_client = CurrencyClient() 