"""Asset Management routes - Assets, Maintenance, Rentals."""

from datetime import datetime, date
from typing import List, Optional
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.core.auth import require_permission, get_tenant_db, get_org_id
from dario_app.modules.usuarios.models import Usuario

from .models import Asset, MaintenanceSchedule, MaintenanceOrder, RentalAgreement, AssetTransfer, AssetMeter

router = APIRouter(prefix="/api/asset-management", tags=["Asset Management"])


# Schemas

class AssetCreate(BaseModel):
    name: str
    descripcion: Optional[str] = None
    category: str
    acquisition_date: Optional[str] = None
    acquisition_cost: float = 0
    manufacturer: Optional[str] = None
    model_number: Optional[str] = None
    serial_number: Optional[str] = None
    is_rentable: bool = False
    daily_rental_rate: float = 0


class MaintenanceScheduleCreate(BaseModel):
    asset_id: int
    name: str
    descripcion: Optional[str] = None
    frequency_interval_days: Optional[int] = None
    estimated_duration_hours: Optional[int] = None
    estimated_cost: float = 0


class MaintenanceOrderCreate(BaseModel):
    asset_id: int
    maintenance_type: str = "preventive"
    priority: str = "medium"
    scheduled_date: Optional[str] = None
    description: str


class RentalAgreementCreate(BaseModel):
    asset_id: int
    customer_name: str
    customer_id: Optional[int] = None
    start_date: str
    end_date: str
    billing_frequency: str = "daily"
    rental_rate: float
    security_deposit: float = 0


class AssetTransferCreate(BaseModel):
    asset_id: int
    transfer_type: str = "location"
    from_location: Optional[str] = None
    to_location: Optional[str] = None
    transfer_date: str
    reason: Optional[str] = None


class MeterReadingCreate(BaseModel):
    asset_id: int
    meter_type: str
    reading_value: float
    reading_date: Optional[str] = None
    notes: Optional[str] = None


# Assets

