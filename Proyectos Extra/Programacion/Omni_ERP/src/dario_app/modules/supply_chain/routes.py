"""Supply Chain API routes - MRP, Reorder Policies, Landed Cost."""

from datetime import datetime
from typing import List, Optional
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.core.auth import require_permission, get_tenant_db, get_org_id
from dario_app.modules.usuarios.models import Usuario
from .models import (
    ReorderPolicy, MRPRun, MRPRequirement, LandedCostHeader,
    LandedCostLine, LandedCostAllocation, InventoryLocation, InventoryByLocation
)
from .service import SupplyChainService


router = APIRouter(prefix="/api/supply-chain", tags=["Supply Chain"])


# ========== REORDER POLICY SCHEMAS ==========

class ReorderPolicyCreate(BaseModel):
    producto_id: int
    policy_type: str = "reorder_point"
    min_quantity: Decimal = Decimal("0")
    max_quantity: Decimal = Decimal("0")
    reorder_point: Decimal = Decimal("0")
    reorder_quantity: Decimal = Decimal("0")
    safety_stock: Decimal = Decimal("0")
    lead_time_days: int = 0
    annual_demand: Optional[Decimal] = None
    holding_cost_percent: Optional[Decimal] = None
    ordering_cost: Optional[Decimal] = None
    auto_reorder_enabled: bool = False
    preferred_supplier_id: Optional[int] = None


class ReorderPolicyResponse(BaseModel):
    id: int
    producto_id: int
    producto_codigo: Optional[str]
    producto_nombre: Optional[str]
    policy_type: str
    reorder_point: Decimal
    reorder_quantity: Decimal
    safety_stock: Decimal
    auto_reorder_enabled: bool
    
    class Config:
        from_attributes = True


class EOQCalculateRequest(BaseModel):
    annual_demand: Decimal
    ordering_cost: Decimal
    holding_cost_percent: Decimal
    unit_cost: Decimal


# ========== MRP SCHEMAS ==========

class MRPRunRequest(BaseModel):
    horizon_days: int = Field(90, ge=1, le=365)


class MRPRunResponse(BaseModel):
    id: int
    run_date: datetime
    horizon_days: int
    status: str
    total_requirements: int
    duration_seconds: Optional[int]
    
    class Config:
        from_attributes = True


class MRPRequirementResponse(BaseModel):
    id: int
    producto_codigo: Optional[str]
    producto_nombre: Optional[str]
    required_quantity: Decimal
    required_date: datetime
    available_quantity: Decimal
    suggested_action: str
    order_quantity: Optional[Decimal]
    
    class Config:
        from_attributes = True


# ========== LANDED COST SCHEMAS ==========

class LandedCostCreate(BaseModel):
    compra_id: int
    shipment_reference: Optional[str] = None
    shipment_date: Optional[datetime] = None
    notas: Optional[str] = None


class LandedCostLineCreate(BaseModel):
    cost_type: str
    descripcion: str
    cost_amount: Decimal
    allocation_method: str = "by_value"
    proveedor_id: Optional[int] = None
    invoice_number: Optional[str] = None


class LandedCostResponse(BaseModel):
    id: int
    compra_id: int
    compra_numero: Optional[str]
    merchandise_value: Decimal
    total_landed_costs: Decimal
    total_value: Decimal
    status: str
    
    class Config:
        from_attributes = True


# ========== INVENTORY LOCATION SCHEMAS ==========

class LocationCreate(BaseModel):
    location_code: str
    location_name: str
    location_type: str = "warehouse"
    address: Optional[str] = None
    city: Optional[str] = None


class LocationResponse(BaseModel):
    id: int
    location_code: str
    location_name: str
    location_type: str
    activo: bool
    
    class Config:
        from_attributes = True


# ========== REORDER POLICY ENDPOINTS ==========

@router.post("/reorder-policies", response_model=ReorderPolicyResponse)
async def create_reorder_policy(
    policy_data: ReorderPolicyCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("supply_chain.policies.create")),
    org_id: int = Depends(get_org_id)
):
    """Create a reorder policy for a product."""
    from dario_app.modules.inventario.models import Producto
    
    # Verify product exists
    stmt = select(Producto).where(
        Producto.id == policy_data.producto_id,
        Producto.organization_id == org_id
    )
    result = await db.execute(stmt)
    producto = result.scalar_one_or_none()
    
    if not producto:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if policy already exists
    stmt_existing = select(ReorderPolicy).where(
        ReorderPolicy.organization_id == org_id,
        ReorderPolicy.producto_id == policy_data.producto_id
    )
    result_existing = await db.execute(stmt_existing)
    existing = result_existing.scalar_one_or_none()
    
    if existing:
        raise HTTPException(status_code=400, detail="Reorder policy already exists for this product")
    
    # Get supplier name if provided
    supplier_name = None
    if policy_data.preferred_supplier_id:
        from dario_app.modules.inventario.models import Proveedor
        stmt_sup = select(Proveedor).where(Proveedor.id == policy_data.preferred_supplier_id)
        result_sup = await db.execute(stmt_sup)
        supplier = result_sup.scalar_one_or_none()
        if supplier:
            supplier_name = supplier.nombre
    
    policy = ReorderPolicy(
        organization_id=org_id,
        producto_codigo=producto.codigo,
        producto_nombre=producto.nombre,
        preferred_supplier_name=supplier_name,
        **policy_data.model_dump()
    )
    
    db.add(policy)
    await db.commit()
    await db.refresh(policy)
    
    return policy


