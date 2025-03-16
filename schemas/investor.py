from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class InvestorProfileResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True

class DaftarProfileResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True

class DaftarInvestorCreate(BaseModel):
    investor_id: int
    role: str = "member"

class DaftarInvestorResponse(BaseModel):
    id: int
    investor_id: int
    first_name: str
    last_name: str
    role: str
    joined_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

class InvestorBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

class InvestorCreate(InvestorBase):
    password: str

class InvestorUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class SampleQuestionResponse(BaseModel):
    id: int
    scout_id: int
    question_text: str
    video_url: Optional[str]  # From sample_pitch_answers
    
    class Config:
        from_attributes = True

class CustomQuestionCreate(BaseModel):
    scout_id: int
    question_text: str

class CustomQuestionResponse(BaseModel):
    id: int
    scout_id: int
    question_text: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class InvestorNoteCreate(BaseModel):
    note_text: str

class InvestorNoteResponse(BaseModel):
    id: int
    pitch_id: int
    investor_id: int
    note_text: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class TeamMemberAnalysisCreate(BaseModel):
    market_analysis: Optional[str] = None
    competitive_analysis: Optional[str] = None
    financial_analysis: Optional[str] = None
    team_analysis: Optional[str] = None
    overall_analysis: Optional[str] = None

class TeamMemberAnalysisResponse(BaseModel):
    id: int
    pitch_id: int
    team_member_id: int
    market_analysis: Optional[str]
    competitive_analysis: Optional[str]
    financial_analysis: Optional[str]
    team_analysis: Optional[str]
    overall_analysis: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True 