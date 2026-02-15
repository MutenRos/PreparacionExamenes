"""Field Service models: assets, work orders, tasks, schedules."""

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column

from dario_app.database import Base


class ServiceAsset(Base):
    """Installed base assets under service contract."""

    __tablename__ = "service_assets"
    __table_args__ = (
        Index("idx_asset_org_code", "organization_id", "asset_code", unique=True),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    asset_code: Mapped[str] = mapped_column(String(100), nullable=False)
    asset_name: Mapped[str] = mapped_column(String(255), nullable=False)
    asset_type: Mapped[Optional[str]] = mapped_column(String(100))
    model: Mapped[Optional[str]] = mapped_column(String(100))
    serial_number: Mapped[Optional[str]] = mapped_column(String(100))

    customer_id: Mapped[Optional[int]] = mapped_column(Integer)
    customer_name: Mapped[Optional[str]] = mapped_column(String(255))
    location_name: Mapped[Optional[str]] = mapped_column(String(255))
    latitude: Mapped[Optional[float]] = mapped_column(Numeric(10, 6))
    longitude: Mapped[Optional[float]] = mapped_column(Numeric(10, 6))

    installed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    sla_hours: Mapped[Optional[int]] = mapped_column(Integer)

    status: Mapped[str] = mapped_column(String(50), default="active")
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class WorkOrder(Base):
    """Field work order for technicians."""

    __tablename__ = "service_work_orders"
    __table_args__ = (
        Index("idx_wo_org_status", "organization_id", "status"),
        Index("idx_wo_org_sla", "organization_id", "sla_due"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    work_order_number: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)

    asset_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("service_assets.id"))
    asset_code: Mapped[Optional[str]] = mapped_column(String(100))
    asset_name: Mapped[Optional[str]] = mapped_column(String(255))

    customer_id: Mapped[Optional[int]] = mapped_column(Integer)
    customer_name: Mapped[Optional[str]] = mapped_column(String(255))

    priority: Mapped[str] = mapped_column(String(20), default="medium")  # low, medium, high, critical
    status: Mapped[str] = mapped_column(String(30), default="open")  # open, scheduled, in_progress, completed, canceled

    scheduled_start: Mapped[Optional[datetime]] = mapped_column(DateTime)
    scheduled_end: Mapped[Optional[datetime]] = mapped_column(DateTime)
    sla_due: Mapped[Optional[datetime]] = mapped_column(DateTime)

    address: Mapped[Optional[str]] = mapped_column(String(255))
    city: Mapped[Optional[str]] = mapped_column(String(100))
    latitude: Mapped[Optional[float]] = mapped_column(Numeric(10, 6))
    longitude: Mapped[Optional[float]] = mapped_column(Numeric(10, 6))

    assigned_to_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    assigned_to_name: Mapped[Optional[str]] = mapped_column(String(255))

    created_by_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    created_by_user_name: Mapped[Optional[str]] = mapped_column(String(255))

    completion_notes: Mapped[Optional[str]] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class WorkOrderTask(Base):
    """Checklist tasks for a work order."""

    __tablename__ = "service_work_order_tasks"
    __table_args__ = (
        Index("idx_wotask_org_wo", "organization_id", "work_order_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    work_order_id: Mapped[int] = mapped_column(Integer, ForeignKey("service_work_orders.id"), nullable=False)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(30), default="pending")  # pending, in_progress, done
    estimated_minutes: Mapped[Optional[int]] = mapped_column(Integer)
    actual_minutes: Mapped[Optional[int]] = mapped_column(Integer)

    completed_by_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    completed_by_name: Mapped[Optional[str]] = mapped_column(String(255))
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class WorkOrderSchedule(Base):
    """Technician scheduling slots for a work order."""

    __tablename__ = "service_work_order_schedules"
    __table_args__ = (
        Index("idx_woschedule_org_wo", "organization_id", "work_order_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    work_order_id: Mapped[int] = mapped_column(Integer, ForeignKey("service_work_orders.id"), nullable=False)

    technician_id: Mapped[Optional[int]] = mapped_column(Integer)
    technician_name: Mapped[Optional[str]] = mapped_column(String(255))
    start_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    end_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
