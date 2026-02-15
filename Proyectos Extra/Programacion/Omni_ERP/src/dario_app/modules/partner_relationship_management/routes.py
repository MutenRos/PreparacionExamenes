"""
Partner Relationship Management (PRM) - Routes
Manage partner onboarding, deal registration, incentives, and certifications.
"""
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.database import get_db
from dario_app.modules.partner_relationship_management.models import (
    PartnerProgram,
    Partner,
    PartnerDealRegistration,
    PartnerIncentive,
    PartnerCertification,
)

router = APIRouter(prefix="/prm", tags=["Partner Relationship Management"])


# Programs
@router.post("/programs")
async def create_program(
    organization_id: int,
    name: str,
    description: Optional[str] = None,
    tiering_model: Optional[str] = None,
    requirements: Optional[dict] = None,
    benefits: Optional[dict] = None,
    db: AsyncSession = Depends(get_db),
):
    """Create a partner program."""
    result = await db.execute(select(func.count(PartnerProgram.id)))
    count = result.scalar() or 0
    program_code = f"PRG-{count + 1:04d}"

    program = PartnerProgram(
        organization_id=organization_id,
        program_code=program_code,
        name=name,
        description=description,
        tiering_model=tiering_model,
        requirements=requirements or {},
        benefits=benefits or {},
        created_by="system",
    )
    db.add(program)
    await db.commit()
    await db.refresh(program)
    return program


@router.get("/programs")
async def list_programs(organization_id: int, is_active: Optional[bool] = None, db: AsyncSession = Depends(get_db)):
    """List partner programs."""
    query = select(PartnerProgram).where(PartnerProgram.organization_id == organization_id)
    if is_active is not None:
        query = query.where(PartnerProgram.is_active == is_active)
    result = await db.execute(query)
    return result.scalars().all()


# Partners
@router.post("/partners")
async def create_partner(
    organization_id: int,
    name: str,
    partner_type: Optional[str] = None,
    program_id: Optional[int] = None,
    region: Optional[str] = None,
    industry_focus: Optional[str] = None,
    contact_email: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """Register a new partner."""
    result = await db.execute(select(func.count(Partner.id)))
    count = result.scalar() or 0
    partner_code = f"PAR-{count + 1:05d}"

    partner = Partner(
        organization_id=organization_id,
        program_id=program_id,
        partner_code=partner_code,
        name=name,
        partner_type=partner_type,
        region=region,
        industry_focus=industry_focus,
        contact_email=contact_email,
        onboarding_status="Active",
        created_by="system",
    )
    db.add(partner)
    await db.commit()
    await db.refresh(partner)
    return partner


@router.get("/partners")
async def list_partners(
    organization_id: int,
    tier: Optional[str] = None,
    region: Optional[str] = None,
    program_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    """List partners with optional filters."""
    query = select(Partner).where(Partner.organization_id == organization_id)
    if tier:
        query = query.where(Partner.tier == tier)
    if region:
        query = query.where(Partner.region == region)
    if program_id:
        query = query.where(Partner.program_id == program_id)
    result = await db.execute(query)
    return result.scalars().all()


# Deal registrations
@router.post("/deals")
async def register_deal(
    organization_id: int,
    partner_id: int,
    customer_name: str,
    estimated_amount: float,
    probability: Optional[float] = None,
    db: AsyncSession = Depends(get_db),
):
    """Register a partner deal."""
    result = await db.execute(select(func.count(PartnerDealRegistration.id)))
    count = result.scalar() or 0
    deal_code = f"DR-{count + 1:05d}"

    deal = PartnerDealRegistration(
        organization_id=organization_id,
        partner_id=partner_id,
        deal_code=deal_code,
        customer_name=customer_name,
        estimated_amount=estimated_amount,
        probability=probability,
        stage="Registered",
    )
    db.add(deal)
    await db.commit()
    await db.refresh(deal)
    return deal


@router.patch("/deals/{deal_id}/stage")
async def update_deal_stage(
    deal_id: int,
    stage: str,
    probability: Optional[float] = None,
    approved_by: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """Update deal stage and probability."""
    result = await db.execute(select(PartnerDealRegistration).where(PartnerDealRegistration.id == deal_id))
    deal = result.scalar_one_or_none()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    deal.stage = stage
    if probability is not None:
        deal.probability = probability
    if stage == "Approved":
        deal.approved_at = datetime.utcnow()
        deal.approved_by = approved_by

    await db.commit()
    await db.refresh(deal)
    return deal


# Incentives
@router.post("/incentives")
async def allocate_incentive(
    organization_id: int,
    partner_id: int,
    incentive_type: str,
    amount: float,
    currency: str = "USD",
    description: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """Allocate an incentive to a partner."""
    result = await db.execute(select(func.count(PartnerIncentive.id)))
    count = result.scalar() or 0
    incentive_code = f"INC-{count + 1:05d}"

    incentive = PartnerIncentive(
        organization_id=organization_id,
        partner_id=partner_id,
        incentive_code=incentive_code,
        incentive_type=incentive_type,
        amount=amount,
        currency=currency,
        description=description,
    )
    db.add(incentive)
    await db.commit()
    await db.refresh(incentive)
    return incentive


# Certifications
@router.post("/certifications")
async def issue_certification(
    organization_id: int,
    partner_id: int,
    name: str,
    category: Optional[str] = None,
    level: Optional[str] = None,
    expires_at: Optional[datetime] = None,
    db: AsyncSession = Depends(get_db),
):
    """Issue a certification to a partner."""
    result = await db.execute(select(func.count(PartnerCertification.id)))
    count = result.scalar() or 0
    certification_code = f"CERT-{count + 1:05d}"

    cert = PartnerCertification(
        organization_id=organization_id,
        partner_id=partner_id,
        certification_code=certification_code,
        name=name,
        category=category,
        level=level,
        expires_at=expires_at,
    )
    db.add(cert)
    await db.commit()
    await db.refresh(cert)
    return cert


# Analytics
@router.get("/analytics/partner-performance")
async def partner_performance(organization_id: int, db: AsyncSession = Depends(get_db)):
    """Aggregate total registered deal value per partner."""
    result = await db.execute(
        select(Partner.name, func.sum(PartnerDealRegistration.estimated_amount))
        .join(PartnerDealRegistration, Partner.id == PartnerDealRegistration.partner_id)
        .where(Partner.organization_id == organization_id)
        .group_by(Partner.id)
    )
    return [{"partner": row[0], "total_estimated": float(row[1] or 0)} for row in result.all()]
