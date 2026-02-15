"""
Multi-Channel Communication Hub - Routes
Omni-channel messaging across email, SMS, chat, and social.
"""
from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.database import get_db
from dario_app.modules.communication_hub.models import (
    CommunicationChannel,
    MessageTemplate,
    ConversationThread,
    Message,
    ContactPreference,
)

router = APIRouter(prefix="/communication-hub", tags=["Communication Hub"])


# Channels
@router.post("/channels")
async def create_channel(
    organization_id: int,
    channel_type: str,
    provider: Optional[str] = None,
    configuration: Optional[dict] = None,
    is_default: bool = False,
    db: AsyncSession = Depends(get_db),
):
    """Create a new communication channel."""
    result = await db.execute(
        select(func.count(CommunicationChannel.id)).where(CommunicationChannel.organization_id == organization_id)
    )
    count = result.scalar() or 0
    channel_code = f"COMM-{count + 1:04d}"

    channel = CommunicationChannel(
        organization_id=organization_id,
        channel_code=channel_code,
        channel_type=channel_type,
        provider=provider,
        configuration=configuration or {},
        is_default=is_default,
        created_by="system",
    )
    db.add(channel)
    await db.commit()
    await db.refresh(channel)
    return channel


@router.get("/channels")
async def list_channels(
    organization_id: int,
    channel_type: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: AsyncSession = Depends(get_db),
):
    """List configured channels."""
    query = select(CommunicationChannel).where(CommunicationChannel.organization_id == organization_id)
    if channel_type:
        query = query.where(CommunicationChannel.channel_type == channel_type)
    if is_active is not None:
        query = query.where(CommunicationChannel.is_active == is_active)
    result = await db.execute(query)
    return result.scalars().all()


# Templates
@router.post("/templates")
async def create_template(
    organization_id: int,
    channel_id: int,
    name: str,
    subject: Optional[str] = None,
    body: Optional[str] = None,
    category: Optional[str] = None,
    variables: Optional[dict] = None,
    db: AsyncSession = Depends(get_db),
):
    """Create a reusable template."""
    result = await db.execute(
        select(func.count(MessageTemplate.id)).where(MessageTemplate.organization_id == organization_id)
    )
    count = result.scalar() or 0
    template_code = f"TPL-{count + 1:04d}"

    template = MessageTemplate(
        organization_id=organization_id,
        channel_id=channel_id,
        template_code=template_code,
        name=name,
        subject=subject,
        body=body,
        category=category,
        variables=variables or {},
        created_by="system",
    )
    db.add(template)
    await db.commit()
    await db.refresh(template)
    return template


@router.get("/templates")
async def list_templates(
    organization_id: int,
    channel_id: Optional[int] = None,
    category: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: AsyncSession = Depends(get_db),
):
    """List templates with filters."""
    query = select(MessageTemplate).where(MessageTemplate.organization_id == organization_id)
    if channel_id:
        query = query.where(MessageTemplate.channel_id == channel_id)
    if category:
        query = query.where(MessageTemplate.category == category)
    if is_active is not None:
        query = query.where(MessageTemplate.is_active == is_active)
    result = await db.execute(query)
    return result.scalars().all()


# Threads
@router.post("/threads")
async def create_thread(
    organization_id: int,
    channel_id: int,
    subject: Optional[str] = None,
    customer_id: Optional[int] = None,
    contact_point: Optional[str] = None,
    priority: str = "Normal",
    db: AsyncSession = Depends(get_db),
):
    """Open a conversation thread."""
    result = await db.execute(select(func.count(ConversationThread.id)))
    count = result.scalar() or 0
    thread_code = f"THR-{count + 1:05d}"

    thread = ConversationThread(
        organization_id=organization_id,
        channel_id=channel_id,
        thread_code=thread_code,
        subject=subject,
        customer_id=customer_id,
        contact_point=contact_point,
        priority=priority,
        unread_count=0,
    )
    db.add(thread)
    await db.commit()
    await db.refresh(thread)
    return thread


