"""
Customer Self-Service Portal - Routes
Portal operations for cases, requests, feedback, and knowledge views.
"""
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.database import get_db
from dario_app.modules.self_service_portal.models import (
    PortalUserProfile,
    PortalCase,
    PortalRequest,
    PortalFeedback,
    PortalKnowledgeView,
)

router = APIRouter(prefix="/self-service-portal", tags=["Self-Service Portal"])


# Users
@router.post("/users")
async def create_portal_user(
    organization_id: int,
    contact_email: str,
    display_name: Optional[str] = None,
    locale: str = "en-US",
    time_zone: str = "UTC",
    db: AsyncSession = Depends(get_db),
):
    """Create a portal user profile."""
    profile = PortalUserProfile(
        organization_id=organization_id,
        contact_email=contact_email,
        display_name=display_name,
        locale=locale,
        time_zone=time_zone,
    )
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    return profile


@router.get("/users")
async def list_portal_users(organization_id: int, status: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    """List portal users."""
    query = select(PortalUserProfile).where(PortalUserProfile.organization_id == organization_id)
    if status:
        query = query.where(PortalUserProfile.status == status)
    result = await db.execute(query)
    return result.scalars().all()


# Cases
@router.post("/cases")
async def create_case(
    organization_id: int,
    user_id: int,
    subject: str,
    description: Optional[str] = None,
    category: Optional[str] = None,
    priority: str = "Normal",
    db: AsyncSession = Depends(get_db),
):
    """Create a support case from the portal."""
    result = await db.execute(select(func.count(PortalCase.id)))
    count = result.scalar() or 0
    case_number = f"CASE-{count + 1:06d}"

    case = PortalCase(
        organization_id=organization_id,
        user_id=user_id,
        case_number=case_number,
        subject=subject,
        description=description,
        category=category,
        priority=priority,
    )
    db.add(case)
    await db.commit()
    await db.refresh(case)
    return case


@router.get("/cases")
async def list_cases(
    organization_id: int,
    status: Optional[str] = None,
    user_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    """List portal cases."""
    query = select(PortalCase).where(PortalCase.organization_id == organization_id)
    if status:
        query = query.where(PortalCase.status == status)
    if user_id:
        query = query.where(PortalCase.user_id == user_id)
    query = query.order_by(PortalCase.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/cases/{case_id}/status")
async def update_case_status(
    case_id: int,
    status: Optional[str] = None,
    assigned_to: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """Update case status or assignment."""
    result = await db.execute(select(PortalCase).where(PortalCase.id == case_id))
    case = result.scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    if status:
        case.status = status
        if status == "Resolved":
            case.resolved_at = datetime.utcnow()
    if assigned_to:
        case.assigned_to = assigned_to
    case.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(case)
    return case


# Requests
@router.post("/requests")
async def create_request(
    organization_id: int,
    user_id: int,
    request_type: str,
    details: Optional[dict] = None,
    priority: str = "Normal",
    db: AsyncSession = Depends(get_db),
):
    """Create a portal service request."""
    result = await db.execute(select(func.count(PortalRequest.id)))
    count = result.scalar() or 0
    request_number = f"REQ-{count + 1:06d}"

    req = PortalRequest(
        organization_id=organization_id,
        user_id=user_id,
        request_number=request_number,
        request_type=request_type,
        details=details or {},
        priority=priority,
    )
    db.add(req)
    await db.commit()
    await db.refresh(req)
    return req


@router.patch("/requests/{request_id}/status")
async def update_request_status(
    request_id: int,
    status: Optional[str] = None,
    scheduled_at: Optional[datetime] = None,
    completed_at: Optional[datetime] = None,
    db: AsyncSession = Depends(get_db),
):
    """Update portal request status."""
    result = await db.execute(select(PortalRequest).where(PortalRequest.id == request_id))
    req = result.scalar_one_or_none()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")

    if status:
        req.status = status
    if scheduled_at:
        req.scheduled_at = scheduled_at
    if completed_at:
        req.completed_at = completed_at
    req.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(req)
    return req


# Feedback
@router.post("/feedback")
async def submit_feedback(
    organization_id: int,
    user_id: int,
    rating: int,
    comment: Optional[str] = None,
    category: Optional[str] = None,
    target_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    """Submit portal feedback."""
    feedback = PortalFeedback(
        organization_id=organization_id,
        user_id=user_id,
        rating=rating,
        comment=comment,
        category=category,
        target_id=target_id,
    )
    db.add(feedback)
    await db.commit()
    await db.refresh(feedback)
    return feedback


# Knowledge views
@router.post("/knowledge/views")
async def record_knowledge_view(
    organization_id: int,
    user_id: int,
    article_id: int,
    duration_seconds: Optional[int] = None,
    device_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """Record an article view from the portal."""
    view = PortalKnowledgeView(
        organization_id=organization_id,
        user_id=user_id,
        article_id=article_id,
        duration_seconds=duration_seconds,
        device_type=device_type,
    )
    db.add(view)
    await db.commit()
    await db.refresh(view)
    return view


# Analytics
@router.get("/analytics/portal-health")
async def portal_health(organization_id: int, db: AsyncSession = Depends(get_db)):
    """Key metrics: open cases, resolved cases, average rating."""
    open_cases = await db.execute(
        select(func.count(PortalCase.id)).where(
            PortalCase.organization_id == organization_id, PortalCase.status != "Resolved"
        )
    )
    resolved_cases = await db.execute(
        select(func.count(PortalCase.id)).where(
            PortalCase.organization_id == organization_id, PortalCase.status == "Resolved"
        )
    )
    ratings = await db.execute(
        select(func.avg(PortalFeedback.rating)).where(PortalFeedback.organization_id == organization_id)
    )
    return {
        "open_cases": open_cases.scalar() or 0,
        "resolved_cases": resolved_cases.scalar() or 0,
        "average_rating": float(ratings.scalar() or 0),
    }
