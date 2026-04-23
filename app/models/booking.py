from sqlalchemy import Column, Integer, String, Float, JSON, Boolean, DateTime, ForeignKey
from datetime import datetime
from app.core.database import Base

class BookingRecord(Base):
    """
    The financial and execution record for a finalized booking.
    """
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    
    # Financial Data
    total_amount = Column(Float)
    currency = Column(String, default="USD")
    payment_intent_id = Column(String) # Stripe Intent ID
    
    # Vendor Data
    vendor_type = Column(String) # 'flight', 'hotel'
    vendor_name = Column(String) # 'Duffel', 'Marriott'
    vendor_pnr = Column(String)  # The actual ticket/confirmation code
    
    # Status Management
    # ['INITIATED', 'PAID', 'PENDING_VENDOR', 'CONFIRMED', 'CANCELLED']
    status = Column(String, default="INITIATED")
    
    raw_response = Column(JSON) # Store raw vendor response for debugging
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Booking(id={self.id}, pnr='{self.vendor_pnr}', status='{self.status}')>"
