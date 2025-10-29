#!/usr/bin/env python3

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import discover_destinations

async def test_dallas_500():
    """Test the comprehensive cost calculation for Dallas to vacation with $500 budget"""
    print("🧪 Testing Dallas $500 vacation search...")
    
    request = {
        'query': 'vacation',
        'origin': 'Dallas',
        'budget': '500',
        'dates': '2024-12-15 to 2024-12-20',
        'travelers': '1',
        'type': ''
    }
    
    try:
        result = await discover_destinations(request)
        destinations = result.get('destinations', [])
        
        print(f"\n✅ Found {len(destinations)} destinations within $500 budget!")
        budget_usd = result.get('budget_usd', 0)
        if isinstance(budget_usd, dict):
            budget_usd = budget_usd.get('converted_amount', 0)
        budget_usd = float(budget_usd)
        print(f"Budget: ${budget_usd:.2f}")
        print(f"Origin: {result.get('origin', 'N/A')}")
        
        print("\n🏆 Top 5 destinations:")
        for i, dest in enumerate(destinations[:5], 1):
            print(f"\n{i}. {dest['name']}, {dest['country']}")
            print(f"   💰 Total Cost: ${dest['total_cost']:.2f}")
            print(f"   💵 Remaining: ${dest['budget_remaining']:.2f}")
            print(f"   📊 Budget Used: {dest['budget_utilization']:.1f}%")
            print(f"   ✈️  Flights: ${dest['flight_price']:.2f}")
            print(f"   🏨 Hotel: ${dest['hotel_price']:.2f}")
            print(f"   🍽️  Daily: ${dest['daily_cost']:.2f}")
            print(f"   ⭐ Rating: {dest['rating']}/5.0")
            print(f"   🏷️  Type: {dest['type']}")
            
            # Show detailed breakdown
            breakdown = dest.get('cost_breakdown', {})
            if breakdown:
                print(f"   📋 Breakdown:")
                print(f"      - Flights: ${breakdown['flights']['total']:.2f}")
                print(f"      - Hotel: ${breakdown['hotel']['total']:.2f}")
                print(f"      - Daily Expenses: ${breakdown['daily_expenses']['total']:.2f}")
                print(f"      - Additional: ${breakdown['additional']['total']:.2f}")
        
        if len(destinations) == 0:
            print("\n❌ No destinations found within budget. Try increasing budget or checking different dates.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_dallas_500())
