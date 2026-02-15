"""Contract Lifecycle Management models."""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, Index
from sqlalchemy.orm import Mapped, mapped_column

from dario_app.database import Base


class ContractTemplate(Base):
    """Contract template."""
    __tablename__ = "clm_templates"
    __table_args__ = (
        Index("idx_clmtempl_org_status", "organization_id", "status"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    template_code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    contract_type: Mapped[str] = mapped_column(String(50), nullable=False)  # service, supply, employment, license, lease
    
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    
    # Content
    template_content: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Terms
    default_duration_days: Mapped[Optional[int]] = mapped_column(Integer)
    default_renewal_days: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default="active")
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Contract(Base):
    """Master contract record."""
    __tablename__ = "clm_contracts"
    __table_args__ = (
        Index("idx_clmcont_org_status", "organization_id", "status"),
        Index("idx_clmcont_org_party", "organization_id", "counterparty_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    contract_number: Mapped[str] = mapped_column(String(50), nullable=False)
    
    contract_type: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    
    # Parties
    counterparty_id: Mapped[int] = mapped_column(Integer, nullable=False)  # FK to clientes or proveedores
    counterparty_name: Mapped[str] = mapped_column(String(255), nullable=False)
    counterparty_contact: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Template
    template_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("clm_templates.id"))
    
    # Timeline
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    
    # Renewal
    auto_renewal: Mapped[bool] = mapped_column(Boolean, default=False)
    renewal_notice_days: Mapped[Optional[int]] = mapped_column(Integer, default=30)
    
    # Value
    contract_value: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2))
    currency: Mapped[Optional[str]] = mapped_column(String(3), default="USD")
    
    # Key information
    key_terms: Mapped[Optional[str]] = mapped_column(Text)  # JSON
    payment_terms: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Lifecycle stage
    status: Mapped[str] = mapped_column(String(30), default="draft")  # draft, pending_approval, active, on_hold, expired, terminated
    
    # Document
    document_path: Mapped[Optional[str]] = mapped_column(String(500))
    document_version: Mapped[Optional[int]] = mapped_column(Integer, default=1)
    
    # Owner
    contract_owner_id: Mapped[Optional[int]] = mapped_column(Integer)
    contract_owner_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ContractClause(Base):
    """Contract clause/section."""
    __tablename__ = "clm_clauses"
    __table_args__ = (
        Index("idx_clmclause_org_contract", "organization_id", "contract_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    contract_id: Mapped[int] = mapped_column(Integer, ForeignKey("clm_contracts.id"), nullable=False)

    clause_number: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    
    clause_type: Mapped[str] = mapped_column(String(50), nullable=False)  # payment, liability, termination, confidentiality, ip
    
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    risk_level: Mapped[str] = mapped_column(String(20), default="medium")  # low, medium, high, critical
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ContractApproval(Base):
    """Contract approval workflow step."""
    __tablename__ = "clm_approvals"
    __table_args__ = (
        Index("idx_clmappr_org_contract", "organization_id", "contract_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    contract_id: Mapped[int] = mapped_column(Integer, ForeignKey("clm_contracts.id"), nullable=False)

    approval_step: Mapped[int] = mapped_column(Integer, nullable=False)  # sequence
    
    approver_id: Mapped[int] = mapped_column(Integer, nullable=False)
    approver_name: Mapped[str] = mapped_column(String(255), nullable=False)
    approver_role: Mapped[Optional[str]] = mapped_column(String(100))
    
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, approved, rejected
    
    comments: Mapped[Optional[str]] = mapped_column(Text)
    
    response_date: Mapped[Optional[date]] = mapped_column(Date)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ContractMilestone(Base):
    """Contract milestone/obligation."""
    __tablename__ = "clm_milestones"
    __table_args__ = (
        Index("idx_clmmile_org_contract", "organization_id", "contract_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    contract_id: Mapped[int] = mapped_column(Integer, ForeignKey("clm_contracts.id"), nullable=False)

    milestone_number: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    
    milestone_type: Mapped[str] = mapped_column(String(50), nullable=False)  # payment, delivery, compliance, renewal
    
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    completion_date: Mapped[Optional[date]] = mapped_column(Date)
    
    # Value
    associated_value: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2))
    
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, in_progress, completed, at_risk, overdue
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ContractRenewal(Base):
    """Contract renewal record."""
    __tablename__ = "clm_renewals"
    __table_args__ = (
        Index("idx_clmrenew_org_contract", "organization_id", "original_contract_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    original_contract_id: Mapped[int] = mapped_column(Integer, ForeignKey("clm_contracts.id"), nullable=False)
    new_contract_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("clm_contracts.id"))
    
    renewal_number: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Renewal terms
    renewal_start_date: Mapped[date] = mapped_column(Date, nullable=False)
    renewal_end_date: Mapped[date] = mapped_column(Date, nullable=False)
    renewal_duration_days: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Terms change
    new_value: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2))
    value_change_percent: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2))
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, approved, declined, auto_renewed
    
    # Dates
    renewal_decision_date: Mapped[Optional[date]] = mapped_column(Date)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
