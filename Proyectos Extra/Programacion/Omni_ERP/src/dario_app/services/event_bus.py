"""Enterprise event bus for event-driven architecture."""

from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, asdict
import asyncio
import json
from collections import defaultdict


class EventType(str, Enum):
    """System event types."""
    # User events
    USER_CREATED = "user.created"
    USER_UPDATED = "user.updated"
    USER_DELETED = "user.deleted"
    USER_LOGIN = "user.login"
    USER_LOGOUT = "user.logout"
    
    # Product events
    PRODUCT_CREATED = "product.created"
    PRODUCT_UPDATED = "product.updated"
    PRODUCT_DELETED = "product.deleted"
    PRODUCT_LOW_STOCK = "product.low_stock"
    PRODUCT_OUT_OF_STOCK = "product.out_of_stock"
    
    # Order events
    ORDER_CREATED = "order.created"
    ORDER_UPDATED = "order.updated"
    ORDER_APPROVED = "order.approved"
    ORDER_COMPLETED = "order.completed"
    ORDER_CANCELLED = "order.cancelled"
    
    # Purchase events
    PURCHASE_CREATED = "purchase.created"
    PURCHASE_APPROVED = "purchase.approved"
    PURCHASE_RECEIVED = "purchase.received"
    PURCHASE_COMPLETED = "purchase.completed"
    
    # Inventory events
    STOCK_UPDATED = "stock.updated"
    STOCK_MOVEMENT = "stock.movement"
    
    # Integration events
    WEBHOOK_RECEIVED = "webhook.received"
    API_ERROR = "api.error"
    
    # System events
    BACKUP_COMPLETED = "system.backup_completed"
    MAINTENANCE_STARTED = "system.maintenance_started"
    MAINTENANCE_COMPLETED = "system.maintenance_completed"


@dataclass
class Event:
    """Event data structure."""
    event_type: EventType
    org_id: int
    data: Dict[str, Any]
    timestamp: datetime = None
    user_id: Optional[int] = None
    correlation_id: Optional[str] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        result = asdict(self)
        result['event_type'] = self.event_type.value
        result['timestamp'] = self.timestamp.isoformat()
        return result
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), default=str)


class EventBus:
    """Enterprise event bus for pub/sub pattern."""
    
    def __init__(self):
        self._subscribers: Dict[EventType, List[Callable]] = defaultdict(list)
        self._event_history: List[Event] = []
        self._max_history = 1000
    
    def subscribe(self, event_type: EventType, handler: Callable):
        """Subscribe to an event type."""
        self._subscribers[event_type].append(handler)
    
    def unsubscribe(self, event_type: EventType, handler: Callable):
        """Unsubscribe from an event type."""
        if handler in self._subscribers[event_type]:
            self._subscribers[event_type].remove(handler)
    
    async def publish(self, event: Event):
        """Publish an event to all subscribers."""
        # Store in history
        self._event_history.append(event)
        if len(self._event_history) > self._max_history:
            self._event_history.pop(0)
        
        # Notify subscribers
        handlers = self._subscribers.get(event.event_type, [])
        tasks = [self._call_handler(handler, event) for handler in handlers]
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _call_handler(self, handler: Callable, event: Event):
        """Call event handler safely."""
        try:
            if asyncio.iscoroutinefunction(handler):
                await handler(event)
            else:
                handler(event)
        except Exception as e:
            print(f"Event handler error: {e}")
    
    def get_history(
        self, 
        event_type: Optional[EventType] = None,
        org_id: Optional[int] = None,
        limit: int = 100
    ) -> List[Event]:
        """Get event history with optional filters."""
        history = self._event_history
        
        if event_type:
            history = [e for e in history if e.event_type == event_type]
        
        if org_id:
            history = [e for e in history if e.org_id == org_id]
        
        return history[-limit:]


# Global event bus instance
event_bus = EventBus()


# Convenience functions
async def emit_event(
    event_type: EventType,
    org_id: int,
    data: Dict[str, Any],
    user_id: Optional[int] = None,
    correlation_id: Optional[str] = None
):
    """Emit an event to the event bus."""
    event = Event(
        event_type=event_type,
        org_id=org_id,
        data=data,
        user_id=user_id,
        correlation_id=correlation_id
    )
    await event_bus.publish(event)


def on_event(event_type: EventType):
    """Decorator for event handlers."""
    def decorator(func):
        event_bus.subscribe(event_type, func)
        return func
    return decorator
