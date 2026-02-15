"""Enterprise API routes for advanced features."""

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from dario_app.core.auth import get_org_id, require_auth, get_tenant_db, get_current_user_org
from dario_app.services.cache_service import cache, cached, invalidate_org_cache
from dario_app.services.event_bus import emit_event, EventType, event_bus
from dario_app.services.audit_service import AuditService, AuditAction, AuditSeverity
from dario_app.services.webhook_service import webhook_service
from dario_app.services.two_factor_service import TwoFactorService
from dario_app.services.analytics_service import AnalyticsService
from dario_app.services.analytics_advanced import AdvancedAnalyticsService
from dario_app.services.command_palette import get_all_commands, search_commands

router = APIRouter(prefix="/api/enterprise", tags=["enterprise"])

# Templates
templates_dir = Path(__file__).parent.parent.parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))


# Enterprise Dashboard Page
@router.get("/dashboard", response_class=HTMLResponse, include_in_schema=False)
async def enterprise_dashboard(request: Request):
    """Enterprise features dashboard."""
    user_context = await get_current_user_org(request)
    if not user_context:
        return templates.TemplateResponse("login.html", {"request": request})
    
    return templates.TemplateResponse("enterprise.html", {"request": request})


# Cache Management
@router.post("/cache/clear")
async def clear_cache(
    org_id: int = Depends(get_org_id),
    user_context: dict = Depends(require_auth)
):
    """Clear organization cache."""
    await invalidate_org_cache(org_id)
    return {"status": "success", "message": "Cache cleared"}


# Event History
@router.get("/events")
async def get_event_history(
    event_type: Optional[str] = None,
    limit: int = 100,
    org_id: int = Depends(get_org_id)
):
    """Get organization event history."""
    from dario_app.services.event_bus import EventType
    
    event_type_enum = EventType(event_type) if event_type else None
    history = event_bus.get_history(
        event_type=event_type_enum,
        org_id=org_id,
        limit=limit
    )
    
    return {
        "count": len(history),
        "events": [event.to_dict() for event in history]
    }


# Audit Logs
@router.get("/audit-logs")
async def get_audit_logs(
    user_id: Optional[int] = None,
    resource_type: Optional[str] = None,
    action: Optional[str] = None,
    days: int = 30,
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id)
):
    """Get audit logs with filters."""
    from dario_app.services.audit_service import AuditAction
    
    start_date = datetime.utcnow() - timedelta(days=days)
    action_enum = AuditAction(action) if action else None
    
    logs = await AuditService.get_logs(
        db=db,
        organization_id=org_id,
        user_id=user_id,
        resource_type=resource_type,
        action=action_enum,
        start_date=start_date,
        limit=1000
    )
    
    return {
        "count": len(logs),
        "logs": [
            {
                "id": log.id,
                "user_id": log.user_id,
                "user_email": log.user_email,
                "action": log.action,
                "resource_type": log.resource_type,
                "resource_id": log.resource_id,
                "description": log.description,
                "severity": log.severity,
                "timestamp": log.timestamp.isoformat(),
                "ip_address": log.ip_address
            }
            for log in logs
        ]
    }


@router.get("/audit-logs/user-activity/{user_id}")
async def get_user_activity(
    user_id: int,
    days: int = 30,
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id)
):
    """Get user activity summary."""
    activity = await AuditService.get_user_activity(
        db=db,
        organization_id=org_id,
        user_id=user_id,
        days=days
    )
    return activity


@router.get("/audit-logs/compliance-report")
async def get_compliance_report(
    start_date: datetime,
    end_date: datetime,
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id)
):
    """Generate compliance report."""
    report = await AuditService.compliance_report(
        db=db,
        organization_id=org_id,
        start_date=start_date,
        end_date=end_date
    )
    return report


