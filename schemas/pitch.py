from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class FounderInPitch(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone: str

class PitchResponse(BaseModel):
    id: int
    pitch_name: str
    scout_id: int
    founder_language: Optional[str]
    ask_for_investor: bool
    has_confirmed: bool
    status_founder: str
    created_at: datetime
    demo_link: Optional[str]

    class Config:
        from_attributes = True

class PitchCreate(BaseModel):
    pitch_name: str
    scout_id: int
    founder_language: Optional[str] = None
    ask_for_investor: bool = False
    demo_link: Optional[str] = None

class PitchUpdate(BaseModel):
    pitch_name: Optional[str] = None
    founder_language: Optional[str] = None
    ask_for_investor: Optional[bool] = None
    has_confirmed: Optional[bool] = None
    status_founder: Optional[str] = None
    demo_link: Optional[str] = None 