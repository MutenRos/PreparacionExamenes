"""Asset Management models for equipment, maintenance, and rentals."""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, Index
from sqlalchemy.orm import Mapped, mapped_column

from dario_app.database import Base


class Asset(Base):
    """Physical asset / equipment."""
    __tablename__ = "asset_assets"
    __table_args__ = (
        Index("idx_asset_org_status", "organization_id", "status"),
        Index("idx_asset_org_category", "organization_id", "category"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    asset_code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    
    category: Mapped[str] = mapped_column(String(100), nullable=False)  # vehicles, machinery, IT, etc.
    status: Mapped[str] = mapped_column(String(30), default="available")  # available, in_use, maintenance, retired
    
    # Acquisition
    acquisition_date: Mapped[Optional[date]] = mapped_column(Date)
    acquisition_cost: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    supplier_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Depreciation
    useful_life_years: Mapped[Optional[int]] = mapped_column(Integer)
    depreciation_method: Mapped[str] = mapped_column(String(30), default="straight_line")
    current_value: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    
    # Location
    current_location: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Specifications
    manufacturer: Mapped[Optional[str]] = mapped_column(String(255))
    model_number: Mapped[Optional[str]] = mapped_column(String(100))
    serial_number: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Rental/billable
    is_rentable: Mapped[bool] = mapped_column(Boolean, default=False)
    daily_rental_rate: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    hourly_rental_rate: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    
    # Maintenance
    last_maintenance_date: Mapped[Optional[date]] = mapped_column(Date)
    next_maintenance_date: Mapped[Optional[date]] = mapped_column(Date)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MaintenanceSchedule(Base):
    """Planned maintenance schedule."""
    __tablename__ = "asset_maintenance_schedules"
    __table_args__ = (
        Index("idx_maint_sched_org_asset", "organization_id", "asset_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    asset_id: Mapped[int] = mapped_column(Integer, ForeignKey("asset_assets.id"), nullable=False)

    schedule_code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    
    frequency_type: Mapped[str] = mapped_column(String(30), default="periodic")  # periodic, usage_based
    frequency_interval_days: Mapped[Optional[int]] = mapped_column(Integer)
    
    status: Mapped[str] = mapped_column(String(30), default="active")  # active, inactive
    
    estimated_duration_hours: Mapped[Optional[int]] = mapped_column(Integer)
    estimated_cost: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MaintenanceOrder(Base):
    """Maintenance work order."""
    __tablename__ = "asset_maintenance_orders"
    __table_args__ = (
        Index("idx_maint_order_org_asset", "organization_id", "asset_id"),
        Index("idx_maint_order_org_status", "organization_id", "status"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    asset_id: Mapped[int] = mapped_column(Integer, ForeignKey("asset_assets.id"), nullable=False)

    order_number: Mapped[str] = mapped_column(String(50), nullable=False)
    
    maintenance_type: Mapped[str] = mapped_column(String(30), default="preventive")  # preventive, corrective, inspection
    priority: Mapped[str] = mapped_column(String(20), default="medium")  # low, medium, high, critical
    status: Mapped[str] = mapped_column(String(30), default="scheduled")  # scheduled, in_progress, completed, canceled
    
    scheduled_date: Mapped[Optional[date]] = mapped_column(Date)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    description: Mapped[str] = mapped_column(Text, nullable=False)
    work_performed: Mapped[Optional[str]] = mapped_column(Text)
    
    assigned_to_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    assigned_to_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    actual_duration_hours: Mapped[Optional[int]] = mapped_column(Integer)
    actual_cost: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    
    downtime_hours: Mapped[Optional[int]] = mapped_column(Integer)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class RentalAgreement(Base):
    """Asset rental/lease agreement."""
    __tablename__ = "asset_rental_agreements"
    __table_args__ = (
        Index("idx_rental_org_asset", "organization_id", "asset_id"),
        Index("idx_rental_org_status", "organization_id", "status"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    asset_id: Mapped[int] = mapped_column(Integer, ForeignKey("asset_assets.id"), nullable=False)

    agreement_number: Mapped[str] = mapped_column(String(50), nullable=False)
    
    customer_id: Mapped[Optional[int]] = mapped_column(Integer)  # FK to clientes
    customer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    status: Mapped[str] = mapped_column(String(30), default="active")  # draft, active, completed, canceled
    
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    actual_return_date: Mapped[Optional[date]] = mapped_column(Date)
    
    billing_frequency: Mapped[str] = mapped_column(String(30), default="daily")  # hourly, daily, weekly, monthly
    rental_rate: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    
    security_deposit: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    
    total_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    paid_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AssetTransfer(Base):
    """Asset location/ownership transfer."""
    __tablename__ = "asset_transfers"
    __table_args__ = (
        Index("idx_asset_transfer_org_asset", "organization_id", "asset_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    asset_id: Mapped[int] = mapped_column(Integer, ForeignKey("asset_assets.id"), nullable=False)

    transfer_number: Mapped[str] = mapped_column(String(50), nullable=False)
    
    transfer_type: Mapped[str] = mapped_column(String(30), default="location")  # location, custody, ownership
    
    from_location: Mapped[Optional[str]] = mapped_column(String(255))
    to_location: Mapped[Optional[str]] = mapped_column(String(255))
    
    from_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    from_user_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    to_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    to_user_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    transfer_date: Mapped[date] = mapped_column(Date, nullable=False)
    reason: Mapped[Optional[str]] = mapped_column(Text)
    
    status: Mapped[str] = mapped_column(String(30), default="completed")  # pending, completed, rejected
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class AssetMeter(Base):
    """Asset usage meter reading (hours, km, cycles, etc)."""
    __tablename__ = "asset_meters"
    __table_args__ = (
        Index("idx_asset_meter_org_asset", "organization_id", "asset_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    asset_id: Mapped[int] = mapped_column(Integer, ForeignKey("asset_assets.id"), nullable=False)

    meter_type: Mapped[str] = mapped_column(String(30), nullable=False)  # hours, kilometers, cycles
    reading_value: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    reading_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    recorded_by_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    recorded_by_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
