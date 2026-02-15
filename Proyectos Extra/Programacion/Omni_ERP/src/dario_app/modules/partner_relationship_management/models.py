"""
Partner Relationship Management (PRM) - Models
Manage partner programs, onboarding, incentives, and deal registrations.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship

from dario_app.database import Base


class PartnerProgram(Base):
    """Partner program definition with requirements and benefits."""
    __tablename__ = "prm_programs"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)

    program_code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    tiering_model = Column(String(50))  # Silver/Gold/Platinum or points-based
    requirements = Column(JSON)  # revenue targets, certifications
    benefits = Column(JSON)  # discounts, MDF, leads
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))

    partners = relationship("Partner", back_populates="program")


class Partner(Base):
    """Registered partner organization."""
    __tablename__ = "prm_partners"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    program_id = Column(Integer, ForeignKey("prm_programs.id"))

    partner_code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    partner_type = Column(String(100))  # Reseller, ISV, SI, OEM
    tier = Column(String(50))  # Silver, Gold, Platinum
    region = Column(String(100))
    industry_focus = Column(String(200))
    primary_contact = Column(String(200))
    contact_email = Column(String(200))
    contact_phone = Column(String(100))

    onboarding_status = Column(String(50), default="Pending")
    score = Column(Float)
    health = Column(String(50), default="Good")
    mdf_balance = Column(Float, default=0.0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))

    program = relationship("PartnerProgram", back_populates="partners")
    deals = relationship("PartnerDealRegistration", back_populates="partner", cascade="all, delete-orphan")
    incentives = relationship("PartnerIncentive", back_populates="partner", cascade="all, delete-orphan")
    certifications = relationship("PartnerCertification", back_populates="partner", cascade="all, delete-orphan")


class PartnerDealRegistration(Base):
    """Deal registration with approval workflow."""
    __tablename__ = "prm_deal_registrations"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    partner_id = Column(Integer, ForeignKey("prm_partners.id"))

    deal_code = Column(String(50), unique=True, nullable=False, index=True)
    customer_name = Column(String(200))
    customer_id = Column(Integer, index=True)
    estimated_amount = Column(Float)
    probability = Column(Float)
    stage = Column(String(50), default="Registered")  # Registered, Approved, Rejected, Won, Lost
    expected_close_date = Column(DateTime)
    notes = Column(Text)

    registered_at = Column(DateTime, default=datetime.utcnow)
    approved_at = Column(DateTime)
    approved_by = Column(String(100))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    partner = relationship("Partner", back_populates="deals")


class PartnerIncentive(Base):
    """Incentives and MDF allocations for partners."""
    __tablename__ = "prm_incentives"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    partner_id = Column(Integer, ForeignKey("prm_partners.id"))

    incentive_code = Column(String(50), unique=True, nullable=False, index=True)
    incentive_type = Column(String(100))  # MDF, Rebate, SPIFF
    amount = Column(Float)
    currency = Column(String(10), default="USD")
    status = Column(String(50), default="Allocated")  # Allocated, Claimed, Paid
    claim_reference = Column(String(100))
    description = Column(Text)

    allocation_date = Column(DateTime, default=datetime.utcnow)
    claimed_at = Column(DateTime)
    paid_at = Column(DateTime)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    partner = relationship("Partner", back_populates="incentives")


class PartnerCertification(Base):
    """Partner certifications and competency levels."""
    __tablename__ = "prm_certifications"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    partner_id = Column(Integer, ForeignKey("prm_partners.id"))

    certification_code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    category = Column(String(100))  # Technical, Sales, Delivery
    level = Column(String(50))  # Associate, Professional, Expert
    issued_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    status = Column(String(50), default="Active")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    partner = relationship("Partner", back_populates="certifications")
