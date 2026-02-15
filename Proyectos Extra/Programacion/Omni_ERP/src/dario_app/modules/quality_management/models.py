"""Quality Management models for inspections and quality control."""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, Index
from sqlalchemy.orm import Mapped, mapped_column

from dario_app.database import Base


class QualityOrder(Base):
    """Quality inspection order."""
    __tablename__ = "quality_orders"
    __table_args__ = (
        Index("idx_qorder_org_status", "organization_id", "status"),
        Index("idx_qorder_org_type", "organization_id", "order_type"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    order_number: Mapped[str] = mapped_column(String(50), nullable=False)
    
    order_type: Mapped[str] = mapped_column(String(30), default="receiving")  # receiving, in_process, final, audit
    status: Mapped[str] = mapped_column(String(30), default="pending")  # pending, in_progress, completed, failed, canceled
    
    reference_type: Mapped[Optional[str]] = mapped_column(String(50))  # purchase_order, sales_order, production_order
    reference_id: Mapped[Optional[int]] = mapped_column(Integer)
    reference_number: Mapped[Optional[str]] = mapped_column(String(50))
    
    product_id: Mapped[Optional[int]] = mapped_column(Integer)  # FK to productos
    product_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    quantity_to_inspect: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    quantity_inspected: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    quantity_passed: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    quantity_failed: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    
    inspector_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    inspector_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    scheduled_date: Mapped[Optional[date]] = mapped_column(Date)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    inspection_result: Mapped[Optional[str]] = mapped_column(String(30))  # pass, fail, conditional
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class QualityCheckpoint(Base):
    """Quality checkpoint/test within an order."""
    __tablename__ = "quality_checkpoints"
    __table_args__ = (
        Index("idx_qcheckpoint_org_order", "organization_id", "quality_order_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    quality_order_id: Mapped[int] = mapped_column(Integer, ForeignKey("quality_orders.id"), nullable=False)

    checkpoint_name: Mapped[str] = mapped_column(String(255), nullable=False)
    checkpoint_type: Mapped[str] = mapped_column(String(30), default="visual")  # visual, measurement, functional, destructive
    
    specification: Mapped[Optional[str]] = mapped_column(Text)
    acceptance_criteria: Mapped[Optional[str]] = mapped_column(Text)
    
    measured_value: Mapped[Optional[str]] = mapped_column(String(255))
    result: Mapped[Optional[str]] = mapped_column(String(20))  # pass, fail, na
    
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class NonConformance(Base):
    """Non-conformance record (NCR)."""
    __tablename__ = "quality_nonconformances"
    __table_args__ = (
        Index("idx_ncr_org_status", "organization_id", "status"),
        Index("idx_ncr_org_severity", "organization_id", "severity"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    ncr_number: Mapped[str] = mapped_column(String(50), nullable=False)
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    severity: Mapped[str] = mapped_column(String(20), default="medium")  # low, medium, high, critical
    status: Mapped[str] = mapped_column(String(30), default="open")  # open, investigating, corrective_action, closed
    
    detected_date: Mapped[date] = mapped_column(Date, nullable=False)
    detected_by_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    detected_by_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    product_id: Mapped[Optional[int]] = mapped_column(Integer)
    product_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    reference_type: Mapped[Optional[str]] = mapped_column(String(50))
    reference_id: Mapped[Optional[int]] = mapped_column(Integer)
    reference_number: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Root cause analysis
    root_cause: Mapped[Optional[str]] = mapped_column(Text)
    
    # Corrective action
    corrective_action: Mapped[Optional[str]] = mapped_column(Text)
    action_assigned_to_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    action_assigned_to_name: Mapped[Optional[str]] = mapped_column(String(255))
    action_due_date: Mapped[Optional[date]] = mapped_column(Date)
    action_completed_date: Mapped[Optional[date]] = mapped_column(Date)
    
    # Financial impact
    cost_impact: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    
    closed_date: Mapped[Optional[date]] = mapped_column(Date)
    closed_by_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    closed_by_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class QualitySpecification(Base):
    """Product quality specification."""
    __tablename__ = "quality_specifications"
    __table_args__ = (
        Index("idx_qspec_org_product", "organization_id", "product_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    spec_code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    product_id: Mapped[Optional[int]] = mapped_column(Integer)  # FK to productos
    product_category: Mapped[Optional[str]] = mapped_column(String(100))
    
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    status: Mapped[str] = mapped_column(String(30), default="active")  # active, inactive, obsolete
    version: Mapped[int] = mapped_column(Integer, default=1)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class QualitySpecificationLine(Base):
    """Individual test/measurement in a specification."""
    __tablename__ = "quality_specification_lines"
    __table_args__ = (
        Index("idx_qspecline_org_spec", "organization_id", "specification_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    specification_id: Mapped[int] = mapped_column(Integer, ForeignKey("quality_specifications.id"), nullable=False)

    line_number: Mapped[int] = mapped_column(Integer, nullable=False)
    test_name: Mapped[str] = mapped_column(String(255), nullable=False)
    test_type: Mapped[str] = mapped_column(String(30), default="measurement")
    
    target_value: Mapped[Optional[str]] = mapped_column(String(100))
    min_value: Mapped[Optional[str]] = mapped_column(String(100))
    max_value: Mapped[Optional[str]] = mapped_column(String(100))
    unit_of_measure: Mapped[Optional[str]] = mapped_column(String(20))
    
    is_mandatory: Mapped[bool] = mapped_column(Boolean, default=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class QualityAudit(Base):
    """Quality audit."""
    __tablename__ = "quality_audits"
    __table_args__ = (
        Index("idx_qaudit_org_status", "organization_id", "status"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    audit_number: Mapped[str] = mapped_column(String(50), nullable=False)
    audit_type: Mapped[str] = mapped_column(String(30), default="internal")  # internal, external, supplier
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    status: Mapped[str] = mapped_column(String(30), default="planned")  # planned, in_progress, completed
    
    scheduled_date: Mapped[date] = mapped_column(Date, nullable=False)
    completed_date: Mapped[Optional[date]] = mapped_column(Date)
    
    auditor_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    auditor_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Results
    findings_count: Mapped[int] = mapped_column(Integer, default=0)
    ncrs_raised: Mapped[int] = mapped_column(Integer, default=0)
    
    audit_report: Mapped[Optional[str]] = mapped_column(Text)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
