from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from .pitch import FounderInPitch

class ScoutPitchResponse(BaseModel):
    id: int
    pitch_name: str
    investor_question_language: Optional[str]
    ask_for_investor: bool
    has_confirmed: bool
    created_at: datetime
    founders: List[FounderInPitch]

    class Config:
        from_attributes = True

class ScoutBase(BaseModel):
    name: str
    description: Optional[str] = None

class ScoutCreate(ScoutBase):
    daftar_id: int

class ScoutUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None 