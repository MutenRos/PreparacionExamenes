"""Transportation Management System routes."""

from datetime import datetime, date, timedelta
from typing import Optional
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.core.auth import require_permission, get_tenant_db, get_org_id
from dario_app.modules.usuarios.models import Usuario

from .models import (
    Carrier, TransportRoute, FreightOrder, LoadPlan, LoadPlanItem,
    RateQuote, TransportEvent
)

router = APIRouter(prefix="/api/transportation", tags=["Transportation Management"])


# Schemas

class CarrierCreate(BaseModel):
    name: str
    carrier_type: str = "ground"
    contact_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    base_rate: Decimal = Decimal("0")


class RouteCreate(BaseModel):
    name: str
    origin: str
    destination: str
    distance_km: Decimal
    estimated_duration_hours: Decimal
    preferred_carrier_id: Optional[int] = None


class FreightOrderCreate(BaseModel):
    origin_address: str
    destination_address: str
    carrier_id: int
    service_type: str = "standard"
    scheduled_pickup_date: str
    scheduled_delivery_date: str
    total_weight_kg: Decimal
    total_volume_m3: Decimal = Decimal("0")
    package_count: int = 1


class LoadPlanCreate(BaseModel):
    vehicle_id: Optional[int] = None
    driver_id: Optional[int] = None
    max_weight_kg: Decimal
    max_volume_m3: Decimal
    planned_date: str


class RateQuoteCreate(BaseModel):
    carrier_id: int
    origin: str
    destination: str
    service_type: str = "standard"
    weight_kg: Decimal
    volume_m3: Optional[Decimal] = None
    valid_days: int = 30


# Carriers

