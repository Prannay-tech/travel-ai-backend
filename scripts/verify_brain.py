import asyncio
import os
import json
from dotenv import load_dotenv
from app.services.ai_agent import TravelAgent

# Load environment variables (API Keys)
load_dotenv()

async def verify_trotter_brain():
    """
    Diagnostic script to verify the Trotter AI Agentic Brain.
    Tests Tool-use, Multi-turn reasoning, and Policy Enforcement.
    """
    print("\n" + "="*50)
    print("🧠 TROTTER AI: BRAIN VERIFICATION ENGINE")
    print("="*50 + "\n")

    # Initialize Agent with our chosen Groq model
    model_name = os.getenv("LLM_MODEL", "groq/llama-3.3-70b-versatile")
    agent = TravelAgent(model=model_name)
    
    # ---------------------------------------------------------
    # SCENARIO 1: Personal Mode + Curation Tool
    # ---------------------------------------------------------
    print("▶️ TEST 1: Personal Curation (Scraping)")
    print("Query: 'Plan a 3-day budget trip to Tokyo, find some hidden gems from blogs.'")
    
    msg_personal = [{"role": "user", "content": "I want to visit Tokyo for 3 days on a budget. Can you search for some hidden gems from travel blogs for me?"}]
    
    try:
        response_p = await agent.chat(msg_personal, is_business=False)
        print(f"\n[AGENT RESPONSE]:\n{response_p['content']}\n")
    except Exception as e:
        print(f"[ERROR]: {str(e)}")

    print("-" * 30)

    # ---------------------------------------------------------
    # SCENARIO 2: Business Mode + Policy Enforcement
    # ---------------------------------------------------------
    print("▶️ TEST 2: Business Compliance (Arbiter + Policy)")
    print("Query: 'Find me a luxury hotel in Paris for tonight.'")
    
    msg_business = [{"role": "user", "content": "I need a luxury hotel in Paris for tonight. I'm on a business trip."}]
    
    try:
        response_b = await agent.chat(msg_business, is_business=True)
        print(f"\n[AGENT RESPONSE]:\n{response_b['content']}\n")
    except Exception as e:
        print(f"[ERROR]: {str(e)}")

    print("\n" + "="*50)
    print("🏁 VERIFICATION COMPLETE")
    print("="*50)

if __name__ == "__main__":
    asyncio.run(verify_trotter_brain())
