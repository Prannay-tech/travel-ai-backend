import logging
from typing import Dict, List
from sqlalchemy.orm import Session
from app.models.booking import BookingRecord
from app.services.arbiter import arbiter
from app.services.distributed_lock import transactional_lock, DistributedLockError
# from app.services.payment import stripe_service # Placeholder for Stripe

logger = logging.getLogger(__name__)

class BookingOrchestrator:
    """
    Orchestrates the transactional flow between Stripe and Travel Providers.
    """

    @staticmethod
    async def execute_flight_booking(db: Session, user_id: int, offer_id: str, passengers: List[Dict], payment_token: str):
        
        lock_key = f"user_{user_id}_offer_{offer_id}"
        
        try:
            async with transactional_lock(lock_key, timeout_seconds=45):
                # 1. Create Initial Record
                record = BookingRecord(
                    user_id=user_id,
                    status="INITIATED",
                    vendor_type="flight",
                    vendor_name="Duffel"
                )
                db.add(record)
                db.commit()

                # 2. Capture Payment (Simulated)
                # In production: payment = await stripe_service.capture(payment_token)
                record.status = "PAID"
                record.payment_intent_id = f"pi_mock_{record.id}"
                db.commit()

                # 3. Call Travel Provider
                duffel_provider = arbiter.flight_providers[0] # Assuming first for demo
                result = await duffel_provider.book(offer_id, passengers)

                if result.get("status") == "success":
                    record.status = "CONFIRMED"
                    record.vendor_pnr = result["vendor_pnr"]
                    record.raw_response = result["raw_data"]
                    db.commit()
                    return {"status": "confirmed", "booking_id": record.id, "pnr": record.vendor_pnr}
                else:
                    # Rollback payment intent here in production
                    record.status = "FAILED"
                    db.commit()
                    return {"status": "failed", "error": result.get("message")}
                    
        except DistributedLockError as e:
            return {"status": "failed", "error": str(e)}

booking_orchestrator = BookingOrchestrator()