@router.post("/carriers")
async def create_carrier(
    payload: CarrierCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("transportation.carriers.create")),
    org_id: int = Depends(get_org_id),
):
    # Generate carrier code
    stmt = select(Carrier).where(Carrier.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    carrier_code = f"CAR-{count + 1:04d}"
    
    carrier = Carrier(
        organization_id=org_id,
        carrier_code=carrier_code,
        **payload.model_dump()
    )
    db.add(carrier)
    await db.commit()
    await db.refresh(carrier)
    return carrier


@router.get("/carriers")
async def list_carriers(
    status: Optional[str] = None,
    carrier_type: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("transportation.carriers.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(Carrier).where(Carrier.organization_id == org_id)
    if status:
        query = query.where(Carrier.status == status)
    if carrier_type:
        query = query.where(Carrier.carrier_type == carrier_type)
    result = await db.execute(query)
    return result.scalars().all()


# Routes

@router.post("/routes")
async def create_route(
    payload: RouteCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("transportation.routes.create")),
    org_id: int = Depends(get_org_id),
):
    # Generate route code
    stmt = select(TransportRoute).where(TransportRoute.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    route_code = f"RTE-{count + 1:04d}"
    
    route = TransportRoute(
        organization_id=org_id,
        route_code=route_code,
        **payload.model_dump()
    )
    db.add(route)
    await db.commit()
    await db.refresh(route)
    return route


@router.get("/routes")
async def list_routes(
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("transportation.routes.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(TransportRoute).where(TransportRoute.organization_id == org_id)
    if status:
        query = query.where(TransportRoute.status == status)
    result = await db.execute(query)
    return result.scalars().all()


# Freight Orders

@router.post("/freight-orders")
async def create_freight_order(
    payload: FreightOrderCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("transportation.freight.create")),
    org_id: int = Depends(get_org_id),
):
    # Generate freight number
    now = datetime.now()
    stmt = select(FreightOrder).where(FreightOrder.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    freight_number = f"FRT-{now.strftime('%Y%m')}-{count + 1:05d}"
    
    freight = FreightOrder(
        organization_id=org_id,
        freight_number=freight_number,
        **payload.model_dump()
    )
    db.add(freight)
    await db.commit()
    await db.refresh(freight)
    return freight


@router.get("/freight-orders")
async def list_freight_orders(
    status: Optional[str] = None,
    carrier_id: Optional[int] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("transportation.freight.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(FreightOrder).where(FreightOrder.organization_id == org_id)
    if status:
        query = query.where(FreightOrder.status == status)
    if carrier_id:
        query = query.where(FreightOrder.carrier_id == carrier_id)
    query = query.order_by(FreightOrder.scheduled_pickup_date.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/freight-orders/{freight_id}/dispatch")
async def dispatch_freight_order(
    freight_id: int,
    tracking_number: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("transportation.freight.manage")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(FreightOrder).where(
        FreightOrder.id == freight_id,
        FreightOrder.organization_id == org_id
    )
    result = await db.execute(stmt)
    freight = result.scalar_one_or_none()
    
    if not freight:
        raise HTTPException(status_code=404, detail="Freight order not found")
    
    freight.status = "in_transit"
    freight.actual_pickup_date = date.today()
    if tracking_number:
        freight.tracking_number = tracking_number
    
    # Create tracking event
    event = TransportEvent(
        organization_id=org_id,
        freight_order_id=freight_id,
        event_type="pickup",
        event_date=datetime.utcnow(),
        location=freight.origin_address[:255],
        description="Package picked up by carrier",
        recorded_by=user.nombre_completo
    )
    db.add(event)
    
    await db.commit()
    await db.refresh(freight)
    return freight


@router.patch("/freight-orders/{freight_id}/deliver")
async def deliver_freight_order(
    freight_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("transportation.freight.manage")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(FreightOrder).where(
        FreightOrder.id == freight_id,
        FreightOrder.organization_id == org_id
    )
    result = await db.execute(stmt)
    freight = result.scalar_one_or_none()
    
    if not freight:
        raise HTTPException(status_code=404, detail="Freight order not found")
    
    freight.status = "delivered"
    freight.actual_delivery_date = date.today()
    
    # Create tracking event
    event = TransportEvent(
        organization_id=org_id,
        freight_order_id=freight_id,
        event_type="delivery",
        event_date=datetime.utcnow(),
        location=freight.destination_address[:255],
        description="Package delivered successfully",
        recorded_by=user.nombre_completo
    )
    db.add(event)
    
    await db.commit()
    await db.refresh(freight)
    return freight


# Load Planning

@router.post("/load-plans")
async def create_load_plan(
    payload: LoadPlanCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("transportation.load_planning.create")),
    org_id: int = Depends(get_org_id),
):
    # Generate load number
    now = datetime.now()
    stmt = select(LoadPlan).where(LoadPlan.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    load_number = f"LOAD-{now.strftime('%Y%m')}-{count + 1:05d}"
    
    load_plan = LoadPlan(
        organization_id=org_id,
        load_number=load_number,
        **payload.model_dump()
    )
    db.add(load_plan)
    await db.commit()
    await db.refresh(load_plan)
    return load_plan


@router.get("/load-plans")
async def list_load_plans(
    status: Optional[str] = None,
    planned_date: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("transportation.load_planning.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(LoadPlan).where(LoadPlan.organization_id == org_id)
    if status:
        query = query.where(LoadPlan.status == status)
    if planned_date:
        query = query.where(LoadPlan.planned_date == planned_date)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/load-plans/{load_id}/items")
async def add_freight_to_load(
    load_id: int,
    freight_order_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("transportation.load_planning.manage")),
    org_id: int = Depends(get_org_id),
):
    # Get load plan
    load_stmt = select(LoadPlan).where(
        LoadPlan.id == load_id,
        LoadPlan.organization_id == org_id
    )
    load_result = await db.execute(load_stmt)
    load_plan = load_result.scalar_one_or_none()
    
    if not load_plan:
        raise HTTPException(status_code=404, detail="Load plan not found")
    
    # Get freight order
    freight_stmt = select(FreightOrder).where(
        FreightOrder.id == freight_order_id,
        FreightOrder.organization_id == org_id
    )
    freight_result = await db.execute(freight_stmt)
    freight = freight_result.scalar_one_or_none()
    
    if not freight:
        raise HTTPException(status_code=404, detail="Freight order not found")
    
    # Check capacity
    new_weight = load_plan.current_weight_kg + freight.total_weight_kg
    new_volume = load_plan.current_volume_m3 + freight.total_volume_m3
    
    if new_weight > load_plan.max_weight_kg:
        raise HTTPException(status_code=400, detail="Exceeds weight capacity")
    if new_volume > load_plan.max_volume_m3:
        raise HTTPException(status_code=400, detail="Exceeds volume capacity")
    
    # Get next sequence
    items_stmt = select(LoadPlanItem).where(LoadPlanItem.load_plan_id == load_id)
    items_result = await db.execute(items_stmt)
    items = items_result.scalars().all()
    sequence = len(items) + 1
    
    # Add item
    item = LoadPlanItem(
        organization_id=org_id,
        load_plan_id=load_id,
        freight_order_id=freight_order_id,
        sequence=sequence,
        weight_kg=freight.total_weight_kg,
        volume_m3=freight.total_volume_m3
    )
    db.add(item)
    
    # Update load plan
    load_plan.current_weight_kg = new_weight
    load_plan.current_volume_m3 = new_volume
    load_plan.weight_utilization = (new_weight / load_plan.max_weight_kg * 100) if load_plan.max_weight_kg > 0 else Decimal("0")
    load_plan.volume_utilization = (new_volume / load_plan.max_volume_m3 * 100) if load_plan.max_volume_m3 > 0 else Decimal("0")
    
    await db.commit()
    await db.refresh(item)
    return item


# Rate Quotes

@router.post("/rate-quotes")
async def request_rate_quote(
    payload: RateQuoteCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("transportation.quotes.create")),
    org_id: int = Depends(get_org_id),
):
    # Generate quote number
    now = datetime.now()
    stmt = select(RateQuote).where(RateQuote.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    quote_number = f"RQ-{now.strftime('%Y%m')}-{count + 1:05d}"
    
    # Get carrier
    carrier_stmt = select(Carrier).where(
        Carrier.id == payload.carrier_id,
        Carrier.organization_id == org_id
    )
    carrier_result = await db.execute(carrier_stmt)
    carrier = carrier_result.scalar_one_or_none()
    
    if not carrier:
        raise HTTPException(status_code=404, detail="Carrier not found")
    
    # Calculate quote (simple formula)
    base_rate = carrier.base_rate
    weight_charge = payload.weight_kg * carrier.per_kg_rate
    fuel_surcharge = (base_rate + weight_charge) * Decimal("0.15")  # 15% fuel surcharge
    total_quote = base_rate + weight_charge + fuel_surcharge
    
    quote = RateQuote(
        organization_id=org_id,
        quote_number=quote_number,
        carrier_id=payload.carrier_id,
        origin=payload.origin,
        destination=payload.destination,
        service_type=payload.service_type,
        weight_kg=payload.weight_kg,
        volume_m3=payload.volume_m3,
        quoted_rate=base_rate + weight_charge,
        fuel_surcharge=fuel_surcharge,
        total_quote=total_quote,
        quote_date=date.today(),
        valid_until=date.today() + timedelta(days=payload.valid_days)
    )
    db.add(quote)
    await db.commit()
    await db.refresh(quote)
    return quote


@router.get("/rate-quotes")
async def list_rate_quotes(
    carrier_id: Optional[int] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("transportation.quotes.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(RateQuote).where(RateQuote.organization_id == org_id)
    if carrier_id:
        query = query.where(RateQuote.carrier_id == carrier_id)
    if status:
        query = query.where(RateQuote.status == status)
    query = query.order_by(RateQuote.quote_date.desc())
    result = await db.execute(query)
    return result.scalars().all()


# Tracking

@router.post("/events")
async def create_transport_event(
    freight_order_id: int,
    event_type: str,
    location: str,
    description: str,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("transportation.tracking.manage")),
    org_id: int = Depends(get_org_id),
):
    event = TransportEvent(
        organization_id=org_id,
        freight_order_id=freight_order_id,
        event_type=event_type,
        event_date=datetime.utcnow(),
        location=location,
        description=description,
        recorded_by=user.nombre_completo
    )
    db.add(event)
    await db.commit()
    await db.refresh(event)
    return event


@router.get("/freight-orders/{freight_id}/tracking")
async def get_freight_tracking(
    freight_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("transportation.tracking.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(TransportEvent).where(
        TransportEvent.organization_id == org_id,
        TransportEvent.freight_order_id == freight_id
    ).order_by(TransportEvent.event_date)
    result = await db.execute(query)
    return result.scalars().all()


# Analytics

@router.get("/analytics/carrier-performance")
async def get_carrier_performance(
    days: int = 30,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("transportation.analytics.read")),
    org_id: int = Depends(get_org_id),
):
    """Calculate carrier performance metrics."""
    cutoff_date = date.today() - timedelta(days=days)
    
    # Get delivered orders
    stmt = select(FreightOrder).where(
        FreightOrder.organization_id == org_id,
        FreightOrder.status == "delivered",
        FreightOrder.actual_delivery_date >= cutoff_date
    )
    result = await db.execute(stmt)
    orders = result.scalars().all()
    
    # Group by carrier
    carrier_stats = {}
    for order in orders:
        carrier_id = order.carrier_id
        if carrier_id not in carrier_stats:
            carrier_stats[carrier_id] = {
                "total_shipments": 0,
                "on_time": 0,
                "late": 0,
                "total_cost": Decimal("0")
            }
        
        carrier_stats[carrier_id]["total_shipments"] += 1
        carrier_stats[carrier_id]["total_cost"] += order.total_cost
        
        if order.actual_delivery_date and order.scheduled_delivery_date:
            if order.actual_delivery_date <= order.scheduled_delivery_date:
                carrier_stats[carrier_id]["on_time"] += 1
            else:
                carrier_stats[carrier_id]["late"] += 1
    
    # Calculate percentages
    for carrier_id, stats in carrier_stats.items():
        total = stats["total_shipments"]
        stats["on_time_rate"] = (stats["on_time"] / total * 100) if total > 0 else 0
        stats["avg_cost"] = float(stats["total_cost"] / total) if total > 0 else 0
    
    return carrier_stats
