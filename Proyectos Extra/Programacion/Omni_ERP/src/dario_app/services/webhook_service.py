"""Enterprise webhook service for integrations."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
import asyncio
import json
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Index
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import httpx

from dario_app.database import Base


class WebhookStatus(str, Enum):
    """Webhook delivery status."""
    PENDING = "pending"
    DELIVERED = "delivered"
    FAILED = "failed"
    RETRYING = "retrying"


class Webhook(Base):
    """Webhook configuration model."""
    
    __tablename__ = "webhooks"
    
    id: int = Column(Integer, primary_key=True, index=True)
    organization_id: int = Column(Integer, nullable=False, index=True)
    
    # Configuration
    name: str = Column(String(200), nullable=False)
    url: str = Column(String(500), nullable=False)
    event_types: str = Column(Text, nullable=False)  # JSON array
    secret: str = Column(String(100), nullable=True)
    
    # Status
    is_active: bool = Column(Boolean, default=True, nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_triggered: datetime = Column(DateTime, nullable=True)
    
    # Stats
    success_count: int = Column(Integer, default=0, nullable=False)
    failure_count: int = Column(Integer, default=0, nullable=False)


class WebhookDelivery(Base):
    """Webhook delivery log."""
    
    __tablename__ = "webhook_deliveries"
    
    id: int = Column(Integer, primary_key=True, index=True)
    webhook_id: int = Column(Integer, nullable=False, index=True)
    organization_id: int = Column(Integer, nullable=False, index=True)
    
    # Request
    event_type: str = Column(String(100), nullable=False)
    payload: str = Column(Text, nullable=False)  # JSON
    
    # Response
    status: str = Column(String(20), default="pending", nullable=False)
    status_code: int = Column(Integer, nullable=True)
    response_body: str = Column(Text, nullable=True)
    error_message: str = Column(Text, nullable=True)
    
    # Timing
    created_at: datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
    delivered_at: datetime = Column(DateTime, nullable=True)
    retry_count: int = Column(Integer, default=0, nullable=False)
    next_retry_at: datetime = Column(DateTime, nullable=True)
    
    __table_args__ = (
        Index('ix_webhook_deliveries_status', 'status', 'next_retry_at'),
    )


class WebhookService:
    """Enterprise webhook service."""
    
    def __init__(self):
        self._client = httpx.AsyncClient(timeout=30.0)
    
    async def create_webhook(
        self,
        db: AsyncSession,
        organization_id: int,
        name: str,
        url: str,
        event_types: list[str],
        secret: Optional[str] = None
    ) -> Webhook:
        """Create new webhook configuration."""
        webhook = Webhook(
            organization_id=organization_id,
            name=name,
            url=url,
            event_types=json.dumps(event_types),
            secret=secret,
            is_active=True
        )
        
        db.add(webhook)
        await db.commit()
        await db.refresh(webhook)
        
        return webhook
    
    async def trigger_webhooks(
        self,
        db: AsyncSession,
        organization_id: int,
        event_type: str,
        data: Dict[str, Any]
    ):
        """Trigger all webhooks for an event."""
        # Get active webhooks
        query = select(Webhook).where(
            Webhook.organization_id == organization_id,
            Webhook.is_active == True
        )
        result = await db.execute(query)
        webhooks = result.scalars().all()
        
        # Filter by event type
        matching_webhooks = [
            wh for wh in webhooks
            if event_type in json.loads(wh.event_types)
        ]
        
        # Trigger each webhook asynchronously
        tasks = [
            self._deliver_webhook(db, webhook, event_type, data)
            for webhook in matching_webhooks
        ]
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _deliver_webhook(
        self,
        db: AsyncSession,
        webhook: Webhook,
        event_type: str,
        data: Dict[str, Any]
    ):
        """Deliver webhook to endpoint."""
        # Create delivery record
        delivery = WebhookDelivery(
            webhook_id=webhook.id,
            organization_id=webhook.organization_id,
            event_type=event_type,
            payload=json.dumps(data, default=str),
            status=WebhookStatus.PENDING.value
        )
        
        db.add(delivery)
        await db.commit()
        await db.refresh(delivery)
        
        try:
            # Prepare payload
            payload = {
                "event_type": event_type,
                "data": data,
                "timestamp": datetime.utcnow().isoformat(),
                "webhook_id": webhook.id
            }
            
            # Add signature if secret provided
            headers = {"Content-Type": "application/json"}
            if webhook.secret:
                import hmac
                import hashlib
                signature = hmac.new(
                    webhook.secret.encode(),
                    json.dumps(payload).encode(),
                    hashlib.sha256
                ).hexdigest()
                headers["X-Webhook-Signature"] = signature
            
            # Send request
            response = await self._client.post(
                webhook.url,
                json=payload,
                headers=headers
            )
            
            # Update delivery
            delivery.status = WebhookStatus.DELIVERED.value
            delivery.status_code = response.status_code
            delivery.response_body = response.text[:1000]  # Truncate
            delivery.delivered_at = datetime.utcnow()
            
            # Update webhook stats
            webhook.success_count += 1
            webhook.last_triggered = datetime.utcnow()
            
        except Exception as e:
            delivery.status = WebhookStatus.FAILED.value
            delivery.error_message = str(e)[:500]
            webhook.failure_count += 1
            
            # Schedule retry
            if delivery.retry_count < 3:
                from datetime import timedelta
                delivery.status = WebhookStatus.RETRYING.value
                delivery.next_retry_at = datetime.utcnow() + timedelta(
                    minutes=5 * (2 ** delivery.retry_count)  # Exponential backoff
                )
        
        await db.commit()
    
    async def retry_failed_deliveries(self, db: AsyncSession):
        """Retry failed webhook deliveries."""
        query = select(WebhookDelivery).where(
            WebhookDelivery.status == WebhookStatus.RETRYING.value,
            WebhookDelivery.next_retry_at <= datetime.utcnow()
        ).limit(100)
        
        result = await db.execute(query)
        deliveries = result.scalars().all()
        
        for delivery in deliveries:
            # Get webhook
            webhook_query = select(Webhook).where(Webhook.id == delivery.webhook_id)
            webhook_result = await db.execute(webhook_query)
            webhook = webhook_result.scalar_one_or_none()
            
            if webhook and webhook.is_active:
                delivery.retry_count += 1
                data = json.loads(delivery.payload)
                await self._deliver_webhook(db, webhook, delivery.event_type, data)


# Global webhook service
webhook_service = WebhookService()
