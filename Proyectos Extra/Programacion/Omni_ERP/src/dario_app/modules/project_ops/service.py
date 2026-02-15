"""Project Operations services."""

from datetime import datetime
from decimal import Decimal
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import BillingEvent, TimesheetEntry, Expense, Project


class ProjectOpsService:
    @staticmethod
    async def approve_timesheets(db: AsyncSession, org_id: int, ts_ids: List[int], user_id: int, user_name: str):
        stmt = select(TimesheetEntry).where(
            TimesheetEntry.organization_id == org_id,
            TimesheetEntry.id.in_(ts_ids),
        )
        result = await db.execute(stmt)
        entries = result.scalars().all()
        for e in entries:
            e.status = "approved"
            e.approved_at = datetime.utcnow()
            e.approved_by_user_id = user_id
            e.approved_by_user_name = user_name
        await db.commit()
        return entries

    @staticmethod
    async def approve_expenses(db: AsyncSession, org_id: int, exp_ids: List[int], user_id: int, user_name: str):
        stmt = select(Expense).where(
            Expense.organization_id == org_id,
            Expense.id.in_(exp_ids),
        )
        result = await db.execute(stmt)
        expenses = result.scalars().all()
        for e in expenses:
            e.status = "approved"
            e.approved_at = datetime.utcnow()
            e.approved_by_user_id = user_id
            e.approved_by_user_name = user_name
        await db.commit()
        return expenses

    @staticmethod
    async def generate_billing_events(db: AsyncSession, org_id: int, project_id: int):
        # Sum approved timesheets and expenses
        ts_stmt = select(TimesheetEntry).where(
            TimesheetEntry.organization_id == org_id,
            TimesheetEntry.project_id == project_id,
            TimesheetEntry.status == "approved",
        )
        ts_result = await db.execute(ts_stmt)
        ts_entries = ts_result.scalars().all()
        hours_total = sum([t.hours for t in ts_entries], Decimal("0"))

        exp_stmt = select(Expense).where(
            Expense.organization_id == org_id,
            Expense.project_id == project_id,
            Expense.status == "approved",
        )
        exp_result = await db.execute(exp_stmt)
        exp_entries = exp_result.scalars().all()
        expenses_total = sum([e.amount for e in exp_entries], Decimal("0"))

        bill_events = []
        if hours_total > 0:
            ev = BillingEvent(
                organization_id=org_id,
                project_id=project_id,
                event_type="time_and_materials",
                description=f"Horas aprobadas {hours_total}",
                amount=hours_total,  # simplistic; real calc should use bill rates
                status="ready",
                ready_at=datetime.utcnow(),
            )
            db.add(ev)
            bill_events.append(ev)
        if expenses_total > 0:
            ev = BillingEvent(
                organization_id=org_id,
                project_id=project_id,
                event_type="expense",
                description="Gastos aprobados",
                amount=expenses_total,
                status="ready",
                ready_at=datetime.utcnow(),
            )
            db.add(ev)
            bill_events.append(ev)
        await db.commit()
        return bill_events

    @staticmethod
    async def convert_to_sale(db: AsyncSession, org_id: int, project_id: int, user_id: int, user_name: str):
        """Convert an approved/completed project into a sales order.
        
        This function:
        1. Validates the project exists and is in appropriate status
        2. Creates a sales order with project details
        3. Creates line items from project tasks
        4. Links the sale back to the project for tracking
        """
        # Get project
        stmt = select(Project).where(
            Project.organization_id == org_id,
            Project.id == project_id,
        )
        result = await db.execute(stmt)
        project = result.scalar_one_or_none()
        
        if not project:
            raise ValueError(f"Project {project_id} not found")
        
        # Validate status: only active, completed, or draft with budget can convert
        if project.status not in ["active", "completed", "draft"]:
            raise ValueError(
                f"Cannot convert project with status '{project.status}'. "
                "Only 'draft', 'active', or 'completed' projects can be converted to sales."
            )
        
        # Try to import sales module dynamically to avoid circular imports
        try:
            from dario_app.modules.ventas.models import VentaQuote, VentaQuoteItem
        except ImportError:
            raise ValueError("Sales module (ventas) not found")
        
        # Get all tasks for line items
        from .models import ProjectTask
        task_stmt = select(ProjectTask).where(
            ProjectTask.organization_id == org_id,
            ProjectTask.project_id == project_id,
        )
        task_result = await db.execute(task_stmt)
        tasks = task_result.scalars().all()
        
        # Create sales quote
        quote = VentaQuote(
            organization_id=org_id,
            quote_number=f"PROJ-{project.project_code}",
            customer_id=project.customer_id,
            customer_name=project.customer_name,
            total_amount=float(project.budget_amount),
            status="draft",
            description=f"Convertido del Proyecto: {project.name}",
            created_by_user_id=user_id,
            created_by_user_name=user_name,
        )
        db.add(quote)
        await db.flush()  # Get the quote ID
        
        # Create line items from tasks
        for task in tasks:
            item = VentaQuoteItem(
                organization_id=org_id,
                quote_id=quote.id,
                description=task.name,
                quantity=1,
                unit_price=float(project.budget_amount / len(tasks)) if tasks else float(project.budget_amount),
                line_amount=float(project.budget_amount / len(tasks)) if tasks else float(project.budget_amount),
            )
            db.add(item)
        
        # Update project to track conversion
        project.status = "converted_to_sale"
        project.updated_at = datetime.utcnow()
        
        await db.commit()
        
        return {
            "success": True,
            "project_id": project_id,
            "quote_id": quote.id,
            "quote_number": quote.quote_number,
            "message": f"Proyecto '{project.name}' convertido a cotización de venta #{quote.quote_number}",
            "quote": {
                "id": quote.id,
                "number": quote.quote_number,
                "customer": quote.customer_name,
                "total": float(quote.total_amount),
                "items_count": len(tasks),
            }
        }
    @staticmethod
    async def approve_timesheets(db: AsyncSession, org_id: int, ts_ids: List[int], user_id: int, user_name: str):
        stmt = select(TimesheetEntry).where(
            TimesheetEntry.organization_id == org_id,
            TimesheetEntry.id.in_(ts_ids),
        )
        result = await db.execute(stmt)
        entries = result.scalars().all()
        for e in entries:
            e.status = "approved"
            e.approved_at = datetime.utcnow()
            e.approved_by_user_id = user_id
            e.approved_by_user_name = user_name
        await db.commit()
        return entries

    @staticmethod
    async def approve_expenses(db: AsyncSession, org_id: int, exp_ids: List[int], user_id: int, user_name: str):
        stmt = select(Expense).where(
            Expense.organization_id == org_id,
            Expense.id.in_(exp_ids),
        )
        result = await db.execute(stmt)
        expenses = result.scalars().all()
        for e in expenses:
            e.status = "approved"
            e.approved_at = datetime.utcnow()
            e.approved_by_user_id = user_id
            e.approved_by_user_name = user_name
        await db.commit()
        return expenses

    @staticmethod
    async def generate_billing_events(db: AsyncSession, org_id: int, project_id: int):
        # Sum approved timesheets and expenses
        ts_stmt = select(TimesheetEntry).where(
            TimesheetEntry.organization_id == org_id,
            TimesheetEntry.project_id == project_id,
            TimesheetEntry.status == "approved",
        )
        ts_result = await db.execute(ts_stmt)
        ts_entries = ts_result.scalars().all()
        hours_total = sum([t.hours for t in ts_entries], Decimal("0"))

        exp_stmt = select(Expense).where(
            Expense.organization_id == org_id,
            Expense.project_id == project_id,
            Expense.status == "approved",
        )
        exp_result = await db.execute(exp_stmt)
        exp_entries = exp_result.scalars().all()
        expenses_total = sum([e.amount for e in exp_entries], Decimal("0"))

        bill_events = []
        if hours_total > 0:
            ev = BillingEvent(
                organization_id=org_id,
                project_id=project_id,
                event_type="time_and_materials",
                description=f"Horas aprobadas {hours_total}",
                amount=hours_total,  # simplistic; real calc should use bill rates
                status="ready",
                ready_at=datetime.utcnow(),
            )
            db.add(ev)
            bill_events.append(ev)
        if expenses_total > 0:
            ev = BillingEvent(
                organization_id=org_id,
                project_id=project_id,
                event_type="expense",
                description="Gastos aprobados",
                amount=expenses_total,
                status="ready",
                ready_at=datetime.utcnow(),
            )
            db.add(ev)
            bill_events.append(ev)
        await db.commit()
        return bill_events