# Webhooks
@router.get("/webhooks")
async def list_webhooks(
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id)
):
    """List all webhooks for organization."""
    from sqlalchemy import select
    from dario_app.services.webhook_service import Webhook
    
    query = select(Webhook).where(Webhook.organization_id == org_id)
    result = await db.execute(query)
    webhooks = result.scalars().all()
    
    return {
        "count": len(webhooks),
        "webhooks": [
            {
                "id": wh.id,
                "name": wh.name,
                "url": wh.url,
                "event_types": wh.event_types,
                "is_active": wh.is_active,
                "success_count": wh.success_count,
                "failure_count": wh.failure_count,
                "last_triggered": wh.last_triggered.isoformat() if wh.last_triggered else None
            }
            for wh in webhooks
        ]
    }


@router.post("/webhooks")
async def create_webhook(
    name: str,
    url: str,
    event_types: List[str],
    secret: Optional[str] = None,
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id)
):
    """Create new webhook."""
    webhook = await webhook_service.create_webhook(
        db=db,
        organization_id=org_id,
        name=name,
        url=url,
        event_types=event_types,
        secret=secret
    )
    
    return {
        "id": webhook.id,
        "name": webhook.name,
        "url": webhook.url,
        "event_types": webhook.event_types,
        "is_active": webhook.is_active
    }


# 2FA Management
@router.post("/2fa/setup")
async def setup_2fa(
    request: Request,
    db: AsyncSession = Depends(get_tenant_db),
    user_context: dict = Depends(require_auth),
    org_id: int = Depends(get_org_id)
):
    """Setup 2FA for current user."""
    user_id = user_context["user_id"]
    user_email = user_context["email"]
    
    result = await TwoFactorService.setup_2fa(
        db=db,
        user_id=user_id,
        organization_id=org_id,
        user_email=user_email
    )
    
    # Log audit
    await AuditService.log(
        db=db,
        organization_id=org_id,
        action=AuditAction.EXECUTE,
        resource_type="2fa",
        user_id=user_id,
        description="2FA setup initiated",
        ip_address=request.client.host
    )
    
    return result


@router.post("/2fa/enable")
async def enable_2fa(
    verification_token: str,
    db: AsyncSession = Depends(get_tenant_db),
    user_context: dict = Depends(require_auth)
):
    """Enable 2FA after verification."""
    user_id = user_context["user_id"]
    
    success = await TwoFactorService.enable_2fa(
        db=db,
        user_id=user_id,
        verification_token=verification_token
    )
    
    if not success:
        raise HTTPException(status_code=400, detail="Invalid verification token")
    
    return {"status": "success", "message": "2FA enabled"}


@router.post("/2fa/disable")
async def disable_2fa(
    db: AsyncSession = Depends(get_tenant_db),
    user_context: dict = Depends(require_auth)
):
    """Disable 2FA for current user."""
    user_id = user_context["user_id"]
    
    await TwoFactorService.disable_2fa(db=db, user_id=user_id)
    
    return {"status": "success", "message": "2FA disabled"}


# Advanced Analytics
@router.get("/analytics/revenue-forecast")
async def get_revenue_forecast(
    days: int = 30,
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id)
):
    """Get revenue forecast using ML."""
    forecast = await AnalyticsService.get_revenue_forecast(
        db=db,
        org_id=org_id,
        days=days
    )
    return forecast


@router.get("/analytics/customer-segmentation")
async def get_customer_segmentation(
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id)
):
    """Get customer segmentation (RFM analysis)."""
    segmentation = await AnalyticsService.get_customer_segmentation(
        db=db,
        org_id=org_id
    )
    return segmentation


@router.get("/analytics/product-performance")
async def get_product_performance(
    days: int = 30,
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id)
):
    """Get product performance analysis."""
    performance = await AnalyticsService.get_product_performance(
        db=db,
        org_id=org_id,
        days=days
    )
    return performance


@router.get("/analytics/inventory-optimization")
async def get_inventory_optimization(
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id)
):
    """Get inventory optimization recommendations."""
    recommendations = await AnalyticsService.get_inventory_optimization(
        db=db,
        org_id=org_id
    )
    return recommendations


