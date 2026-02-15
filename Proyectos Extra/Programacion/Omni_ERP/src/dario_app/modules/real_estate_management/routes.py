"""Real Estate Management Routes."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, date

from dario_app.database import get_db
from dario_app.modules.real_estate_management import models
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/api/real-estate", tags=["real_estate_management"])


# Pydantic Schemas
class PropertyCreate(BaseModel):
    property_name: str
    property_type: str
    address: str
    total_area_sqft: float


class LeaseAgreementCreate(BaseModel):
    property_id: int
    tenant_name: str
    lease_type: str
    commencement_date: str
    expiration_date: str
    base_rent_annual: float


class MaintenanceRequestCreate(BaseModel):
    property_id: int
    maintenance_type: str
    description: str
    priority: str


class SpaceAllocationCreate(BaseModel):
    property_id: int
    department: str
    allocated_area_sqft: float
    allocation_type: str


# Property Endpoints
@router.post("/properties")
async def create_property(
    property_data: PropertyCreate,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Create a new property."""
    import uuid
    property_code = f"PROP-{str(uuid.uuid4())[:8].upper()}"
    
    db_property = models.Property(
        organization_id=organization_id,
        property_code=property_code,
        property_name=property_data.property_name,
        property_type=property_data.property_type,
        address=property_data.address,
        total_area_sqft=property_data.total_area_sqft,
        usable_area_sqft=property_data.total_area_sqft * 0.85,
        property_status="active",
    )
    db.add(db_property)
    await db.commit()
    await db.refresh(db_property)
    return {"id": db_property.id, "property_code": db_property.property_code}


