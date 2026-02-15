"""Manufacturing Execution System Routes - Shop Floor API."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from dario_app.database import get_db
from dario_app.modules.manufacturing_execution import models
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/api/mes", tags=["manufacturing_execution"])


# Pydantic Schemas
class WorkOrderCreate(BaseModel):
    production_order_id: int
    work_order_number: str
    operation_sequence: int
    work_center_id: int
    quantity_planned: float
    standard_hours: Optional[float] = None


class EquipmentCreate(BaseModel):
    equipment_code: str
    equipment_name: str
    equipment_type: str
    manufacturer: Optional[str] = None
    model_number: Optional[str] = None


class QualityInspectionCreate(BaseModel):
    work_order_id: Optional[int] = None
    inspection_type: str
    sample_size: int
    accepted_count: int
    rejected_count: int


class ProductionEventCreate(BaseModel):
    work_order_id: int
    event_type: str
    event_description: Optional[str] = None
    production_count: Optional[int] = None
    operator_id: Optional[int] = None


# Work Order Endpoints
@router.post("/work-orders")
async def create_work_order(
    order: WorkOrderCreate,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Create a new work order."""
    db_order = models.ShopFloorWorkOrder(
        organization_id=organization_id,
        production_order_id=order.production_order_id,
        work_order_number=order.work_order_number,
        operation_sequence=order.operation_sequence,
        work_center_id=order.work_center_id,
        quantity_planned=order.quantity_planned,
        standard_hours=order.standard_hours,
    )
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    return {"id": db_order.id, "work_order_number": db_order.work_order_number, "status": "created"}


