#!/usr/bin/env python3

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import discover_destinations

async def test_simple_dallas():
    """Test with a simple request that should work with fallback data"""
    print("🧪 Testing simple Dallas vacation search...")
    
    # Use a higher budget to ensure we get results
    request = {
        'query': 'vacation',
        'origin': 'Dallas',
        'budget': '2000',  # Higher budget
        'dates': '2024-12-15 to 2024-12-20',
        'travelers': '1',
        'type': 'city'
    }
    
    try:
        result = await discover_destinations(request)
        destinations = result.get('destinations', [])
        
        print(f"\n✅ Found {len(destinations)} destinations!")
        print(f"Budget: ${result.get('budget_usd', 0)}")
        print(f"Origin: {result.get('origin', 'N/A')}")
        
        if destinations:
            print("\n🏆 Top 3 destinations:")
            for i, dest in enumerate(destinations[:3], 1):
                print(f"\n{i}. {dest['name']}, {dest['country']}")
                print(f"   💰 Total Cost: ${dest.get('total_cost', 0):.2f}")
                print(f"   💵 Remaining: ${dest.get('budget_remaining', 0):.2f}")
                print(f"   📊 Budget Used: {dest.get('budget_utilization', 0):.1f}%")
                print(f"   ✈️  Flights: ${dest.get('flight_price', 0):.2f}")
                print(f"   🏨 Hotel: ${dest.get('hotel_price', 0):.2f}")
                print(f"   🍽️  Daily: ${dest.get('daily_cost', 0):.2f}")
                print(f"   ⭐ Rating: {dest.get('rating', 0)}/5.0")
                print(f"   🏷️  Type: {dest.get('type', 'N/A')}")
        else:
            print("\n❌ No destinations found. This might be due to:")
            print("   - API rate limiting")
            print("   - Budget too low")
            print("   - No suitable destinations in dataset")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_simple_dallas())
