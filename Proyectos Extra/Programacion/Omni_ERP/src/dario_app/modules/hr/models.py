"""HR and Payroll models."""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from sqlalchemy import (
    Boolean,
    Date,
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


class Job(Base):
    __tablename__ = "hr_jobs"
    __table_args__ = (
        Index("idx_hr_job_org_code", "organization_id", "job_code", unique=True),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    job_code: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    department: Mapped[Optional[str]] = mapped_column(String(100))
    salary_min: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2))
    salary_max: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2))
    descripcion: Mapped[Optional[str]] = mapped_column(Text)

    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Position(Base):
    __tablename__ = "hr_positions"
    __table_args__ = (
        Index("idx_hr_pos_org_code", "organization_id", "position_code", unique=True),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    position_code: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    job_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("hr_jobs.id"))
    department: Mapped[Optional[str]] = mapped_column(String(100))
    location: Mapped[Optional[str]] = mapped_column(String(255))
    manager_position_id: Mapped[Optional[int]] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(30), default="open")  # open, filled, inactive

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Employee(Base):
    __tablename__ = "hr_employees"
    __table_args__ = (
        Index("idx_hr_emp_org_code", "organization_id", "employee_code", unique=True),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    employee_code: Mapped[str] = mapped_column(String(50), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(255))
    position_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("hr_positions.id"))
    manager_id: Mapped[Optional[int]] = mapped_column(Integer)

    start_date: Mapped[Optional[date]] = mapped_column(Date)
    end_date: Mapped[Optional[date]] = mapped_column(Date)

    salary: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2))
    hourly_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    employment_type: Mapped[Optional[str]] = mapped_column(String(50))  # full_time, part_time, contractor, temporary
    contract_type: Mapped[Optional[str]] = mapped_column(String(100))  # indefinido, temporal, obra_servicio, formativo, practicas
    status: Mapped[str] = mapped_column(String(30), default="active")

    # Seguridad Social fields
    ss_number: Mapped[Optional[str]] = mapped_column(String(50))  # Número de afiliación
    ss_status: Mapped[Optional[str]] = mapped_column(String(30))  # alta, baja, suspension
    ss_alta_date: Mapped[Optional[date]] = mapped_column(Date)  # Fecha de alta en SS
    ss_baja_date: Mapped[Optional[date]] = mapped_column(Date)  # Fecha de baja en SS
    ss_notes: Mapped[Optional[str]] = mapped_column(Text)  # Notas sobre trámites

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class LeaveRequest(Base):
    __tablename__ = "hr_leave_requests"
    __table_args__ = (
        Index("idx_hr_leave_org_emp", "organization_id", "employee_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    employee_id: Mapped[int] = mapped_column(Integer, ForeignKey("hr_employees.id"), nullable=False)

    leave_type: Mapped[str] = mapped_column(String(50), nullable=False)  # vacation, sick, unpaid
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="pending")  # pending, approved, rejected
    reason: Mapped[Optional[str]] = mapped_column(Text)

    approved_by_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    approved_by_user_name: Mapped[Optional[str]] = mapped_column(String(255))
    approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Timesheet(Base):
    __tablename__ = "hr_timesheets"
    __table_args__ = (
        Index("idx_hr_ts_org_emp", "organization_id", "employee_id", "period_start", "period_end"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    employee_id: Mapped[int] = mapped_column(Integer, ForeignKey("hr_employees.id"), nullable=False)

    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="draft")  # draft, submitted, approved, rejected
    submitted_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    approved_by_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    approved_by_user_name: Mapped[Optional[str]] = mapped_column(String(255))

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class TimesheetLine(Base):
    __tablename__ = "hr_timesheet_lines"
    __table_args__ = (
        Index("idx_hr_tsline_org_ts", "organization_id", "timesheet_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    timesheet_id: Mapped[int] = mapped_column(Integer, ForeignKey("hr_timesheets.id"), nullable=False)

    work_date: Mapped[date] = mapped_column(Date, nullable=False)
    project: Mapped[Optional[str]] = mapped_column(String(100))
    task: Mapped[Optional[str]] = mapped_column(String(255))
    hours: Mapped[Decimal] = mapped_column(Numeric(6, 2), nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class PayrollRun(Base):
    __tablename__ = "hr_payroll_runs"
    __table_args__ = (
        Index("idx_hr_payroll_org_period", "organization_id", "period_start", "period_end"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)

    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="open")  # open, calculated, posted
    total_gross: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=Decimal("0"))
    total_net: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=Decimal("0"))

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    posted_at: Mapped[Optional[datetime]] = mapped_column(DateTime)


class PayrollLine(Base):
    __tablename__ = "hr_payroll_lines"
    __table_args__ = (
        Index("idx_hr_payline_org_run", "organization_id", "payroll_run_id"),
        {"extend_existing": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    payroll_run_id: Mapped[int] = mapped_column(Integer, ForeignKey("hr_payroll_runs.id"), nullable=False)
    employee_id: Mapped[int] = mapped_column(Integer, ForeignKey("hr_employees.id"), nullable=False)

    gross_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=Decimal("0"))
    tax_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=Decimal("0"))
    net_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=Decimal("0"))
    status: Mapped[str] = mapped_column(String(30), default="calculated")

    notes: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
