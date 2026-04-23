from typing import List, Dict, Optional
from typing import List, Dict, Optional, Any
from pydantic import BaseModel

class UserPreferenceMap(BaseModel):
    # Moving away from strict floats. 
    # The AI now just extracts natural language 'tags' like ["Secluded", "Quiet", "Ocean View"]
    core_desires: List[str] = []
    hard_dealbreakers: List[str] = [] # Things they absolutely DO NOT want
    must_haves: List[str] = [] # Things they absolutely MUST have
    budget_flexibility: str = "Strict" # 'Strict', 'Moderate', 'High'

class LocationIntel(BaseModel):
    name: str
    best_months: List[int]
    blackout_months: List[int] # Bad weather/Holidays
    major_events: List[Dict] # [{'name': 'Mardi Gras', 'month': 2, 'vibe': 'Party'}]

class TrotterSalesmanEngine:
    """
    Expert Logic: Operates like a consultative travel agent.
    Replaced brittle float-math with robust Tag-Intersection Logic.
    """
    
    @staticmethod
    def calculate_match_score(item: Dict, prefs: UserPreferenceMap) -> float:
        """
        Calculates match using Dynamic Tag Intersection, which is highly scalable.
        """
        score = 0.0
        item_tags = set(item.get('amenities', []) + item.get('tags', []))
        item_tags_lower = {t.lower() for t in item_tags}
        
        # 1. The Dealbreaker Guillotine
        for breaker in prefs.hard_dealbreakers:
            if breaker.lower() in item_tags_lower:
                return -1.0 # Completely disqualify this option
                
        # 2. Must-Haves (Heavy Weight)
        for must in prefs.must_haves:
            if must.lower() in item_tags_lower:
                score += 1.0
            else:
                score -= 0.5 # Penalty for missing a must-have
                
        # 3. Soft Desires (Bonus points)
        for desire in prefs.core_desires:
            if desire.lower() in item_tags_lower:
                score += 0.3
                
        return score

    @staticmethod
    def check_seasonality(location: str, month: int) -> Dict:
        """
        Returns weather suitability and potential bucket-list events.
        """
        # In production, this pulls from a 'Live Knowledge Base'
        intel_kb = {
            "New Orleans": LocationIntel(
                name="New Orleans",
                best_months=[2, 3, 4, 10, 11],
                blackout_months=[7, 8], # Brutal heat
                major_events=[{"name": "Mardi Gras", "month": 2, "importance": "Bucket List"}]
            ),
            "Tokyo": LocationIntel(
                name="Tokyo",
                best_months=[3, 4, 5, 10, 11],
                blackout_months=[6, 9], # Rainy/Typhoon
                major_events=[{"name": "Cherry Blossom Season", "month": 4, "importance": "Extreme"}]
            )
        }
        
        intel = intel_kb.get(location)
        if not intel:
            return {"status": "neutral", "events": []}
            
        if month in intel.blackout_months:
            return {"status": "bad_weather", "warning": f"Avoid {location} in this month due to extreme climate conditions."}
            
        relevant_events = [e for e in intel.major_events if e['month'] == month]
        return {"status": "optimal", "events": relevant_events}

expert_engine = TrotterExpertEngine()
