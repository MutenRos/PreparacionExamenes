"""Project Operations routes."""

from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.core.auth import require_permission, get_tenant_db, get_org_id
from dario_app.modules.usuarios.models import Usuario

from .models import Project, ProjectTask, ResourceAssignment, TimesheetEntry, Expense, BillingEvent
from .service import ProjectOpsService

router = APIRouter(prefix="/api/project-ops", tags=["Project Operations"])
templates = Jinja2Templates(directory="/home/dario/src/dario_app/templates")


# Schemas

class ProjectCreate(BaseModel):
    project_code: str
    name: str
    customer_id: Optional[int] = None
    customer_name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget_amount: float = 0


class ProjectTaskCreate(BaseModel):
    name: str
    descripcion: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    planned_hours: float = 0


class AssignmentCreate(BaseModel):
    task_id: Optional[int] = None
    resource_id: int
    resource_name: Optional[str] = None
    role: Optional[str] = None
    bill_rate: float = 0
    cost_rate: float = 0
    capacity_hours: float = 0


class TimesheetCreate(BaseModel):
    task_id: Optional[int] = None
    resource_id: int
    resource_name: Optional[str] = None
    work_date: date
    hours: float
    notes: Optional[str] = None


class ExpenseCreate(BaseModel):
    task_id: Optional[int] = None
    resource_id: int
    resource_name: Optional[str] = None
    expense_date: date
    amount: float
    category: Optional[str] = None
    notes: Optional[str] = None


class ApprovalPayload(BaseModel):
    ids: List[int]


# Projects

