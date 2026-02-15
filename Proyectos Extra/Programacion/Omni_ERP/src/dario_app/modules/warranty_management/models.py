"""Warranty Management models."""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, Index
from sqlalchemy.orm import Mapped, mapped_column

from dario_app.database import Base


class WarrantyPolicy(Base):
    """Warranty policy template."""
    __tablename__ = "wty_policies"
    __table_args__ = (
        Index("idx_wtypol_org_status", "organization_id", "status"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    policy_code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    
    # Coverage
    warranty_type: Mapped[str] = mapped_column(String(50), nullable=False)  # manufacturer, extended, service, parts
    
    # Duration
    duration_months: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # What's covered
    covers_parts: Mapped[bool] = mapped_column(Boolean, default=True)
    covers_labor: Mapped[bool] = mapped_column(Boolean, default=True)
    covers_shipping: Mapped[bool] = mapped_column(Boolean, default=False)
    covers_accidental_damage: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Exclusions
    exclusions: Mapped[Optional[str]] = mapped_column(Text)  # JSON array
    
    # Claim process
    deductible_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    max_claim_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2))
    claim_processing_days: Mapped[Optional[int]] = mapped_column(Integer, default=30)
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default="active")
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ProductWarranty(Base):
    """Warranty coverage for a product."""
    __tablename__ = "wty_product_warranties"
    __table_args__ = (
        Index("idx_wtyprod_org_product", "organization_id", "product_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    product_id: Mapped[int] = mapped_column(Integer, nullable=False)  # FK to productos
    policy_id: Mapped[int] = mapped_column(Integer, ForeignKey("wty_policies.id"), nullable=False)
    
    # Apply to variants
    applies_to_all_variants: Mapped[bool] = mapped_column(Boolean, default=True)
    product_variant_id: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Cost
    warranty_cost: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0"))
    cost_type: Mapped[str] = mapped_column(String(20), default="included")  # included, paid_option
    
    status: Mapped[str] = mapped_column(String(20), default="active")
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class WarrantyRegistration(Base):
    """Customer warranty registration."""
    __tablename__ = "wty_registrations"
    __table_args__ = (
        Index("idx_wtyreg_org_customer", "organization_id", "customer_id"),
        Index("idx_wtyreg_org_product", "organization_id", "product_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    registration_number: Mapped[str] = mapped_column(String(50), nullable=False)
    
    customer_id: Mapped[int] = mapped_column(Integer, nullable=False)  # FK to clientes
    customer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    product_id: Mapped[int] = mapped_column(Integer, nullable=False)
    product_code: Mapped[str] = mapped_column(String(100), nullable=False)
    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    serial_number: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Purchase info
    purchase_date: Mapped[date] = mapped_column(Date, nullable=False)
    purchase_order_number: Mapped[Optional[str]] = mapped_column(String(50))
    retailer_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Warranty policy
    policy_id: Mapped[int] = mapped_column(Integer, ForeignKey("wty_policies.id"), nullable=False)
    
    # Warranty period
    warranty_start_date: Mapped[date] = mapped_column(Date, nullable=False)
    warranty_end_date: Mapped[date] = mapped_column(Date, nullable=False)
    
    # Extended warranty
    extended_warranty_purchased: Mapped[bool] = mapped_column(Boolean, default=False)
    extended_warranty_end_date: Mapped[Optional[date]] = mapped_column(Date)
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default="active")  # active, expired, claim_pending, claim_approved
    
    # Contact
    contact_email: Mapped[Optional[str]] = mapped_column(String(255))
    contact_phone: Mapped[Optional[str]] = mapped_column(String(50))
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class WarrantyClaim(Base):
    """Warranty claim."""
    __tablename__ = "wty_claims"
    __table_args__ = (
        Index("idx_wtyclaim_org_registration", "organization_id", "registration_id"),
        Index("idx_wtyclaim_org_status", "organization_id", "status"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    claim_number: Mapped[str] = mapped_column(String(50), nullable=False)
    
    registration_id: Mapped[int] = mapped_column(Integer, ForeignKey("wty_registrations.id"), nullable=False)
    
    # Claim details
    claim_type: Mapped[str] = mapped_column(String(50), nullable=False)  # defect, damage, malfunction, failure
    
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Issue date
    issue_date: Mapped[date] = mapped_column(Date, nullable=False)
    reported_date: Mapped[date] = mapped_column(Date, nullable=False)
    
    # Assessment
    assessed_date: Mapped[Optional[date]] = mapped_column(Date)
    assessment_notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Resolution
    resolution_type: Mapped[Optional[str]] = mapped_column(String(50))  # repair, replace, refund
    
    # Amount
    claimed_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    approved_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    
    # Status
    status: Mapped[str] = mapped_column(String(30), default="submitted")  # submitted, under_review, approved, denied, resolved, closed
    
    # Dates
    approval_date: Mapped[Optional[date]] = mapped_column(Date)
    resolution_date: Mapped[Optional[date]] = mapped_column(Date)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class WarrantyService(Base):
    """Warranty service/repair record."""
    __tablename__ = "wty_services"
    __table_args__ = (
        Index("idx_wtysvc_org_claim", "organization_id", "claim_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    service_number: Mapped[str] = mapped_column(String(50), nullable=False)
    
    claim_id: Mapped[int] = mapped_column(Integer, ForeignKey("wty_claims.id"), nullable=False)
    
    # Service provider
    service_provider_name: Mapped[str] = mapped_column(String(255), nullable=False)
    service_provider_id: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Service details
    service_type: Mapped[str] = mapped_column(String(50), nullable=False)  # repair, replacement, inspection
    
    # Timeline
    service_start_date: Mapped[date] = mapped_column(Date, nullable=False)
    service_end_date: Mapped[Optional[date]] = mapped_column(Date)
    
    # Labor
    labor_hours: Mapped[Optional[Decimal]] = mapped_column(Numeric(8, 2))
    labor_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    
    # Parts
    parts_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    parts_list: Mapped[Optional[str]] = mapped_column(Text)  # JSON array
    
    # Total cost
    total_cost: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0"))
    
    # Notes
    service_notes: Mapped[Optional[str]] = mapped_column(Text)
    
    status: Mapped[str] = mapped_column(String(20), default="in_progress")  # in_progress, completed, failed
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
