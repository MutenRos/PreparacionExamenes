"""Field Service routes: assets, work orders, tasks, schedules."""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.core.auth import require_permission, get_tenant_db, get_org_id
from dario_app.modules.usuarios.models import Usuario

from .models import ServiceAsset, WorkOrder, WorkOrderTask, WorkOrderSchedule
from .service import FieldServiceService

router = APIRouter(prefix="/api/field-service", tags=["Field Service"])


# ========= Schemas =========

class AssetCreate(BaseModel):
    asset_code: str
    asset_name: str
    asset_type: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    customer_id: Optional[int] = None
    customer_name: Optional[str] = None
    location_name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    installed_at: Optional[datetime] = None
    sla_hours: Optional[int] = None


class AssetResponse(BaseModel):
    id: int
    asset_code: str
    asset_name: str
    asset_type: Optional[str]
    model: Optional[str]
    serial_number: Optional[str]
    customer_name: Optional[str]
    location_name: Optional[str]
    status: str

    class Config:
        from_attributes = True


class WorkOrderCreate(BaseModel):
    title: str
    descripcion: Optional[str] = None
    asset_id: Optional[int] = None
    customer_id: Optional[int] = None
    customer_name: Optional[str] = None
    priority: str = "medium"
    scheduled_start: Optional[datetime] = None
    scheduled_end: Optional[datetime] = None
    sla_due: Optional[datetime] = None
    address: Optional[str] = None
    city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    assigned_to_user_id: Optional[int] = None
    assigned_to_name: Optional[str] = None


class WorkOrderResponse(BaseModel):
    id: int
    work_order_number: str
    title: str
    descripcion: Optional[str]
    status: str
    priority: str
    asset_code: Optional[str]
    asset_name: Optional[str]
    customer_name: Optional[str]
    scheduled_start: Optional[datetime]
    scheduled_end: Optional[datetime]
    sla_due: Optional[datetime]
    address: Optional[str]
    assigned_to_name: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    title: str
    descripcion: Optional[str] = None
    estimated_minutes: Optional[int] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    status: str
    estimated_minutes: Optional[int]
    actual_minutes: Optional[int]
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True


class ScheduleCreate(BaseModel):
    technician_id: Optional[int] = None
    technician_name: Optional[str] = None
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None


class ScheduleResponse(BaseModel):
    id: int
    technician_name: Optional[str]
    start_at: Optional[datetime]
    end_at: Optional[datetime]

    class Config:
        from_attributes = True


class StatusUpdate(BaseModel):
    status: str


# ========= Assets =========

