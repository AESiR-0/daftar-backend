from pydantic import BaseModel, constr
from datetime import datetime
from typing import List, Optional
from .pitch import FounderInPitch

# Base Scout Creation
class ScoutCreate(BaseModel):
    daftar_id: int
    name: str
    status: str = "draft"  # draft, pending, approved, rejected

class ScoutResponse(BaseModel):
    id: int
    daftar_id: int
    name: str
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Scout Details
class ScoutDetailsUpdate(BaseModel):
    name: str
    vision: str

# Scout Audience
class ScoutAudienceUpdate(BaseModel):
    location: str  # country/state/city
    community: str
    age_range: str
    stage: str
    sector: str

# Scout Collaboration
class ScoutCollaborationUpdate(BaseModel):
    team_size: int
    collaboration_type: str
    collaboration_details: str

# Scout FAQ
class ScoutFAQCreate(BaseModel):
    question: str
    answer: str

class ScoutFAQResponse(BaseModel):
    id: int
    scout_id: int
    question: str
    answer: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Scout Schedule
class ScoutScheduleCreate(BaseModel):
    date: datetime
    time_slot: str
    availability: bool = True

class ScoutScheduleResponse(BaseModel):
    id: int
    scout_id: int
    date: datetime
    time_slot: str
    availability: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

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

class ScoutUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ScoutUpdateCreate(BaseModel):
    description: str

class ScoutUpdateResponse(BaseModel):
    id: int
    scout_id: int
    description: str
    created_at: datetime
    created_by: int
    
    class Config:
        from_attributes = True 