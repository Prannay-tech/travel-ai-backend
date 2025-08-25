"""
Test script for the currency client using Exchangerate.host API.
"""

import asyncio
import os
from clients.currency_client import currency_client

async def test_currency_client():
    """Test the currency client functionality."""
    print("🧪 Testing Currency Client (Exchangerate.host)")
    print("=" * 50)
    
    # Test 1: Get exchange rates
    print("\n1. Testing get_exchange_rates...")
    try:
        rates = await currency_client.get_exchange_rates("USD")
        print(f"✅ Successfully retrieved {len(rates)} exchange rates")
        print(f"Sample rates: {dict(list(rates.items())[:5])}")
    except Exception as e:
        print(f"❌ Error getting exchange rates: {e}")
    
    # Test 2: Convert currency
    print("\n2. Testing convert_currency...")
    try:
        converted = await currency_client.convert_currency(1000, "USD", "EUR")
        if converted:
            print(f"✅ Successfully converted 1000 USD to {converted:.2f} EUR")
        else:
            print("❌ Currency conversion failed")
    except Exception as e:
        print(f"❌ Error converting currency: {e}")
    
    # Test 3: Get supported currencies
    print("\n3. Testing get_supported_currencies...")
    try:
        currencies = await currency_client.get_supported_currencies()
        print(f"✅ Supported currencies: {currencies}")
    except Exception as e:
        print(f"❌ Error getting supported currencies: {e}")
    
    # Test 4: Check if currency is supported
    print("\n4. Testing is_supported_currency...")
    test_currencies = ["USD", "EUR", "INVALID"]
    for currency in test_currencies:
        is_supported = currency_client.is_supported_currency(currency)
        print(f"   {currency}: {'✅ Supported' if is_supported else '❌ Not supported'}")
    
    # Test 5: Historical rates (if API key is available)
    print("\n5. Testing historical rates...")
    if currency_client.api_key:
        try:
            historical = await currency_client.get_historical_rates("2024-01-01", "USD")
            if historical:
                print(f"✅ Successfully retrieved historical rates for 2024-01-01")
                print(f"Sample historical rates: {dict(list(historical.items())[:3])}")
            else:
                print("❌ Historical rates retrieval failed")
        except Exception as e:
            print(f"❌ Error getting historical rates: {e}")
    else:
        print("⚠️  Skipping historical rates test (no API key)")
    
    print("\n" + "=" * 50)
    print("🏁 Currency client testing completed!")

if __name__ == "__main__":
    # Set up environment for testing
    if not os.getenv("EXCHANGERATE_API_KEY"):
        print("⚠️  No EXCHANGERATE_API_KEY found. Some features may use fallback data.")
    
    asyncio.run(test_currency_client()) 