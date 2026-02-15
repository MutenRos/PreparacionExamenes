"""Enterprise audit logging and compliance service."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Index
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from dario_app.database import Base


class AuditAction(str, Enum):
    """Audit action types."""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    LOGOUT = "logout"
    EXPORT = "export"
    IMPORT = "import"
    APPROVE = "approve"
    REJECT = "reject"
    EXECUTE = "execute"


class AuditSeverity(str, Enum):
    """Audit severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AuditLog(Base):
    """Audit log model for compliance."""
    
    __tablename__ = "audit_logs"
    
    id: int = Column(Integer, primary_key=True, index=True)
    organization_id: int = Column(Integer, nullable=False, index=True)
    
    # Who
    user_id: int = Column(Integer, nullable=True, index=True)
    user_email: str = Column(String(255), nullable=True)
    
    # What
    action: str = Column(String(50), nullable=False, index=True)
    resource_type: str = Column(String(100), nullable=False, index=True)
    resource_id: str = Column(String(100), nullable=True, index=True)
    
    # Details
    description: str = Column(Text, nullable=True)
    changes: str = Column(Text, nullable=True)  # JSON
    severity: str = Column(String(20), default="info", nullable=False)
    
    # When & Where
    timestamp: datetime = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    ip_address: str = Column(String(45), nullable=True)
    user_agent: str = Column(String(500), nullable=True)
    
    # Compliance
    is_sensitive: bool = Column(Boolean, default=False, nullable=False)
    retention_until: datetime = Column(DateTime, nullable=True)
    
    # Indexes for performance
    __table_args__ = (
        Index('ix_audit_org_timestamp', 'organization_id', 'timestamp'),
        Index('ix_audit_user_timestamp', 'user_id', 'timestamp'),
        Index('ix_audit_resource', 'resource_type', 'resource_id'),
    )


class AuditService:
    """Enterprise audit service for compliance and security."""
    
    @staticmethod
    async def log(
        db: AsyncSession,
        organization_id: int,
        action: AuditAction,
        resource_type: str,
        resource_id: Optional[str] = None,
        user_id: Optional[int] = None,
        user_email: Optional[str] = None,
        description: Optional[str] = None,
        changes: Optional[Dict[str, Any]] = None,
        severity: AuditSeverity = AuditSeverity.INFO,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        is_sensitive: bool = False
    ) -> AuditLog:
        """Create audit log entry."""
        import json
        
        audit_entry = AuditLog(
            organization_id=organization_id,
            user_id=user_id,
            user_email=user_email,
            action=action.value,
            resource_type=resource_type,
            resource_id=str(resource_id) if resource_id else None,
            description=description,
            changes=json.dumps(changes) if changes else None,
            severity=severity.value,
            ip_address=ip_address,
            user_agent=user_agent,
            is_sensitive=is_sensitive,
            timestamp=datetime.utcnow()
        )
        
        db.add(audit_entry)
        await db.commit()
        await db.refresh(audit_entry)
        
        return audit_entry
    
    @staticmethod
    async def get_logs(
        db: AsyncSession,
        organization_id: int,
        user_id: Optional[int] = None,
        resource_type: Optional[str] = None,
        action: Optional[AuditAction] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> list[AuditLog]:
        """Query audit logs with filters."""
        query = select(AuditLog).where(
            AuditLog.organization_id == organization_id
        )
        
        if user_id:
            query = query.where(AuditLog.user_id == user_id)
        
        if resource_type:
            query = query.where(AuditLog.resource_type == resource_type)
        
        if action:
            query = query.where(AuditLog.action == action.value)
        
        if start_date:
            query = query.where(AuditLog.timestamp >= start_date)
        
        if end_date:
            query = query.where(AuditLog.timestamp <= end_date)
        
        query = query.order_by(AuditLog.timestamp.desc()).limit(limit)
        
        result = await db.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def get_user_activity(
        db: AsyncSession,
        organization_id: int,
        user_id: int,
        days: int = 30
    ) -> Dict[str, Any]:
        """Get user activity summary."""
        from datetime import timedelta
        
        start_date = datetime.utcnow() - timedelta(days=days)
        
        logs = await AuditService.get_logs(
            db=db,
            organization_id=organization_id,
            user_id=user_id,
            start_date=start_date,
            limit=1000
        )
        
        return {
            "total_actions": len(logs),
            "actions_by_type": _count_by_field(logs, "action"),
            "resources_accessed": _count_by_field(logs, "resource_type"),
            "last_login": _get_last_action(logs, "login"),
            "sensitive_actions": sum(1 for log in logs if log.is_sensitive)
        }
    
    @staticmethod
    async def compliance_report(
        db: AsyncSession,
        organization_id: int,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """Generate compliance report."""
        logs = await AuditService.get_logs(
            db=db,
            organization_id=organization_id,
            start_date=start_date,
            end_date=end_date,
            limit=10000
        )
        
        return {
            "period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat()
            },
            "total_events": len(logs),
            "events_by_severity": _count_by_field(logs, "severity"),
            "events_by_action": _count_by_field(logs, "action"),
            "unique_users": len(set(log.user_id for log in logs if log.user_id)),
            "sensitive_events": sum(1 for log in logs if log.is_sensitive),
            "data_exports": sum(1 for log in logs if log.action == "export"),
            "failed_logins": sum(
                1 for log in logs 
                if log.action == "login" and log.severity == "error"
            )
        }


def _count_by_field(logs: list, field: str) -> Dict[str, int]:
    """Count logs by field value."""
    from collections import Counter
    return dict(Counter(getattr(log, field) for log in logs))


def _get_last_action(logs: list, action: str) -> Optional[str]:
    """Get timestamp of last action of type."""
    for log in logs:
        if log.action == action:
            return log.timestamp.isoformat()
    return None
