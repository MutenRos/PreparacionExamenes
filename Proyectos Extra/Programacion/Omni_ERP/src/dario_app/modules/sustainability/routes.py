"""Sustainability Management routes."""

from datetime import datetime, date
from typing import Optional
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.core.auth import require_permission, get_tenant_db, get_org_id
from dario_app.modules.usuarios.models import Usuario

from .models import SustainabilityGoal, EmissionSource, EmissionRecord, WasteRecord, SustainabilityReport, ComplianceRequirement

router = APIRouter(prefix="/api/sustainability", tags=["Sustainability Management"])


# Schemas

class GoalCreate(BaseModel):
    title: str
    esg_category: str
    target_value: Decimal
    target_unit: str
    target_year: int


class EmissionSourceCreate(BaseModel):
    name: str
    scope: str
    category: str
    emission_factor: Decimal
    emission_factor_unit: str


class EmissionRecordCreate(BaseModel):
    source_id: int
    reporting_period: str
    quantity: Decimal
    quantity_unit: str


# Goals

@router.post("/goals")
async def create_goal(
    payload: GoalCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("sustainability.goals.create")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(SustainabilityGoal).where(SustainabilityGoal.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    goal_code = f"GOAL-{count + 1:04d}"
    
    goal = SustainabilityGoal(
        organization_id=org_id,
        goal_code=goal_code,
        **payload.model_dump()
    )
    db.add(goal)
    await db.commit()
    await db.refresh(goal)
    return goal


@router.get("/goals")
async def list_goals(
    esg_category: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("sustainability.goals.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(SustainabilityGoal).where(SustainabilityGoal.organization_id == org_id)
    if esg_category:
        query = query.where(SustainabilityGoal.esg_category == esg_category)
    result = await db.execute(query)
    return result.scalars().all()


# Emission Sources

@router.post("/emission-sources")
async def create_emission_source(
    payload: EmissionSourceCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("sustainability.emissions.create")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(EmissionSource).where(EmissionSource.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    source_code = f"SRC-{count + 1:04d}"
    
    source = EmissionSource(
        organization_id=org_id,
        source_code=source_code,
        **payload.model_dump()
    )
    db.add(source)
    await db.commit()
    await db.refresh(source)
    return source


@router.get("/emission-sources")
async def list_emission_sources(
    scope: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("sustainability.emissions.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(EmissionSource).where(EmissionSource.organization_id == org_id)
    if scope:
        query = query.where(EmissionSource.scope == scope)
    result = await db.execute(query)
    return result.scalars().all()


# Emission Records

@router.post("/emission-records")
async def record_emission(
    payload: EmissionRecordCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("sustainability.emissions.create")),
    org_id: int = Depends(get_org_id),
):
    # Get source
    src_stmt = select(EmissionSource).where(
        EmissionSource.id == payload.source_id,
        EmissionSource.organization_id == org_id
    )
    src_result = await db.execute(src_stmt)
    source = src_result.scalar_one_or_none()
    
    if not source:
        raise HTTPException(status_code=404, detail="Emission source not found")
    
    # Calculate emissions
    emissions_kg_co2e = payload.quantity * source.emission_factor
    
    record = EmissionRecord(
        organization_id=org_id,
        **payload.model_dump(),
        emissions_kg_co2e=emissions_kg_co2e
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record


@router.get("/emission-records")
async def list_emission_records(
    reporting_period: Optional[str] = None,
    source_id: Optional[int] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("sustainability.emissions.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(EmissionRecord).where(EmissionRecord.organization_id == org_id)
    if reporting_period:
        query = query.where(EmissionRecord.reporting_period == reporting_period)
    if source_id:
        query = query.where(EmissionRecord.source_id == source_id)
    result = await db.execute(query)
    return result.scalars().all()


# Reports

@router.get("/reports")
async def list_reports(
    reporting_year: Optional[int] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("sustainability.reports.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(SustainabilityReport).where(SustainabilityReport.organization_id == org_id)
    if reporting_year:
        query = query.where(SustainabilityReport.reporting_year == reporting_year)
    result = await db.execute(query)
    return result.scalars().all()


# Analytics

@router.get("/analytics/carbon-footprint")
async def get_carbon_footprint(
    year: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("sustainability.analytics.read")),
    org_id: int = Depends(get_org_id),
):
    """Get total carbon footprint for a year."""
    period_prefix = f"{year}-"
    
    stmt = select(EmissionRecord).where(
        EmissionRecord.organization_id == org_id,
        EmissionRecord.reporting_period.startswith(period_prefix)
    )
    result = await db.execute(stmt)
    records = result.scalars().all()
    
    total_emissions = sum(r.emissions_kg_co2e for r in records)
    
    return {
        "year": year,
        "total_emissions_kg_co2e": float(total_emissions),
        "total_emissions_metric_tons": float(total_emissions / 1000),
        "record_count": len(records)
    }
