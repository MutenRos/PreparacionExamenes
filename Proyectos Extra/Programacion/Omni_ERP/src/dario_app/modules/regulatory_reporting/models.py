"""
Regulatory Reporting & Tax Management - Models
Manages tax entities, returns, filings, and compliance audits.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from dario_app.database import Base


class TaxEntity(Base):
    """Legal entity for tax and reporting."""
    __tablename__ = "tax_entities"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)

    entity_code = Column(String(50), unique=True, nullable=False, index=True)
    legal_name = Column(String(200), nullable=False)
    country = Column(String(100))
    tax_id = Column(String(100), index=True)
    registration_number = Column(String(100))
    industry = Column(String(100))
    reporting_currency = Column(String(10), default="USD")
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    returns = relationship("TaxReturn", back_populates="entity", cascade="all, delete-orphan")


class TaxReturn(Base):
    """Periodic tax return."""
    __tablename__ = "tax_returns"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    entity_id = Column(Integer, ForeignKey("tax_entities.id"))

    return_code = Column(String(50), unique=True, nullable=False, index=True)
    period_start = Column(DateTime)
    period_end = Column(DateTime)
    jurisdiction = Column(String(100))
    form_type = Column(String(100))  # VAT, GST, Income, SalesTax
    status = Column(String(50), default="Draft")  # Draft, Prepared, Submitted, Accepted, Rejected
    total_tax_due = Column(Float)
    total_tax_collected = Column(Float)
    total_tax_paid = Column(Float)
    return_metadata = Column("metadata", JSON)

    submitted_at = Column(DateTime)
    accepted_at = Column(DateTime)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    entity = relationship("TaxEntity", back_populates="returns")
    schedules = relationship("TaxFilingSchedule", back_populates="tax_return", cascade="all, delete-orphan")
    transactions = relationship("TaxTransaction", back_populates="tax_return", cascade="all, delete-orphan")


class TaxFilingSchedule(Base):
    """Filing schedules and reminders."""
    __tablename__ = "tax_filing_schedules"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    tax_return_id = Column(Integer, ForeignKey("tax_returns.id"))

    due_date = Column(DateTime)
    reminder_days_before = Column(Integer, default=7)
    submitted_at = Column(DateTime)
    status = Column(String(50), default="Pending")  # Pending, Submitted, Overdue

    created_at = Column(DateTime, default=datetime.utcnow)

    tax_return = relationship("TaxReturn", back_populates="schedules")


class TaxTransaction(Base):
    """Tax transactions (inputs/outputs)."""
    __tablename__ = "tax_transactions"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    tax_return_id = Column(Integer, ForeignKey("tax_returns.id"))

    transaction_type = Column(String(50))  # Output, Input, Adjustment
    amount = Column(Float)
    tax_amount = Column(Float)
    currency = Column(String(10), default="USD")
    description = Column(Text)
    reference_id = Column(String(100))

    transaction_date = Column(DateTime, default=datetime.utcnow)

    tax_return = relationship("TaxReturn", back_populates="transactions")


class TaxAuditTrail(Base):
    """Audit log for tax filings and changes."""
    __tablename__ = "tax_audit_trails"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)

    target_type = Column(String(50))  # Return, Entity, Schedule
    target_id = Column(Integer)
    action = Column(String(100))  # Created, Updated, Submitted
    performed_by = Column(String(100))
    details = Column(JSON)
    performed_at = Column(DateTime, default=datetime.utcnow)
