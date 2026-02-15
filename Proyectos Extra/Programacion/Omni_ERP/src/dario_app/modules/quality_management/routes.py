"""Quality Management routes - Inspections, NCRs, Audits."""

from datetime import datetime, date
from typing import Optional
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.core.auth import require_permission, get_tenant_db, get_org_id
from dario_app.modules.usuarios.models import Usuario

from .models import (
    QualityOrder, QualityCheckpoint, NonConformance, 
    QualitySpecification, QualitySpecificationLine, QualityAudit
)

router = APIRouter(prefix="/api/quality-management", tags=["Quality Management"])


# Schemas

class QualityOrderCreate(BaseModel):
    order_type: str = "receiving"
    product_id: Optional[int] = None
    product_name: Optional[str] = None
    quantity_to_inspect: float
    reference_type: Optional[str] = None
    reference_id: Optional[int] = None
    reference_number: Optional[str] = None
    scheduled_date: Optional[str] = None


class CheckpointCreate(BaseModel):
    checkpoint_name: str
    checkpoint_type: str = "visual"
    specification: Optional[str] = None
    acceptance_criteria: Optional[str] = None


class CheckpointResult(BaseModel):
    measured_value: Optional[str] = None
    result: str
    notes: Optional[str] = None


class NonConformanceCreate(BaseModel):
    title: str
    description: str
    severity: str = "medium"
    detected_date: str
    product_id: Optional[int] = None
    product_name: Optional[str] = None
    reference_type: Optional[str] = None
    reference_id: Optional[int] = None


class SpecificationCreate(BaseModel):
    name: str
    product_id: Optional[int] = None
    product_category: Optional[str] = None
    description: Optional[str] = None


class SpecLineCreate(BaseModel):
    test_name: str
    test_type: str = "measurement"
    target_value: Optional[str] = None
    min_value: Optional[str] = None
    max_value: Optional[str] = None
    unit_of_measure: Optional[str] = None
    is_mandatory: bool = True


class AuditCreate(BaseModel):
    audit_type: str = "internal"
    title: str
    description: Optional[str] = None
    scheduled_date: str


# Quality Orders