@router.get("/reorder-policies", response_model=List[ReorderPolicyResponse])
async def list_reorder_policies(
    activo: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("supply_chain.policies.read")),
    org_id: int = Depends(get_org_id)
):
    """List reorder policies."""
    query = select(ReorderPolicy).where(ReorderPolicy.organization_id == org_id)
    
    if activo is not None:
        query = query.where(ReorderPolicy.activo == activo)
    
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/reorder-policies/{policy_id}", response_model=ReorderPolicyResponse)
async def get_reorder_policy(
    policy_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("supply_chain.policies.read")),
    org_id: int = Depends(get_org_id)
):
    """Get a specific reorder policy."""
    stmt = select(ReorderPolicy).where(
        ReorderPolicy.id == policy_id,
        ReorderPolicy.organization_id == org_id
    )
    result = await db.execute(stmt)
    policy = result.scalar_one_or_none()
    
    if not policy:
        raise HTTPException(status_code=404, detail="Reorder policy not found")
    
    return policy


@router.post("/eoq/calculate")
async def calculate_eoq(
    request: EOQCalculateRequest,
    user: Usuario = Depends(require_permission("supply_chain.calculate"))
):
    """Calculate Economic Order Quantity (EOQ)."""
    result = await SupplyChainService.calculate_eoq(
        request.annual_demand,
        request.ordering_cost,
        request.holding_cost_percent,
        request.unit_cost
    )
    return result


@router.get("/reorder-check")
async def check_reorder_needs(
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("supply_chain.policies.read")),
    org_id: int = Depends(get_org_id)
):
    """Check all products for reorder needs."""
    
    # Get all active policies
    stmt = select(ReorderPolicy).where(
        ReorderPolicy.organization_id == org_id,
        ReorderPolicy.activo == True
    )
    result = await db.execute(stmt)
    policies = result.scalars().all()
    
    reorder_needed = []
    
    for policy in policies:
        check_result = await SupplyChainService.check_reorder_needed(
            db, org_id, policy.producto_id
        )
        if check_result:
            reorder_needed.append(check_result)
    
    return {
        "total_policies": len(policies),
        "reorder_needed_count": len(reorder_needed),
        "reorder_items": reorder_needed
    }


# ========== MRP ENDPOINTS ==========

@router.post("/mrp/run", response_model=MRPRunResponse)
async def run_mrp(
    request: MRPRunRequest,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("supply_chain.mrp.run")),
    org_id: int = Depends(get_org_id)
):
    """Run MRP calculation."""
    mrp_run = await SupplyChainService.run_mrp(
        db, org_id, request.horizon_days, user.id, user.nombre_completo
    )
    return mrp_run


@router.get("/mrp/runs", response_model=List[MRPRunResponse])
async def list_mrp_runs(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("supply_chain.mrp.read")),
    org_id: int = Depends(get_org_id)
):
    """List MRP runs."""
    query = select(MRPRun).where(MRPRun.organization_id == org_id)
    
    if status:
        query = query.where(MRPRun.status == status)
    
    query = query.order_by(MRPRun.run_date.desc()).offset(skip).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/mrp/runs/{run_id}/requirements", response_model=List[MRPRequirementResponse])
async def get_mrp_requirements(
    run_id: int,
    suggested_action: Optional[str] = None,
    skip: int = 0,
    limit: int = 200,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("supply_chain.mrp.read")),
    org_id: int = Depends(get_org_id)
):
    """Get requirements from an MRP run."""
    query = select(MRPRequirement).where(
        MRPRequirement.mrp_run_id == run_id,
        MRPRequirement.organization_id == org_id
    )
    
    if suggested_action:
        query = query.where(MRPRequirement.suggested_action == suggested_action)
    
    query = query.order_by(MRPRequirement.required_date).offset(skip).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()


# ========== LANDED COST ENDPOINTS ==========

@router.post("/landed-costs", response_model=LandedCostResponse)
async def create_landed_cost(
    lc_data: LandedCostCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("supply_chain.landed_cost.create")),
    org_id: int = Depends(get_org_id)
):
    """Create a landed cost calculation for a purchase order."""
    from dario_app.modules.compras.models import Compra
    
    # Verify purchase order exists
    stmt = select(Compra).where(
        Compra.id == lc_data.compra_id,
        Compra.organization_id == org_id
    )
    result = await db.execute(stmt)
    compra = result.scalar_one_or_none()
    
    if not compra:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    
    landed_cost = LandedCostHeader(
        organization_id=org_id,
        compra_numero=compra.numero_compra,
        **lc_data.model_dump()
    )
    
    db.add(landed_cost)
    await db.commit()
    await db.refresh(landed_cost)
    
    return landed_cost