@router.post("/assets", response_model=AssetResponse)
async def create_asset(
    asset_data: AssetCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("field_service.assets.create")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(ServiceAsset).where(
        ServiceAsset.organization_id == org_id,
        ServiceAsset.asset_code == asset_data.asset_code,
    )
    exists = await db.execute(stmt)
    if exists.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Asset code already exists")

    asset = ServiceAsset(organization_id=org_id, **asset_data.model_dump())
    db.add(asset)
    await db.commit()
    await db.refresh(asset)
    return asset


@router.get("/assets", response_model=List[AssetResponse])
async def list_assets(
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("field_service.assets.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(ServiceAsset).where(ServiceAsset.organization_id == org_id)
    if status:
        query = query.where(ServiceAsset.status == status)
    result = await db.execute(query)
    return result.scalars().all()


# ========= Work Orders =========

@router.post("/work-orders", response_model=WorkOrderResponse)
async def create_work_order(
    data: WorkOrderCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("field_service.workorders.create")),
    org_id: int = Depends(get_org_id),
):
    asset_code = None
    asset_name = None
    if data.asset_id:
        stmt = select(ServiceAsset).where(
            ServiceAsset.id == data.asset_id,
            ServiceAsset.organization_id == org_id,
        )
        result = await db.execute(stmt)
        asset = result.scalar_one_or_none()
        if asset:
            asset_code = asset.asset_code
            asset_name = asset.asset_name

    wo_number = FieldServiceService.generate_work_order_number(org_id)
    wo = WorkOrder(
        organization_id=org_id,
        work_order_number=wo_number,
        asset_id=data.asset_id,
        asset_code=asset_code,
        asset_name=asset_name,
        customer_id=data.customer_id,
        customer_name=data.customer_name,
        title=data.title,
        descripcion=data.descripcion,
        priority=data.priority,
        scheduled_start=data.scheduled_start,
        scheduled_end=data.scheduled_end,
        sla_due=data.sla_due,
        address=data.address,
        city=data.city,
        latitude=data.latitude,
        longitude=data.longitude,
        assigned_to_user_id=data.assigned_to_user_id,
        assigned_to_name=data.assigned_to_name,
        created_by_user_id=user.id,
        created_by_user_name=user.nombre_completo,
    )
    db.add(wo)
    await db.commit()
    await db.refresh(wo)
    return wo


@router.get("/work-orders", response_model=List[WorkOrderResponse])
async def list_work_orders(
    status: Optional[str] = Query(default=None),
    priority: Optional[str] = Query(default=None),
    limit: int = 50,
    skip: int = 0,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("field_service.workorders.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(WorkOrder).where(WorkOrder.organization_id == org_id)
    if status:
        query = query.where(WorkOrder.status == status)
    if priority:
        query = query.where(WorkOrder.priority == priority)
    query = query.order_by(WorkOrder.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/work-orders/{wo_id}", response_model=WorkOrderResponse)
async def get_work_order(
    wo_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("field_service.workorders.read")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(WorkOrder).where(
        WorkOrder.id == wo_id,
        WorkOrder.organization_id == org_id,
    )
    result = await db.execute(stmt)
    wo = result.scalar_one_or_none()
    if not wo:
        raise HTTPException(status_code=404, detail="Work order not found")
    return wo


@router.post("/work-orders/{wo_id}/status", response_model=WorkOrderResponse)
async def update_work_order_status(
    wo_id: int,
    payload: StatusUpdate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("field_service.workorders.update")),
    org_id: int = Depends(get_org_id),
):
    wo = await FieldServiceService.update_work_order_status(db, org_id, wo_id, payload.status)
    if not wo:
        raise HTTPException(status_code=404, detail="Work order not found")
    return wo


# ========= Tasks =========

@router.post("/work-orders/{wo_id}/tasks", response_model=TaskResponse)
async def add_task(
    wo_id: int,
    data: TaskCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("field_service.tasks.manage")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(WorkOrder).where(
        WorkOrder.id == wo_id,
        WorkOrder.organization_id == org_id,
    )
    exists = await db.execute(stmt)
    if not exists.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Work order not found")

    task = WorkOrderTask(
        organization_id=org_id,
        work_order_id=wo_id,
        title=data.title,
        descripcion=data.descripcion,
        estimated_minutes=data.estimated_minutes,
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


@router.get("/work-orders/{wo_id}/tasks", response_model=List[TaskResponse])
async def list_tasks(
    wo_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("field_service.tasks.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(WorkOrderTask).where(
        WorkOrderTask.work_order_id == wo_id,
        WorkOrderTask.organization_id == org_id,
    )
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/work-orders/{wo_id}/tasks/{task_id}/complete", response_model=TaskResponse)
async def complete_task(
    wo_id: int,
    task_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("field_service.tasks.manage")),
    org_id: int = Depends(get_org_id),
):
    task = await FieldServiceService.complete_task(db, org_id, task_id, user.id, user.nombre_completo)
    if not task or task.work_order_id != wo_id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# ========= Scheduling =========

@router.post("/work-orders/{wo_id}/schedule", response_model=ScheduleResponse)
async def add_schedule(
    wo_id: int,
    data: ScheduleCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("field_service.schedule.manage")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(WorkOrder).where(
        WorkOrder.id == wo_id,
        WorkOrder.organization_id == org_id,
    )
    exists = await db.execute(stmt)
    if not exists.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Work order not found")

    sched = WorkOrderSchedule(
        organization_id=org_id,
        work_order_id=wo_id,
        technician_id=data.technician_id,
        technician_name=data.technician_name,
        start_at=data.start_at,
        end_at=data.end_at,
    )
    db.add(sched)
    await db.commit()
    await db.refresh(sched)
    return sched


@router.get("/work-orders/{wo_id}/schedule", response_model=List[ScheduleResponse])
async def list_schedule(
    wo_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("field_service.schedule.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(WorkOrderSchedule).where(
        WorkOrderSchedule.work_order_id == wo_id,
        WorkOrderSchedule.organization_id == org_id,
    )
    result = await db.execute(query)
    return result.scalars().all()