@router.post("/assets")
async def create_asset(
    payload: AssetCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("asset_management.assets.create")),
    org_id: int = Depends(get_org_id),
):
    # Generate asset code
    stmt = select(Asset).where(Asset.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    asset_code = f"ASSET-{count + 1:05d}"
    
    asset = Asset(
        organization_id=org_id,
        asset_code=asset_code,
        current_value=Decimal(str(payload.acquisition_cost)),
        **payload.model_dump()
    )
    db.add(asset)
    await db.commit()
    await db.refresh(asset)
    return asset


@router.get("/assets")
async def list_assets(
    status: Optional[str] = None,
    category: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("asset_management.assets.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(Asset).where(Asset.organization_id == org_id)
    if status:
        query = query.where(Asset.status == status)
    if category:
        query = query.where(Asset.category == category)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/assets/{asset_id}")
async def get_asset(
    asset_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("asset_management.assets.read")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(Asset).where(Asset.id == asset_id, Asset.organization_id == org_id)
    result = await db.execute(stmt)
    asset = result.scalar_one_or_none()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@router.patch("/assets/{asset_id}/status")
async def update_asset_status(
    asset_id: int,
    status: str,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("asset_management.assets.manage")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(Asset).where(Asset.id == asset_id, Asset.organization_id == org_id)
    result = await db.execute(stmt)
    asset = result.scalar_one_or_none()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    asset.status = status
    await db.commit()
    await db.refresh(asset)
    return asset


# Maintenance Schedules

@router.post("/maintenance-schedules")
async def create_maintenance_schedule(
    payload: MaintenanceScheduleCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("asset_management.maintenance.create")),
    org_id: int = Depends(get_org_id),
):
    # Generate schedule code
    stmt = select(MaintenanceSchedule).where(MaintenanceSchedule.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    schedule_code = f"MSCH-{count + 1:04d}"
    
    schedule = MaintenanceSchedule(
        organization_id=org_id,
        schedule_code=schedule_code,
        **payload.model_dump()
    )
    db.add(schedule)
    await db.commit()
    await db.refresh(schedule)
    return schedule


@router.get("/maintenance-schedules")
async def list_maintenance_schedules(
    asset_id: Optional[int] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("asset_management.maintenance.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(MaintenanceSchedule).where(MaintenanceSchedule.organization_id == org_id)
    if asset_id:
        query = query.where(MaintenanceSchedule.asset_id == asset_id)
    if status:
        query = query.where(MaintenanceSchedule.status == status)
    result = await db.execute(query)
    return result.scalars().all()


# Maintenance Orders

@router.post("/maintenance-orders")
async def create_maintenance_order(
    payload: MaintenanceOrderCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("asset_management.maintenance.create")),
    org_id: int = Depends(get_org_id),
):
    # Generate order number
    stmt = select(MaintenanceOrder).where(MaintenanceOrder.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    order_number = f"MO-{datetime.now().strftime('%Y%m')}-{count + 1:04d}"
    
    order = MaintenanceOrder(
        organization_id=org_id,
        order_number=order_number,
        **payload.model_dump()
    )
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order


@router.get("/maintenance-orders")
async def list_maintenance_orders(
    asset_id: Optional[int] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("asset_management.maintenance.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(MaintenanceOrder).where(MaintenanceOrder.organization_id == org_id)
    if asset_id:
        query = query.where(MaintenanceOrder.asset_id == asset_id)
    if status:
        query = query.where(MaintenanceOrder.status == status)
    if priority:
        query = query.where(MaintenanceOrder.priority == priority)
    query = query.order_by(MaintenanceOrder.scheduled_date.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/maintenance-orders/{order_id}/start")
async def start_maintenance(
    order_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("asset_management.maintenance.execute")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(MaintenanceOrder).where(
        MaintenanceOrder.id == order_id,
        MaintenanceOrder.organization_id == org_id
    )
    result = await db.execute(stmt)
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Maintenance order not found")
    
    order.status = "in_progress"
    order.started_at = datetime.utcnow()
    
    # Update asset status
    asset_stmt = select(Asset).where(Asset.id == order.asset_id, Asset.organization_id == org_id)
    asset_result = await db.execute(asset_stmt)
    asset = asset_result.scalar_one_or_none()
    if asset:
        asset.status = "maintenance"
    
    await db.commit()
    await db.refresh(order)
    return order


@router.patch("/maintenance-orders/{order_id}/complete")
async def complete_maintenance(
    order_id: int,
    work_performed: str,
    actual_duration_hours: Optional[int] = None,
    actual_cost: float = 0,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("asset_management.maintenance.execute")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(MaintenanceOrder).where(
        MaintenanceOrder.id == order_id,
        MaintenanceOrder.organization_id == org_id
    )
    result = await db.execute(stmt)
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Maintenance order not found")
    
    order.status = "completed"
    order.completed_at = datetime.utcnow()
    order.work_performed = work_performed
    order.actual_duration_hours = actual_duration_hours
    order.actual_cost = Decimal(str(actual_cost))
    
    # Update asset
    asset_stmt = select(Asset).where(Asset.id == order.asset_id, Asset.organization_id == org_id)
    asset_result = await db.execute(asset_stmt)
    asset = asset_result.scalar_one_or_none()
    if asset:
        asset.status = "available"
        asset.last_maintenance_date = date.today()
    
    await db.commit()
    await db.refresh(order)
    return order


# Rental Agreements

@router.post("/rental-agreements")
async def create_rental_agreement(
    payload: RentalAgreementCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("asset_management.rentals.create")),
    org_id: int = Depends(get_org_id),
):
    # Generate agreement number
    stmt = select(RentalAgreement).where(RentalAgreement.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    agreement_number = f"RENT-{datetime.now().strftime('%Y%m')}-{count + 1:04d}"
    
    agreement = RentalAgreement(
        organization_id=org_id,
        agreement_number=agreement_number,
        **payload.model_dump()
    )
    db.add(agreement)
    
    # Update asset status
    asset_stmt = select(Asset).where(Asset.id == payload.asset_id, Asset.organization_id == org_id)
    asset_result = await db.execute(asset_stmt)
    asset = asset_result.scalar_one_or_none()
    if asset:
        asset.status = "in_use"
    
    await db.commit()
    await db.refresh(agreement)
    return agreement


@router.get("/rental-agreements")
async def list_rental_agreements(
    asset_id: Optional[int] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("asset_management.rentals.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(RentalAgreement).where(RentalAgreement.organization_id == org_id)
    if asset_id:
        query = query.where(RentalAgreement.asset_id == asset_id)
    if status:
        query = query.where(RentalAgreement.status == status)
    query = query.order_by(RentalAgreement.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/rental-agreements/{agreement_id}/return")
async def return_rental(
    agreement_id: int,
    return_date: str,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("asset_management.rentals.manage")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(RentalAgreement).where(
        RentalAgreement.id == agreement_id,
        RentalAgreement.organization_id == org_id
    )
    result = await db.execute(stmt)
    agreement = result.scalar_one_or_none()
    if not agreement:
        raise HTTPException(status_code=404, detail="Rental agreement not found")
    
    agreement.status = "completed"
    agreement.actual_return_date = datetime.strptime(return_date, "%Y-%m-%d").date()
    
    # Update asset status
    asset_stmt = select(Asset).where(Asset.id == agreement.asset_id, Asset.organization_id == org_id)
    asset_result = await db.execute(asset_stmt)
    asset = asset_result.scalar_one_or_none()
    if asset:
        asset.status = "available"
    
    await db.commit()
    await db.refresh(agreement)
    return agreement


# Asset Transfers

@router.post("/asset-transfers")
async def create_asset_transfer(
    payload: AssetTransferCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("asset_management.assets.transfer")),
    org_id: int = Depends(get_org_id),
):
    # Generate transfer number
    stmt = select(AssetTransfer).where(AssetTransfer.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    transfer_number = f"TRF-{datetime.now().strftime('%Y%m')}-{count + 1:04d}"
    
    transfer = AssetTransfer(
        organization_id=org_id,
        transfer_number=transfer_number,
        **payload.model_dump()
    )
    db.add(transfer)
    
    # Update asset location
    if payload.to_location:
        asset_stmt = select(Asset).where(Asset.id == payload.asset_id, Asset.organization_id == org_id)
        asset_result = await db.execute(asset_stmt)
        asset = asset_result.scalar_one_or_none()
        if asset:
            asset.current_location = payload.to_location
    
    await db.commit()
    await db.refresh(transfer)
    return transfer


@router.get("/asset-transfers")
async def list_asset_transfers(
    asset_id: Optional[int] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("asset_management.assets.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(AssetTransfer).where(AssetTransfer.organization_id == org_id)
    if asset_id:
        query = query.where(AssetTransfer.asset_id == asset_id)
    query = query.order_by(AssetTransfer.transfer_date.desc())
    result = await db.execute(query)
    return result.scalars().all()


# Meter Readings

@router.post("/meter-readings")
async def create_meter_reading(
    payload: MeterReadingCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("asset_management.assets.read")),
    org_id: int = Depends(get_org_id),
):
    reading_date = datetime.strptime(payload.reading_date, "%Y-%m-%d %H:%M:%S") if payload.reading_date else datetime.utcnow()
    
    meter = AssetMeter(
        organization_id=org_id,
        recorded_by_user_id=user.id,
        recorded_by_name=user.nombre_completo,
        reading_date=reading_date,
        **payload.model_dump(exclude={"reading_date"})
    )
    db.add(meter)
    await db.commit()
    await db.refresh(meter)
    return meter


@router.get("/meter-readings")
async def list_meter_readings(
    asset_id: Optional[int] = None,
    meter_type: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("asset_management.assets.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(AssetMeter).where(AssetMeter.organization_id == org_id)
    if asset_id:
        query = query.where(AssetMeter.asset_id == asset_id)
    if meter_type:
        query = query.where(AssetMeter.meter_type == meter_type)
    query = query.order_by(AssetMeter.reading_date.desc())
    result = await db.execute(query)
    return result.scalars().all()
