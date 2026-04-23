import asyncio
import json
import os
from dotenv import load_dotenv
from app.services.graph_agent import graph_brain

load_dotenv()

TEST_SCENARIOS = [
    {
        "name": "Luxury Business Trip (Policy Test)",
        "query": "I need a 5-star hotel in London for tonight. Budget is $400. This is a business trip.",
        "is_business": True,
        "success_criteria": ["Caught policy violation (if price > max)", "Professional tone", "Real-time hotel lookup"]
    },
    {
        "name": "Leisure Persona Test (Age 70)",
        "query": "I want a 3-day trip to Rome. I'm 70 years old and love art.",
        "is_business": False,
        "success_criteria": ["Low-intensity activities only", "Art-focused gems", "Geographical logical flow"]
    },
    {
        "name": "Multi-Vendor Search (Arbiter Test)",
        "query": "Find me the cheapest flights and a hotel for a weekend in NYC.",
        "is_business": False,
        "success_criteria": ["Called flight provider", "Called hotel provider", "Unified price matches"]
    }
]

async def run_inference_evals():
    print("\n" + "="*60)
    print("🧠 TROTTER AI: INFERENCE QUALITY EVALUATION")
    print("="*60 + "\n")

    for scenario in TEST_SCENARIOS:
        print(f"▶️ RUNNING: {scenario['name']}")
        print(f"   Query: {scenario['query']}")
        
        try:
            # We wrap the brain execution to capture intermediate steps
            result = await graph_brain.run(
                query=scenario['query'],
                is_business=scenario['is_business']
            )
            
            # The final response is the last message content
            final_inference = result["messages"][-1].content
            
            print("\n   [RESULT]:")
            print(f"   {final_inference[:300]}...") # Truncated
            
            print("\n   [BRAIN STATE]:")
            print(f"   Violations Count: {len(result.get('policy_violations', []))}")
            print(f"   Data Points Found: {len(result.get('data_results', []))}")
            
            print("\n" + "-"*40)
        except Exception as e:
            print(f"   ❌ FAILED: {str(e)}")

    print("\n🏁 EVALUATIONS COMPLETE")

if __name__ == "__main__":
    asyncio.run(run_inference_evals())
