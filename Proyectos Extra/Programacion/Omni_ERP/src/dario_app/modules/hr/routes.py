"""HR and Payroll routes."""

from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.core.auth import require_permission, get_tenant_db, get_org_id
from dario_app.modules.usuarios.models import Usuario

from .models import (
    Job,
    Position,
    Employee,
    LeaveRequest,
    Timesheet,
    TimesheetLine,
    PayrollRun,
    PayrollLine,
)
from .service import HRService

router = APIRouter(prefix="/api/hr", tags=["HR & Payroll"])


# ===== Schemas =====

class JobCreate(BaseModel):
    job_code: str
    title: str
    department: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    descripcion: Optional[str] = None


class PositionCreate(BaseModel):
    position_code: str
    title: str
    job_id: Optional[int] = None
    department: Optional[str] = None
    location: Optional[str] = None
    manager_position_id: Optional[int] = None


class EmployeeCreate(BaseModel):
    employee_code: str
    first_name: str
    last_name: str
    email: Optional[str] = None
    position_id: Optional[int] = None
    manager_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    salary: Optional[float] = None
    hourly_rate: Optional[float] = None
    employment_type: Optional[str] = None
    contract_type: Optional[str] = None
    ss_number: Optional[str] = None
    ss_status: Optional[str] = None
    ss_alta_date: Optional[date] = None
    ss_baja_date: Optional[date] = None
    ss_notes: Optional[str] = None


class LeaveCreate(BaseModel):
    employee_id: int
    leave_type: str
    start_date: date
    end_date: date
    reason: Optional[str] = None


class LeaveApproval(BaseModel):
    status: str


class TimesheetCreate(BaseModel):
    employee_id: int
    period_start: date
    period_end: date


class TimesheetLineCreate(BaseModel):
    work_date: date
    project: Optional[str] = None
    task: Optional[str] = None
    hours: float
    notes: Optional[str] = None


class PayrollRunCreate(BaseModel):
    period_start: date
    period_end: date


# ===== Jobs =====

