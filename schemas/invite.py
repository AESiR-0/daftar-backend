from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class PitchTeamInviteCreate(BaseModel):
    invited_email: EmailStr
    first_name: str
    last_name: str
    designation: str
    role: str
    pitch_id: int

class PitchTeamInviteResponse(BaseModel):
    id: int
    pitch_id: int
    invited_email: str
    first_name: str
    last_name: str
    designation: str
    status: str
    role: str
    created_at: datetime
    accepted_at: Optional[datetime]

    class Config:
        from_attributes = True

class DaftarInviteCreate(BaseModel):
    invited_email: EmailStr
    role: str = "member"

class DaftarInviteResponse(BaseModel):
    id: int
    daftar_id: int
    invited_email: str
    status: str
    role: str
    created_at: datetime
    accepted_at: Optional[datetime]

    class Config:
        from_attributes = True 