from typing import List, Dict, Any

class LogisticsEngine:
    """
    Handles anticipatory logistics, buffers, and 'In-Trip Companion' downtime.
    """

    @staticmethod
    def calculate_transfer_buffer(origin_type: str, dest_type: str) -> int:
        """Returns required buffer time in minutes based on location switch."""
        friction_map = {
            ("International Flight", "City Center"): 120, # Customs, bag claim, taxi
            ("Domestic Flight", "City Center"): 90,
            ("Train Station", "City Center"): 45,
            ("Activity", "Activity"): 30 # General walk/transit average
        }
        return friction_map.get((origin_type, dest_type), 60)

    @staticmethod
    def identify_empty_hours(itinerary: List[Dict]) -> List[Dict]:
        """
        Scans an itinerary for gaps larger than 2 hours.
        Flags them as 'Flexible Companion Blocks' rather than forcing an activity.
        """
        flexible_blocks = []
        for i in range(len(itinerary) - 1):
            current_end = itinerary[i].get("end_time")
            next_start = itinerary[i+1].get("start_time")
            
            # Simplified mock logic for timeline detection
            if next_start and current_end:
                gap = next_start - current_end
                if gap > 2:
                    flexible_blocks.append({
                        "after": itinerary[i]['name'],
                        "before": itinerary[i+1]['name'],
                        "duration_hours": gap,
                        "type": "Companion-Managed Free Time",
                        "note": "Trotter will suggest local coffees or resting spots during this time based on your mood."
                    })
        return flexible_blocks

    @staticmethod
    def apply_arrival_rest_protocol(itinerary_day: Dict) -> Dict:
        """
        Enforces the rule that 'Arrival Day' should only contain
        low-intensity, mood-dependent activities.
        """
        if itinerary_day.get("is_arrival_day"):
            for activity in itinerary_day.get("activities", []):
                if activity.get("intensity") == "High":
                    activity["escalation_warning"] = "Warning: High intensity activity on arrival day."
                    activity["status"] = "Requires User Confirmaton"
        return itinerary_day

logistics_engine = LogisticsEngine()
