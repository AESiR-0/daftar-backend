from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class FounderProfileResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    gender: str
    phone: str
    email: EmailStr
    designation: Optional[str]
    location: Optional[str]
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True

class FounderBase(BaseModel):
    first_name: str
    last_name: str
    gender: str
    phone: str
    email: EmailStr
    designation: Optional[str] = None
    location: Optional[str] = None

class FounderCreate(FounderBase):
    password: str

class FounderUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    designation: Optional[str] = None
    location: Optional[str] = None

class InvestorQuestionResponse(BaseModel):
    id: int
    question_text: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class QuestionAnswerResponse(BaseModel):
    question_id: int
    question_text: str
    answer_video_url: Optional[str]
    answer_text: Optional[str]
    answered_at: Optional[datetime]
    
    class Config:
        from_attributes = True 