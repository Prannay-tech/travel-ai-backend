from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    itineraries = relationship("Itinerary", back_populates="owner")

class Itinerary(Base):
    __tablename__ = "itineraries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    destination = Column(String, index=True)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    
    # Store the massive JSON dump of the generated itinerary
    content = Column(JSON, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="itineraries")

class ChatSession(Base):
    """
    Optional persistence of chat sessions.
    Though typically in Redis for fast access, storing completed ones here for analytics / continuity.
    """
    __tablename__ = "chat_sessions"
    
    id = Column(String, primary_key=True, index=True) # UUID
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    state_data = Column(JSON) # The accumulated conversational state
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
