class CorporatePolicyEngine:
    """
    Handles travel policy compliance for B2B clients dynamically.
    """

    @staticmethod
    def validate_hotel(hotel: Dict, policy: Dict) -> Dict:
        """
        Checks if a hotel offer is compliant against a dynamic policy.
        """
        if not policy:
            return {**hotel, "policy_status": "no_policy_defined"}

    def validate_hotel(self, hotel: Dict, policy: Optional[Dict] = None) -> Dict:
        """
        Checks if a hotel offer is compliant. 
        Returns the hotel with a 'policy_status' flag.
        """
        p = policy or self.default_policy
        
        # Simple validation logic
        is_compliant = True
        violations = []

        raw_price = hotel.get('price', 0)
        # Handle string prices like "$250"
        if isinstance(raw_price, str):
            try:
                raw_price = float(raw_price.replace('$', '').replace(',', ''))
            except:
                raw_price = 0

        if raw_price > p["max_hotel_price"]:
            is_compliant = False
            violations.append(f"Price exceeds limit of ${p['max_hotel_price']}")

        if float(hotel.get('rating', 0)) < p["min_hotel_rating"]:
            is_compliant = False
            violations.append(f"Rating below {p['min_hotel_rating']} stars")

        return {
            **hotel,
            "policy_status": "compliant" if is_compliant else "out_of_policy",
            "policy_violations": violations
        }

    def filter_compliant_results(self, results: List[Dict], type: str) -> List[Dict]:
        """
        Filters a list of results based on policy (used for some clients).
        """
        if type == "hotel":
            return [self.validate_hotel(h) for h in results]
        return results

policy_engine = CorporatePolicyEngine()
