"""Field Service domain services."""

from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import WorkOrder, WorkOrderTask


class FieldServiceService:
    @staticmethod
    def generate_work_order_number(org_id: int) -> str:
        now = datetime.utcnow()
        return f"WO-{org_id}-{int(now.timestamp())}"

    @staticmethod
    async def update_work_order_status(db: AsyncSession, org_id: int, wo_id: int, status: str) -> Optional[WorkOrder]:
        stmt = select(WorkOrder).where(
            WorkOrder.id == wo_id,
            WorkOrder.organization_id == org_id,
        )
        result = await db.execute(stmt)
        wo = result.scalar_one_or_none()
        if not wo:
            return None
        wo.status = status
        wo.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(wo)
        return wo

    @staticmethod
    async def complete_task(db: AsyncSession, org_id: int, task_id: int, user_id: int, user_name: str) -> Optional[WorkOrderTask]:
        stmt = select(WorkOrderTask).where(
            WorkOrderTask.id == task_id,
            WorkOrderTask.organization_id == org_id,
        )
        result = await db.execute(stmt)
        task = result.scalar_one_or_none()
        if not task:
            return None
        task.status = "done"
        task.completed_by_user_id = user_id
        task.completed_by_name = user_name
        task.completed_at = datetime.utcnow()
        await db.commit()
        await db.refresh(task)
        return task