@router.post("/jobs")
async def create_job(
    payload: JobCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("hr.jobs.create")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(Job).where(Job.organization_id == org_id, Job.job_code == payload.job_code)
    existing = await db.execute(stmt)
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Job code already exists")
    job = Job(organization_id=org_id, **payload.model_dump())
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job


@router.get("/jobs")
async def list_jobs(
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("hr.jobs.read")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(Job).where(Job.organization_id == org_id)
    result = await db.execute(stmt)
    return result.scalars().all()


# ===== Positions =====

@router.post("/positions")
async def create_position(
    payload: PositionCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("hr.positions.create")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(Position).where(Position.organization_id == org_id, Position.position_code == payload.position_code)
    existing = await db.execute(stmt)
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Position code already exists")
    pos = Position(organization_id=org_id, **payload.model_dump())
    db.add(pos)
    await db.commit()
    await db.refresh(pos)
    return pos


@router.get("/positions")
async def list_positions(
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("hr.positions.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(Position).where(Position.organization_id == org_id)
    if status:
        query = query.where(Position.status == status)
    result = await db.execute(query)
    return result.scalars().all()


# ===== Employees =====

@router.post("/employees")
async def create_employee(
    payload: EmployeeCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("hr.employees.create")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(Employee).where(Employee.organization_id == org_id, Employee.employee_code == payload.employee_code)
    existing = await db.execute(stmt)
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Employee code exists")
    emp = Employee(organization_id=org_id, **payload.model_dump())
    db.add(emp)
    await db.commit()
    await db.refresh(emp)
    return emp


@router.get("/employees")
async def list_employees(
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("hr.employees.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(Employee).where(Employee.organization_id == org_id)
    if status:
        query = query.where(Employee.status == status)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/employees/{emp_id}")
async def get_employee(
    emp_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("hr.employees.read")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(Employee).where(Employee.id == emp_id, Employee.organization_id == org_id)
    result = await db.execute(stmt)
    emp = result.scalar_one_or_none()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp


class SSUpdate(BaseModel):
    ss_status: str  # alta, baja
    ss_number: Optional[str] = None
    ss_date: Optional[date] = None
    ss_notes: Optional[str] = None


@router.post("/employees/{emp_id}/ss")
async def update_ss_status(
    emp_id: int,
    payload: SSUpdate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("hr.employees.manage")),
    org_id: int = Depends(get_org_id),
):
    """Actualiza estado de Seguridad Social (alta/baja)."""
    stmt = select(Employee).where(Employee.id == emp_id, Employee.organization_id == org_id)
    result = await db.execute(stmt)
    emp = result.scalar_one_or_none()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    emp.ss_status = payload.ss_status
    if payload.ss_number:
        emp.ss_number = payload.ss_number
    if payload.ss_notes:
        emp.ss_notes = payload.ss_notes
    
    if payload.ss_status == "alta":
        emp.ss_alta_date = payload.ss_date or date.today()
        emp.ss_baja_date = None
    elif payload.ss_status == "baja":
        emp.ss_baja_date = payload.ss_date or date.today()
    
    await db.commit()
    await db.refresh(emp)
    return emp


# ===== Leave =====

@router.post("/leave")
async def request_leave(
    payload: LeaveCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("hr.leave.create")),
    org_id: int = Depends(get_org_id),
):
    leave = LeaveRequest(organization_id=org_id, **payload.model_dump())
    db.add(leave)
    await db.commit()
    await db.refresh(leave)
    return leave


@router.post("/leave/{leave_id}/approve")
async def approve_leave(
    leave_id: int,
    payload: LeaveApproval,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("hr.leave.approve")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(LeaveRequest).where(LeaveRequest.id == leave_id, LeaveRequest.organization_id == org_id)
    result = await db.execute(stmt)
    leave = result.scalar_one_or_none()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")
    leave.status = payload.status
    leave.approved_by_user_id = user.id
    leave.approved_by_user_name = user.nombre_completo
    leave.approved_at = leave.approved_at or leave.created_at
    await db.commit()
    await db.refresh(leave)
    return leave


@router.get("/leave")
async def list_leave(
    status: Optional[str] = None,
    employee_id: Optional[int] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("hr.leave.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(LeaveRequest).where(LeaveRequest.organization_id == org_id)
    if status:
        query = query.where(LeaveRequest.status == status)
    if employee_id:
        query = query.where(LeaveRequest.employee_id == employee_id)
    result = await db.execute(query)
    return result.scalars().all()


# ===== Timesheets =====

@router.post("/timesheets")
async def create_timesheet(
    payload: TimesheetCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("hr.timesheets.create")),
    org_id: int = Depends(get_org_id),
):
    ts = Timesheet(organization_id=org_id, **payload.model_dump())
    db.add(ts)
    await db.commit()
    await db.refresh(ts)
    return ts


@router.post("/timesheets/{ts_id}/submit")
async def submit_timesheet(
    ts_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("hr.timesheets.submit")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(Timesheet).where(Timesheet.id == ts_id, Timesheet.organization_id == org_id)
    result = await db.execute(stmt)
    ts = result.scalar_one_or_none()
    if not ts:
        raise HTTPException(status_code=404, detail="Timesheet not found")
    ts.status = "submitted"
    ts.submitted_at = ts.submitted_at or ts.created_at
    await db.commit()
    await db.refresh(ts)
    return ts


@router.post("/timesheets/{ts_id}/approve")
async def approve_timesheet(
    ts_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("hr.timesheets.approve")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(Timesheet).where(Timesheet.id == ts_id, Timesheet.organization_id == org_id)
    result = await db.execute(stmt)
    ts = result.scalar_one_or_none()
    if not ts:
        raise HTTPException(status_code=404, detail="Timesheet not found")
    ts.status = "approved"
    ts.approved_at = ts.approved_at or ts.submitted_at
    ts.approved_by_user_id = user.id
    ts.approved_by_user_name = user.nombre_completo
    await db.commit()
    await db.refresh(ts)
    return ts


@router.post("/timesheets/{ts_id}/lines")
async def add_timesheet_line(
    ts_id: int,
    payload: TimesheetLineCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("hr.timesheets.manage")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(Timesheet).where(Timesheet.id == ts_id, Timesheet.organization_id == org_id)
    exists = await db.execute(stmt)
    if not exists.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Timesheet not found")
    line = TimesheetLine(organization_id=org_id, timesheet_id=ts_id, **payload.model_dump())
    db.add(line)
    await db.commit()
    await db.refresh(line)
    return line


@router.get("/timesheets/{ts_id}/lines")
async def list_timesheet_lines(
    ts_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("hr.timesheets.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(TimesheetLine).where(TimesheetLine.organization_id == org_id, TimesheetLine.timesheet_id == ts_id)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/timesheets")
async def list_timesheets(
    status: Optional[str] = None,
    employee_id: Optional[int] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("hr.timesheets.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(Timesheet).where(Timesheet.organization_id == org_id)
    if status:
        query = query.where(Timesheet.status == status)
    if employee_id:
        query = query.where(Timesheet.employee_id == employee_id)
    result = await db.execute(query)
    return result.scalars().all()


# ===== Payroll =====

@router.post("/payroll/runs")
async def create_payroll_run(
    payload: PayrollRunCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("hr.payroll.create")),
    org_id: int = Depends(get_org_id),
):
    run = PayrollRun(organization_id=org_id, **payload.model_dump())
    db.add(run)
    await db.commit()
    await db.refresh(run)
    return run


@router.post("/payroll/runs/{run_id}/calculate")
async def calculate_payroll(
    run_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("hr.payroll.calculate")),
    org_id: int = Depends(get_org_id),
):
    try:
        run = await HRService.calculate_payroll(db, org_id, run_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return run


@router.post("/payroll/runs/{run_id}/post")
async def post_payroll(
    run_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("hr.payroll.post")),
    org_id: int = Depends(get_org_id),
):
    try:
        run = await HRService.post_payroll(db, org_id, run_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return run


@router.get("/payroll/runs")
async def list_payroll_runs(
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("hr.payroll.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(PayrollRun).where(PayrollRun.organization_id == org_id)
    if status:
        query = query.where(PayrollRun.status == status)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/payroll/runs/{run_id}/lines")
async def list_payroll_lines(
    run_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("hr.payroll.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(PayrollLine).where(PayrollLine.organization_id == org_id, PayrollLine.payroll_run_id == run_id)
    result = await db.execute(query)
    return result.scalars().all()
