"""Service Scheduling models."""

from datetime import datetime, date, time, timedelta
from decimal import Decimal
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, Time, Index
from sqlalchemy.orm import Mapped, mapped_column

from dario_app.database import Base


class ServiceResource(Base):
    """Service resource (technician, equipment, etc)."""
    __tablename__ = "sched_resources"
    __table_args__ = (
        Index("idx_schedres_org_status", "organization_id", "status"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    resource_code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    resource_type: Mapped[str] = mapped_column(String(30), default="technician")  # technician, equipment, vehicle, location
    
    # Capacity
    capacity: Mapped[Optional[int]] = mapped_column(Integer)  # concurrent appointments
    
    # Scheduling
    working_hours_start: Mapped[Optional[time]] = mapped_column(Time)
    working_hours_end: Mapped[Optional[time]] = mapped_column(Time)
    available_days: Mapped[Optional[str]] = mapped_column(String(20))  # "MTWRFSU"
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default="active")
    
    # Contact
    phone: Mapped[Optional[str]] = mapped_column(String(50))
    email: Mapped[Optional[str]] = mapped_column(String(255))
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ServiceSlot(Base):
    """Available service appointment slot."""
    __tablename__ = "sched_slots"
    __table_args__ = (
        Index("idx_schedslot_org_resource", "organization_id", "resource_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    resource_id: Mapped[int] = mapped_column(Integer, ForeignKey("sched_resources.id"), nullable=False)

    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)
    
    block_reason: Mapped[Optional[str]] = mapped_column(String(255))
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ServiceAppointment(Base):
    """Service appointment."""
    __tablename__ = "sched_appointments"
    __table_args__ = (
        Index("idx_schedappt_org_status", "organization_id", "status"),
        Index("idx_schedappt_org_customer", "organization_id", "customer_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    appointment_number: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Customer
    customer_id: Mapped[int] = mapped_column(Integer, nullable=False)  # FK to clientes
    customer_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Service
    service_type: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    # Scheduling
    scheduled_start: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    scheduled_end: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    actual_start: Mapped[Optional[datetime]] = mapped_column(DateTime)
    actual_end: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    duration_minutes: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Resources
    assigned_resource_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("sched_resources.id"))
    assigned_resource_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Location
    location: Mapped[Optional[str]] = mapped_column(String(255))
    address: Mapped[Optional[str]] = mapped_column(Text)
    
    # Status
    status: Mapped[str] = mapped_column(String(30), default="scheduled")  # scheduled, confirmed, in_progress, completed, cancelled, no_show
    
    # Notes
    notes: Mapped[Optional[str]] = mapped_column(Text)
    completion_notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Reminder
    reminder_sent: Mapped[bool] = mapped_column(Boolean, default=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ServiceScheduleTemplate(Base):
    """Recurring service schedule template."""
    __tablename__ = "sched_templates"
    __table_args__ = (
        Index("idx_schedtpl_org_status", "organization_id", "status"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    template_name: Mapped[str] = mapped_column(String(255), nullable=False)
    service_type: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Recurrence
    frequency: Mapped[str] = mapped_column(String(20), default="weekly")  # daily, weekly, monthly, yearly
    frequency_interval: Mapped[int] = mapped_column(Integer, default=1)
    
    # Time
    day_of_week: Mapped[Optional[str]] = mapped_column(String(10))  # MON, TUE, etc
    time_of_day: Mapped[Optional[time]] = mapped_column(Time)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=60)
    
    # Resource preference
    preferred_resource_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("sched_resources.id"))
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default="active")
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ResourceAvailability(Base):
    """Resource availability/unavailability periods."""
    __tablename__ = "sched_availability"
    __table_args__ = (
        Index("idx_schedavail_org_resource", "organization_id", "resource_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    resource_id: Mapped[int] = mapped_column(Integer, ForeignKey("sched_resources.id"), nullable=False)

    availability_type: Mapped[str] = mapped_column(String(20), default="available")  # available, unavailable
    
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    
    start_time: Mapped[Optional[time]] = mapped_column(Time)
    end_time: Mapped[Optional[time]] = mapped_column(Time)
    
    reason: Mapped[Optional[str]] = mapped_column(String(255))
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
