from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.itinerary import Itinerary
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class ItineraryCreate(BaseModel):
    title: str
    destination: str
    is_business: bool
    activities: List[dict]
    user_age: int

@router.post("/save")
async def save_itinerary(payload: ItineraryCreate, db: Session = Depends(get_db)):
    """
    Saves an AI-generated itinerary to the database.
    """
    try:
        db_itinerary = Itinerary(
            title=payload.title,
            destination=payload.destination,
            is_business=payload.is_business,
            activities=payload.activities,
            user_age_at_booking=payload.user_age
        )
        db.add(db_itinerary)
        db.commit()
        db.refresh(db_itinerary)
        return {"status": "success", "itinerary_id": db_itinerary.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/list/{user_id}")
async def get_user_itineraries(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieves all itineraries for a specific user.
    """
    return db.query(Itinerary).filter(Itinerary.user_id == user_id).all()
