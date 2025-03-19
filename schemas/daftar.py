from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DaftarCreate(BaseModel):
    name: str
    type: str
    daftar_code: str
    website: Optional[str] = None
    location: Optional[str] = None
    big_picture: Optional[str] = None
    billing_plan: Optional[str] = None
    billing_information: Optional[str] = None

class DaftarResponse(BaseModel):
    id: int
    name: str
    type: str
    daftar_code: str
    website: Optional[str]
    location: Optional[str]
    big_picture: Optional[str]
    on_daftar_since: datetime
    billing_plan: Optional[str]
    billing_information: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True 