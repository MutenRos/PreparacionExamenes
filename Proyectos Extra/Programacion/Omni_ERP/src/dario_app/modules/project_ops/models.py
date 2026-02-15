"""Project Operations models."""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, Index
from sqlalchemy.orm import Mapped, mapped_column

from dario_app.database import Base


class Project(Base):
    __tablename__ = "proj_projects"
    __table_args__ = (
        Index("idx_proj_org_code", "organization_id", "project_code", unique=True),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    project_code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    customer_id: Mapped[Optional[int]] = mapped_column(Integer)
    customer_name: Mapped[Optional[str]] = mapped_column(String(255))
    start_date: Mapped[Optional[date]] = mapped_column(Date)
    end_date: Mapped[Optional[date]] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(30), default="draft")  # draft, active, completed, canceled
    manager_id: Mapped[Optional[int]] = mapped_column(Integer)
    manager_name: Mapped[Optional[str]] = mapped_column(String(255))
    budget_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=Decimal("0"))

    # Conversion tracking
    converted_to_sale_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    converted_to_sale_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ProjectTask(Base):
    __tablename__ = "proj_tasks"
    __table_args__ = (
        Index("idx_proj_task_org_proj", "organization_id", "project_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("proj_projects.id"), nullable=False)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    start_date: Mapped[Optional[date]] = mapped_column(Date)
    end_date: Mapped[Optional[date]] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(30), default="planned")  # planned, in_progress, done
    planned_hours: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0"))
    actual_hours: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0"))

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ResourceAssignment(Base):
    __tablename__ = "proj_assignments"
    __table_args__ = (
        Index("idx_proj_assign_org_proj", "organization_id", "project_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("proj_projects.id"), nullable=False)
    task_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("proj_tasks.id"))

    resource_id: Mapped[int] = mapped_column(Integer)
    resource_name: Mapped[Optional[str]] = mapped_column(String(255))
    role: Mapped[Optional[str]] = mapped_column(String(100))
    bill_rate: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0"))
    cost_rate: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0"))
    capacity_hours: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0"))

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class TimesheetEntry(Base):
    __tablename__ = "proj_timesheets"
    __table_args__ = (
        Index("idx_proj_ts_org_proj", "organization_id", "project_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("proj_projects.id"), nullable=False)
    task_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("proj_tasks.id"))

    resource_id: Mapped[int] = mapped_column(Integer)
    resource_name: Mapped[Optional[str]] = mapped_column(String(255))
    work_date: Mapped[date] = mapped_column(Date, nullable=False)
    hours: Mapped[Decimal] = mapped_column(Numeric(6, 2), nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(30), default="submitted")  # submitted, approved, rejected

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    approved_by_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    approved_by_user_name: Mapped[Optional[str]] = mapped_column(String(255))


class Expense(Base):
    __tablename__ = "proj_expenses"
    __table_args__ = (
        Index("idx_proj_exp_org_proj", "organization_id", "project_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("proj_projects.id"), nullable=False)
    task_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("proj_tasks.id"))

    resource_id: Mapped[int] = mapped_column(Integer)
    resource_name: Mapped[Optional[str]] = mapped_column(String(255))
    expense_date: Mapped[date] = mapped_column(Date, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    category: Mapped[Optional[str]] = mapped_column(String(100))
    notes: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(30), default="submitted")  # submitted, approved, rejected

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    approved_by_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    approved_by_user_name: Mapped[Optional[str]] = mapped_column(String(255))


class BillingEvent(Base):
    __tablename__ = "proj_billing_events"
    __table_args__ = (
        Index("idx_proj_bill_org_proj", "organization_id", "project_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("proj_projects.id"), nullable=False)

    event_type: Mapped[str] = mapped_column(String(50))  # milestone, time_and_materials, expense
    description: Mapped[Optional[str]] = mapped_column(Text)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    status: Mapped[str] = mapped_column(String(30), default="draft")  # draft, ready, invoiced

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    ready_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    invoiced_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