@router.get("/properties")
async def list_properties(
    organization_id: int = Query(...),
    property_type: Optional[str] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List properties."""
    query = db.query(models.Property).filter(
        models.Property.organization_id == organization_id
    )
    
    if property_type:
        query = query.filter(models.Property.property_type == property_type)
    if status:
        query = query.filter(models.Property.property_status == status)
    
    properties = await query.all()
    total_value = sum([p.current_market_value or 0 for p in properties])
    return {"properties": properties, "total": len(properties), "total_portfolio_value": total_value}


@router.get("/properties/{property_id}")
async def get_property(
    property_id: int,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Get property details."""
    property_obj = await db.query(models.Property).filter(
        models.Property.id == property_id,
        models.Property.organization_id == organization_id
    ).first()
    
    if not property_obj:
        raise HTTPException(status_code=404, detail="Property not found")
    
    return {"property": property_obj}


# Lease Agreement Endpoints
@router.post("/leases")
async def create_lease_agreement(
    lease: LeaseAgreementCreate,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Create a lease agreement."""
    import uuid
    lease_number = f"LEASE-{str(uuid.uuid4())[:8].upper()}"
    
    from datetime import datetime as dt
    commencement = dt.strptime(lease.commencement_date, "%Y-%m-%d").date()
    expiration = dt.strptime(lease.expiration_date, "%Y-%m-%d").date()
    
    db_lease = models.LeaseAgreement(
        organization_id=organization_id,
        property_id=lease.property_id,
        lease_number=lease_number,
        tenant_name=lease.tenant_name,
        lease_type=lease.lease_type,
        commencement_date=commencement,
        expiration_date=expiration,
        lease_term_years=(expiration.year - commencement.year),
        base_rent_annual=lease.base_rent_annual,
        lease_status="active",
    )
    db.add(db_lease)
    await db.commit()
    await db.refresh(db_lease)
    return {"id": db_lease.id, "lease_number": db_lease.lease_number}


@router.get("/leases")
async def list_leases(
    organization_id: int = Query(...),
    property_id: Optional[int] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List lease agreements."""
    query = db.query(models.LeaseAgreement).filter(
        models.LeaseAgreement.organization_id == organization_id
    )
    
    if property_id:
        query = query.filter(models.LeaseAgreement.property_id == property_id)
    if status:
        query = query.filter(models.LeaseAgreement.lease_status == status)
    
    leases = await query.all()
    total_annual_rent = sum([l.base_rent_annual or 0 for l in leases])
    return {"leases": leases, "total": len(leases), "total_annual_rent": total_annual_rent}


# Rent Collection Endpoints
@router.get("/rent-collection")
async def get_rent_collection(
    organization_id: int = Query(...),
    lease_id: Optional[int] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get rent collection data."""
    query = db.query(models.RentCollection).filter(
        models.RentCollection.organization_id == organization_id
    )
    
    if lease_id:
        query = query.filter(models.RentCollection.lease_id == lease_id)
    if status:
        query = query.filter(models.RentCollection.collection_status == status)
    
    collections = await query.all()
    
    total_due = sum([c.total_due or 0 for c in collections])
    total_collected = sum([c.amount_paid or 0 for c in collections])
    overdue_count = sum([1 for c in collections if c.collection_status == "overdue"])
    
    return {
        "collections": collections,
        "total_due": total_due,
        "total_collected": total_collected,
        "overdue_count": overdue_count
    }


# Maintenance Request Endpoints
@router.post("/maintenance-requests")
async def create_maintenance_request(
    request: MaintenanceRequestCreate,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Create a maintenance request."""
    import uuid
    request_number = f"MR-{str(uuid.uuid4())[:8].upper()}"
    
    db_request = models.MaintenanceRequest(
        organization_id=organization_id,
        property_id=request.property_id,
        request_number=request_number,
        maintenance_type=request.maintenance_type,
        description=request.description,
        priority=request.priority,
        status="open",
    )
    db.add(db_request)
    await db.commit()
    await db.refresh(db_request)
    return {"id": db_request.id, "request_number": db_request.request_number}


@router.get("/maintenance-requests")
async def list_maintenance_requests(
    organization_id: int = Query(...),
    property_id: Optional[int] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List maintenance requests."""
    query = db.query(models.MaintenanceRequest).filter(
        models.MaintenanceRequest.organization_id == organization_id
    )
    
    if property_id:
        query = query.filter(models.MaintenanceRequest.property_id == property_id)
    if status:
        query = query.filter(models.MaintenanceRequest.status == status)
    if priority:
        query = query.filter(models.MaintenanceRequest.priority == priority)
    
    requests = await query.all()
    
    critical_count = sum([1 for r in requests if r.priority == "critical"])
    open_count = sum([1 for r in requests if r.status == "open"])
    
    return {
        "requests": requests,
        "total": len(requests),
        "critical_count": critical_count,
        "open_count": open_count
    }


@router.put("/maintenance-requests/{request_id}/complete")
async def complete_maintenance_request(
    request_id: int,
    actual_cost: float,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Mark maintenance request as completed."""
    maintenance = await db.query(models.MaintenanceRequest).filter(
        models.MaintenanceRequest.id == request_id,
        models.MaintenanceRequest.organization_id == organization_id
    ).first()
    
    if not maintenance:
        raise HTTPException(status_code=404, detail="Maintenance request not found")
    
    maintenance.status = "completed"
    maintenance.completion_date = datetime.utcnow()
    maintenance.actual_cost = actual_cost
    await db.commit()
    return {"id": maintenance.id, "status": "completed"}


# Space Allocation Endpoints
@router.post("/space-allocation")
async def create_space_allocation(
    allocation: SpaceAllocationCreate,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Create space allocation."""
    db_allocation = models.SpaceAllocation(
        organization_id=organization_id,
        property_id=allocation.property_id,
        department=allocation.department,
        allocated_area_sqft=allocation.allocated_area_sqft,
        allocation_type=allocation.allocation_type,
        allocation_status="occupied",
    )
    db.add(db_allocation)
    await db.commit()
    await db.refresh(db_allocation)
    return {"id": db_allocation.id, "department": db_allocation.department}


@router.get("/space-allocation")
async def list_space_allocations(
    organization_id: int = Query(...),
    property_id: Optional[int] = None,
    department: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List space allocations."""
    query = db.query(models.SpaceAllocation).filter(
        models.SpaceAllocation.organization_id == organization_id
    )
    
    if property_id:
        query = query.filter(models.SpaceAllocation.property_id == property_id)
    if department:
        query = query.filter(models.SpaceAllocation.department == department)
    
    allocations = await query.all()
    total_allocated = sum([a.allocated_area_sqft or 0 for a in allocations])
    return {"allocations": allocations, "total_allocated_sqft": total_allocated}


# Portfolio Analysis Endpoints
@router.get("/portfolio-analysis")
async def get_portfolio_analysis(
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Get real estate portfolio analysis."""
    analysis = await db.query(models.PropertyPortfolioAnalysis).filter(
        models.PropertyPortfolioAnalysis.organization_id == organization_id
    ).order_by(models.PropertyPortfolioAnalysis.analysis_date.desc()).first()
    
    if not analysis:
        return {"message": "No portfolio analysis available"}
    
    return {"analysis": analysis}


@router.post("/portfolio-analysis")
async def create_portfolio_analysis(
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Generate portfolio analysis."""
    properties = await db.query(models.Property).filter(
        models.Property.organization_id == organization_id
    ).all()
    
    leases = await db.query(models.LeaseAgreement).filter(
        models.LeaseAgreement.organization_id == organization_id
    ).all()
    
    total_value = sum([p.current_market_value or 0 for p in properties])
    total_area = sum([p.total_area_sqft or 0 for p in properties])
    total_rent = sum([l.base_rent_annual or 0 for l in leases])
    
    analysis = models.PropertyPortfolioAnalysis(
        organization_id=organization_id,
        total_properties=len(properties),
        total_portfolio_value=total_value,
        total_area_sqft=total_area,
        total_annual_rent=total_rent,
        cost_per_sqft=total_value / total_area if total_area > 0 else 0,
        number_of_leases=len(leases),
    )
    db.add(analysis)
    await db.commit()
    await db.refresh(analysis)
    return {"id": analysis.id, "total_portfolio_value": analysis.total_portfolio_value}


# Health Check
@router.get("/health")
async def health_check():
    """Check real estate management module health."""
    return {
        "status": "healthy",
        "module": "real_estate_management",
        "version": "1.0.0",
        "features": [
            "Property Portfolio Management",
            "Lease Agreement Tracking",
            "Rent Collection Management",
            "Maintenance Request Management",
            "Space Allocation Planning",
            "Facility Condition Assessment",
            "Portfolio Analytics",
            "Sustainability Tracking"
        ]
    }
