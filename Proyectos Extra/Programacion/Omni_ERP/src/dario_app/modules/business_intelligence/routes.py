"""
Business Intelligence & Analytics Module - Routes
REST API endpoints for dashboards, KPIs, reports, and analytics
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func
from typing import List, Optional
from datetime import datetime, timedelta

from dario_app.database import get_db
from dario_app.modules.business_intelligence.models import (
    Dashboard, KPI, Report, DataVisualization, AnalyticsQuery, MetricDefinition
)

router = APIRouter(prefix="/business-intelligence", tags=["Business Intelligence"])


# ============================================================================
# DASHBOARDS
# ============================================================================

@router.post("/dashboards")
async def create_dashboard(
    organization_id: int,
    name: str,
    description: Optional[str] = None,
    category: Optional[str] = None,
    layout_config: Optional[dict] = None,
    db: AsyncSession = Depends(get_db)
):
    """Create a new dashboard"""
    # Generate dashboard code
    result = await db.execute(
        select(func.count(Dashboard.id)).where(Dashboard.organization_id == organization_id)
    )
    count = result.scalar() or 0
    dashboard_code = f"DASH-{count + 1:04d}"
    
    dashboard = Dashboard(
        organization_id=organization_id,
        dashboard_code=dashboard_code,
        name=name,
        description=description,
        category=category,
        layout_config=layout_config or {},
        created_by="system"
    )
    
    db.add(dashboard)
    await db.commit()
    await db.refresh(dashboard)
    return dashboard


@router.get("/dashboards")
async def get_dashboards(
    organization_id: int,
    category: Optional[str] = None,
    is_favorite: Optional[bool] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all dashboards with optional filters"""
    query = select(Dashboard).where(Dashboard.organization_id == organization_id)
    
    if category:
        query = query.where(Dashboard.category == category)
    if is_favorite is not None:
        query = query.where(Dashboard.is_favorite == is_favorite)
    
    query = query.order_by(Dashboard.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/dashboards/{dashboard_id}")
async def get_dashboard(dashboard_id: int, db: AsyncSession = Depends(get_db)):
    """Get dashboard details with KPIs and visualizations"""
    result = await db.execute(
        select(Dashboard).where(Dashboard.id == dashboard_id)
    )
    dashboard = result.scalar_one_or_none()
    if not dashboard:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    
    # Update view count
    dashboard.total_views += 1
    dashboard.last_viewed_at = datetime.utcnow()
    await db.commit()
    
    return dashboard


@router.patch("/dashboards/{dashboard_id}")
async def update_dashboard(
    dashboard_id: int,
    name: Optional[str] = None,
    layout_config: Optional[dict] = None,
    filters: Optional[dict] = None,
    is_favorite: Optional[bool] = None,
    db: AsyncSession = Depends(get_db)
):
    """Update dashboard configuration"""
    result = await db.execute(select(Dashboard).where(Dashboard.id == dashboard_id))
    dashboard = result.scalar_one_or_none()
    if not dashboard:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    
    if name: dashboard.name = name
    if layout_config: dashboard.layout_config = layout_config
    if filters: dashboard.filters = filters
    if is_favorite is not None: dashboard.is_favorite = is_favorite
    
    await db.commit()
    await db.refresh(dashboard)
    return dashboard


# ============================================================================
# KPIs
# ============================================================================

@router.post("/kpis")
async def create_kpi(
    organization_id: int,
    name: str,
    dashboard_id: Optional[int] = None,
    metric_type: Optional[str] = None,
    calculation_formula: Optional[str] = None,
    target_value: Optional[float] = None,
    db: AsyncSession = Depends(get_db)
):
    """Create a new KPI"""
    # Generate KPI code
    result = await db.execute(
        select(func.count(KPI.id)).where(KPI.organization_id == organization_id)
    )
    count = result.scalar() or 0
    kpi_code = f"KPI-{count + 1:04d}"
    
    kpi = KPI(
        organization_id=organization_id,
        dashboard_id=dashboard_id,
        kpi_code=kpi_code,
        name=name,
        metric_type=metric_type,
        calculation_formula=calculation_formula,
        target_value=target_value,
        created_by="system"
    )
    
    db.add(kpi)
    await db.commit()
    await db.refresh(kpi)
    return kpi


@router.get("/kpis")
async def get_kpis(
    organization_id: int,
    dashboard_id: Optional[int] = None,
    category: Optional[str] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all KPIs with optional filters"""
    query = select(KPI).where(KPI.organization_id == organization_id)
    
    if dashboard_id:
        query = query.where(KPI.dashboard_id == dashboard_id)
    if category:
        query = query.where(KPI.category == category)
    if status:
        query = query.where(KPI.status == status)
    
    result = await db.execute(query)
    return result.scalars().all()


@router.patch("/kpis/{kpi_id}/update-value")
async def update_kpi_value(
    kpi_id: int,
    current_value: float,
    db: AsyncSession = Depends(get_db)
):
    """Update KPI current value and calculate metrics"""
    result = await db.execute(select(KPI).where(KPI.id == kpi_id))
    kpi = result.scalar_one_or_none()
    if not kpi:
        raise HTTPException(status_code=404, detail="KPI not found")
    
    # Store previous value
    kpi.previous_value = kpi.current_value
    kpi.current_value = current_value
    
    # Calculate change
    if kpi.previous_value:
        kpi.change_value = current_value - kpi.previous_value
        kpi.change_percentage = (kpi.change_value / kpi.previous_value) * 100
    
    # Calculate target achievement
    if kpi.target_value:
        kpi.target_achievement = (current_value / kpi.target_value) * 100
        
        # Update status based on thresholds
        if current_value >= kpi.target_value:
            kpi.status = "Exceeded"
        elif kpi.threshold_critical and current_value <= kpi.threshold_critical:
            kpi.status = "Critical"
        elif kpi.threshold_warning and current_value <= kpi.threshold_warning:
            kpi.status = "Warning"
        else:
            kpi.status = "On_Track"
    
    # Determine trend
    if kpi.change_percentage:
        if kpi.change_percentage > 5:
            kpi.trend = "Improving"
        elif kpi.change_percentage < -5:
            kpi.trend = "Declining"
        else:
            kpi.trend = "Stable"
    
    kpi.last_calculated_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(kpi)
    return kpi


# ============================================================================
# REPORTS
# ============================================================================

@router.post("/reports")
async def create_report(
    organization_id: int,
    name: str,
    category: str,
    report_type: str,
    query_definition: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Create a new report"""
    # Generate report code
    result = await db.execute(
        select(func.count(Report.id)).where(Report.organization_id == organization_id)
    )
    count = result.scalar() or 0
    report_code = f"REP-{count + 1:04d}"
    
    report = Report(
        organization_id=organization_id,
        report_code=report_code,
        name=name,
        category=category,
        report_type=report_type,
        query_definition=query_definition,
        created_by="system"
    )
    
    db.add(report)
    await db.commit()
    await db.refresh(report)
    return report


@router.get("/reports")
async def get_reports(
    organization_id: int,
    category: Optional[str] = None,
    status: Optional[str] = None,
    is_scheduled: Optional[bool] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all reports with optional filters"""
    query = select(Report).where(Report.organization_id == organization_id)
    
    if category:
        query = query.where(Report.category == category)
    if status:
        query = query.where(Report.status == status)
    if is_scheduled is not None:
        query = query.where(Report.is_scheduled == is_scheduled)
    
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/reports/{report_id}/execute")
async def execute_report(
    report_id: int,
    parameters: Optional[dict] = None,
    db: AsyncSession = Depends(get_db)
):
    """Execute a report and return results"""
    result = await db.execute(select(Report).where(Report.id == report_id))
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    start_time = datetime.utcnow()
    
    # TODO: Execute actual query here
    # This would integrate with your query engine
    
    end_time = datetime.utcnow()
    duration_ms = int((end_time - start_time).total_seconds() * 1000)
    
    # Update execution stats
    report.last_run_at = datetime.utcnow()
    report.last_run_duration_ms = duration_ms
    report.last_run_status = "Success"
    report.total_runs += 1
    
    await db.commit()
    
    return {
        "report_id": report_id,
        "status": "Success",
        "duration_ms": duration_ms,
        "data": []  # Report data would go here
    }


# ============================================================================
# VISUALIZATIONS
# ============================================================================

@router.post("/visualizations")
async def create_visualization(
    organization_id: int,
    name: str,
    chart_type: str,
    data_source: Optional[str] = None,
    dashboard_id: Optional[int] = None,
    report_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """Create a new data visualization"""
    # Generate visualization code
    result = await db.execute(
        select(func.count(DataVisualization.id)).where(
            DataVisualization.organization_id == organization_id
        )
    )
    count = result.scalar() or 0
    viz_code = f"VIZ-{count + 1:04d}"
    
    viz = DataVisualization(
        organization_id=organization_id,
        dashboard_id=dashboard_id,
        report_id=report_id,
        visualization_code=viz_code,
        name=name,
        chart_type=chart_type,
        data_source=data_source,
        created_by="system"
    )
    
    db.add(viz)
    await db.commit()
    await db.refresh(viz)
    return viz


@router.get("/visualizations")
async def get_visualizations(
    organization_id: int,
    dashboard_id: Optional[int] = None,
    chart_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all visualizations with optional filters"""
    query = select(DataVisualization).where(
        DataVisualization.organization_id == organization_id
    )
    
    if dashboard_id:
        query = query.where(DataVisualization.dashboard_id == dashboard_id)
    if chart_type:
        query = query.where(DataVisualization.chart_type == chart_type)
    
    result = await db.execute(query)
    return result.scalars().all()


# ============================================================================
# ANALYTICS QUERIES
# ============================================================================

@router.post("/analytics-queries")
async def create_analytics_query(
    organization_id: int,
    name: str,
    query_text: str,
    category: Optional[str] = None,
    query_type: str = "SQL",
    db: AsyncSession = Depends(get_db)
):
    """Create a saved analytics query"""
    # Generate query code
    result = await db.execute(
        select(func.count(AnalyticsQuery.id)).where(
            AnalyticsQuery.organization_id == organization_id
        )
    )
    count = result.scalar() or 0
    query_code = f"QRY-{count + 1:04d}"
    
    query_obj = AnalyticsQuery(
        organization_id=organization_id,
        query_code=query_code,
        name=name,
        query_text=query_text,
        category=category,
        query_type=query_type,
        created_by="system"
    )
    
    db.add(query_obj)
    await db.commit()
    await db.refresh(query_obj)
    return query_obj


@router.get("/analytics-queries")
async def get_analytics_queries(
    organization_id: int,
    category: Optional[str] = None,
    is_public: Optional[bool] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all saved analytics queries"""
    query = select(AnalyticsQuery).where(
        AnalyticsQuery.organization_id == organization_id
    )
    
    if category:
        query = query.where(AnalyticsQuery.category == category)
    if is_public is not None:
        query = query.where(AnalyticsQuery.is_public == is_public)
    
    result = await db.execute(query)
    return result.scalars().all()


# ============================================================================
# METRIC DEFINITIONS
# ============================================================================

@router.post("/metric-definitions")
async def create_metric_definition(
    organization_id: int,
    name: str,
    calculation_formula: str,
    category: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Create a standardized metric definition"""
    # Generate metric code
    result = await db.execute(
        select(func.count(MetricDefinition.id)).where(
            MetricDefinition.organization_id == organization_id
        )
    )
    count = result.scalar() or 0
    metric_code = f"MET-{count + 1:04d}"
    
    metric = MetricDefinition(
        organization_id=organization_id,
        metric_code=metric_code,
        name=name,
        calculation_formula=calculation_formula,
        category=category,
        created_by="system"
    )
    
    db.add(metric)
    await db.commit()
    await db.refresh(metric)
    return metric


@router.get("/metric-definitions")
async def get_metric_definitions(
    organization_id: int,
    category: Optional[str] = None,
    approval_status: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all metric definitions"""
    query = select(MetricDefinition).where(
        MetricDefinition.organization_id == organization_id
    )
    
    if category:
        query = query.where(MetricDefinition.category == category)
    if approval_status:
        query = query.where(MetricDefinition.approval_status == approval_status)
    
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/analytics/dashboard-usage")
async def get_dashboard_usage_analytics(
    organization_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get dashboard usage analytics"""
    result = await db.execute(
        select(Dashboard).where(
            Dashboard.organization_id == organization_id
        ).order_by(Dashboard.total_views.desc()).limit(10)
    )
    top_dashboards = result.scalars().all()
    
    # Calculate total stats
    stats_result = await db.execute(
        select(
            func.count(Dashboard.id),
            func.sum(Dashboard.total_views),
            func.avg(Dashboard.load_time_ms)
        ).where(Dashboard.organization_id == organization_id)
    )
    total_dashboards, total_views, avg_load_time = stats_result.first()
    
    return {
        "total_dashboards": total_dashboards or 0,
        "total_views": total_views or 0,
        "avg_load_time_ms": float(avg_load_time) if avg_load_time else 0,
        "top_dashboards": [
            {
                "name": d.name,
                "views": d.total_views,
                "last_viewed": d.last_viewed_at
            } for d in top_dashboards
        ]
    }
