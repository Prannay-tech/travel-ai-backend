from weather_client import WeatherClient

if __name__ == "__main__":
    client = WeatherClient()
    
    # Test coordinates for New York City
    lat, lon = 40.7128, -74.0060
    
    print("=== Testing Current Weather ===")
    current_weather = client.get_current_weather(lat, lon)
    print(f"Current temperature: {current_weather['current']['temperature_2m']}°C")
    print(f"Humidity: {current_weather['current']['relative_humidity_2m']}%")
    print(f"Weather code: {current_weather['current']['weather_code']}")
    
    print("\n=== Testing 7-Day Forecast ===")
    forecast = client.get_forecast(lat, lon, days=7)
    print(f"Forecast for {len(forecast['daily']['time'])} days:")
    for i in range(min(3, len(forecast['daily']['time']))):  # Show first 3 days
        date = forecast['daily']['time'][i]
        max_temp = forecast['daily']['temperature_2m_max'][i]
        min_temp = forecast['daily']['temperature_2m_min'][i]
        print(f"  {date}: {min_temp}°C to {max_temp}°C") 