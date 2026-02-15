"""Subscription Billing models for recurring revenue."""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, Index
from sqlalchemy.orm import Mapped, mapped_column

from dario_app.database import Base


class SubscriptionPlan(Base):
    """Subscription plan template."""
    __tablename__ = "sub_plans"
    __table_args__ = (
        Index("idx_subplan_org_status", "organization_id", "status"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    plan_code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    
    status: Mapped[str] = mapped_column(String(30), default="active")  # active, inactive
    
    billing_frequency: Mapped[str] = mapped_column(String(30), default="monthly")  # monthly, quarterly, annual
    billing_period_value: Mapped[int] = mapped_column(Integer, default=1)
    
    base_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="EUR")
    
    # Trial
    trial_period_days: Mapped[int] = mapped_column(Integer, default=0)
    
    # Usage-based
    is_usage_based: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Features (JSON string)
    features: Mapped[Optional[str]] = mapped_column(Text)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Subscription(Base):
    """Customer subscription."""
    __tablename__ = "subscriptions"
    __table_args__ = (
        Index("idx_sub_org_status", "organization_id", "status"),
        Index("idx_sub_org_customer", "organization_id", "customer_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    subscription_number: Mapped[str] = mapped_column(String(50), nullable=False)
    
    customer_id: Mapped[int] = mapped_column(Integer, nullable=False)  # FK to clientes
    customer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    plan_id: Mapped[int] = mapped_column(Integer, ForeignKey("sub_plans.id"), nullable=False)
    plan_name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    status: Mapped[str] = mapped_column(String(30), default="active")  # active, trial, suspended, canceled, expired
    
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    trial_end_date: Mapped[Optional[date]] = mapped_column(Date)
    next_billing_date: Mapped[Optional[date]] = mapped_column(Date)
    end_date: Mapped[Optional[date]] = mapped_column(Date)
    
    billing_frequency: Mapped[str] = mapped_column(String(30), default="monthly")
    
    base_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    discount_percent: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=Decimal("0"))
    
    # Auto-renewal
    auto_renew: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Cancellation
    canceled_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    cancellation_reason: Mapped[Optional[str]] = mapped_column(Text)
    
    # MRR tracking
    mrr: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))  # Monthly Recurring Revenue
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SubscriptionInvoice(Base):
    """Subscription billing invoice."""
    __tablename__ = "sub_invoices"
    __table_args__ = (
        Index("idx_subinv_org_subscription", "organization_id", "subscription_id"),
        Index("idx_subinv_org_status", "organization_id", "status"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    subscription_id: Mapped[int] = mapped_column(Integer, ForeignKey("subscriptions.id"), nullable=False)

    invoice_number: Mapped[str] = mapped_column(String(50), nullable=False)
    
    invoice_date: Mapped[date] = mapped_column(Date, nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    
    billing_period_start: Mapped[date] = mapped_column(Date, nullable=False)
    billing_period_end: Mapped[date] = mapped_column(Date, nullable=False)
    
    subtotal: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    tax_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    total_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    
    status: Mapped[str] = mapped_column(String(30), default="pending")  # pending, paid, overdue, void
    
    paid_date: Mapped[Optional[date]] = mapped_column(Date)
    payment_method: Mapped[Optional[str]] = mapped_column(String(50))
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class SubscriptionUsage(Base):
    """Usage tracking for usage-based billing."""
    __tablename__ = "sub_usage"
    __table_args__ = (
        Index("idx_subusage_org_subscription", "organization_id", "subscription_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    subscription_id: Mapped[int] = mapped_column(Integer, ForeignKey("subscriptions.id"), nullable=False)

    usage_date: Mapped[date] = mapped_column(Date, nullable=False)
    
    metric_name: Mapped[str] = mapped_column(String(100), nullable=False)  # API calls, users, storage GB, etc.
    quantity: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12, 4), nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class SubscriptionChange(Base):
    """Subscription change history (upgrades, downgrades)."""
    __tablename__ = "sub_changes"
    __table_args__ = (
        Index("idx_subchange_org_subscription", "organization_id", "subscription_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    subscription_id: Mapped[int] = mapped_column(Integer, ForeignKey("subscriptions.id"), nullable=False)

    change_type: Mapped[str] = mapped_column(String(30), nullable=False)  # upgrade, downgrade, pause, resume, cancel
    
    old_plan_id: Mapped[Optional[int]] = mapped_column(Integer)
    old_plan_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    new_plan_id: Mapped[Optional[int]] = mapped_column(Integer)
    new_plan_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    old_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    new_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    
    effective_date: Mapped[date] = mapped_column(Date, nullable=False)
    
    reason: Mapped[Optional[str]] = mapped_column(Text)
    
    changed_by_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    changed_by_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class RevenueRecognition(Base):
    """Revenue recognition schedule."""
    __tablename__ = "revenue_recognition"
    __table_args__ = (
        Index("idx_revenue_org_subscription", "organization_id", "subscription_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    subscription_id: Mapped[int] = mapped_column(Integer, ForeignKey("subscriptions.id"), nullable=False)
    invoice_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("sub_invoices.id"))

    recognition_date: Mapped[date] = mapped_column(Date, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    
    status: Mapped[str] = mapped_column(String(30), default="scheduled")  # scheduled, recognized
    
    recognized_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
