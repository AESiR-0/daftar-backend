from pydantic import BaseModel, constr
from datetime import datetime
from typing import Optional

class OfferCreate(BaseModel):
    pitch_id: int
    offer_desc: str

class OfferResponse(BaseModel):
    id: int
    pitch_id: int
    investor_id: int
    offer_desc: str
    status: str  # pending, accepted, rejected, withdrawn
    offer_sent_at: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

class OfferActionCreate(BaseModel):
    action: str
    notes: Optional[str] = None 