@router.get("/work-orders")
async def list_work_orders(
    organization_id: int = Query(...),
    status: Optional[str] = None,
    work_center_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """List work orders."""
    query = db.query(models.ShopFloorWorkOrder).filter(
        models.ShopFloorWorkOrder.organization_id == organization_id
    )
    
    if status:
        query = query.filter(models.ShopFloorWorkOrder.status == status)
    if work_center_id:
        query = query.filter(models.ShopFloorWorkOrder.work_center_id == work_center_id)
    
    orders = await query.all()
    return {"work_orders": orders, "total": len(orders)}


@router.get("/work-orders/{order_id}")
async def get_work_order(
    order_id: int,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific work order."""
    order = await db.query(models.ShopFloorWorkOrder).filter(
        models.ShopFloorWorkOrder.id == order_id,
        models.ShopFloorWorkOrder.organization_id == organization_id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Work order not found")
    
    return {
        "id": order.id,
        "work_order_number": order.work_order_number,
        "status": order.status,
        "quantity_planned": order.quantity_planned,
        "quantity_produced": order.quantity_produced,
        "progress": (order.quantity_produced or 0) / (order.quantity_planned or 1) * 100,
    }


@router.put("/work-orders/{order_id}/start")
async def start_work_order(
    order_id: int,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Start a work order."""
    order = await db.query(models.ShopFloorWorkOrder).filter(
        models.ShopFloorWorkOrder.id == order_id,
        models.ShopFloorWorkOrder.organization_id == organization_id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Work order not found")
    
    order.status = "in_progress"
    order.actual_start = datetime.utcnow()
    await db.commit()
    return {"id": order.id, "status": "in_progress"}


@router.put("/work-orders/{order_id}/complete")
async def complete_work_order(
    order_id: int,
    quantity_produced: float,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Complete a work order."""
    order = await db.query(models.ShopFloorWorkOrder).filter(
        models.ShopFloorWorkOrder.id == order_id,
        models.ShopFloorWorkOrder.organization_id == organization_id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Work order not found")
    
    order.status = "completed"
    order.quantity_produced = quantity_produced
    order.actual_end = datetime.utcnow()
    await db.commit()
    return {"id": order.id, "status": "completed", "quantity_produced": quantity_produced}


# Equipment Endpoints
@router.post("/equipment")
async def create_equipment(
    equipment: EquipmentCreate,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Register new equipment."""
    db_equipment = models.Equipment(
        organization_id=organization_id,
        equipment_code=equipment.equipment_code,
        equipment_name=equipment.equipment_name,
        equipment_type=equipment.equipment_type,
        manufacturer=equipment.manufacturer,
        model_number=equipment.model_number,
    )
    db.add(db_equipment)
    await db.commit()
    await db.refresh(db_equipment)
    return {"id": db_equipment.id, "equipment_code": db_equipment.equipment_code}


@router.get("/equipment")
async def list_equipment(
    organization_id: int = Query(...),
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List all equipment."""
    query = db.query(models.Equipment).filter(
        models.Equipment.organization_id == organization_id
    )
    
    if status:
        query = query.filter(models.Equipment.status == status)
    
    equipment_list = await query.all()
    return {"equipment": equipment_list, "total": len(equipment_list)}


@router.get("/equipment/{equipment_id}")
async def get_equipment(
    equipment_id: int,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Get equipment details."""
    equipment = await db.query(models.Equipment).filter(
        models.Equipment.id == equipment_id,
        models.Equipment.organization_id == organization_id
    ).first()
    
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    return {
        "id": equipment.id,
        "equipment_code": equipment.equipment_code,
        "equipment_name": equipment.equipment_name,
        "status": equipment.status,
        "total_runtime_hours": equipment.total_runtime_hours,
        "next_maintenance": equipment.next_maintenance,
    }


# Quality Inspection Endpoints
@router.post("/quality-inspections")
async def create_quality_inspection(
    inspection: QualityInspectionCreate,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Record quality inspection."""
    db_inspection = models.QualityInspection(
        organization_id=organization_id,
        work_order_id=inspection.work_order_id,
        inspection_type=inspection.inspection_type,
        sample_size=inspection.sample_size,
        accepted_count=inspection.accepted_count,
        rejected_count=inspection.rejected_count,
    )
    
    # Calculate acceptance rate
    total = inspection.accepted_count + inspection.rejected_count
    if total > 0:
        db_inspection.acceptance_rate = (inspection.accepted_count / total) * 100
    
    db.add(db_inspection)
    await db.commit()
    await db.refresh(db_inspection)
    return {"id": db_inspection.id, "acceptance_rate": db_inspection.acceptance_rate}


@router.get("/quality-inspections")
async def list_quality_inspections(
    organization_id: int = Query(...),
    inspection_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List quality inspections."""
    query = db.query(models.QualityInspection).filter(
        models.QualityInspection.organization_id == organization_id
    )
    
    if inspection_type:
        query = query.filter(models.QualityInspection.inspection_type == inspection_type)
    
    inspections = await query.all()
    return {"inspections": inspections, "total": len(inspections)}


# Production Events Endpoints
@router.post("/production-events")
async def log_production_event(
    event: ProductionEventCreate,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Log production event from shop floor."""
    db_event = models.ProductionEventLog(
        organization_id=organization_id,
        work_order_id=event.work_order_id,
        event_type=event.event_type,
        event_description=event.event_description,
        production_count=event.production_count,
        operator_id=event.operator_id,
    )
    db.add(db_event)
    await db.commit()
    await db.refresh(db_event)
    return {"id": db_event.id, "event_type": db_event.event_type, "recorded_at": db_event.recorded_at}


@router.get("/production-events")
async def get_production_events(
    organization_id: int = Query(...),
    work_order_id: Optional[int] = None,
    limit: int = Query(50, ge=1, le=500),
    db: AsyncSession = Depends(get_db)
):
    """Get production events."""
    query = db.query(models.ProductionEventLog).filter(
        models.ProductionEventLog.organization_id == organization_id
    )
    
    if work_order_id:
        query = query.filter(models.ProductionEventLog.work_order_id == work_order_id)
    
    events = await query.order_by(models.ProductionEventLog.recorded_at.desc()).limit(limit).all()
    return {"events": events, "total": len(events)}


# Maintenance Endpoints
@router.post("/maintenance")
async def schedule_maintenance(
    equipment_id: int,
    maintenance_type: str,
    scheduled_date: Optional[str] = None,
    description: Optional[str] = None,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Schedule equipment maintenance."""
    maintenance = models.MaintenanceRecord(
        organization_id=organization_id,
        equipment_id=equipment_id,
        maintenance_type=maintenance_type,
        description=description,
        scheduled_date=datetime.fromisoformat(scheduled_date) if scheduled_date else None,
    )
    db.add(maintenance)
    await db.commit()
    await db.refresh(maintenance)
    return {"id": maintenance.id, "status": "pending"}


@router.get("/maintenance")
async def get_maintenance_records(
    organization_id: int = Query(...),
    equipment_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get maintenance records."""
    query = db.query(models.MaintenanceRecord).filter(
        models.MaintenanceRecord.organization_id == organization_id
    )
    
    if equipment_id:
        query = query.filter(models.MaintenanceRecord.equipment_id == equipment_id)
    
    records = await query.all()
    return {"maintenance_records": records, "total": len(records)}


# Health Check
@router.get("/health")
async def health_check():
    """Check MES module health."""
    return {
        "status": "healthy",
        "module": "manufacturing_execution",
        "version": "1.0.0",
        "features": [
            "Shop Floor Work Orders",
            "Equipment Management",
            "Quality Control",
            "Production Events",
            "Maintenance Tracking",
            "Labor Tracking",
            "Scrap Tracking",
            "Material Consumption"
        ]
    }
