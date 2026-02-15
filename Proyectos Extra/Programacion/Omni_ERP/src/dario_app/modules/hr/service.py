"""HR service helpers."""

from datetime import datetime
from decimal import Decimal
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Employee, PayrollRun, PayrollLine


class HRService:
    @staticmethod
    async def calculate_payroll(db: AsyncSession, org_id: int, run_id: int) -> PayrollRun:
        stmt = select(PayrollRun).where(
            PayrollRun.id == run_id,
            PayrollRun.organization_id == org_id,
        )
        result = await db.execute(stmt)
        run = result.scalar_one_or_none()
        if not run:
            raise ValueError("Payroll run not found")

        # Delete existing lines for idempotency
        await db.execute(
            PayrollLine.__table__.delete().where(
                PayrollLine.payroll_run_id == run_id,
                PayrollLine.organization_id == org_id,
            )
        )

        emp_stmt = select(Employee).where(
            Employee.organization_id == org_id,
            Employee.status == "active",
        )
        emp_result = await db.execute(emp_stmt)
        employees: List[Employee] = emp_result.scalars().all()

        total_gross = Decimal("0")
        total_net = Decimal("0")

        for emp in employees:
            gross = emp.salary or (emp.hourly_rate or Decimal("0")) * Decimal("160")
            tax = gross * Decimal("0.3")
            net = gross - tax
            line = PayrollLine(
                organization_id=org_id,
                payroll_run_id=run_id,
                employee_id=emp.id,
                gross_amount=gross,
                tax_amount=tax,
                net_amount=net,
                status="calculated",
            )
            db.add(line)
            total_gross += gross
            total_net += net

        run.total_gross = total_gross
        run.total_net = total_net
        run.status = "calculated"
        await db.commit()
        await db.refresh(run)
        return run

    @staticmethod
    async def post_payroll(db: AsyncSession, org_id: int, run_id: int) -> PayrollRun:
        stmt = select(PayrollRun).where(
            PayrollRun.id == run_id,
            PayrollRun.organization_id == org_id,
        )
        result = await db.execute(stmt)
        run = result.scalar_one_or_none()
        if not run:
            raise ValueError("Payroll run not found")
        run.status = "posted"
        run.posted_at = datetime.utcnow()
        await db.commit()
        await db.refresh(run)
        return run
