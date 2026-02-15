"""Recruitment Management models."""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, Index
from sqlalchemy.orm import Mapped, mapped_column

from dario_app.database import Base


class JobPosition(Base):
    """Job position/opening."""
    __tablename__ = "rcm_job_positions"
    __table_args__ = (
        Index("idx_rcmjob_org_status", "organization_id", "status"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    position_code: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    
    # Details
    department: Mapped[str] = mapped_column(String(100), nullable=False)
    reports_to: Mapped[Optional[str]] = mapped_column(String(255))
    job_level: Mapped[str] = mapped_column(String(30), default="individual_contributor")  # entry, mid, senior, manager, executive
    
    # Compensation
    salary_min: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    salary_max: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD")
    
    # Vacancy details
    required_headcount: Mapped[int] = mapped_column(Integer, default=1)
    filled_headcount: Mapped[int] = mapped_column(Integer, default=0)
    
    # Timeline
    posted_date: Mapped[date] = mapped_column(Date, nullable=False)
    target_start_date: Mapped[Optional[date]] = mapped_column(Date)
    deadline_date: Mapped[Optional[date]] = mapped_column(Date)
    
    # Status
    status: Mapped[str] = mapped_column(String(30), default="draft")  # draft, open, on_hold, closed, cancelled
    
    # Requirements
    required_education: Mapped[Optional[str]] = mapped_column(String(100))
    required_experience_years: Mapped[Optional[int]] = mapped_column(Integer)
    required_skills: Mapped[Optional[str]] = mapped_column(Text)  # JSON array
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Candidate(Base):
    """Job candidate."""
    __tablename__ = "rcm_candidates"
    __table_args__ = (
        Index("idx_rcmcand_org_status", "organization_id", "status"),
        Index("idx_rcmcand_org_email", "organization_id", "email"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    candidate_id: Mapped[str] = mapped_column(String(50), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Professional info
    current_title: Mapped[Optional[str]] = mapped_column(String(255))
    current_company: Mapped[Optional[str]] = mapped_column(String(255))
    years_experience: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Education
    highest_education: Mapped[Optional[str]] = mapped_column(String(100))
    education_field: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Files
    resume_path: Mapped[Optional[str]] = mapped_column(String(500))
    cover_letter_path: Mapped[Optional[str]] = mapped_column(String(500))
    
    # Assessment
    skills: Mapped[Optional[str]] = mapped_column(Text)  # JSON array
    strengths: Mapped[Optional[str]] = mapped_column(Text)
    weaknesses: Mapped[Optional[str]] = mapped_column(Text)
    overall_rating: Mapped[Optional[Decimal]] = mapped_column(Numeric(3, 1))  # 1-5
    
    # Status
    status: Mapped[str] = mapped_column(String(30), default="new")  # new, screening, interview, offer, hired, rejected, withdrawn
    rejection_reason: Mapped[Optional[str]] = mapped_column(Text)
    
    # Tracking
    source: Mapped[Optional[str]] = mapped_column(String(50))  # linkedin, indeed, referral, website
    applied_date: Mapped[date] = mapped_column(Date, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Application(Base):
    """Job application."""
    __tablename__ = "rcm_applications"
    __table_args__ = (
        Index("idx_rcmapp_org_position", "organization_id", "position_id"),
        Index("idx_rcmapp_org_candidate", "organization_id", "candidate_id"),
        Index("idx_rcmapp_org_status", "organization_id", "status"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    position_id: Mapped[int] = mapped_column(Integer, ForeignKey("rcm_job_positions.id"), nullable=False)
    candidate_id: Mapped[int] = mapped_column(Integer, ForeignKey("rcm_candidates.id"), nullable=False)
    
    # Status
    status: Mapped[str] = mapped_column(String(30), default="applied")  # applied, screening, interviewing, offered, accepted, rejected
    
    # Assessment
    screening_score: Mapped[Optional[Decimal]] = mapped_column(Numeric(3, 1))
    interview_score: Mapped[Optional[Decimal]] = mapped_column(Numeric(3, 1))
    final_score: Mapped[Optional[Decimal]] = mapped_column(Numeric(3, 1))
    
    # Timeline
    applied_date: Mapped[date] = mapped_column(Date, nullable=False)
    screening_date: Mapped[Optional[date]] = mapped_column(Date)
    interview_date: Mapped[Optional[date]] = mapped_column(Date)
    decision_date: Mapped[Optional[date]] = mapped_column(Date)
    
    # Notes
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Interview(Base):
    """Interview record."""
    __tablename__ = "rcm_interviews"
    __table_args__ = (
        Index("idx_rcmint_org_application", "organization_id", "application_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    application_id: Mapped[int] = mapped_column(Integer, ForeignKey("rcm_applications.id"), nullable=False)
    
    interview_type: Mapped[str] = mapped_column(String(30), default="phone")  # phone, video, in_person, panel
    
    # Schedule
    scheduled_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    completed_date: Mapped[Optional[datetime]] = mapped_column(DateTime)
    duration_minutes: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Interviewer
    interviewer_id: Mapped[Optional[int]] = mapped_column(Integer)
    interviewer_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Assessment
    score: Mapped[Optional[Decimal]] = mapped_column(Numeric(3, 1))
    feedback: Mapped[Optional[str]] = mapped_column(Text)
    
    # Questions
    questions: Mapped[Optional[str]] = mapped_column(Text)  # JSON array
    answers: Mapped[Optional[str]] = mapped_column(Text)  # JSON array
    
    # Status
    status: Mapped[str] = mapped_column(String(30), default="scheduled")  # scheduled, completed, cancelled, no_show
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class JobOffer(Base):
    """Job offer."""
    __tablename__ = "rcm_job_offers"
    __table_args__ = (
        Index("idx_rcmoffer_org_application", "organization_id", "application_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    application_id: Mapped[int] = mapped_column(Integer, ForeignKey("rcm_applications.id"), nullable=False)
    
    offer_number: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Offer details
    offered_position_title: Mapped[str] = mapped_column(String(255), nullable=False)
    offered_salary: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    offered_currency: Mapped[str] = mapped_column(String(3), default="USD")
    
    # Terms
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    employment_type: Mapped[str] = mapped_column(String(30), default="full_time")  # full_time, part_time, contract, seasonal
    
    # Benefits (JSON)
    benefits: Mapped[Optional[str]] = mapped_column(Text)
    
    # Timeline
    offer_date: Mapped[date] = mapped_column(Date, nullable=False)
    expiration_date: Mapped[date] = mapped_column(Date, nullable=False)
    accepted_date: Mapped[Optional[date]] = mapped_column(Date)
    declined_date: Mapped[Optional[date]] = mapped_column(Date)
    
    # Status
    status: Mapped[str] = mapped_column(String(30), default="pending")  # pending, accepted, declined, expired, withdrawn
    
    # Conditions
    contingent_on: Mapped[Optional[str]] = mapped_column(String(255))  # background check, etc
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class CandidateRating(Base):
    """Candidate skill rating."""
    __tablename__ = "rcm_candidate_ratings"
    __table_args__ = (
        Index("idx_rcmrating_org_candidate", "organization_id", "candidate_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    candidate_id: Mapped[int] = mapped_column(Integer, ForeignKey("rcm_candidates.id"), nullable=False)

    skill: Mapped[str] = mapped_column(String(100), nullable=False)
    proficiency_level: Mapped[str] = mapped_column(String(20), default="intermediate")  # beginner, intermediate, advanced, expert
    
    years_of_experience: Mapped[Optional[int]] = mapped_column(Integer)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
