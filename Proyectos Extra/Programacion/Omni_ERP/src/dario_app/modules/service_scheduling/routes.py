"""Service Scheduling routes."""

from datetime import datetime, date, time
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.core.auth import require_permission, get_tenant_db, get_org_id
from dario_app.modules.usuarios.models import Usuario

from .models import ServiceResource, ServiceSlot, ServiceAppointment, ServiceScheduleTemplate, ResourceAvailability

router = APIRouter(prefix="/api/service-scheduling", tags=["Service Scheduling"])


# Schemas

class ResourceCreate(BaseModel):
    name: str
    resource_type: str = "technician"
    capacity: Optional[int] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class AppointmentCreate(BaseModel):
    customer_id: int
    service_type: str
    scheduled_start: str
    scheduled_end: str
    location: Optional[str] = None
    description: Optional[str] = None


# Resources

@router.post("/resources")
async def create_resource(
    payload: ResourceCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("scheduling.resources.create")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(ServiceResource).where(ServiceResource.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    resource_code = f"RES-{count + 1:04d}"
    
    resource = ServiceResource(
        organization_id=org_id,
        resource_code=resource_code,
        **payload.model_dump()
    )
    db.add(resource)
    await db.commit()
    await db.refresh(resource)
    return resource


@router.get("/resources")
async def list_resources(
    resource_type: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("scheduling.resources.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(ServiceResource).where(ServiceResource.organization_id == org_id)
    if resource_type:
        query = query.where(ServiceResource.resource_type == resource_type)
    result = await db.execute(query)
    return result.scalars().all()


# Appointments

@router.post("/appointments")
async def create_appointment(
    payload: AppointmentCreate,
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id),
):
    now = datetime.now()
    stmt = select(ServiceAppointment).where(ServiceAppointment.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    appointment_number = f"APT-{now.strftime('%Y%m%d')}-{count + 1:04d}"
    
    scheduled_start = datetime.fromisoformat(payload.scheduled_start)
    scheduled_end = datetime.fromisoformat(payload.scheduled_end)
    
    appointment = ServiceAppointment(
        organization_id=org_id,
        appointment_number=appointment_number,
        scheduled_start=scheduled_start,
        scheduled_end=scheduled_end,
        duration_minutes=int((scheduled_end - scheduled_start).total_seconds() / 60),
        **payload.model_dump(exclude={"scheduled_start", "scheduled_end"})
    )
    db.add(appointment)
    await db.commit()
    await db.refresh(appointment)
    return appointment


@router.get("/appointments")
async def list_appointments(
    status: Optional[str] = None,
    customer_id: Optional[int] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("scheduling.appointments.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(ServiceAppointment).where(ServiceAppointment.organization_id == org_id)
    if status:
        query = query.where(ServiceAppointment.status == status)
    if customer_id:
        query = query.where(ServiceAppointment.customer_id == customer_id)
    query = query.order_by(ServiceAppointment.scheduled_start.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/appointments/{appointment_id}/complete")
async def complete_appointment(
    appointment_id: int,
    completion_notes: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("scheduling.appointments.manage")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(ServiceAppointment).where(
        ServiceAppointment.id == appointment_id,
        ServiceAppointment.organization_id == org_id
    )
    result = await db.execute(stmt)
    appt = result.scalar_one_or_none()
    
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    appt.status = "completed"
    appt.actual_end = datetime.utcnow()
    if completion_notes:
        appt.completion_notes = completion_notes
    
    await db.commit()
    await db.refresh(appt)
    return appt