@router.get("/analytics/kpi-dashboard")
async def get_kpi_dashboard(
    days: int = 30,
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id)
):
    """Get KPI dashboard data."""
    kpis = await AnalyticsService.get_kpi_dashboard(
        db=db,
        org_id=org_id,
        period_days=days
    )
    return kpis


# Command Palette
@router.get("/analytics/dso")
async def get_dso(
    days: int = 90,
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id)
):
    """Get Days Sales Outstanding (DSO) - collection efficiency."""
    dso = await AdvancedAnalyticsService.calculate_dso(
        db=db,
        org_id=org_id,
        period_days=days
    )
    return dso


@router.get("/analytics/dpo")
async def get_dpo(
    days: int = 90,
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id)
):
    """Get Days Payable Outstanding (DPO) - payment period."""
    dpo = await AdvancedAnalyticsService.calculate_dpo(
        db=db,
        org_id=org_id,
        period_days=days
    )
    return dpo


@router.get("/analytics/cash-flow-forecast")
async def get_cash_flow_forecast_advanced(
    days: int = 30,
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id)
):
    """Get detailed cash flow forecast with confidence intervals."""
    forecast = await AdvancedAnalyticsService.calculate_cash_flow_forecast(
        db=db,
        org_id=org_id,
        forecast_days=days
    )
    return forecast


@router.get("/analytics/inventory-turnover")
async def get_inventory_turnover(
    days: int = 365,
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id)
):
    """Get inventory turnover ratio and slow-moving items."""
    turnover = await AdvancedAnalyticsService.calculate_inventory_turnover(
        db=db,
        org_id=org_id,
        period_days=days
    )
    return turnover


@router.get("/analytics/otif")
async def get_otif(
    days: int = 30,
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id)
):
    """Get On-Time In-Full (OTIF) delivery performance."""
    otif = await AdvancedAnalyticsService.calculate_otif(
        db=db,
        org_id=org_id,
        period_days=days
    )
    return otif


@router.get("/analytics/order-fill-rate")
async def get_order_fill_rate(
    days: int = 30,
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id)
):
    """Get order fill rate (stock availability)."""
    fill_rate = await AdvancedAnalyticsService.calculate_order_fill_rate(
        db=db,
        org_id=org_id,
        period_days=days
    )
    return fill_rate


# Role-Based Dashboards
@router.get("/dashboards/executive")
async def get_executive_dashboard(
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id)
):
    """Executive dashboard with high-level KPIs."""
    dashboard = await AdvancedAnalyticsService.get_executive_dashboard(
        db=db,
        org_id=org_id
    )
    return dashboard


@router.get("/dashboards/sales")
async def get_sales_dashboard(
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id)
):
    """Sales team dashboard."""
    dashboard = await AdvancedAnalyticsService.get_sales_dashboard(
        db=db,
        org_id=org_id
    )
    return dashboard


@router.get("/dashboards/operations")
async def get_operations_dashboard(
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id)
):
    """Operations dashboard with fulfillment metrics."""
    dashboard = await AdvancedAnalyticsService.get_operations_dashboard(
        db=db,
        org_id=org_id
    )
    return dashboard


@router.get("/dashboards/financial")
async def get_financial_dashboard(
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id)
):
    """Financial controller dashboard."""
    dashboard = await AdvancedAnalyticsService.get_financial_dashboard(
        db=db,
        org_id=org_id
    )
    return dashboard


# Command Palette
@router.get("/commands")
async def get_commands():
    """Get all available commands."""
    return {"commands": get_all_commands()}


@router.get("/commands/search")
async def search_commands_endpoint(query: str):
    """Search commands."""
    results = search_commands(query)
    return {"results": results}


# System Health
@router.get("/health")
async def health_check():
    """System health check."""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "features": {
            "cache": True,
            "events": True,
            "webhooks": True,
            "2fa": True,
            "analytics": True,
            "graphql": True,
            "rate_limiting": True
        }
    }
