"""Advanced Inventory Optimization Routes."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from dario_app.database import get_db
from dario_app.modules.advanced_inventory_optimization import models
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/api/inventory-optimization", tags=["inventory_optimization"])


# Pydantic Schemas
class ABCAnalysisCreate(BaseModel):
    product_id: int
    category: str
    annual_consumption_value: float


class DemandForecastCreate(BaseModel):
    product_id: int
    forecast_period: str
    forecasting_method: str
    forecast_quantity: float


class SafetyStockCreate(BaseModel):
    product_id: int
    average_demand: float
    demand_std_deviation: float
    service_level: float


class ReorderOptimizationCreate(BaseModel):
    product_id: int
    current_reorder_point: float
    holding_cost_per_unit: float
    ordering_cost_per_order: float


# ABC Analysis Endpoints
@router.post("/abc-analysis")
async def create_abc_analysis(
    analysis: ABCAnalysisCreate,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Create ABC analysis for a product."""
    db_analysis = models.ABCAnalysisResult(
        organization_id=organization_id,
        product_id=analysis.product_id,
        category=analysis.category,
        annual_consumption_value=analysis.annual_consumption_value,
    )
    db.add(db_analysis)
    await db.commit()
    await db.refresh(db_analysis)
    return {"id": db_analysis.id, "category": db_analysis.category}


