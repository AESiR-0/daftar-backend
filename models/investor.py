from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from models.base import Base
from datetime import datetime

class Investor(Base):
    __tablename__ = "investors"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    gender = Column(String(50), nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    password_hashed = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    deleted_on = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    location = Column(String(255), nullable=True)

class InvestorScout(Base):
    __tablename__ = "investor_scouts"

    id = Column(Integer, primary_key=True, index=True)
    investor_id = Column(Integer, ForeignKey("investors.id"), nullable=False)
    scout_id = Column(Integer, ForeignKey("scouts.id"), nullable=False)

    investor = relationship("Investor", backref="scout_relationships")
    scout = relationship("Scout", backref="investor_relationships")

class TeamMemberAnalysis(Base):
    __tablename__ = "team_member_analysis"

    id = Column(Integer, primary_key=True, index=True)
    pitch_id = Column(Integer, ForeignKey("pitches.id"), nullable=False)
    team_member_id = Column(Integer, ForeignKey("founders.id"), nullable=False)
    analysis_text = Column(Text, nullable=False)

    pitch = relationship("Pitch", backref="team_analyses")

class InvestorNote(Base):
    __tablename__ = "investor_notes"

    id = Column(Integer, primary_key=True, index=True)
    pitch_id = Column(Integer, ForeignKey("pitches.id"), nullable=False)
    investor_id = Column(Integer, ForeignKey("investors.id"), nullable=False)
    note_text = Column(Text, nullable=False)

    pitch = relationship("Pitch", backref="investor_notes")
    investor = relationship("Investor", backref="notes")

class Daftar(Base):
    __tablename__ = "daftars"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    type = Column(String(255), nullable=False)
    daftar_code = Column(String(100), unique=True, nullable=False)
    website = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    big_picture = Column(Text, nullable=True)
    on_daftar_since = Column(DateTime, default=datetime.utcnow)
    billing_plan = Column(String(100), nullable=True)
    billing_information = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    deleted_on = Column(DateTime, nullable=True)

class DaftarTeamMember(Base):
    __tablename__ = "daftar_team_members"

    id = Column(Integer, primary_key=True, index=True)
    daftar_id = Column(Integer, ForeignKey("daftars.id"), nullable=False)
    designation = Column(String(255), nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)

    daftar = relationship("Daftar", backref="team_members")

class DaftarPendingInvite(Base):
    __tablename__ = "daftar_pending_invites"

    id = Column(Integer, primary_key=True, index=True)
    daftar_id = Column(Integer, ForeignKey("daftars.id"), nullable=False)
    email = Column(String(255), nullable=False)
    invited_by = Column(Integer, ForeignKey("investors.id"), nullable=False)
    invited_at = Column(DateTime, default=datetime.utcnow)

    daftar = relationship("Daftar", backref="pending_invites")
    inviter = relationship("Investor", backref="sent_invites")

class DaftarDeleteApproval(Base):
    __tablename__ = "daftar_delete_approvals"

    id = Column(Integer, primary_key=True, index=True)
    daftar_id = Column(Integer, ForeignKey("daftars.id"), nullable=False)
    approved_by = Column(Integer, ForeignKey("daftar_team_members.id"), nullable=False)
    approved_at = Column(DateTime, default=datetime.utcnow)

    daftar = relationship("Daftar", backref="delete_approvals")
    approver = relationship("DaftarTeamMember", backref="approved_deletions")

class Scout(Base):
    __tablename__ = "scouts"

    id = Column(Integer, primary_key=True, index=True)
    daftar_id = Column(Integer, ForeignKey("daftars.id"), nullable=False)
    scout_name = Column(String(255), nullable=False)
    scout_description = Column(Text, nullable=False)
    audience_country = Column(String(100), nullable=True)
    audience_state = Column(String(100), nullable=True)
    audience_city = Column(String(100), nullable=True)
    audience_community = Column(String(100), nullable=True)
    audience_age_start = Column(Integer, nullable=True)
    audience_age_end = Column(Integer, nullable=True)
    audience_gender = Column(String(50), nullable=True)
    audience_stage = Column(String(100), nullable=True)
    audience_sector = Column(String(100), nullable=True)
    is_sample = Column(Boolean, default=False)
    investor_pitch_video = Column(String(255), nullable=True)
    investor_pitch_uploaded_at = Column(DateTime, nullable=True)
    schedule_last_day_to_pitch = Column(DateTime, nullable=True)
    schedule_launch_date = Column(DateTime, nullable=True)
    status = Column(String(50), nullable=False)

    daftar = relationship("Daftar", backref="scouts")

class ScoutCollaborator(Base):
    __tablename__ = "scout_collaborators"

    id = Column(Integer, primary_key=True, index=True)
    scout_id = Column(Integer, ForeignKey("scouts.id"), nullable=False)
    collaborator_id = Column(Integer, ForeignKey("investors.id"), nullable=False)

    scout = relationship("Scout", backref="collaborators")
    investor = relationship("Investor", backref="collaborating_scouts")

class ScoutDocument(Base):
    __tablename__ = "scout_documents"

    id = Column(Integer, primary_key=True, index=True)
    scout_id = Column(Integer, ForeignKey("scouts.id"), nullable=False)
    uploaded_by = Column(Integer, ForeignKey("investors.id"), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    document_url = Column(String(255), nullable=False)
    is_private = Column(Boolean, default=False)

    scout = relationship("Scout", backref="documents")
    uploader = relationship("Investor", backref="uploaded_scout_documents")

class SampleInvestorQuestion(Base):
    __tablename__ = "sample_investor_questions"

    id = Column(Integer, primary_key=True, index=True)
    scout_id = Column(Integer, ForeignKey("scouts.id"), nullable=False)
    question_text = Column(Text, nullable=False)

    scout = relationship("Scout", backref="sample_questions")

class SamplePitchAnswer(Base):
    __tablename__ = "sample_pitch_answers"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("sample_investor_questions.id"), nullable=False)
    video_url = Column(String(255), nullable=False)

    question = relationship("SampleInvestorQuestion", backref="sample_answers")

class CustomInvestorQuestion(Base):
    __tablename__ = "custom_investor_questions"

    id = Column(Integer, primary_key=True, index=True)
    scout_id = Column(Integer, ForeignKey("scouts.id"), nullable=False)
    question_text = Column(Text, nullable=False)

    scout = relationship("Scout", backref="custom_questions")

class ScoutFAQ(Base):
    __tablename__ = "scout_faq"

    id = Column(Integer, primary_key=True, index=True)
    scout_id = Column(Integer, ForeignKey("scouts.id"), nullable=False)
    faq_question = Column(Text, nullable=False)
    faq_answer = Column(Text, nullable=False)

    scout = relationship("Scout", backref="faqs")

class ScoutPendingApproval(Base):
    __tablename__ = "scout_pending_approvals"

    id = Column(Integer, primary_key=True, index=True)
    scout_id = Column(Integer, ForeignKey("scouts.id"), nullable=False)
    team_member_id = Column(Integer, ForeignKey("daftar_team_members.id"), nullable=False)

    scout = relationship("Scout", backref="pending_approvals")
    team_member = relationship("DaftarTeamMember", backref="pending_scout_approvals")

class ScoutPendingDetail(Base):
    __tablename__ = "scout_pending_details"

    id = Column(Integer, primary_key=True, index=True)
    scout_id = Column(Integer, ForeignKey("scouts.id"), nullable=False)
    pending_detail = Column(Text, nullable=False)

    scout = relationship("Scout", backref="pending_details")

class ScoutDeleteApproval(Base):
    __tablename__ = "scout_delete_approvals"

    id = Column(Integer, primary_key=True, index=True)
    scout_id = Column(Integer, ForeignKey("scouts.id"), nullable=False)
    approved_by = Column(Integer, ForeignKey("daftar_team_members.id"), nullable=False)
    approved_at = Column(DateTime, default=datetime.utcnow)

    scout = relationship("Scout", backref="delete_approvals")
    approver = relationship("DaftarTeamMember", backref="approved_scout_deletions")

class Update(Base):
    __tablename__ = "updates"

    id = Column(Integer, primary_key=True, index=True)
    scout_id = Column(Integer, ForeignKey("scouts.id"), nullable=False)
    update_description = Column(Text, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow)

    scout = relationship("Scout", backref="updates")