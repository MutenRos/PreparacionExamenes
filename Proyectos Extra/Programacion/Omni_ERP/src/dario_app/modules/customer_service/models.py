"""Customer Service models for case management, knowledge base, and entitlements."""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, Index
from sqlalchemy.orm import Mapped, mapped_column

from dario_app.database import Base


class Case(Base):
    """Support case/ticket."""
    __tablename__ = "cs_cases"
    __table_args__ = (
        Index("idx_cs_case_org_customer", "organization_id", "customer_id"),
        Index("idx_cs_case_org_status", "organization_id", "status"),
        Index("idx_cs_case_org_priority", "organization_id", "priority"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    case_number: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    
    customer_id: Mapped[Optional[int]] = mapped_column(Integer)
    customer_name: Mapped[Optional[str]] = mapped_column(String(255))
    contact_email: Mapped[Optional[str]] = mapped_column(String(255))
    contact_phone: Mapped[Optional[str]] = mapped_column(String(50))
    
    status: Mapped[str] = mapped_column(String(30), default="new")  # new, active, resolved, closed, canceled
    priority: Mapped[str] = mapped_column(String(20), default="normal")  # low, normal, high, urgent
    severity: Mapped[str] = mapped_column(String(20), default="minor")  # minor, moderate, major, critical
    
    category: Mapped[Optional[str]] = mapped_column(String(100))  # billing, technical, general, etc.
    subcategory: Mapped[Optional[str]] = mapped_column(String(100))
    product: Mapped[Optional[str]] = mapped_column(String(255))
    
    assigned_to_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    assigned_to_name: Mapped[Optional[str]] = mapped_column(String(255))
    assigned_team: Mapped[Optional[str]] = mapped_column(String(100))
    
    # SLA tracking
    sla_due: Mapped[Optional[datetime]] = mapped_column(DateTime)
    first_response_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    escalated: Mapped[bool] = mapped_column(Boolean, default=False)
    escalated_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    escalated_to_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    entitlement_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("cs_entitlements.id"))
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CaseComment(Base):
    """Comments/notes on a case."""
    __tablename__ = "cs_case_comments"
    __table_args__ = (
        Index("idx_cs_comment_org_case", "organization_id", "case_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    case_id: Mapped[int] = mapped_column(Integer, ForeignKey("cs_cases.id"), nullable=False)

    comment: Mapped[str] = mapped_column(Text, nullable=False)
    author_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    author_name: Mapped[Optional[str]] = mapped_column(String(255))
    is_internal: Mapped[bool] = mapped_column(Boolean, default=False)  # internal note vs customer-visible

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class CSKnowledgeArticle(Base):
    """Knowledge base article for self-service (Customer Service module)."""
    __tablename__ = "cs_kb_articles"
    __table_args__ = (
        Index("idx_cs_kb_org_status", "organization_id", "status"),
        Index("idx_cs_kb_org_category", "organization_id", "category"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    article_number: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(String(500))
    
    category: Mapped[Optional[str]] = mapped_column(String(100))
    keywords: Mapped[Optional[str]] = mapped_column(Text)  # comma-separated for search
    
    status: Mapped[str] = mapped_column(String(30), default="draft")  # draft, published, archived
    language: Mapped[str] = mapped_column(String(10), default="es")
    
    author_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    author_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    helpful_count: Mapped[int] = mapped_column(Integer, default=0)
    not_helpful_count: Mapped[int] = mapped_column(Integer, default=0)
    
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Entitlement(Base):
    """Customer entitlement for support (hours, incidents, etc)."""
    __tablename__ = "cs_entitlements"
    __table_args__ = (
        Index("idx_cs_entitlement_org_customer", "organization_id", "customer_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    entitlement_number: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    customer_id: Mapped[Optional[int]] = mapped_column(Integer)
    customer_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    
    entitlement_type: Mapped[str] = mapped_column(String(30), default="incidents")  # incidents, hours, unlimited
    total_incidents: Mapped[Optional[int]] = mapped_column(Integer)  # null if unlimited
    used_incidents: Mapped[int] = mapped_column(Integer, default=0)
    total_hours: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    used_hours: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0"))
    
    status: Mapped[str] = mapped_column(String(30), default="active")  # draft, active, expired, canceled
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
