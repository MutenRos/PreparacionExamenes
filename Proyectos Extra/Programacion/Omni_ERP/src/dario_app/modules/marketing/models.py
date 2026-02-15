"""Marketing models for campaigns, email marketing, and customer journeys."""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, Index, JSON
from sqlalchemy.orm import Mapped, mapped_column

from dario_app.database import Base


class Campaign(Base):
    """Marketing campaign."""
    __tablename__ = "mkt_campaigns"
    __table_args__ = (
        Index("idx_mkt_campaign_org_status", "organization_id", "status"),
        Index("idx_mkt_campaign_org_type", "organization_id", "campaign_type"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    campaign_code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    
    campaign_type: Mapped[str] = mapped_column(String(50), default="email")  # email, social, event, webinar, etc.
    status: Mapped[str] = mapped_column(String(30), default="draft")  # draft, scheduled, active, completed, canceled
    
    start_date: Mapped[Optional[date]] = mapped_column(Date)
    end_date: Mapped[Optional[date]] = mapped_column(Date)
    
    budget: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    actual_cost: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    expected_revenue: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    
    target_audience: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Metrics
    total_sent: Mapped[int] = mapped_column(Integer, default=0)
    total_delivered: Mapped[int] = mapped_column(Integer, default=0)
    total_opened: Mapped[int] = mapped_column(Integer, default=0)
    total_clicked: Mapped[int] = mapped_column(Integer, default=0)
    total_leads_generated: Mapped[int] = mapped_column(Integer, default=0)
    total_opportunities_generated: Mapped[int] = mapped_column(Integer, default=0)
    
    owner_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    owner_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CampaignActivity(Base):
    """Campaign activity (email send, event, etc)."""
    __tablename__ = "mkt_campaign_activities"
    __table_args__ = (
        Index("idx_mkt_activity_org_campaign", "organization_id", "campaign_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    campaign_id: Mapped[int] = mapped_column(Integer, ForeignKey("mkt_campaigns.id"), nullable=False)

    activity_type: Mapped[str] = mapped_column(String(50), nullable=False)  # email, call, event, webinar
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    
    scheduled_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    executed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    status: Mapped[str] = mapped_column(String(30), default="pending")  # pending, executing, completed, failed
    
    target_list_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("mkt_lists.id"))
    
    # Email specific
    email_template_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("mkt_email_templates.id"))
    sender_email: Mapped[Optional[str]] = mapped_column(String(255))
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class MarketingList(Base):
    """Marketing list/segment."""
    __tablename__ = "mkt_lists"
    __table_args__ = (
        Index("idx_mkt_list_org_type", "organization_id", "list_type"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    list_code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    
    list_type: Mapped[str] = mapped_column(String(30), default="static")  # static, dynamic
    status: Mapped[str] = mapped_column(String(30), default="active")  # active, inactive
    
    # Dynamic list criteria (JSON)
    criteria: Mapped[Optional[str]] = mapped_column(Text)  # Store as JSON string
    
    member_count: Mapped[int] = mapped_column(Integer, default=0)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class EmailTemplate(Base):
    """Email template for marketing."""
    __tablename__ = "mkt_email_templates"
    __table_args__ = (
        Index("idx_mkt_template_org_type", "organization_id", "template_type"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    template_code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    template_type: Mapped[str] = mapped_column(String(50), default="newsletter")  # newsletter, promo, transactional
    
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    html_content: Mapped[str] = mapped_column(Text, nullable=False)
    plain_text_content: Mapped[Optional[str]] = mapped_column(Text)
    
    # Merge fields available: {{nombre}}, {{email}}, etc.
    
    status: Mapped[str] = mapped_column(String(30), default="draft")  # draft, active, archived
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CustomerJourney(Base):
    """Customer journey / automation workflow."""
    __tablename__ = "mkt_customer_journeys"
    __table_args__ = (
        Index("idx_mkt_journey_org_status", "organization_id", "status"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    journey_code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    
    status: Mapped[str] = mapped_column(String(30), default="draft")  # draft, active, stopped
    
    # Journey definition (JSON with steps, triggers, conditions)
    workflow_definition: Mapped[Optional[str]] = mapped_column(Text)
    
    # Entry criteria
    entry_list_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("mkt_lists.id"))
    entry_trigger: Mapped[Optional[str]] = mapped_column(String(100))  # form_submit, lead_created, etc.
    
    # Metrics
    total_participants: Mapped[int] = mapped_column(Integer, default=0)
    active_participants: Mapped[int] = mapped_column(Integer, default=0)
    completed_participants: Mapped[int] = mapped_column(Integer, default=0)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class LeadScore(Base):
    """Lead scoring configuration and history."""
    __tablename__ = "mkt_lead_scores"
    __table_args__ = (
        Index("idx_mkt_score_org_lead", "organization_id", "lead_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    lead_id: Mapped[int] = mapped_column(Integer, nullable=False)  # FK to CRM Lead
    
    total_score: Mapped[int] = mapped_column(Integer, default=0)
    demographic_score: Mapped[int] = mapped_column(Integer, default=0)
    behavioral_score: Mapped[int] = mapped_column(Integer, default=0)
    
    grade: Mapped[Optional[str]] = mapped_column(String(10))  # A, B, C, D, F
    
    last_activity_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    # Scoring factors (JSON)
    scoring_details: Mapped[Optional[str]] = mapped_column(Text)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
