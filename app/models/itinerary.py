from sqlalchemy import Column, Integer, String, JSON, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Itinerary(Base):
    """
    SQLAlchemy model for saved travel itineraries.
    """
    __tablename__ = "itineraries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True) # Linked to user in future auth phase
    title = Column(String)
    destination = Column(String)
    is_business = Column(Boolean, default=False)
    
    # Modular storage for our expert activities
    # format: List[TrotterActivity]
    activities = Column(JSON)
    
    # Metadata for personalization tracking
    user_age_at_booking = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Starred/Favorite status
    is_favorite = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Itinerary(id={self.id}, title='{self.title}')>"
