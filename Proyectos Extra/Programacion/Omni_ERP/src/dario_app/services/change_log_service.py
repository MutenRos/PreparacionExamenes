"""Change log service for critical tables tracking - Dynamics 365 style."""

from datetime import datetime
from typing import Any, Dict, Optional
from sqlalchemy import Column, Integer, String, DateTime, Text, Index, JSON
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.database import Base


class ChangeLog(Base):
    """Change log for critical tables."""
    
    __tablename__ = "change_logs"
    __table_args__ = (
        Index("ix_changelog_org_table", "organization_id", "table_name"),
        Index("ix_changelog_record", "table_name", "record_id"),
        {"extend_existing": True},
    )
    
    id: int = Column(Integer, primary_key=True, index=True)
    organization_id: int = Column(Integer, nullable=False, index=True)
    
    # What changed
    table_name: str = Column(String(100), nullable=False, index=True)
    record_id: int = Column(Integer, nullable=False, index=True)
    operation: str = Column(String(20), nullable=False)  # insert, update, delete
    
    # Who changed it
    user_id: int | None = Column(Integer, nullable=True, index=True)
    user_email: str | None = Column(String(255), nullable=True)
    
    # What changed (JSON diff)
    old_values: str | None = Column(Text, nullable=True)  # JSON
    new_values: str | None = Column(Text, nullable=True)  # JSON
    changed_fields: str | None = Column(Text, nullable=True)  # JSON list
    
    # When
    changed_at: datetime = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Where
    ip_address: str | None = Column(String(45), nullable=True)
    user_agent: str | None = Column(String(500), nullable=True)
    
    # Context
    reason: str | None = Column(Text, nullable=True)


class ChangeLogService:
    """Service to track changes in critical tables."""
    
    CRITICAL_TABLES = {
        "ventas", "compras", "productos", "clientes", "usuarios",
        "roles", "permisos", "ventas_detalle", "compras_detalle"
    }
    
    @staticmethod
    async def log_change(
        db: AsyncSession,
        organization_id: int,
        table_name: str,
        record_id: int,
        operation: str,
        old_values: Optional[Dict[str, Any]] = None,
        new_values: Optional[Dict[str, Any]] = None,
        user_id: Optional[int] = None,
        user_email: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        reason: Optional[str] = None
    ) -> Optional[ChangeLog]:
        """Log a change in a critical table."""
        import json
        
        # Only log critical tables
        if table_name not in ChangeLogService.CRITICAL_TABLES:
            return None
        
        # Calculate changed fields
        changed_fields = []
        if old_values and new_values:
            for key in new_values:
                if key in old_values and old_values[key] != new_values[key]:
                    changed_fields.append(key)
        
        change_entry = ChangeLog(
            organization_id=organization_id,
            table_name=table_name,
            record_id=record_id,
            operation=operation,
            user_id=user_id,
            user_email=user_email,
            old_values=json.dumps(old_values) if old_values else None,
            new_values=json.dumps(new_values) if new_values else None,
            changed_fields=json.dumps(changed_fields) if changed_fields else None,
            changed_at=datetime.utcnow(),
            ip_address=ip_address,
            user_agent=user_agent,
            reason=reason
        )
        
        db.add(change_entry)
        # Don't commit here - let caller control transaction
        
        return change_entry
    
    @staticmethod
    async def get_record_history(
        db: AsyncSession,
        organization_id: int,
        table_name: str,
        record_id: int,
        limit: int = 50
    ) -> list[ChangeLog]:
        """Get change history for a specific record."""
        from sqlalchemy import select
        
        query = select(ChangeLog).where(
            ChangeLog.organization_id == organization_id,
            ChangeLog.table_name == table_name,
            ChangeLog.record_id == record_id
        ).order_by(ChangeLog.changed_at.desc()).limit(limit)
        
        result = await db.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def get_user_changes(
        db: AsyncSession,
        organization_id: int,
        user_id: int,
        start_date: Optional[datetime] = None,
        limit: int = 100
    ) -> list[ChangeLog]:
        """Get all changes made by a user."""
        from sqlalchemy import select
        
        query = select(ChangeLog).where(
            ChangeLog.organization_id == organization_id,
            ChangeLog.user_id == user_id
        )
        
        if start_date:
            query = query.where(ChangeLog.changed_at >= start_date)
        
        query = query.order_by(ChangeLog.changed_at.desc()).limit(limit)
        
        result = await db.execute(query)
        return result.scalars().all()
