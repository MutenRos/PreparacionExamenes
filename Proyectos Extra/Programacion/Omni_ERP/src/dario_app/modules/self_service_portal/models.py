"""
Customer Self-Service Portal - Models
Supports portal users, cases, requests, feedback, and knowledge interactions.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from dario_app.database import Base


class PortalUserProfile(Base):
    """Portal user linked to a customer/contact."""
    __tablename__ = "ssp_user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    customer_id = Column(Integer, index=True)
    contact_email = Column(String(200), nullable=False, index=True)
    display_name = Column(String(200))
    locale = Column(String(20), default="en-US")
    time_zone = Column(String(50), default="UTC")
    status = Column(String(50), default="Active")
    preferences = Column(JSON)

    last_login_at = Column(DateTime)
    last_password_reset = Column(DateTime)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    cases = relationship("PortalCase", back_populates="user", cascade="all, delete-orphan")
    requests = relationship("PortalRequest", back_populates="user", cascade="all, delete-orphan")
    feedbacks = relationship("PortalFeedback", back_populates="user", cascade="all, delete-orphan")


class PortalCase(Base):
    """Support case created from the portal."""
    __tablename__ = "ssp_cases"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("ssp_user_profiles.id"))

    case_number = Column(String(50), unique=True, nullable=False, index=True)
    subject = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(100))
    priority = Column(String(50), default="Normal")
    status = Column(String(50), default="Open")
    assigned_to = Column(String(100))
    sla_due_at = Column(DateTime)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = Column(DateTime)

    user = relationship("PortalUserProfile", back_populates="cases")


class PortalRequest(Base):
    """Service request (returns, orders, appointments) from portal."""
    __tablename__ = "ssp_requests"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("ssp_user_profiles.id"))

    request_number = Column(String(50), unique=True, nullable=False, index=True)
    request_type = Column(String(100))  # RMA, Service, Appointment, DataRequest
    details = Column(JSON)
    status = Column(String(50), default="Pending")
    priority = Column(String(50), default="Normal")
    scheduled_at = Column(DateTime)
    completed_at = Column(DateTime)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("PortalUserProfile", back_populates="requests")


class PortalFeedback(Base):
    """Feedback on portal experience or content."""
    __tablename__ = "ssp_feedback"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("ssp_user_profiles.id"))

    rating = Column(Integer)  # 1-5
    comment = Column(Text)
    category = Column(String(100))  # Case, Knowledge, Experience
    target_id = Column(Integer)  # optional link to case/article

    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("PortalUserProfile", back_populates="feedbacks")


class PortalKnowledgeView(Base):
    """Tracks article views from portal users."""
    __tablename__ = "ssp_knowledge_views"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("ssp_user_profiles.id"))

    article_id = Column(Integer, index=True)
    view_at = Column(DateTime, default=datetime.utcnow)
    duration_seconds = Column(Integer)
    device_type = Column(String(50))

    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("PortalUserProfile")