@router.get("/abc-analysis")
async def list_abc_analysis(
    organization_id: int = Query(...),
    category: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List ABC analysis results."""
    query = db.query(models.ABCAnalysisResult).filter(
        models.ABCAnalysisResult.organization_id == organization_id
    )
    
    if category:
        query = query.filter(models.ABCAnalysisResult.category == category)
    
    results = await query.all()
    return {"abc_analysis": results, "total": len(results)}


# Demand Forecasting Endpoints
@router.post("/demand-forecasts")
async def create_demand_forecast(
    forecast: DemandForecastCreate,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Create demand forecast for a product."""
    db_forecast = models.DemandForecast(
        organization_id=organization_id,
        product_id=forecast.product_id,
        forecast_period=forecast.forecast_period,
        forecasting_method=forecast.forecasting_method,
        forecast_quantity=forecast.forecast_quantity,
        forecast_date=datetime.utcnow(),
    )
    db.add(db_forecast)
    await db.commit()
    await db.refresh(db_forecast)
    return {"id": db_forecast.id, "forecast_quantity": db_forecast.forecast_quantity}


@router.get("/demand-forecasts")
async def list_demand_forecasts(
    organization_id: int = Query(...),
    product_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """List demand forecasts."""
    query = db.query(models.DemandForecast).filter(
        models.DemandForecast.organization_id == organization_id
    )
    
    if product_id:
        query = query.filter(models.DemandForecast.product_id == product_id)
    
    forecasts = await query.all()
    return {"forecasts": forecasts, "total": len(forecasts)}


# Safety Stock Endpoints
@router.post("/safety-stock")
async def calculate_safety_stock(
    calc: SafetyStockCreate,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Calculate optimal safety stock."""
    z_score = 1.96  # 95% confidence
    safety_stock = z_score * calc.demand_std_deviation * (5 ** 0.5)  # 5 day lead time
    
    db_calc = models.SafetyStockCalculation(
        organization_id=organization_id,
        product_id=calc.product_id,
        average_demand=calc.average_demand,
        demand_std_deviation=calc.demand_std_deviation,
        service_level=calc.service_level,
        z_score=z_score,
        calculated_safety_stock=safety_stock,
        reorder_point=calc.average_demand * 5 + safety_stock,
    )
    db.add(db_calc)
    await db.commit()
    await db.refresh(db_calc)
    return {"id": db_calc.id, "safety_stock": db_calc.calculated_safety_stock}


@router.get("/safety-stock")
async def list_safety_stock(
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """List safety stock calculations."""
    calcs = await db.query(models.SafetyStockCalculation).filter(
        models.SafetyStockCalculation.organization_id == organization_id
    ).all()
    return {"safety_stock_calcs": calcs, "total": len(calcs)}


# Supplier Performance Endpoints
@router.get("/supplier-performance")
async def get_supplier_performance(
    organization_id: int = Query(...),
    supplier_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get supplier performance metrics."""
    query = db.query(models.SupplierPerformance).filter(
        models.SupplierPerformance.organization_id == organization_id
    )
    
    if supplier_id:
        query = query.filter(models.SupplierPerformance.supplier_id == supplier_id)
    
    results = await query.all()
    
    if results:
        avg_score = sum([r.overall_performance_score for r in results]) / len(results)
        return {"suppliers": results, "average_performance_score": avg_score}
    
    return {"suppliers": [], "average_performance_score": 0}


# Reorder Optimization Endpoints
@router.post("/reorder-optimization")
async def optimize_reorder(
    opt: ReorderOptimizationCreate,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Calculate economic order quantity and reorder point."""
    import math
    
    # EOQ = sqrt(2 * D * S / H)
    eoq = math.sqrt(2 * 1000 * opt.ordering_cost_per_order / opt.holding_cost_per_unit)
    
    db_opt = models.ReorderOptimization(
        organization_id=organization_id,
        product_id=opt.product_id,
        current_reorder_point=opt.current_reorder_point,
        current_order_quantity=100,
        economic_order_quantity=eoq,
        holding_cost_per_unit=opt.holding_cost_per_unit,
        ordering_cost_per_order=opt.ordering_cost_per_order,
    )
    db.add(db_opt)
    await db.commit()
    await db.refresh(db_opt)
    return {"id": db_opt.id, "eoq": db_opt.economic_order_quantity}


@router.get("/reorder-optimization")
async def list_reorder_optimization(
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """List reorder optimization recommendations."""
    opts = await db.query(models.ReorderOptimization).filter(
        models.ReorderOptimization.organization_id == organization_id
    ).all()
    return {"optimizations": opts, "total": len(opts)}


# Inventory Turnover Analysis Endpoints
@router.get("/turnover-analysis")
async def get_inventory_turnover(
    organization_id: int = Query(...),
    product_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get inventory turnover analysis."""
    query = db.query(models.InventoryTurnoverAnalysis).filter(
        models.InventoryTurnoverAnalysis.organization_id == organization_id
    )
    
    if product_id:
        query = query.filter(models.InventoryTurnoverAnalysis.product_id == product_id)
    
    results = await query.all()
    
    if results:
        avg_turnover = sum([r.turnover_ratio for r in results if r.turnover_ratio]) / len(results)
        slow_moving_count = sum([1 for r in results if r.slow_moving_indicator])
        return {
            "analysis": results,
            "average_turnover": avg_turnover,
            "slow_moving_count": slow_moving_count
        }
    
    return {"analysis": [], "average_turnover": 0, "slow_moving_count": 0}


# Stockout Prevention Endpoints
@router.get("/stockout-prevention")
async def get_stockout_alerts(
    organization_id: int = Query(...),
    alert_status: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get stockout prevention alerts."""
    query = db.query(models.StockoutPrevention).filter(
        models.StockoutPrevention.organization_id == organization_id
    )
    
    if alert_status:
        query = query.filter(models.StockoutPrevention.alert_status == alert_status)
    
    alerts = await query.all()
    
    critical_count = sum([1 for a in alerts if a.alert_status == "critical"])
    warning_count = sum([1 for a in alerts if a.alert_status == "warning"])
    
    return {
        "alerts": alerts,
        "critical_count": critical_count,
        "warning_count": warning_count
    }


# Optimization Report Endpoints
@router.get("/optimization-report")
async def get_optimization_report(
    organization_id: int = Query(...),
    report_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get inventory optimization report."""
    if report_id:
        report = await db.query(models.InventoryOptimizationReport).filter(
            models.InventoryOptimizationReport.id == report_id,
            models.InventoryOptimizationReport.organization_id == organization_id
        ).first()
        
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        
        return {"report": report}
    
    reports = await db.query(models.InventoryOptimizationReport).filter(
        models.InventoryOptimizationReport.organization_id == organization_id
    ).all()
    
    return {"reports": reports, "total": len(reports)}


@router.post("/optimization-report")
async def create_optimization_report(
    report_name: str,
    period_covered: str,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Create an inventory optimization report."""
    report = models.InventoryOptimizationReport(
        organization_id=organization_id,
        report_name=report_name,
        period_covered=period_covered,
        total_products_analyzed=0,
    )
    db.add(report)
    await db.commit()
    await db.refresh(report)
    return {"id": report.id, "report_name": report.report_name}


# Health Check
@router.get("/health")
async def health_check():
    """Check inventory optimization module health."""
    return {
        "status": "healthy",
        "module": "advanced_inventory_optimization",
        "version": "1.0.0",
        "features": [
            "ABC Analysis",
            "Demand Forecasting",
            "Safety Stock Optimization",
            "Supplier Performance Tracking",
            "Reorder Optimization",
            "Inventory Turnover Analysis",
            "Stockout Prevention",
            "Optimization Reports"
        ]
    }
