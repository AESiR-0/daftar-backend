from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from models.base import Base
from datetime import datetime

class Scout(Base):
    __tablename__ = "scouts"

    id = Column(Integer, primary_key=True, index=True)
    daftar_id = Column(Integer, ForeignKey("daftars.id"), nullable=False)
    name = Column(String(255), nullable=False)
    vision = Column(Text, nullable=True)
    
    # Audience Details
    location = Column(String(255), nullable=True)
    community = Column(String(255), nullable=True)
    age_range = Column(String(100), nullable=True)
    stage = Column(String(100), nullable=True)
    sector = Column(String(255), nullable=True)
    
    # Collaboration Details
    team_size = Column(Integer, nullable=True)
    collaboration_type = Column(String(100), nullable=True)
    collaboration_details = Column(Text, nullable=True)
    
    status = Column(String(50), default="draft")  # draft, pending, approved, rejected
    created_at = Column(DateTime, default=datetime.utcnow)
    approved_at = Column(DateTime, nullable=True)
    approved_by = Column(Integer, ForeignKey("daftar_team_members.id"), nullable=True)

    daftar = relationship("Daftar", backref="scouts")
    approver = relationship("DaftarTeamMember", backref="approved_scouts")

class ScoutFAQ(Base):
    __tablename__ = "scout_faqs"

    id = Column(Integer, primary_key=True, index=True)
    scout_id = Column(Integer, ForeignKey("scouts.id"), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    scout = relationship("Scout", backref="faqs")

class ScoutSchedule(Base):
    __tablename__ = "scout_schedules"

    id = Column(Integer, primary_key=True, index=True)
    scout_id = Column(Integer, ForeignKey("scouts.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    time_slot = Column(String(50), nullable=False)
    availability = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    scout = relationship("Scout", backref="schedules")

class ScoutUpdate(Base):
    __tablename__ = "scout_updates"

    id = Column(Integer, primary_key=True, index=True)
    scout_id = Column(Integer, ForeignKey("scouts.id"), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("daftar_team_members.id"), nullable=False)

    scout = relationship("Scout", backref="updates")
    creator = relationship("DaftarTeamMember", backref="scout_updates") 