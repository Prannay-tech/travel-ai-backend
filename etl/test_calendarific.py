from calendarific_client import CalendarificClient

if __name__ == "__main__":
    client = CalendarificClient()
    # Example: United States, 2024
    holidays = client.get_holidays(country="US", year=2024)
    print(f"Found {len(holidays)} holidays:")
    for holiday in holidays[:5]:  # Print first 5 holidays
        print(f"- {holiday['name']} on {holiday['date']['iso']}") 