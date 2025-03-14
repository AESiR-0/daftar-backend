from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from models.base import Base
from datetime import datetime

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    pitch_id = Column(Integer, ForeignKey("pitches.id"), nullable=False)
    document_url = Column(String(255), nullable=False)
    document_type = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    is_private = Column(Boolean, default=False)
    uploaded_by_type = Column(String(50), nullable=False)  # "founder" or "investor"
    uploaded_by_id = Column(Integer, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    pitch = relationship("Pitch", backref="documents") 