@router.get("/threads")
async def list_threads(
    organization_id: int,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """List conversation threads."""
    query = select(ConversationThread).where(ConversationThread.organization_id == organization_id)
    if status:
        query = query.where(ConversationThread.status == status)
    if priority:
        query = query.where(ConversationThread.priority == priority)
    query = query.order_by(ConversationThread.updated_at.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/threads/{thread_id}")
async def get_thread(thread_id: int, db: AsyncSession = Depends(get_db)):
    """Get thread details with messages."""
    result = await db.execute(select(ConversationThread).where(ConversationThread.id == thread_id))
    thread = result.scalar_one_or_none()
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    return thread


@router.post("/threads/{thread_id}/messages")
async def send_message(
    thread_id: int,
    organization_id: int,
    direction: str,
    body: str,
    channel_type: Optional[str] = None,
    sender: Optional[str] = None,
    recipient: Optional[str] = None,
    subject: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """Append a message to a thread and update counters."""
    result = await db.execute(select(ConversationThread).where(ConversationThread.id == thread_id))
    thread = result.scalar_one_or_none()
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")

    message = Message(
        organization_id=organization_id,
        thread_id=thread_id,
        direction=direction,
        channel_type=channel_type,
        sender=sender,
        recipient=recipient,
        subject=subject,
        body=body,
        status="Sent" if direction == "Outbound" else "Delivered",
        sent_at=datetime.utcnow(),
    )
    db.add(message)

    now = datetime.utcnow()
    thread.last_message_at = now
    if direction == "Inbound":
        thread.last_inbound_at = now
        thread.unread_count = (thread.unread_count or 0) + 1
    else:
        thread.last_outbound_at = now

    await db.commit()
    await db.refresh(message)
    await db.refresh(thread)
    return {"message": message, "thread": thread}


@router.patch("/threads/{thread_id}/status")
async def update_thread_status(
    thread_id: int,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    unread_count: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    """Update thread status or counters."""
    result = await db.execute(select(ConversationThread).where(ConversationThread.id == thread_id))
    thread = result.scalar_one_or_none()
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")

    if status:
        thread.status = status
    if priority:
        thread.priority = priority
    if unread_count is not None:
        thread.unread_count = unread_count
    thread.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(thread)
    return thread


# Contact preferences
@router.post("/contact-preferences")
async def upsert_contact_preference(
    organization_id: int,
    customer_id: int,
    preferred_channels: Optional[List[str]] = None,
    quiet_hours: Optional[dict] = None,
    opt_in_marketing: Optional[bool] = None,
    opt_in_service: Optional[bool] = None,
    blocked: Optional[bool] = None,
    db: AsyncSession = Depends(get_db),
):
    """Upsert contact preferences for a customer."""
    result = await db.execute(
        select(ContactPreference).where(
            ContactPreference.organization_id == organization_id,
            ContactPreference.customer_id == customer_id,
        )
    )
    pref = result.scalar_one_or_none()
    if not pref:
        pref = ContactPreference(
            organization_id=organization_id,
            customer_id=customer_id,
        )
        db.add(pref)

    if preferred_channels is not None:
        pref.preferred_channels = preferred_channels
    if quiet_hours is not None:
        pref.quiet_hours = quiet_hours
    if opt_in_marketing is not None:
        pref.opt_in_marketing = opt_in_marketing
    if opt_in_service is not None:
        pref.opt_in_service = opt_in_service
    if blocked is not None:
        pref.blocked = blocked
    pref.updated_at = datetime.utcnow()
    pref.updated_by = "system"

    await db.commit()
    await db.refresh(pref)
    return pref


# Analytics
@router.get("/analytics/channel-performance")
async def channel_performance(organization_id: int, db: AsyncSession = Depends(get_db)):
    """Aggregate message counts per channel type."""
    result = await db.execute(
        select(Message.channel_type, func.count(Message.id))
        .where(Message.organization_id == organization_id)
        .group_by(Message.channel_type)
    )
    rows = result.all()
    return {row[0] or "Unknown": row[1] for row in rows}
