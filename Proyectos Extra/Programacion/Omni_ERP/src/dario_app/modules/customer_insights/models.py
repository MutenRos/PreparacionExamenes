"""Customer Insights models for analytics and segmentation."""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, Index
from sqlalchemy.orm import Mapped, mapped_column

from dario_app.database import Base


class CustomerSegment(Base):
    """Customer segment definition."""
    __tablename__ = "ci_segments"
    __table_args__ = (
        Index("idx_cisegment_org_status", "organization_id", "status"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    segment_code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    
    segment_type: Mapped[str] = mapped_column(String(30), default="dynamic")  # static, dynamic
    status: Mapped[str] = mapped_column(String(30), default="active")  # active, inactive
    
    # Criteria (JSON)
    criteria: Mapped[Optional[str]] = mapped_column(Text)
    
    # Metrics
    member_count: Mapped[int] = mapped_column(Integer, default=0)
    avg_lifetime_value: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    avg_purchase_frequency: Mapped[Decimal] = mapped_column(Numeric(8, 2), default=Decimal("0"))
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CustomerSegmentMember(Base):
    """Customer membership in a segment."""
    __tablename__ = "ci_segment_members"
    __table_args__ = (
        Index("idx_cisegmember_org_segment", "organization_id", "segment_id"),
        Index("idx_cisegmember_org_customer", "organization_id", "customer_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    segment_id: Mapped[int] = mapped_column(Integer, ForeignKey("ci_segments.id"), nullable=False)

    customer_id: Mapped[int] = mapped_column(Integer, nullable=False)  # FK to clientes
    
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    left_at: Mapped[Optional[datetime]] = mapped_column(DateTime)


class CustomerMetric(Base):
    """Customer-level metrics and KPIs."""
    __tablename__ = "ci_customer_metrics"
    __table_args__ = (
        Index("idx_cimetric_org_customer", "organization_id", "customer_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    customer_id: Mapped[int] = mapped_column(Integer, nullable=False)  # FK to clientes

    # Lifetime metrics
    lifetime_value: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    total_orders: Mapped[int] = mapped_column(Integer, default=0)
    total_revenue: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    
    # Time-based
    first_purchase_date: Mapped[Optional[date]] = mapped_column(Date)
    last_purchase_date: Mapped[Optional[date]] = mapped_column(Date)
    days_since_last_purchase: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Frequency
    avg_days_between_purchases: Mapped[Optional[int]] = mapped_column(Integer)
    purchase_frequency_score: Mapped[int] = mapped_column(Integer, default=0)  # 0-100
    
    # Monetary
    avg_order_value: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    
    # RFM Scores
    recency_score: Mapped[int] = mapped_column(Integer, default=0)  # 1-5
    frequency_score: Mapped[int] = mapped_column(Integer, default=0)  # 1-5
    monetary_score: Mapped[int] = mapped_column(Integer, default=0)  # 1-5
    rfm_segment: Mapped[Optional[str]] = mapped_column(String(50))  # Champions, Loyal, etc.
    
    # Churn prediction
    churn_risk_score: Mapped[int] = mapped_column(Integer, default=0)  # 0-100
    churn_risk_level: Mapped[str] = mapped_column(String(20), default="low")  # low, medium, high
    
    # Engagement
    email_open_rate: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=Decimal("0"))
    email_click_rate: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=Decimal("0"))
    
    calculated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CustomerJourney(Base):
    """Customer journey tracking."""
    __tablename__ = "ci_journeys"
    __table_args__ = (
        Index("idx_cijourney_org_customer", "organization_id", "customer_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    customer_id: Mapped[int] = mapped_column(Integer, nullable=False)  # FK to clientes

    journey_type: Mapped[str] = mapped_column(String(50), nullable=False)  # acquisition, retention, winback
    stage: Mapped[str] = mapped_column(String(50), nullable=False)  # awareness, consideration, purchase, loyalty
    
    touchpoint: Mapped[str] = mapped_column(String(100), nullable=False)  # email, website, phone, store
    touchpoint_detail: Mapped[Optional[str]] = mapped_column(String(255))
    
    outcome: Mapped[Optional[str]] = mapped_column(String(50))  # conversion, bounce, click, etc.
    
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    # Context
    campaign_id: Mapped[Optional[int]] = mapped_column(Integer)
    source: Mapped[Optional[str]] = mapped_column(String(100))
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class CustomerPrediction(Base):
    """Customer prediction/recommendation."""
    __tablename__ = "ci_predictions"
    __table_args__ = (
        Index("idx_cipred_org_customer", "organization_id", "customer_id"),
        Index("idx_cipred_org_type", "organization_id", "prediction_type"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    customer_id: Mapped[int] = mapped_column(Integer, nullable=False)  # FK to clientes

    prediction_type: Mapped[str] = mapped_column(String(50), nullable=False)  # churn, next_purchase, product_recommendation
    
    prediction_value: Mapped[str] = mapped_column(String(255), nullable=False)
    confidence_score: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)  # 0-100
    
    # Context
    model_version: Mapped[str] = mapped_column(String(50), default="v1")
    features_used: Mapped[Optional[str]] = mapped_column(Text)  # JSON
    
    # Validation
    actual_outcome: Mapped[Optional[str]] = mapped_column(String(255))
    is_accurate: Mapped[Optional[bool]] = mapped_column(Boolean)
    
    valid_until: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class CustomerInsightReport(Base):
    """Generated insight reports."""
    __tablename__ = "ci_reports"
    __table_args__ = (
        Index("idx_cireport_org_type", "organization_id", "report_type"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    report_number: Mapped[str] = mapped_column(String(50), nullable=False)
    report_type: Mapped[str] = mapped_column(String(50), nullable=False)  # rfm_analysis, cohort_analysis, segmentation
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Results (JSON)
    data: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(Text)
    
    period_start: Mapped[Optional[date]] = mapped_column(Date)
    period_end: Mapped[Optional[date]] = mapped_column(Date)
    
    generated_by_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    generated_by_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class CustomerFeedback(Base):
    """Customer feedback and sentiment."""
    __tablename__ = "ci_feedback"
    __table_args__ = (
        Index("idx_cifeedback_org_customer", "organization_id", "customer_id"),
        Index("idx_cifeedback_org_sentiment", "organization_id", "sentiment"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    customer_id: Mapped[int] = mapped_column(Integer, nullable=False)  # FK to clientes

    feedback_type: Mapped[str] = mapped_column(String(30), default="survey")  # survey, review, nps, support
    
    rating: Mapped[Optional[int]] = mapped_column(Integer)  # 1-10 or 1-5
    nps_score: Mapped[Optional[int]] = mapped_column(Integer)  # -100 to 100
    
    comment: Mapped[Optional[str]] = mapped_column(Text)
    
    sentiment: Mapped[str] = mapped_column(String(20), default="neutral")  # positive, neutral, negative
    sentiment_score: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=Decimal("0"))  # -1 to 1
    
    feedback_date: Mapped[date] = mapped_column(Date, nullable=False)
    
    # Context
    reference_type: Mapped[Optional[str]] = mapped_column(String(50))  # order, product, support_case
    reference_id: Mapped[Optional[int]] = mapped_column(Integer)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
