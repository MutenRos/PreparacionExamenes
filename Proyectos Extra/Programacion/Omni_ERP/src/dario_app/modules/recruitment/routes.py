"""Recruitment Management routes."""

from datetime import datetime, date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.core.auth import require_permission, get_tenant_db, get_org_id
from dario_app.modules.usuarios.models import Usuario

from .models import JobPosition, Candidate, Application, Interview, JobOffer, CandidateRating

router = APIRouter(prefix="/api/recruitment", tags=["Recruitment Management"])


# Schemas

class JobPositionCreate(BaseModel):
    title: str
    department: str
    salary_min: float
    salary_max: float
    required_headcount: int = 1
    posted_date: str


class CandidateCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    current_title: Optional[str] = None
    current_company: Optional[str] = None


# Job Positions

@router.post("/positions")
async def create_position(
    payload: JobPositionCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("recruitment.positions.create")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(JobPosition).where(JobPosition.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    position_code = f"POS-{count + 1:04d}"
    
    position = JobPosition(
        organization_id=org_id,
        position_code=position_code,
        posted_date=datetime.strptime(payload.posted_date, "%Y-%m-%d").date(),
        **payload.model_dump(exclude={"posted_date"})
    )
    db.add(position)
    await db.commit()
    await db.refresh(position)
    return position


@router.get("/positions")
async def list_positions(
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("recruitment.positions.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(JobPosition).where(JobPosition.organization_id == org_id)
    if status:
        query = query.where(JobPosition.status == status)
    result = await db.execute(query)
    return result.scalars().all()


# Candidates

@router.post("/candidates")
async def create_candidate(
    payload: CandidateCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("recruitment.candidates.create")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(Candidate).where(Candidate.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    candidate_id = f"CAN-{count + 1:05d}"
    
    candidate = Candidate(
        organization_id=org_id,
        candidate_id=candidate_id,
        applied_date=date.today(),
        **payload.model_dump()
    )
    db.add(candidate)
    await db.commit()
    await db.refresh(candidate)
    return candidate


@router.get("/candidates")
async def list_candidates(
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("recruitment.candidates.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(Candidate).where(Candidate.organization_id == org_id)
    if status:
        query = query.where(Candidate.status == status)
    result = await db.execute(query)
    return result.scalars().all()


# Applications

@router.get("/applications")
async def list_applications(
    status: Optional[str] = None,
    position_id: Optional[int] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("recruitment.applications.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(Application).where(Application.organization_id == org_id)
    if status:
        query = query.where(Application.status == status)
    if position_id:
        query = query.where(Application.position_id == position_id)
    result = await db.execute(query)
    return result.scalars().all()
