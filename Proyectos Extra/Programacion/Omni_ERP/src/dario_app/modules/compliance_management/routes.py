"""
Compliance Management Module - Routes
REST API endpoints for compliance frameworks, regulations, audits, and violations
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import List, Optional
from datetime import datetime, date

from dario_app.database import get_db
from dario_app.modules.compliance_management.models import (
    ComplianceFramework, Regulation, CertificationProcess,
    ComplianceAudit, ViolationReport
)

router = APIRouter(prefix="/compliance", tags=["Compliance Management"])


# ============================================================================
# COMPLIANCE FRAMEWORKS
# ============================================================================

@router.post("/frameworks")
async def create_framework(
    organization_id: int,
    name: str,
    framework_type: str,
    description: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Create a compliance framework"""
    result = await db.execute(
        select(func.count(ComplianceFramework.id)).where(
            ComplianceFramework.organization_id == organization_id
        )
    )
    count = result.scalar() or 0
    framework_code = f"FRM-{count + 1:04d}"
    
    framework = ComplianceFramework(
        organization_id=organization_id,
        framework_code=framework_code,
        name=name,
        framework_type=framework_type,
        description=description,
        created_by="system"
    )
    
    db.add(framework)
    await db.commit()
    await db.refresh(framework)
    return framework


@router.get("/frameworks")
async def get_frameworks(
    organization_id: int,
    framework_type: Optional[str] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all compliance frameworks"""
    query = select(ComplianceFramework).where(
        ComplianceFramework.organization_id == organization_id
    )
    
    if framework_type:
        query = query.where(ComplianceFramework.framework_type == framework_type)
    if status:
        query = query.where(ComplianceFramework.status == status)
    
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/frameworks/{framework_id}")
async def get_framework(framework_id: int, db: AsyncSession = Depends(get_db)):
    """Get framework details with regulations"""
    result = await db.execute(
        select(ComplianceFramework).where(ComplianceFramework.id == framework_id)
    )
    framework = result.scalar_one_or_none()
    if not framework:
        raise HTTPException(status_code=404, detail="Framework not found")
    return framework


# ============================================================================
# REGULATIONS
# ============================================================================

@router.post("/regulations")
async def create_regulation(
    organization_id: int,
    framework_id: int,
    title: str,
    requirement_text: str,
    reference_number: Optional[str] = None,
    risk_level: str = "Medium",
    db: AsyncSession = Depends(get_db)
):
    """Create a regulation/requirement"""
    result = await db.execute(
        select(func.count(Regulation.id)).where(
            Regulation.organization_id == organization_id
        )
    )
    count = result.scalar() or 0
    regulation_code = f"REG-{count + 1:04d}"
    
    regulation = Regulation(
        organization_id=organization_id,
        framework_id=framework_id,
        regulation_code=regulation_code,
        title=title,
        requirement_text=requirement_text,
        reference_number=reference_number,
        risk_level=risk_level,
        created_by="system"
    )
    
    db.add(regulation)
    await db.commit()
    await db.refresh(regulation)
    return regulation


@router.get("/regulations")
async def get_regulations(
    organization_id: int,
    framework_id: Optional[int] = None,
    compliance_status: Optional[str] = None,
    risk_level: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all regulations"""
    query = select(Regulation).where(Regulation.organization_id == organization_id)
    
    if framework_id:
        query = query.where(Regulation.framework_id == framework_id)
    if compliance_status:
        query = query.where(Regulation.compliance_status == compliance_status)
    if risk_level:
        query = query.where(Regulation.risk_level == risk_level)
    
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/regulations/{regulation_id}/assess")
async def assess_regulation_compliance(
    regulation_id: int,
    compliance_status: str,
    compliance_percentage: float,
    db: AsyncSession = Depends(get_db)
):
    """Assess compliance status of a regulation"""
    result = await db.execute(
        select(Regulation).where(Regulation.id == regulation_id)
    )
    regulation = result.scalar_one_or_none()
    if not regulation:
        raise HTTPException(status_code=404, detail="Regulation not found")
    
    regulation.compliance_status = compliance_status
    regulation.compliance_percentage = compliance_percentage
    regulation.last_assessed_date = date.today()
    
    await db.commit()
    await db.refresh(regulation)
    return regulation


# ============================================================================
# CERTIFICATION PROCESSES
# ============================================================================

@router.post("/certifications")
async def create_certification_process(
    organization_id: int,
    certification_name: str,
    framework_id: Optional[int] = None,
    certification_type: str = "Initial",
    db: AsyncSession = Depends(get_db)
):
    """Create a certification process"""
    result = await db.execute(
        select(func.count(CertificationProcess.id)).where(
            CertificationProcess.organization_id == organization_id
        )
    )
    count = result.scalar() or 0
    cert_code = f"CERT-{count + 1:04d}"
    
    certification = CertificationProcess(
        organization_id=organization_id,
        framework_id=framework_id,
        certification_code=cert_code,
        certification_name=certification_name,
        certification_type=certification_type,
        created_by="system"
    )
    
    db.add(certification)
    await db.commit()
    await db.refresh(certification)
    return certification


@router.get("/certifications")
async def get_certifications(
    organization_id: int,
    status: Optional[str] = None,
    certification_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all certification processes"""
    query = select(CertificationProcess).where(
        CertificationProcess.organization_id == organization_id
    )
    
    if status:
        query = query.where(CertificationProcess.status == status)
    if certification_type:
        query = query.where(CertificationProcess.certification_type == certification_type)
    
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/certifications/{cert_id}/update-stage")
async def update_certification_stage(
    cert_id: int,
    current_stage: str,
    stage_progress_percentage: float,
    db: AsyncSession = Depends(get_db)
):
    """Update certification process stage"""
    result = await db.execute(
        select(CertificationProcess).where(CertificationProcess.id == cert_id)
    )
    cert = result.scalar_one_or_none()
    if not cert:
        raise HTTPException(status_code=404, detail="Certification not found")
    
    cert.current_stage = current_stage
    cert.stage_progress_percentage = stage_progress_percentage
    
    await db.commit()
    await db.refresh(cert)
    return cert


# ============================================================================
# COMPLIANCE AUDITS
# ============================================================================

@router.post("/audits")
async def create_audit(
    organization_id: int,
    audit_name: str,
    audit_type: str,
    planned_start_date: date,
    planned_end_date: date,
    framework_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """Create a compliance audit"""
    result = await db.execute(
        select(func.count(ComplianceAudit.id)).where(
            ComplianceAudit.organization_id == organization_id
        )
    )
    count = result.scalar() or 0
    audit_code = f"AUD-{count + 1:04d}"
    
    audit = ComplianceAudit(
        organization_id=organization_id,
        framework_id=framework_id,
        audit_code=audit_code,
        audit_name=audit_name,
        audit_type=audit_type,
        planned_start_date=planned_start_date,
        planned_end_date=planned_end_date,
        created_by="system"
    )
    
    db.add(audit)
    await db.commit()
    await db.refresh(audit)
    return audit


@router.get("/audits")
async def get_audits(
    organization_id: int,
    status: Optional[str] = None,
    audit_type: Optional[str] = None,
    framework_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all compliance audits"""
    query = select(ComplianceAudit).where(
        ComplianceAudit.organization_id == organization_id
    )
    
    if status:
        query = query.where(ComplianceAudit.status == status)
    if audit_type:
        query = query.where(ComplianceAudit.audit_type == audit_type)
    if framework_id:
        query = query.where(ComplianceAudit.framework_id == framework_id)
    
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/audits/{audit_id}/complete")
async def complete_audit(
    audit_id: int,
    overall_compliance_score: float,
    overall_risk_rating: str,
    is_passed: bool,
    db: AsyncSession = Depends(get_db)
):
    """Complete an audit with final results"""
    result = await db.execute(
        select(ComplianceAudit).where(ComplianceAudit.id == audit_id)
    )
    audit = result.scalar_one_or_none()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    
    audit.status = "Finalized"
    audit.actual_end_date = date.today()
    audit.overall_compliance_score = overall_compliance_score
    audit.overall_risk_rating = overall_risk_rating
    audit.is_passed = is_passed
    audit.final_report_date = date.today()
    
    await db.commit()
    await db.refresh(audit)
    return audit


# ============================================================================
# VIOLATION REPORTS
# ============================================================================

@router.post("/violations")
async def create_violation(
    organization_id: int,
    title: str,
    description: str,
    regulation_id: Optional[int] = None,
    severity: str = "Medium",
    discovered_date: Optional[date] = None,
    db: AsyncSession = Depends(get_db)
):
    """Report a compliance violation"""
    result = await db.execute(
        select(func.count(ViolationReport.id)).where(
            ViolationReport.organization_id == organization_id
        )
    )
    count = result.scalar() or 0
    violation_code = f"VIO-{count + 1:04d}"
    
    violation = ViolationReport(
        organization_id=organization_id,
        regulation_id=regulation_id,
        violation_code=violation_code,
        title=title,
        description=description,
        severity=severity,
        discovered_date=discovered_date or date.today(),
        created_by="system"
    )
    
    db.add(violation)
    await db.commit()
    await db.refresh(violation)
    return violation


@router.get("/violations")
async def get_violations(
    organization_id: int,
    status: Optional[str] = None,
    severity: Optional[str] = None,
    regulation_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all violation reports"""
    query = select(ViolationReport).where(
        ViolationReport.organization_id == organization_id
    )
    
    if status:
        query = query.where(ViolationReport.status == status)
    if severity:
        query = query.where(ViolationReport.severity == severity)
    if regulation_id:
        query = query.where(ViolationReport.regulation_id == regulation_id)
    
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/violations/{violation_id}/resolve")
async def resolve_violation(
    violation_id: int,
    corrective_action_plan: str,
    corrective_action_owner: str,
    corrective_action_deadline: date,
    db: AsyncSession = Depends(get_db)
):
    """Resolve a violation with corrective action"""
    result = await db.execute(
        select(ViolationReport).where(ViolationReport.id == violation_id)
    )
    violation = result.scalar_one_or_none()
    if not violation:
        raise HTTPException(status_code=404, detail="Violation not found")
    
    violation.status = "In_Progress"
    violation.corrective_action_plan = corrective_action_plan
    violation.corrective_action_owner = corrective_action_owner
    violation.corrective_action_deadline = corrective_action_deadline
    
    await db.commit()
    await db.refresh(violation)
    return violation


@router.get("/analytics/compliance-dashboard")
async def get_compliance_dashboard(
    organization_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get compliance dashboard analytics"""
    # Overall compliance
    frameworks_result = await db.execute(
        select(
            func.count(ComplianceFramework.id),
            func.avg(ComplianceFramework.compliance_percentage)
        ).where(ComplianceFramework.organization_id == organization_id)
    )
    total_frameworks, avg_compliance = frameworks_result.first()
    
    # Active violations
    violations_result = await db.execute(
        select(func.count(ViolationReport.id)).where(
            and_(
                ViolationReport.organization_id == organization_id,
                ViolationReport.status.in_(["Open", "In_Progress"])
            )
        )
    )
    active_violations = violations_result.scalar() or 0
    
    # Recent audits
    audits_result = await db.execute(
        select(ComplianceAudit).where(
            ComplianceAudit.organization_id == organization_id
        ).order_by(ComplianceAudit.created_at.desc()).limit(5)
    )
    recent_audits = audits_result.scalars().all()
    
    return {
        "total_frameworks": total_frameworks or 0,
        "avg_compliance_percentage": float(avg_compliance) if avg_compliance else 0,
        "active_violations": active_violations,
        "recent_audits": [
            {
                "audit_name": a.audit_name,
                "audit_type": a.audit_type,
                "status": a.status,
                "compliance_score": a.overall_compliance_score
            } for a in recent_audits
        ]
    }
