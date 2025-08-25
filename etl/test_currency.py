from currency_client import CurrencyClient

if __name__ == "__main__":
    client = CurrencyClient()
    
    print("=== Testing Exchangerate.host API ===")
    
    # Test current exchange rate
    print("\n1. Current USD to EUR exchange rate:")
    try:
        rate_data = client.get_exchange_rate("USD", "EUR")
        if 'rates' in rate_data and 'EUR' in rate_data['rates']:
            print(f"   Rate: 1 USD = {rate_data['rates']['EUR']} EUR")
            print(f"   Date: {rate_data.get('date', 'N/A')}")
        else:
            print(f"   Response: {rate_data}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test currency conversion
    print("\n2. Converting 100 USD to EUR:")
    try:
        conversion = client.convert_amount(100, "USD", "EUR")
        if 'result' in conversion:
            print(f"   100 USD = {conversion['result']} EUR")
            if 'info' in conversion and 'rate' in conversion['info']:
                print(f"   Rate used: {conversion['info']['rate']}")
        else:
            print(f"   Response: {conversion}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test supported currencies
    print("\n3. Getting supported currencies (first 5):")
    try:
        currencies = client.get_supported_currencies()
        if 'symbols' in currencies:
            currency_list = list(currencies['symbols'].keys())[:5]
            print(f"   Supported currencies: {', '.join(currency_list)}")
        else:
            print(f"   Response: {currencies}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n=== Testing Frankfurter.app API ===")
    
    # Test Frankfurter exchange rate
    print("\n4. Frankfurter USD to EUR exchange rate:")
    try:
        frankfurter_rate = client.get_frankfurter_rate("USD", "EUR")
        print(f"   Rate: 1 USD = {frankfurter_rate['rates']['EUR']} EUR")
        print(f"   Date: {frankfurter_rate['date']}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test Frankfurter currencies
    print("\n5. Frankfurter supported currencies (first 5):")
    try:
        frankfurter_currencies = client.get_frankfurter_currencies()
        currency_list = list(frankfurter_currencies.keys())[:5]
        print(f"   Supported currencies: {', '.join(currency_list)}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n✅ Currency API tests completed!") 