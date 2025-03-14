from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, ARRAY, Index, Numeric, Float
from sqlalchemy.orm import relationship
from models.base import Base
from datetime import datetime

class Founder(Base):
    __tablename__ = "founders"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    gender = Column(String(50), nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    password_hashed = Column(String(255), nullable=False)
    designation = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    deleted_on = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    location = Column(String(255), nullable=True)
    journal_content = Column(Text, nullable=True)

class FounderPreferredLanguage(Base):
    __tablename__ = "founder_preferred_languages"

    id = Column(Integer, primary_key=True, index=True)
    founder_id = Column(Integer, ForeignKey("founders.id"), nullable=False)
    language = Column(String(100), nullable=False)

    founder = relationship("Founder", backref="preferred_languages")

class Pitch(Base):
    __tablename__ = "pitches"

    id = Column(Integer, primary_key=True, index=True)
    scout_id = Column(Integer, ForeignKey("scouts.id"), nullable=False)
    pitch_name = Column(String(255), nullable=False)
    founder_language = Column(String(50), nullable=True)
    ask_for_investor = Column(Boolean, default=False)
    has_confirmed = Column(Boolean, default=False)
    status_founder = Column(String(50), nullable=False, default="Inbox")
    created_at = Column(DateTime, default=datetime.utcnow)
    demo_link = Column(String(255), nullable=True)

    scout = relationship("Scout", backref="pitches")

class FounderPitchRelationship(Base):
    __tablename__ = "founder_pitch_relationship"

    id = Column(Integer, primary_key=True, index=True)
    founder_id = Column(Integer, ForeignKey("founders.id"), nullable=False)
    pitch_id = Column(Integer, ForeignKey("pitches.id"), nullable=False)

    founder = relationship("Founder", backref="pitch_relationships")
    pitch = relationship("Pitch", backref="founder_relationships")

class InvestorQuestion(Base):
    __tablename__ = "investor_questions"

    id = Column(Integer, primary_key=True, index=True)
    pitch_id = Column(Integer, ForeignKey("pitches.id"), nullable=False)
    question_text = Column(Text, nullable=False)

    pitch = relationship("Pitch", backref="investor_questions")

class InvestorAnswer(Base):
    __tablename__ = "investor_answers"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("investor_questions.id"), nullable=False)
    video_url = Column(String(255), nullable=False)

    question = relationship("InvestorQuestion", backref="answers")

class PendingConfirmation(Base):
    __tablename__ = "pending_confirmations"

    id = Column(Integer, primary_key=True, index=True)
    pitch_id = Column(Integer, ForeignKey("pitches.id"), nullable=False)
    founder_id = Column(Integer, ForeignKey("founders.id"), nullable=False)

    pitch = relationship("Pitch", backref="pending_confirmations")
    founder = relationship("Founder", backref="pending_confirmations")

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    pitch_id = Column(Integer, ForeignKey("pitches.id"), nullable=False)
    uploaded_by = Column(Integer, ForeignKey("founders.id"), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    document_url = Column(String(255), nullable=False)
    is_private = Column(Boolean, default=False)

    pitch = relationship("Pitch", backref="documents")
    founder = relationship("Founder", backref="uploaded_documents")

class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, index=True)
    pitch_id = Column(Integer, ForeignKey("pitches.id"), nullable=False)
    investor_id = Column(Integer, ForeignKey("investors.id"), nullable=False)
    offer_desc = Column(Text, nullable=False)
    status = Column(String(50), default="pending")  # pending, accepted, rejected, withdrawn
    offer_sent_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    pitch = relationship("Pitch", backref="offers")
    investor = relationship("Investor", backref="offers")

class OfferAction(Base):
    __tablename__ = "offer_actions"

    id = Column(Integer, primary_key=True, index=True)
    offer_id = Column(Integer, ForeignKey("offers.id"), nullable=False)
    action = Column(String(50), nullable=False)  # accepted, rejected, withdrawn
    action_by = Column(Integer, nullable=False)  # Can be either founder_id or investor_id
    notes = Column(Text, nullable=True)
    action_taken_at = Column(DateTime, default=datetime.utcnow)

    offer = relationship("Offer", backref="actions")

class Bill(Base):
    __tablename__ = "bills"

    id = Column(Integer, primary_key=True, index=True)
    pitch_id = Column(Integer, ForeignKey("pitches.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)  # Using Numeric for precise decimal
    description = Column(Text, nullable=False)
    due_date = Column(DateTime, nullable=False)
    payment_link = Column(String(255), nullable=True)
    is_paid = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    paid_at = Column(DateTime, nullable=True)

    pitch = relationship("Pitch", backref="bills")

class FounderMeeting(Base):
    __tablename__ = "founder_meeting"

    meeting_id = Column(Integer, primary_key=True, index=True)
    daftar_id = Column(Integer, ForeignKey("daftars.id"), nullable=False)
    pitch_id = Column(Integer, ForeignKey("pitches.id"), nullable=False)
    invited_guest = Column(Integer, nullable=False)
    start_date = Column(DateTime, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    location = Column(String(255), nullable=False)
    agenda_of_meeting = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("founders.id"), nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    # Add unique index on meeting_id
    __table_args__ = (
        Index('uix_founder_meeting_id', 'meeting_id', unique=True),
    )

    daftar = relationship("Daftar", backref="meetings")
    pitch = relationship("Pitch", backref="meetings")
    creator = relationship("Founder", backref="created_meetings")

class FounderMeetingDetail(Base):
    __tablename__ = "founder_meeting_detail"

    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("founder_meeting.meeting_id"), nullable=False)
    total_invitees = Column(Integer, nullable=False)
    name_of_invitees = Column(ARRAY(String), nullable=False)
    total_attendees = Column(Integer, nullable=False)
    name_of_attendees = Column(ARRAY(String), nullable=False)

    meeting = relationship("FounderMeeting", backref="meeting_details")

class FeatureRequest(Base):
    __tablename__ = "feature_request"

    feature_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("founders.id"), nullable=False)
    does_exist = Column(Boolean, default=False)
    status = Column(String(50), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow)

    founder = relationship("Founder", backref="feature_requests")

class Feedback(Base):
    __tablename__ = "feedback"

    feedback_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("founders.id"), nullable=False)
    description = Column(Text, nullable=False)
    is_happy = Column(Boolean, nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow)

    founder = relationship("Founder", backref="feedbacks")

class PitchTeamInvite(Base):
    __tablename__ = "pitch_team_invites"

    id = Column(Integer, primary_key=True, index=True)
    pitch_id = Column(Integer, ForeignKey("pitches.id"), nullable=False)
    invited_email = Column(String(255), nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    designation = Column(String(255), nullable=False)
    status = Column(String(50), default="pending")  # pending, accepted, rejected
    role = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    accepted_at = Column(DateTime, nullable=True)

    pitch = relationship("Pitch", backref="team_invites")