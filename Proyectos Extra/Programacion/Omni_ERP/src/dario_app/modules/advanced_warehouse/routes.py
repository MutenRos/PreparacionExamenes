"""Advanced Warehouse Management System routes."""

from datetime import datetime, date
from typing import Optional
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.core.auth import require_permission, get_tenant_db, get_org_id
from dario_app.modules.usuarios.models import Usuario

from .models import (
    WarehouseZone, WarehouseBin, Wave, PickTask, PackTask,
    CycleCount, Replenishment, PutawayTask
)

router = APIRouter(prefix="/api/wms", tags=["Advanced Warehouse Management"])


# Schemas

class ZoneCreate(BaseModel):
    warehouse_id: int
    name: str
    zone_type: str = "storage"
    temperature_controlled: bool = False
    hazmat_approved: bool = False


class BinCreate(BaseModel):
    zone_id: int
    aisle: Optional[str] = None
    rack: Optional[str] = None
    shelf: Optional[str] = None
    bin: Optional[str] = None
    max_weight_kg: Decimal = Decimal("1000")
    max_volume_m3: Decimal = Decimal("10")


class WaveCreate(BaseModel):
    warehouse_id: int
    wave_type: str = "batch"
    zone_id: Optional[int] = None
    planned_date: str
    priority: int = 5


class CycleCountCreate(BaseModel):
    count_type: str = "spot"
    warehouse_id: int
    zone_id: Optional[int] = None
    bin_id: Optional[int] = None
    product_id: Optional[int] = None
    expected_quantity: int = 0
    scheduled_date: str


# Warehouse Zones

@router.post("/zones")
async def create_zone(
    payload: ZoneCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("wms.zones.create")),
    org_id: int = Depends(get_org_id),
):
    # Generate zone code
    stmt = select(WarehouseZone).where(
        WarehouseZone.organization_id == org_id,
        WarehouseZone.warehouse_id == payload.warehouse_id
    )
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    zone_code = f"Z{payload.warehouse_id:03d}-{count + 1:02d}"
    
    zone = WarehouseZone(
        organization_id=org_id,
        zone_code=zone_code,
        **payload.model_dump()
    )
    db.add(zone)
    await db.commit()
    await db.refresh(zone)
    return zone


