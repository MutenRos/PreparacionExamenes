"""Subscription Billing routes - Recurring Revenue Management."""

from datetime import datetime, date, timedelta
from typing import Optional
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.core.auth import require_permission, get_tenant_db, get_org_id
from dario_app.modules.usuarios.models import Usuario

from .models import (
    SubscriptionPlan, Subscription, SubscriptionInvoice,
    SubscriptionUsage, SubscriptionChange, RevenueRecognition
)

router = APIRouter(prefix="/api/subscription-billing", tags=["Subscription Billing"])


# Schemas

class PlanCreate(BaseModel):
    name: str
    descripcion: Optional[str] = None
    billing_frequency: str = "monthly"
    base_price: float
    trial_period_days: int = 0
    is_usage_based: bool = False


class SubscriptionCreate(BaseModel):
    customer_id: int
    customer_name: str
    plan_id: int
    start_date: str
    discount_percent: float = 0
    auto_renew: bool = True


class UsageCreate(BaseModel):
    subscription_id: int
    usage_date: str
    metric_name: str
    quantity: float
    unit_price: float


# Subscription Plans

@router.post("/plans")
async def create_plan(
    payload: PlanCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("subscriptions.plans.create")),
    org_id: int = Depends(get_org_id),
):
    # Generate plan code
    stmt = select(SubscriptionPlan).where(SubscriptionPlan.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    plan_code = f"PLAN-{count + 1:04d}"
    
    plan = SubscriptionPlan(
        organization_id=org_id,
        plan_code=plan_code,
        **payload.model_dump()
    )
    db.add(plan)
    await db.commit()
    await db.refresh(plan)
    return plan


@router.get("/plans")
async def list_plans(
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("subscriptions.plans.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(SubscriptionPlan).where(SubscriptionPlan.organization_id == org_id)
    if status:
        query = query.where(SubscriptionPlan.status == status)
    result = await db.execute(query)
    return result.scalars().all()


# Subscriptions

@router.post("/subscriptions")
async def create_subscription(
    payload: SubscriptionCreate,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("subscriptions.manage")),
    org_id: int = Depends(get_org_id),
):
    # Get plan
    plan_stmt = select(SubscriptionPlan).where(
        SubscriptionPlan.id == payload.plan_id,
        SubscriptionPlan.organization_id == org_id
    )
    plan_result = await db.execute(plan_stmt)
    plan = plan_result.scalar_one_or_none()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    # Generate subscription number
    stmt = select(Subscription).where(Subscription.organization_id == org_id)
    result = await db.execute(stmt)
    count = len(result.scalars().all())
    subscription_number = f"SUB-{datetime.now().strftime('%Y%m')}-{count + 1:05d}"
    
    start_date = datetime.strptime(payload.start_date, "%Y-%m-%d").date()
    
    # Calculate trial end and next billing
    trial_end = None
    status = "active"
    if plan.trial_period_days > 0:
        trial_end = start_date + timedelta(days=plan.trial_period_days)
        status = "trial"
        next_billing = trial_end
    else:
        # Calculate next billing based on frequency
        if plan.billing_frequency == "monthly":
            next_billing = start_date + timedelta(days=30)
        elif plan.billing_frequency == "quarterly":
            next_billing = start_date + timedelta(days=90)
        elif plan.billing_frequency == "annual":
            next_billing = start_date + timedelta(days=365)
        else:
            next_billing = start_date + timedelta(days=30)
    
    # Calculate MRR
    effective_price = plan.base_price * (1 - Decimal(str(payload.discount_percent)) / 100)
    if plan.billing_frequency == "monthly":
        mrr = effective_price
    elif plan.billing_frequency == "quarterly":
        mrr = effective_price / 3
    elif plan.billing_frequency == "annual":
        mrr = effective_price / 12
    else:
        mrr = effective_price
    
    subscription = Subscription(
        organization_id=org_id,
        subscription_number=subscription_number,
        plan_name=plan.name,
        base_price=plan.base_price,
        billing_frequency=plan.billing_frequency,
        trial_end_date=trial_end,
        next_billing_date=next_billing,
        status=status,
        mrr=mrr,
        **payload.model_dump()
    )
    db.add(subscription)
    await db.commit()
    await db.refresh(subscription)
    return subscription


@router.get("/subscriptions")
async def list_subscriptions(
    status: Optional[str] = None,
    customer_id: Optional[int] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("subscriptions.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(Subscription).where(Subscription.organization_id == org_id)
    if status:
        query = query.where(Subscription.status == status)
    if customer_id:
        query = query.where(Subscription.customer_id == customer_id)
    query = query.order_by(Subscription.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/subscriptions/{subscription_id}")
async def get_subscription(
    subscription_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("subscriptions.read")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(Subscription).where(
        Subscription.id == subscription_id,
        Subscription.organization_id == org_id
    )
    result = await db.execute(stmt)
    subscription = result.scalar_one_or_none()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription


@router.patch("/subscriptions/{subscription_id}/cancel")
async def cancel_subscription(
    subscription_id: int,
    reason: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("subscriptions.cancel")),
    org_id: int = Depends(get_org_id),
):
    stmt = select(Subscription).where(
        Subscription.id == subscription_id,
        Subscription.organization_id == org_id
    )
    result = await db.execute(stmt)
    subscription = result.scalar_one_or_none()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    subscription.status = "canceled"
    subscription.canceled_at = datetime.utcnow()
    subscription.cancellation_reason = reason
    subscription.end_date = date.today()
    subscription.auto_renew = False
    
    # Record change
    change = SubscriptionChange(
        organization_id=org_id,
        subscription_id=subscription_id,
        change_type="cancel",
        old_price=subscription.base_price,
        new_price=Decimal("0"),
        effective_date=date.today(),
        reason=reason,
        changed_by_user_id=user.id,
        changed_by_name=user.nombre_completo
    )
    db.add(change)
    
    await db.commit()
    await db.refresh(subscription)
    return subscription


@router.post("/subscriptions/{subscription_id}/upgrade")
async def upgrade_subscription(
    subscription_id: int,
    new_plan_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("subscriptions.manage")),
    org_id: int = Depends(get_org_id),
):
    # Get subscription
    sub_stmt = select(Subscription).where(
        Subscription.id == subscription_id,
        Subscription.organization_id == org_id
    )
    sub_result = await db.execute(sub_stmt)
    subscription = sub_result.scalar_one_or_none()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    # Get new plan
    plan_stmt = select(SubscriptionPlan).where(
        SubscriptionPlan.id == new_plan_id,
        SubscriptionPlan.organization_id == org_id
    )
    plan_result = await db.execute(plan_stmt)
    new_plan = plan_result.scalar_one_or_none()
    if not new_plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    # Record change
    change = SubscriptionChange(
        organization_id=org_id,
        subscription_id=subscription_id,
        change_type="upgrade",
        old_plan_id=subscription.plan_id,
        old_plan_name=subscription.plan_name,
        new_plan_id=new_plan.id,
        new_plan_name=new_plan.name,
        old_price=subscription.base_price,
        new_price=new_plan.base_price,
        effective_date=date.today(),
        changed_by_user_id=user.id,
        changed_by_name=user.nombre_completo
    )
    db.add(change)
    
    # Update subscription
    subscription.plan_id = new_plan.id
    subscription.plan_name = new_plan.name
    subscription.base_price = new_plan.base_price
    subscription.billing_frequency = new_plan.billing_frequency
    
    # Recalculate MRR
    effective_price = new_plan.base_price * (1 - subscription.discount_percent / 100)
    if new_plan.billing_frequency == "monthly":
        subscription.mrr = effective_price
    elif new_plan.billing_frequency == "quarterly":
        subscription.mrr = effective_price / 3
    elif new_plan.billing_frequency == "annual":
        subscription.mrr = effective_price / 12
    
    await db.commit()
    await db.refresh(subscription)
    return subscription


# Invoices

@router.post("/subscriptions/{subscription_id}/generate-invoice")
async def generate_invoice(
    subscription_id: int,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("subscriptions.billing.manage")),
    org_id: int = Depends(get_org_id),
):
    # Get subscription
    sub_stmt = select(Subscription).where(
        Subscription.id == subscription_id,
        Subscription.organization_id == org_id
    )
    sub_result = await db.execute(sub_stmt)
    subscription = sub_result.scalar_one_or_none()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    # Generate invoice number
    inv_stmt = select(SubscriptionInvoice).where(SubscriptionInvoice.organization_id == org_id)
    inv_result = await db.execute(inv_stmt)
    count = len(inv_result.scalars().all())
    invoice_number = f"SINV-{datetime.now().strftime('%Y%m')}-{count + 1:05d}"
    
    invoice_date = date.today()
    due_date = invoice_date + timedelta(days=30)
    
    # Calculate billing period
    if subscription.next_billing_date:
        period_start = subscription.next_billing_date
        if subscription.billing_frequency == "monthly":
            period_end = period_start + timedelta(days=30)
        elif subscription.billing_frequency == "quarterly":
            period_end = period_start + timedelta(days=90)
        elif subscription.billing_frequency == "annual":
            period_end = period_start + timedelta(days=365)
        else:
            period_end = period_start + timedelta(days=30)
    else:
        period_start = invoice_date
        period_end = period_start + timedelta(days=30)
    
    effective_price = subscription.base_price * (1 - subscription.discount_percent / 100)
    tax_amount = effective_price * Decimal("0.21")  # 21% IVA
    total_amount = effective_price + tax_amount
    
    invoice = SubscriptionInvoice(
        organization_id=org_id,
        subscription_id=subscription_id,
        invoice_number=invoice_number,
        invoice_date=invoice_date,
        due_date=due_date,
        billing_period_start=period_start,
        billing_period_end=period_end,
        subtotal=effective_price,
        tax_amount=tax_amount,
        total_amount=total_amount
    )
    db.add(invoice)
    
    # Update subscription next billing date
    subscription.next_billing_date = period_end
    
    await db.commit()
    await db.refresh(invoice)
    return invoice


@router.get("/invoices")
async def list_invoices(
    subscription_id: Optional[int] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("subscriptions.billing.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(SubscriptionInvoice).where(SubscriptionInvoice.organization_id == org_id)
    if subscription_id:
        query = query.where(SubscriptionInvoice.subscription_id == subscription_id)
    if status:
        query = query.where(SubscriptionInvoice.status == status)
    query = query.order_by(SubscriptionInvoice.invoice_date.desc())
    result = await db.execute(query)
    return result.scalars().all()


# Usage Tracking

@router.post("/usage")
async def record_usage(
    payload: UsageCreate,
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id),
):
    total_amount = Decimal(str(payload.quantity)) * Decimal(str(payload.unit_price))
    
    usage = SubscriptionUsage(
        organization_id=org_id,
        total_amount=total_amount,
        **payload.model_dump()
    )
    db.add(usage)
    await db.commit()
    await db.refresh(usage)
    return usage


@router.get("/usage")
async def list_usage(
    subscription_id: Optional[int] = None,
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("subscriptions.read")),
    org_id: int = Depends(get_org_id),
):
    query = select(SubscriptionUsage).where(SubscriptionUsage.organization_id == org_id)
    if subscription_id:
        query = query.where(SubscriptionUsage.subscription_id == subscription_id)
    query = query.order_by(SubscriptionUsage.usage_date.desc())
    result = await db.execute(query)
    return result.scalars().all()


# Analytics

@router.get("/analytics/mrr")
async def get_mrr(
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("subscriptions.analytics.read")),
    org_id: int = Depends(get_org_id),
):
    """Get total Monthly Recurring Revenue."""
    stmt = select(Subscription).where(
        Subscription.organization_id == org_id,
        Subscription.status.in_(["active", "trial"])
    )
    result = await db.execute(stmt)
    subscriptions = result.scalars().all()
    
    total_mrr = sum(sub.mrr for sub in subscriptions)
    
    return {
        "total_mrr": float(total_mrr),
        "active_subscriptions": len(subscriptions),
        "currency": "EUR"
    }


@router.get("/analytics/churn")
async def get_churn_rate(
    db: AsyncSession = Depends(get_tenant_db),
    user: Usuario = Depends(require_permission("subscriptions.analytics.read")),
    org_id: int = Depends(get_org_id),
):
    """Calculate churn rate for current month."""
    # Get canceled subscriptions this month
    first_day = date.today().replace(day=1)
    
    canceled_stmt = select(Subscription).where(
        Subscription.organization_id == org_id,
        Subscription.status == "canceled",
        Subscription.canceled_at >= datetime.combine(first_day, datetime.min.time())
    )
    canceled_result = await db.execute(canceled_stmt)
    canceled_count = len(canceled_result.scalars().all())
    
    # Get total active at start of month
    active_stmt = select(Subscription).where(
        Subscription.organization_id == org_id,
        Subscription.status.in_(["active", "trial"])
    )
    active_result = await db.execute(active_stmt)
    active_count = len(active_result.scalars().all())
    
    total_at_start = active_count + canceled_count
    churn_rate = (canceled_count / total_at_start * 100) if total_at_start > 0 else 0
    
    return {
        "churn_rate": round(churn_rate, 2),
        "canceled_count": canceled_count,
        "total_at_start": total_at_start
    }
