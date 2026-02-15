"""Warranty Management routes."""

from datetime import datetime, date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.core.auth import require_permission, get_tenant_db, get_org_id
from dario_app.modules.usuarios.models import Usuario

from .models import WarrantyPolicy, ProductWarranty, WarrantyRegistration, WarrantyClaim, WarrantyService

router = APIRouter(prefix="/api/warranty", tags=["Warranty Management"])


# Schemas

class WarrantyPolicyCreate(BaseModel):
    name: str
    warranty_type: str
    duration_months: int
    covers_parts: bool = True
    covers_labor: bool = True


class WarrantyRegistrationCreate(BaseModel):
    customer_id: int
    customer_name: str
    product_id: int
    product_code: str
    product_name: str
    policy_id: int
    purchase_date: str


class WarrantyClaimCreate(BaseModel):
    registration_id: int
    claim_type: str
    descripcion: str
    issue_date: str


# Policies

@router.post("/policies")
async def create_policy(
    payload: WarrantyPolicyCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("warranty.policies.create")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(WarrantyPolicy).where(WarrantyPolicy.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    policy_code = f"POL-{count + 1:04d}"
    
    policy = WarrantyPolicy(
        organization_id=org_id,
        policy_code=policy_code,
        **payload.model_dump()
    )
    db.add(policy)
    await db.commit()
    await db.refresh(policy)
    return policy


@router.get("/policies")
async def list_policies(
    warranty_type: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("warranty.policies.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(WarrantyPolicy).where(WarrantyPolicy.organization_id == org_id)
    if warranty_type:
        query = query.where(WarrantyPolicy.warranty_type == warranty_type)
    result = await db.execute(query)
    return result.scalars().all()


# Registrations

@router.post("/registrations")
async def register_warranty(
    payload: WarrantyRegistrationCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("warranty.registrations.create")),
    org_id: int = Depends(get_org_id),
):
    now = datetime.now()
    stmt = select(WarrantyRegistration).where(WarrantyRegistration.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    registration_number = f"WRG-{now.strftime('%Y')}-{count + 1:05d}"
    
    # Get policy to calculate warranty dates
    policy_stmt = select(WarrantyPolicy).where(
        WarrantyPolicy.id == payload.policy_id,
        WarrantyPolicy.organization_id == org_id
    )
    policy_result = await db.execute(policy_stmt)
    policy = policy_result.scalar_one_or_none()
    
    if not policy:
        raise HTTPException(status_code=404, detail="Warranty policy not found")
    
    purchase_date = datetime.strptime(payload.purchase_date, "%Y-%m-%d").date()
    from datetime import timedelta
    warranty_end_date = purchase_date + timedelta(days=policy.duration_months * 30)
    
    registration = WarrantyRegistration(
        organization_id=org_id,
        registration_number=registration_number,
        purchase_date=purchase_date,
        warranty_start_date=purchase_date,
        warranty_end_date=warranty_end_date,
        **payload.model_dump(exclude={"purchase_date"})
    )
    db.add(registration)
    await db.commit()
    await db.refresh(registration)
    return registration


@router.get("/registrations")
async def list_registrations(
    customer_id: Optional[int] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("warranty.registrations.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(WarrantyRegistration).where(WarrantyRegistration.organization_id == org_id)
    if customer_id:
        query = query.where(WarrantyRegistration.customer_id == customer_id)
    if status:
        query = query.where(WarrantyRegistration.status == status)
    result = await db.execute(query)
    return result.scalars().all()


# Claims

@router.post("/claims")
async def file_claim(
    payload: WarrantyClaimCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("warranty.claims.create")),
    org_id: int = Depends(get_org_id),
):
    now = datetime.now()
    stmt = select(WarrantyClaim).where(WarrantyClaim.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    claim_number = f"CLM-{now.strftime('%Y')}-{count + 1:05d}"
    
    issue_date = datetime.strptime(payload.issue_date, "%Y-%m-%d").date()
    
    claim = WarrantyClaim(
        organization_id=org_id,
        claim_number=claim_number,
        issue_date=issue_date,
        reported_date=date.today(),
        **payload.model_dump(exclude={"issue_date"})
    )
    db.add(claim)
    await db.commit()
    await db.refresh(claim)
    return claim


@router.get("/claims")
async def list_claims(
    registration_id: Optional[int] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("warranty.claims.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(WarrantyClaim).where(WarrantyClaim.organization_id == org_id)
    if registration_id:
        query = query.where(WarrantyClaim.registration_id == registration_id)
    if status:
        query = query.where(WarrantyClaim.status == status)
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/claims/{claim_id}/approve")
async def approve_claim(
    claim_id: int,
    approved_amount: float,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("warranty.claims.manage")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(WarrantyClaim).where(
        WarrantyClaim.id == claim_id,
        WarrantyClaim.organization_id == org_id
    )
    result = await db.execute(stmt)
    claim = result.scalar_one_or_none()
    
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    
    from decimal import Decimal
    claim.status = "approved"
    claim.approved_amount = Decimal(str(approved_amount))
    claim.approval_date = date.today()
    
    await db.commit()
    await db.refresh(claim)
    return claim
