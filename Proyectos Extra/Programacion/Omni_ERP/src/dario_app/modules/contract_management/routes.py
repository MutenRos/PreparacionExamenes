"""Contract Lifecycle Management routes."""

from datetime import datetime, date
from typing import Optional
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.core.auth import require_permission, get_tenant_db, get_org_id
from dario_app.modules.usuarios.models import Usuario

from .models import ContractTemplate, Contract, ContractClause, ContractApproval, ContractMilestone, ContractRenewal

router = APIRouter(prefix="/api/contract-management", tags=["Contract Lifecycle Management"])


# Schemas

class ContractCreate(BaseModel):
    contract_type: str
    title: str
    counterparty_id: int
    counterparty_name: str
    start_date: str
    end_date: str
    contract_value: Optional[Decimal] = None


class ContractMilestoneCreate(BaseModel):
    contract_id: int
    title: str
    milestone_type: str
    due_date: str
    associated_value: Optional[Decimal] = None


# Contracts

@router.post("/contracts")
async def create_contract(
    payload: ContractCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("contracts.manage.create")),
    org_id: int = Depends(get_org_id),
):
    now = datetime.now()
    stmt = select(Contract).where(Contract.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    contract_number = f"CTR-{now.strftime('%Y')}-{count + 1:05d}"
    
    start_date = datetime.strptime(payload.start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(payload.end_date, "%Y-%m-%d").date()
    
    contract = Contract(
        organization_id=org_id,
        contract_number=contract_number,
        start_date=start_date,
        end_date=end_date,
        **payload.model_dump(exclude={"start_date", "end_date"})
    )
    db.add(contract)
    await db.commit()
    await db.refresh(contract)
    return contract


@router.get("/contracts")
async def list_contracts(
    status: Optional[str] = None,
    contract_type: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("contracts.manage.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(Contract).where(Contract.organization_id == org_id)
    if status:
        query = query.where(Contract.status == status)
    if contract_type:
        query = query.where(Contract.contract_type == contract_type)
    query = query.order_by(Contract.end_date)
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/contracts/{contract_id}/activate")
async def activate_contract(
    contract_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("contracts.manage.manage")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(Contract).where(
        Contract.id == contract_id,
        Contract.organization_id == org_id
    )
    result = await db.execute(stmt)
    contract = result.scalar_one_or_none()
    
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    contract.status = "active"
    await db.commit()
    await db.refresh(contract)
    return contract


# Milestones

@router.post("/milestones")
async def create_milestone(
    payload: ContractMilestoneCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("contracts.manage.create")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(ContractMilestone).where(
        ContractMilestone.organization_id == org_id,
        ContractMilestone.contract_id == payload.contract_id
    )
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    milestone_number = f"MIL-{count + 1:04d}"
    
    due_date = datetime.strptime(payload.due_date, "%Y-%m-%d").date()
    
    milestone = ContractMilestone(
        organization_id=org_id,
        milestone_number=milestone_number,
        due_date=due_date,
        **payload.model_dump(exclude={"due_date"})
    )
    db.add(milestone)
    await db.commit()
    await db.refresh(milestone)
    return milestone


@router.get("/milestones")
async def list_milestones(
    contract_id: Optional[int] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("contracts.manage.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(ContractMilestone).where(ContractMilestone.organization_id == org_id)
    if contract_id:
        query = query.where(ContractMilestone.contract_id == contract_id)
    if status:
        query = query.where(ContractMilestone.status == status)
    query = query.order_by(ContractMilestone.due_date)
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/milestones/{milestone_id}/complete")
async def complete_milestone(
    milestone_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("contracts.manage.manage")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(ContractMilestone).where(
        ContractMilestone.id == milestone_id,
        ContractMilestone.organization_id == org_id
    )
    result = await db.execute(stmt)
    milestone = result.scalar_one_or_none()
    
    if not milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")
    
    milestone.status = "completed"
    milestone.completion_date = date.today()
    
    await db.commit()
    await db.refresh(milestone)
    return milestone


# Renewals

@router.get("/renewals")
async def list_renewals(
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("contracts.manage.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(ContractRenewal).where(ContractRenewal.organization_id == org_id)
    if status:
        query = query.where(ContractRenewal.status == status)
    result = await db.execute(query)
    return result.scalars().all()