@router.post("/landed-costs/{lc_id}/lines")
async def add_landed_cost_line(
    lc_id: int,
    line_data: LandedCostLineCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("supply_chain.landed_cost.create")),
    org_id: int = Depends(get_org_id)
):
    """Add a cost line to landed cost."""
    
    # Verify header exists
    stmt = select(LandedCostHeader).where(
        LandedCostHeader.id == lc_id,
        LandedCostHeader.organization_id == org_id
    )
    result = await db.execute(stmt)
    header = result.scalar_one_or_none()
    
    if not header:
        raise HTTPException(status_code=404, detail="Landed cost not found")
    
    if header.status != "draft":
        raise HTTPException(status_code=400, detail="Cannot add lines to non-draft landed cost")
    
    # Get supplier name if provided
    supplier_name = None
    if line_data.proveedor_id:
        from dario_app.modules.inventario.models import Proveedor
        stmt_sup = select(Proveedor).where(Proveedor.id == line_data.proveedor_id)
        result_sup = await db.execute(stmt_sup)
        supplier = result_sup.scalar_one_or_none()
        if supplier:
            supplier_name = supplier.nombre
    
    line = LandedCostLine(
        organization_id=org_id,
        landed_cost_header_id=lc_id,
        proveedor_nombre=supplier_name,
        **line_data.model_dump()
    )
    
    db.add(line)
    await db.commit()
    await db.refresh(line)
    
    return line


@router.post("/landed-costs/{lc_id}/calculate", response_model=LandedCostResponse)
async def calculate_landed_cost(
    lc_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("supply_chain.landed_cost.calculate")),
    org_id: int = Depends(get_org_id)
):
    """Calculate landed cost allocations."""
    result = await SupplyChainService.calculate_landed_cost(db, org_id, lc_id)
    return result


@router.post("/landed-costs/{lc_id}/apply", response_model=LandedCostResponse)
async def apply_landed_cost(
    lc_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("supply_chain.landed_cost.apply")),
    org_id: int = Depends(get_org_id)
):
    """Apply landed costs to product inventory costs."""
    result = await SupplyChainService.apply_landed_cost(
        db, org_id, lc_id, user.id, user.nombre_completo
    )
    return result


@router.get("/landed-costs", response_model=List[LandedCostResponse])
async def list_landed_costs(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("supply_chain.landed_cost.read")),
    org_id: int = Depends(get_org_id)
):
    """List landed cost calculations."""
    query = select(LandedCostHeader).where(LandedCostHeader.organization_id == org_id)
    
    if status:
        query = query.where(LandedCostHeader.status == status)
    
    query = query.order_by(LandedCostHeader.created_at.desc()).offset(skip).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/landed-costs/{lc_id}/allocations")
async def get_landed_cost_allocations(
    lc_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("supply_chain.landed_cost.read")),
    org_id: int = Depends(get_org_id)
):
    """Get allocated costs for a landed cost calculation."""
    stmt = select(LandedCostAllocation).where(
        LandedCostAllocation.landed_cost_header_id == lc_id,
        LandedCostAllocation.organization_id == org_id
    )
    result = await db.execute(stmt)
    return result.scalars().all()


# ========== INVENTORY LOCATION ENDPOINTS ==========

@router.post("/locations", response_model=LocationResponse)
async def create_location(
    location_data: LocationCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("supply_chain.locations.create")),
    org_id: int = Depends(get_org_id)
):
    """Create an inventory location."""
    
    # Check if code already exists
    stmt = select(InventoryLocation).where(
        InventoryLocation.organization_id == org_id,
        InventoryLocation.location_code == location_data.location_code
    )
    result = await db.execute(stmt)
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(status_code=400, detail="Location code already exists")
    
    location = InventoryLocation(
        organization_id=org_id,
        **location_data.model_dump()
    )
    
    db.add(location)
    await db.commit()
    await db.refresh(location)
    
    return location


@router.get("/locations", response_model=List[LocationResponse])
async def list_locations(
    activo: Optional[bool] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("supply_chain.locations.read")),
    org_id: int = Depends(get_org_id)
):
    """List inventory locations."""
    query = select(InventoryLocation).where(InventoryLocation.organization_id == org_id)
    
    if activo is not None:
        query = query.where(InventoryLocation.activo == activo)
    
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/locations/{location_id}/inventory")
async def get_location_inventory(
    location_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("supply_chain.locations.read")),
    org_id: int = Depends(get_org_id)
):
    """Get inventory quantities for a location."""
    stmt = select(InventoryByLocation).where(
        InventoryByLocation.location_id == location_id,
        InventoryByLocation.organization_id == org_id,
        InventoryByLocation.on_hand > 0
    )
    result = await db.execute(stmt)
    return result.scalars().all()
