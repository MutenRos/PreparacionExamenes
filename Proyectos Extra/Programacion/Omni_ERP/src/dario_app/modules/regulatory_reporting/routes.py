"""
Regulatory Reporting & Tax Management - Routes
Operations for tax entities, returns, filings, and audit trails.
"""
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.database import get_db
from dario_app.modules.regulatory_reporting.models import (
    TaxEntity,
    TaxReturn,
    TaxFilingSchedule,
    TaxTransaction,
    TaxAuditTrail,
)

router = APIRouter(prefix="/regulatory-reporting", tags=["Regulatory Reporting"])


# Entities
@router.post("/entities")
async def create_tax_entity(
    organization_id: int,
    legal_name: str,
    country: str,
    tax_id: Optional[str] = None,
    reporting_currency: str = "USD",
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(func.count(TaxEntity.id)))
    count = result.scalar() or 0
    entity_code = f"TAXENT-{count + 1:04d}"

    entity = TaxEntity(
        organization_id=organization_id,
        entity_code=entity_code,
        legal_name=legal_name,
        country=country,
        tax_id=tax_id,
        reporting_currency=reporting_currency,
    )
    db.add(entity)
    await db.commit()
    await db.refresh(entity)
    return entity


@router.get("/entities")
async def list_tax_entities(organization_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TaxEntity).where(TaxEntity.organization_id == organization_id))
    return result.scalars().all()


# Returns
@router.post("/returns")
async def create_tax_return(
    organization_id: int,
    entity_id: int,
    period_start: datetime,
    period_end: datetime,
    jurisdiction: str,
    form_type: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(func.count(TaxReturn.id)))
    count = result.scalar() or 0
    return_code = f"RET-{count + 1:05d}"

    tax_return = TaxReturn(
        organization_id=organization_id,
        entity_id=entity_id,
        return_code=return_code,
        period_start=period_start,
        period_end=period_end,
        jurisdiction=jurisdiction,
        form_type=form_type,
        status="Draft",
    )
    db.add(tax_return)
    await db.commit()
    await db.refresh(tax_return)
    return tax_return


@router.patch("/returns/{return_id}/submit")
async def submit_return(
    return_id: int,
    total_tax_due: Optional[float] = None,
    total_tax_collected: Optional[float] = None,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(TaxReturn).where(TaxReturn.id == return_id))
    tax_return = result.scalar_one_or_none()
    if not tax_return:
        raise HTTPException(status_code=404, detail="Return not found")

    tax_return.status = "Submitted"
    tax_return.total_tax_due = total_tax_due
    tax_return.total_tax_collected = total_tax_collected
    tax_return.submitted_at = datetime.utcnow()
    tax_return.updated_at = datetime.utcnow()

    audit = TaxAuditTrail(
        organization_id=tax_return.organization_id,
        target_type="Return",
        target_id=tax_return.id,
        action="Submitted",
        performed_by="system",
        details={"return_code": tax_return.return_code},
    )
    db.add(audit)

    await db.commit()
    await db.refresh(tax_return)
    return tax_return


# Filing schedules
@router.post("/filings")
async def create_filing_schedule(
    organization_id: int,
    tax_return_id: int,
    due_date: datetime,
    reminder_days_before: int = 7,
    db: AsyncSession = Depends(get_db),
):
    schedule = TaxFilingSchedule(
        organization_id=organization_id,
        tax_return_id=tax_return_id,
        due_date=due_date,
        reminder_days_before=reminder_days_before,
    )
    db.add(schedule)
    await db.commit()
    await db.refresh(schedule)
    return schedule


@router.patch("/filings/{schedule_id}/submit")
async def mark_filing_submitted(schedule_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TaxFilingSchedule).where(TaxFilingSchedule.id == schedule_id))
    schedule = result.scalar_one_or_none()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    schedule.status = "Submitted"
    schedule.submitted_at = datetime.utcnow()
    await db.commit()
    await db.refresh(schedule)
    return schedule


# Transactions
@router.post("/transactions")
async def record_tax_transaction(
    organization_id: int,
    tax_return_id: int,
    transaction_type: str,
    amount: float,
    tax_amount: float,
    currency: str = "USD",
    reference_id: Optional[str] = None,
    description: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    txn = TaxTransaction(
        organization_id=organization_id,
        tax_return_id=tax_return_id,
        transaction_type=transaction_type,
        amount=amount,
        tax_amount=tax_amount,
        currency=currency,
        reference_id=reference_id,
        description=description,
    )
    db.add(txn)
    await db.commit()
    await db.refresh(txn)
    return txn


# Analytics
@router.get("/analytics/tax-exposure")
async def tax_exposure(organization_id: int, db: AsyncSession = Depends(get_db)):
    """Summaries for tax due and collected by jurisdiction."""
    result = await db.execute(
        select(TaxReturn.jurisdiction, func.sum(TaxReturn.total_tax_due), func.sum(TaxReturn.total_tax_collected))
        .where(TaxReturn.organization_id == organization_id)
        .group_by(TaxReturn.jurisdiction)
    )
    return [
        {
            "jurisdiction": row[0],
            "tax_due": float(row[1] or 0),
            "tax_collected": float(row[2] or 0),
        }
        for row in result.all()
    ]
