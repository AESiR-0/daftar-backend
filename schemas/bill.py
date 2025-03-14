from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from decimal import Decimal

class BillCreate(BaseModel):
    pitch_id: int
    amount: Decimal
    description: str
    due_date: datetime
    payment_link: Optional[str] = None

class BillResponse(BaseModel):
    id: int
    pitch_id: int
    amount: Decimal
    description: str
    due_date: datetime
    payment_link: Optional[str]
    is_paid: bool
    created_at: datetime
    paid_at: Optional[datetime]
    
    class Config:
        from_attributes = True 