@router.post("/quality-orders")
async def create_quality_order(
    payload: QualityOrderCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("quality.orders.create")),
    org_id: int = Depends(get_org_id),
):
    # Generate order number
    stmt = select(QualityOrder).where(QualityOrder.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    order_number = f"QO-{datetime.now().strftime('%Y%m')}-{count + 1:05d}"
    
    order = QualityOrder(
        organization_id=org_id,
        order_number=order_number,
        **payload.model_dump()
    )
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order


@router.get("/quality-orders")
async def list_quality_orders(
    status: Optional[str] = None,
    order_type: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("quality.orders.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(QualityOrder).where(QualityOrder.organization_id == org_id)
    if status:
        query = query.where(QualityOrder.status == status)
    if order_type:
        query = query.where(QualityOrder.order_type == order_type)
    query = query.order_by(QualityOrder.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/quality-orders/{order_id}/start")
async def start_inspection(
    order_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("quality.orders.inspect")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(QualityOrder).where(
        QualityOrder.id == order_id,
        QualityOrder.organization_id == org_id
    )
    result = await db.execute(stmt)
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Quality order not found")
    
    order.status = "in_progress"
    order.started_at = datetime.utcnow()
    order.inspector_user_id = user.id
    order.inspector_name = user.nombre_completo
    
    await db.commit()
    await db.refresh(order)
    return order


@router.post("/quality-orders/{order_id}/checkpoints")
async def add_checkpoint(
    order_id: int,
    payload: CheckpointCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("quality.orders.manage")),
    org_id: int = Depends(get_org_id),
):
    checkpoint = QualityCheckpoint(
        organization_id=org_id,
        quality_order_id=order_id,
        **payload.model_dump()
    )
    db.add(checkpoint)
    await db.commit()
    await db.refresh(checkpoint)
    return checkpoint


@router.get("/quality-orders/{order_id}/checkpoints")
async def list_checkpoints(
    order_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("quality.orders.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(QualityCheckpoint).where(
        QualityCheckpoint.organization_id == org_id,
        QualityCheckpoint.quality_order_id == order_id
    )
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/quality-orders/{order_id}/checkpoints/{checkpoint_id}")
async def record_checkpoint_result(
    order_id: int,
    checkpoint_id: int,
    payload: CheckpointResult,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("quality.orders.inspect")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(QualityCheckpoint).where(
        QualityCheckpoint.id == checkpoint_id,
        QualityCheckpoint.quality_order_id == order_id,
        QualityCheckpoint.organization_id == org_id
    )
    result = await db.execute(stmt)
    checkpoint = result.scalar_one_or_none()
    if not checkpoint:
        raise HTTPException(status_code=404, detail="Checkpoint not found")
    
    checkpoint.measured_value = payload.measured_value
    checkpoint.result = payload.result
    checkpoint.notes = payload.notes
    
    await db.commit()
    await db.refresh(checkpoint)
    return checkpoint


@router.patch("/quality-orders/{order_id}/complete")
async def complete_inspection(
    order_id: int,
    inspection_result: str,
    quantity_passed: float,
    quantity_failed: float,
    notes: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("quality.orders.inspect")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(QualityOrder).where(
        QualityOrder.id == order_id,
        QualityOrder.organization_id == org_id
    )
    result = await db.execute(stmt)
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Quality order not found")
    
    order.status = "completed"
    order.completed_at = datetime.utcnow()
    order.inspection_result = inspection_result
    order.quantity_passed = Decimal(str(quantity_passed))
    order.quantity_failed = Decimal(str(quantity_failed))
    order.quantity_inspected = order.quantity_passed + order.quantity_failed
    if notes:
        order.notes = notes
    
    await db.commit()
    await db.refresh(order)
    return order


# Non-Conformances

@router.post("/non-conformances")
async def create_ncr(
    payload: NonConformanceCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("quality.ncr.create")),
    org_id: int = Depends(get_org_id),
):
    # Generate NCR number
    stmt = select(NonConformance).where(NonConformance.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    ncr_number = f"NCR-{datetime.now().strftime('%Y%m')}-{count + 1:05d}"
    
    ncr = NonConformance(
        organization_id=org_id,
        ncr_number=ncr_number,
        detected_by_user_id=user.id,
        detected_by_name=user.nombre_completo,
        **payload.model_dump()
    )
    db.add(ncr)
    await db.commit()
    await db.refresh(ncr)
    return ncr


@router.get("/non-conformances")
async def list_ncrs(
    status: Optional[str] = None,
    severity: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("quality.ncr.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(NonConformance).where(NonConformance.organization_id == org_id)
    if status:
        query = query.where(NonConformance.status == status)
    if severity:
        query = query.where(NonConformance.severity == severity)
    query = query.order_by(NonConformance.detected_date.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/non-conformances/{ncr_id}/assign-action")
async def assign_corrective_action(
    ncr_id: int,
    corrective_action: str,
    assigned_to_user_id: int,
    assigned_to_name: str,
    due_date: str,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("quality.ncr.manage")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(NonConformance).where(
        NonConformance.id == ncr_id,
        NonConformance.organization_id == org_id
    )
    result = await db.execute(stmt)
    ncr = result.scalar_one_or_none()
    if not ncr:
        raise HTTPException(status_code=404, detail="NCR not found")
    
    ncr.status = "corrective_action"
    ncr.corrective_action = corrective_action
    ncr.action_assigned_to_user_id = assigned_to_user_id
    ncr.action_assigned_to_name = assigned_to_name
    ncr.action_due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
    
    await db.commit()
    await db.refresh(ncr)
    return ncr


@router.patch("/non-conformances/{ncr_id}/close")
async def close_ncr(
    ncr_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("quality.ncr.close")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(NonConformance).where(
        NonConformance.id == ncr_id,
        NonConformance.organization_id == org_id
    )
    result = await db.execute(stmt)
    ncr = result.scalar_one_or_none()
    if not ncr:
        raise HTTPException(status_code=404, detail="NCR not found")
    
    ncr.status = "closed"
    ncr.closed_date = date.today()
    ncr.closed_by_user_id = user.id
    ncr.closed_by_name = user.nombre_completo
    ncr.action_completed_date = date.today()
    
    await db.commit()
    await db.refresh(ncr)
    return ncr


# Quality Specifications

@router.post("/specifications")
async def create_specification(
    payload: SpecificationCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("quality.specs.create")),
    org_id: int = Depends(get_org_id),
):
    # Generate spec code
    stmt = select(QualitySpecification).where(QualitySpecification.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    spec_code = f"QSPEC-{count + 1:04d}"
    
    spec = QualitySpecification(
        organization_id=org_id,
        spec_code=spec_code,
        **payload.model_dump()
    )
    db.add(spec)
    await db.commit()
    await db.refresh(spec)
    return spec


@router.get("/specifications")
async def list_specifications(
    product_id: Optional[int] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("quality.specs.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(QualitySpecification).where(QualitySpecification.organization_id == org_id)
    if product_id:
        query = query.where(QualitySpecification.product_id == product_id)
    if status:
        query = query.where(QualitySpecification.status == status)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/specifications/{spec_id}/lines")
async def add_spec_line(
    spec_id: int,
    payload: SpecLineCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("quality.specs.manage")),
    org_id: int = Depends(get_org_id),
):
    # Get line count
    stmt = select(QualitySpecificationLine).where(
        QualitySpecificationLine.organization_id == org_id,
        QualitySpecificationLine.specification_id == spec_id
    )
    result = await db.execute(stmt)
    line_number = len(result.scalars().all()) + 1
    
    line = QualitySpecificationLine(
        organization_id=org_id,
        specification_id=spec_id,
        line_number=line_number,
        **payload.model_dump()
    )
    db.add(line)
    await db.commit()
    await db.refresh(line)
    return line


@router.get("/specifications/{spec_id}/lines")
async def list_spec_lines(
    spec_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("quality.specs.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(QualitySpecificationLine).where(
        QualitySpecificationLine.organization_id == org_id,
        QualitySpecificationLine.specification_id == spec_id
    ).order_by(QualitySpecificationLine.line_number)
    result = await db.execute(query)
    return result.scalars().all()


# Quality Audits

@router.post("/audits")
async def create_audit(
    payload: AuditCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("quality.audits.create")),
    org_id: int = Depends(get_org_id),
):
    # Generate audit number
    stmt = select(QualityAudit).where(QualityAudit.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    audit_number = f"AUD-{datetime.now().strftime('%Y%m')}-{count + 1:04d}"
    
    audit = QualityAudit(
        organization_id=org_id,
        audit_number=audit_number,
        **payload.model_dump()
    )
    db.add(audit)
    await db.commit()
    await db.refresh(audit)
    return audit


@router.get("/audits")
async def list_audits(
    status: Optional[str] = None,
    audit_type: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("quality.audits.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(QualityAudit).where(QualityAudit.organization_id == org_id)
    if status:
        query = query.where(QualityAudit.status == status)
    if audit_type:
        query = query.where(QualityAudit.audit_type == audit_type)
    query = query.order_by(QualityAudit.scheduled_date.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/audits/{audit_id}/complete")
async def complete_audit(
    audit_id: int,
    findings_count: int,
    ncrs_raised: int,
    audit_report: str,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("quality.audits.manage")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(QualityAudit).where(
        QualityAudit.id == audit_id,
        QualityAudit.organization_id == org_id
    )
    result = await db.execute(stmt)
    audit = result.scalar_one_or_none()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    
    audit.status = "completed"
    audit.completed_date = date.today()
    audit.findings_count = findings_count
    audit.ncrs_raised = ncrs_raised
    audit.audit_report = audit_report
    
    await db.commit()
    await db.refresh(audit)
    return audit