@router.post("/projects")
async def create_project(
    payload: ProjectCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("project_ops.projects.create")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(Project).where(Project.organization_id == org_id, Project.project_code == payload.project_code)
    existing = await db.execute(stmt)
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Project code exists")
    project = Project(organization_id=org_id, **payload.model_dump())
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project


@router.get("/projects")
async def list_projects(
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("project_ops.projects.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(Project).where(Project.organization_id == org_id)
    if status:
        query = query.where(Project.status == status)
    result = await db.execute(query)
    return result.scalars().all()


# Tasks

@router.post("/projects/{project_id}/tasks")
async def create_task(
    project_id: int,
    payload: ProjectTaskCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("project_ops.tasks.create")),
    org_id: int = Depends(get_org_id),
):
    task = ProjectTask(organization_id=org_id, project_id=project_id, **payload.model_dump())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


@router.get("/projects/{project_id}/tasks")
async def list_tasks(
    project_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("project_ops.tasks.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(ProjectTask).where(ProjectTask.organization_id == org_id, ProjectTask.project_id == project_id)
    result = await db.execute(query)
    return result.scalars().all()


# Assignments

@router.post("/projects/{project_id}/assignments")
async def add_assignment(
    project_id: int,
    payload: AssignmentCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("project_ops.assignments.manage")),
    org_id: int = Depends(get_org_id),
):
    assignment = ResourceAssignment(organization_id=org_id, project_id=project_id, **payload.model_dump())
    db.add(assignment)
    await db.commit()
    await db.refresh(assignment)
    return assignment


@router.get("/projects/{project_id}/assignments")
async def list_assignments(
    project_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("project_ops.assignments.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(ResourceAssignment).where(ResourceAssignment.organization_id == org_id, ResourceAssignment.project_id == project_id)
    result = await db.execute(query)
    return result.scalars().all()


# Time & Expenses

@router.post("/projects/{project_id}/timesheets")
async def add_timesheet_entry(
    project_id: int,
    payload: TimesheetCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("project_ops.time.capture")),
    org_id: int = Depends(get_org_id),
):
    entry = TimesheetEntry(organization_id=org_id, project_id=project_id, **payload.model_dump())
    db.add(entry)
    await db.commit()
    await db.refresh(entry)
    return entry


@router.post("/projects/{project_id}/expenses")
async def add_expense(
    project_id: int,
    payload: ExpenseCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("project_ops.expenses.capture")),
    org_id: int = Depends(get_org_id),
):
    exp = Expense(organization_id=org_id, project_id=project_id, **payload.model_dump())
    db.add(exp)
    await db.commit()
    await db.refresh(exp)
    return exp


@router.post("/timesheets/approve")
async def approve_timesheets(
    payload: ApprovalPayload,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("project_ops.time.approve")),
    org_id: int = Depends(get_org_id),
):
    return await ProjectOpsService.approve_timesheets(db, org_id, payload.ids, user.id, user.nombre_completo)


@router.post("/expenses/approve")
async def approve_expenses(
    payload: ApprovalPayload,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("project_ops.expenses.approve")),
    org_id: int = Depends(get_org_id),
):
    return await ProjectOpsService.approve_expenses(db, org_id, payload.ids, user.id, user.nombre_completo)


@router.get("/projects/{project_id}/timesheets")
async def list_timesheets(
    project_id: int,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("project_ops.time.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(TimesheetEntry).where(TimesheetEntry.organization_id == org_id, TimesheetEntry.project_id == project_id)
    if status:
        query = query.where(TimesheetEntry.status == status)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/projects/{project_id}/expenses")
async def list_expenses(
    project_id: int,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("project_ops.expenses.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(Expense).where(Expense.organization_id == org_id, Expense.project_id == project_id)
    if status:
        query = query.where(Expense.status == status)
    result = await db.execute(query)
    return result.scalars().all()


# Billing events

@router.post("/projects/{project_id}/billing/generate")
async def generate_billing_events(
    project_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("project_ops.billing.generate")),
    org_id: int = Depends(get_org_id),
):
    events = await ProjectOpsService.generate_billing_events(db, org_id, project_id)
    return events


@router.get("/projects/{project_id}/billing")
async def list_billing_events(
    project_id: int,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("project_ops.billing.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(BillingEvent).where(BillingEvent.organization_id == org_id, BillingEvent.project_id == project_id)
    if status:
        query = query.where(BillingEvent.status == status)
    result = await db.execute(query)
    return result.scalars().all()


# Convert project to sales order

@router.post("/projects/{project_id}/convert-to-sale")
async def convert_project_to_sale(
    project_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("project_ops.convert_to_sale")),
    org_id: int = Depends(get_org_id),
):
    """Convert an approved/completed project into a sales order."""
    return await ProjectOpsService.convert_to_sale(db, org_id, project_id, user.id, user.nombre_completo)


# Printable project document
@router.get("/projects/{project_id}/print")
async def print_project(
    project_id: int,
    request: Request,
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id),
):
    """Render a printable HTML document for the project with tasks and assignments."""
    proj_stmt = select(Project).where(Project.organization_id == org_id, Project.id == project_id)
    res = await db.execute(proj_stmt)
    project = res.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    tasks_stmt = select(ProjectTask).where(ProjectTask.organization_id == org_id, ProjectTask.project_id == project_id)
    res_tasks = await db.execute(tasks_stmt)
    tasks = res_tasks.scalars().all()

    asg_stmt = select(ResourceAssignment).where(ResourceAssignment.organization_id == org_id, ResourceAssignment.project_id == project_id)
    res_asg = await db.execute(asg_stmt)
    assignments = res_asg.scalars().all()

    # Organization info (optional)
    org = None
    try:
        from dario_app.modules.tenants.models import Organization
        org_res = await db.execute(select(Organization).where(Organization.id == org_id))
        org = org_res.scalar_one_or_none()
    except Exception:
        org = None

    from datetime import datetime
    context = {
        "request": request,
        "project": project,
        "tasks": tasks,
        "assignments": assignments,
        "org": org,
        "now": datetime.now().strftime("%d/%m/%Y %H:%M"),
    }
    return templates.TemplateResponse("print/project.html", context)