@router.get("/zones")
async def list_zones(
    warehouse_id: Optional[int] = None,
    zone_type: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("wms.zones.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(WarehouseZone).where(WarehouseZone.organization_id == org_id)
    if warehouse_id:
        query = query.where(WarehouseZone.warehouse_id == warehouse_id)
    if zone_type:
        query = query.where(WarehouseZone.zone_type == zone_type)
    result = await db.execute(query)
    return result.scalars().all()


# Storage Bins

@router.post("/bins")
async def create_bin(
    payload: BinCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("wms.bins.create")),
    org_id: int = Depends(get_org_id),
):
    # Generate bin code
    stmt = select(WarehouseBin).where(
        WarehouseBin.organization_id == org_id,
        WarehouseBin.zone_id == payload.zone_id
    )
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    
    # Build bin code from location
    if payload.aisle and payload.rack and payload.shelf and payload.bin:
        bin_code = f"{payload.aisle}-{payload.rack}-{payload.shelf}-{payload.bin}"
    else:
        bin_code = f"BIN-{count + 1:04d}"
    
    bin = WarehouseBin(
        organization_id=org_id,
        bin_code=bin_code,
        **payload.model_dump()
    )
    db.add(bin)
    await db.commit()
    await db.refresh(bin)
    return bin


@router.get("/bins")
async def list_bins(
    zone_id: Optional[int] = None,
    is_available: Optional[bool] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("wms.bins.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(WarehouseBin).where(WarehouseBin.organization_id == org_id)
    if zone_id:
        query = query.where(WarehouseBin.zone_id == zone_id)
    if is_available is not None:
        query = query.where(WarehouseBin.is_available == is_available)
    result = await db.execute(query)
    return result.scalars().all()


# Wave Picking

@router.post("/waves")
async def create_wave(
    payload: WaveCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("wms.waves.create")),
    org_id: int = Depends(get_org_id),
):
    # Generate wave number
    now = datetime.now()
    stmt = select(Wave).where(Wave.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    wave_number = f"WAVE-{now.strftime('%Y%m%d')}-{count + 1:03d}"
    
    wave = Wave(
        organization_id=org_id,
        wave_number=wave_number,
        **payload.model_dump()
    )
    db.add(wave)
    await db.commit()
    await db.refresh(wave)
    return wave


@router.get("/waves")
async def list_waves(
    status: Optional[str] = None,
    warehouse_id: Optional[int] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("wms.waves.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(Wave).where(Wave.organization_id == org_id)
    if status:
        query = query.where(Wave.status == status)
    if warehouse_id:
        query = query.where(Wave.warehouse_id == warehouse_id)
    query = query.order_by(Wave.planned_date.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/waves/{wave_id}/release")
async def release_wave(
    wave_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("wms.waves.manage")),
    org_id: int = Depends(get_org_id),
):
    """Release wave for picking."""
    stmt = select(Wave).where(
        Wave.id == wave_id,
        Wave.organization_id == org_id
    )
    result = await db.execute(stmt)
    wave = result.scalar_one_or_none()
    
    if not wave:
        raise HTTPException(status_code=404, detail="Wave not found")
    
    wave.status = "released"
    wave.released_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(wave)
    return wave


@router.patch("/waves/{wave_id}/complete")
async def complete_wave(
    wave_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("wms.waves.manage")),
    org_id: int = Depends(get_org_id),
):
    """Complete wave picking."""
    stmt = select(Wave).where(
        Wave.id == wave_id,
        Wave.organization_id == org_id
    )
    result = await db.execute(stmt)
    wave = result.scalar_one_or_none()
    
    if not wave:
        raise HTTPException(status_code=404, detail="Wave not found")
    
    wave.status = "completed"
    wave.completed_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(wave)
    return wave


# Pick Tasks

@router.get("/pick-tasks")
async def list_pick_tasks(
    wave_id: Optional[int] = None,
    status: Optional[str] = None,
    assigned_user_id: Optional[int] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("wms.picking.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(PickTask).where(PickTask.organization_id == org_id)
    if wave_id:
        query = query.where(PickTask.wave_id == wave_id)
    if status:
        query = query.where(PickTask.status == status)
    if assigned_user_id:
        query = query.where(PickTask.assigned_user_id == assigned_user_id)
    query = query.order_by(PickTask.sequence)
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/pick-tasks/{task_id}/complete")
async def complete_pick_task(
    task_id: int,
    quantity_picked: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("wms.picking.manage")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(PickTask).where(
        PickTask.id == task_id,
        PickTask.organization_id == org_id
    )
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="Pick task not found")
    
    task.quantity_picked = quantity_picked
    task.status = "completed" if quantity_picked >= task.quantity_requested else "short_picked"
    task.completed_at = datetime.utcnow()
    
    # Update wave progress
    if task.wave_id:
        wave_stmt = select(Wave).where(Wave.id == task.wave_id)
        wave_result = await db.execute(wave_stmt)
        wave = wave_result.scalar_one_or_none()
        if wave:
            wave.picked_lines += 1
            wave.picked_quantity += quantity_picked
    
    await db.commit()
    await db.refresh(task)
    return task


# Pack Tasks

@router.get("/pack-tasks")
async def list_pack_tasks(
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("wms.packing.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(PackTask).where(PackTask.organization_id == org_id)
    if status:
        query = query.where(PackTask.status == status)
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/pack-tasks/{task_id}/complete")
async def complete_pack_task(
    task_id: int,
    tracking_number: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("wms.packing.manage")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(PackTask).where(
        PackTask.id == task_id,
        PackTask.organization_id == org_id
    )
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="Pack task not found")
    
    task.status = "completed"
    task.completed_at = datetime.utcnow()
    if tracking_number:
        task.tracking_number = tracking_number
    
    await db.commit()
    await db.refresh(task)
    return task


# Cycle Counting

@router.post("/cycle-counts")
async def create_cycle_count(
    payload: CycleCountCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("wms.cycle_count.create")),
    org_id: int = Depends(get_org_id),
):
    # Generate count number
    now = datetime.now()
    stmt = select(CycleCount).where(CycleCount.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    count_number = f"CC-{now.strftime('%Y%m')}-{count + 1:05d}"
    
    cycle_count = CycleCount(
        organization_id=org_id,
        count_number=count_number,
        **payload.model_dump()
    )
    db.add(cycle_count)
    await db.commit()
    await db.refresh(cycle_count)
    return cycle_count


@router.get("/cycle-counts")
async def list_cycle_counts(
    status: Optional[str] = None,
    warehouse_id: Optional[int] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("wms.cycle_count.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(CycleCount).where(CycleCount.organization_id == org_id)
    if status:
        query = query.where(CycleCount.status == status)
    if warehouse_id:
        query = query.where(CycleCount.warehouse_id == warehouse_id)
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/cycle-counts/{count_id}/record")
async def record_count(
    count_id: int,
    counted_quantity: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("wms.cycle_count.manage")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(CycleCount).where(
        CycleCount.id == count_id,
        CycleCount.organization_id == org_id
    )
    result = await db.execute(stmt)
    count = result.scalar_one_or_none()
    
    if not count:
        raise HTTPException(status_code=404, detail="Cycle count not found")
    
    count.counted_quantity = counted_quantity
    count.variance = counted_quantity - count.expected_quantity
    count.counted_at = datetime.utcnow()
    count.counted_by_id = user.id
    count.counted_by_name = user.nombre_completo
    count.status = "variance_review" if count.variance != 0 else "completed"
    
    await db.commit()
    await db.refresh(count)
    return count


# Replenishment

@router.get("/replenishments")
async def list_replenishments(
    status: Optional[str] = None,
    product_id: Optional[int] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("wms.replenishment.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(Replenishment).where(Replenishment.organization_id == org_id)
    if status:
        query = query.where(Replenishment.status == status)
    if product_id:
        query = query.where(Replenishment.product_id == product_id)
    query = query.order_by(Replenishment.priority.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/replenishments/{repl_id}/complete")
async def complete_replenishment(
    repl_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("wms.replenishment.manage")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(Replenishment).where(
        Replenishment.id == repl_id,
        Replenishment.organization_id == org_id
    )
    result = await db.execute(stmt)
    repl = result.scalar_one_or_none()
    
    if not repl:
        raise HTTPException(status_code=404, detail="Replenishment not found")
    
    repl.status = "completed"
    repl.completed_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(repl)
    return repl


# Putaway

@router.get("/putaway-tasks")
async def list_putaway_tasks(
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("wms.putaway.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(PutawayTask).where(PutawayTask.organization_id == org_id)
    if status:
        query = query.where(PutawayTask.status == status)
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/putaway-tasks/{task_id}/complete")
async def complete_putaway_task(
    task_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("wms.putaway.manage")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(PutawayTask).where(
        PutawayTask.id == task_id,
        PutawayTask.organization_id == org_id
    )
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="Putaway task not found")
    
    task.status = "completed"
    task.completed_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(task)
    return task
