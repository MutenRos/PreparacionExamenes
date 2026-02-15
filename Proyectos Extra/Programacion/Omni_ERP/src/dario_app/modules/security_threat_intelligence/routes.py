"""
Advanced Security & Threat Intelligence - Routes
Operations for alerts, indicators, vulnerabilities, and incidents.
"""
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.database import get_db
from dario_app.modules.security_threat_intelligence.models import (
    ThreatIndicator,
    SecurityAlert,
    Vulnerability,
    Incident,
    SecurityAssessment,
)

router = APIRouter(prefix="/security-threat", tags=["Security & Threat Intelligence"])


# Threat indicators
@router.post("/indicators")
async def create_indicator(
    organization_id: int,
    indicator_type: str,
    value: str,
    confidence: Optional[int] = None,
    source: Optional[str] = None,
    tags: Optional[dict] = None,
    db: AsyncSession = Depends(get_db),
):
    indicator = ThreatIndicator(
        organization_id=organization_id,
        indicator_type=indicator_type,
        value=value,
        confidence=confidence,
        source=source,
        tags=tags or {},
        last_seen=datetime.utcnow(),
    )
    db.add(indicator)
    await db.commit()
    await db.refresh(indicator)
    return indicator


@router.get("/indicators")
async def list_indicators(organization_id: int, is_active: Optional[bool] = None, db: AsyncSession = Depends(get_db)):
    query = select(ThreatIndicator).where(ThreatIndicator.organization_id == organization_id)
    if is_active is not None:
        query = query.where(ThreatIndicator.is_active == is_active)
    result = await db.execute(query)
    return result.scalars().all()


# Alerts
@router.post("/alerts")
async def create_alert(
    organization_id: int,
    title: str,
    severity: str = "Medium",
    category: Optional[str] = None,
    description: Optional[str] = None,
    indicators: Optional[dict] = None,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(func.count(SecurityAlert.id)))
    count = result.scalar() or 0
    alert_code = f"ALRT-{count + 1:06d}"

    alert = SecurityAlert(
        organization_id=organization_id,
        alert_code=alert_code,
        title=title,
        severity=severity,
        category=category,
        description=description,
        indicators=indicators or {},
    )
    db.add(alert)
    await db.commit()
    await db.refresh(alert)
    return alert


@router.patch("/alerts/{alert_id}/status")
async def update_alert_status(
    alert_id: int,
    status: str,
    owner: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(SecurityAlert).where(SecurityAlert.id == alert_id))
    alert = result.scalar_one_or_none()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert.status = status
    if owner:
        alert.owner = owner
    if status == "Resolved":
        alert.resolved_at = datetime.utcnow()
    elif status == "In_Progress" and not alert.acknowledged_at:
        alert.acknowledged_at = datetime.utcnow()

    alert.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(alert)
    return alert


# Vulnerabilities
@router.post("/vulnerabilities")
async def create_vulnerability(
    organization_id: int,
    asset: str,
    cve_id: Optional[str] = None,
    severity: str = "Medium",
    cvss_score: Optional[int] = None,
    remediation_plan: Optional[str] = None,
    due_date: Optional[datetime] = None,
    db: AsyncSession = Depends(get_db),
):
    vul = Vulnerability(
        organization_id=organization_id,
        asset=asset,
        cve_id=cve_id,
        severity=severity,
        cvss_score=cvss_score,
        remediation_plan=remediation_plan,
        due_date=due_date,
    )
    db.add(vul)
    await db.commit()
    await db.refresh(vul)
    return vul


@router.patch("/vulnerabilities/{vul_id}/status")
async def update_vulnerability_status(
    vul_id: int,
    status: Optional[str] = None,
    remediation_owner: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Vulnerability).where(Vulnerability.id == vul_id))
    vul = result.scalar_one_or_none()
    if not vul:
        raise HTTPException(status_code=404, detail="Vulnerability not found")

    if status:
        vul.status = status
        if status == "Resolved":
            vul.resolved_at = datetime.utcnow()
    if remediation_owner:
        vul.remediation_owner = remediation_owner
    vul.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(vul)
    return vul


# Incidents
@router.post("/incidents")
async def create_incident(
    organization_id: int,
    title: str,
    severity: str = "Medium",
    category: Optional[str] = None,
    affected_assets: Optional[dict] = None,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(func.count(Incident.id)))
    count = result.scalar() or 0
    incident_code = f"INC-{count + 1:06d}"

    inc = Incident(
        organization_id=organization_id,
        incident_code=incident_code,
        title=title,
        severity=severity,
        category=category,
        affected_assets=affected_assets or {},
    )
    db.add(inc)
    await db.commit()
    await db.refresh(inc)
    return inc


@router.patch("/incidents/{incident_id}/status")
async def update_incident_status(
    incident_id: int,
    status: str,
    impact: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Incident).where(Incident.id == incident_id))
    inc = result.scalar_one_or_none()
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")

    inc.status = status
    if impact:
        inc.impact = impact
    now = datetime.utcnow()
    if status == "Contained":
        inc.contained_at = now
    if status == "Recovered":
        inc.recovered_at = now
    if status == "Closed":
        inc.closed_at = now
    inc.updated_at = now

    await db.commit()
    await db.refresh(inc)
    return inc


# Assessments
@router.post("/assessments")
async def create_assessment(
    organization_id: int,
    framework: str,
    scope: Optional[str] = None,
    status: str = "Planned",
    recommendations: Optional[dict] = None,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(func.count(SecurityAssessment.id)))
    count = result.scalar() or 0
    assessment_code = f"ASMT-{count + 1:05d}"

    assessment = SecurityAssessment(
        organization_id=organization_id,
        assessment_code=assessment_code,
        framework=framework,
        scope=scope,
        status=status,
        recommendations=recommendations or {},
    )
    db.add(assessment)
    await db.commit()
    await db.refresh(assessment)
    return assessment


@router.patch("/assessments/{assessment_id}/complete")
async def complete_assessment(
    assessment_id: int,
    score: Optional[int] = None,
    findings: Optional[dict] = None,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(SecurityAssessment).where(SecurityAssessment.id == assessment_id))
    assessment = result.scalar_one_or_none()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    assessment.status = "Completed"
    assessment.score = score
    assessment.findings = findings or assessment.findings
    assessment.completed_at = datetime.utcnow()
    assessment.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(assessment)
    return assessment


# Analytics
@router.get("/analytics/security-posture")
async def security_posture(organization_id: int, db: AsyncSession = Depends(get_db)):
    """Summaries for alerts, vulnerabilities, and incidents."""
    alert_counts = await db.execute(
        select(SecurityAlert.severity, func.count(SecurityAlert.id))
        .where(SecurityAlert.organization_id == organization_id)
        .group_by(SecurityAlert.severity)
    )
    vul_counts = await db.execute(
        select(Vulnerability.status, func.count(Vulnerability.id))
        .where(Vulnerability.organization_id == organization_id)
        .group_by(Vulnerability.status)
    )
    incident_counts = await db.execute(
        select(Incident.status, func.count(Incident.id))
        .where(Incident.organization_id == organization_id)
        .group_by(Incident.status)
    )
    return {
        "alerts": {row[0]: row[1] for row in alert_counts.all()},
        "vulnerabilities": {row[0]: row[1] for row in vul_counts.all()},
        "incidents": {row[0]: row[1] for row in incident_counts.all()},
    }
