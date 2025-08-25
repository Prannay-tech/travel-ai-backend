from weatherapi_client import WeatherAPIClient

if __name__ == "__main__":
    client = WeatherAPIClient()
    
    # Test coordinates for New York City
    lat, lon = 40.7128, -74.0060
    
    print("=== Testing WeatherAPI.com ===")
    
    print("\n1. Current Weather:")
    try:
        current_weather = client.get_current_weather(lat, lon)
        location = current_weather['location']
        current = current_weather['current']
        
        print(f"   Location: {location['name']}, {location['country']}")
        print(f"   Temperature: {current['temp_c']}°C ({current['temp_f']}°F)")
        print(f"   Condition: {current['condition']['text']}")
        print(f"   Humidity: {current['humidity']}%")
        print(f"   Wind: {current['wind_kph']} km/h")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n2. 3-Day Forecast:")
    try:
        forecast = client.get_forecast(lat, lon, days=3)
        forecast_days = forecast['forecast']['forecastday']
        
        for day in forecast_days:
            date = day['date']
            day_data = day['day']
            print(f"   {date}: {day_data['maxtemp_c']}°C / {day_data['mintemp_c']}°C - {day_data['condition']['text']}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n3. Astronomy Data:")
    try:
        astronomy = client.get_astronomy(lat, lon)
        astro = astronomy['astronomy']['astro']
        
        print(f"   Sunrise: {astro['sunrise']}")
        print(f"   Sunset: {astro['sunset']}")
        print(f"   Moonrise: {astro['moonrise']}")
        print(f"   Moonset: {astro['moonset']}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n4. Weather by City Name:")
    try:
        city_weather = client.get_weather_by_city("Paris")
        location = city_weather['location']
        current = city_weather['current']
        
        print(f"   {location['name']}, {location['country']}: {current['temp_c']}°C - {current['condition']['text']}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n✅ WeatherAPI.com tests completed!") 