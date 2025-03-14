from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class DocumentCreate(BaseModel):
    document_url: str
    document_type: str  # "pitch_deck", "financial", "legal", etc.
    title: str
    description: Optional[str] = None
    is_private: bool = False

class DocumentResponse(BaseModel):
    id: int
    document_url: str
    document_type: str
    title: str
    description: Optional[str]
    is_private: bool
    uploaded_by_type: str  # "founder" or "investor"
    uploaded_by_id: int
    uploaded_at: datetime
    
    class Config:
        from_attributes = True 