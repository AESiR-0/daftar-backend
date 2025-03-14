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