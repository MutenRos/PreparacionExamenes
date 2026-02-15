"""Advanced Business Intelligence like Microsoft Dynamics 365."""

from datetime import datetime, timedelta, date
from typing import Any, Dict, List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_, cast, Float, case, literal_column, text
from decimal import Decimal
import statistics

from dario_app.modules.ventas.models import Venta, VentaDetalle
from dario_app.modules.compras.models import Compra, CompraDetalle
from dario_app.modules.inventario.models import Producto
from dario_app.modules.clientes.models import Cliente


class AdvancedAnalyticsService:
    """Enterprise BI service matching Dynamics 365 capabilities."""
    
    # ================== FINANCIAL KPIs ==================
    
    @staticmethod
    async def calculate_dso(
        db: AsyncSession,
        org_id: int,
        period_days: int = 90
    ) -> Dict[str, Any]:
        """Calculate Days Sales Outstanding (DSO) - average collection period."""
        start_date = datetime.utcnow() - timedelta(days=period_days)
        
        # Total sales (revenue)
        revenue_query = select(
            func.sum(Venta.total).label('total_revenue')
        ).where(
            Venta.organization_id == org_id,
            Venta.fecha >= start_date
        )
        revenue_result = await db.execute(revenue_query)
        total_revenue = float(revenue_result.scalar() or 0)
        
        # Accounts receivable (pending sales)
        ar_query = select(
            func.sum(Venta.total - Venta.total * 0).label('total_ar')
        ).where(
            Venta.organization_id == org_id,
            Venta.estado != 'pagado'
        )
        ar_result = await db.execute(ar_query)
        total_ar = float(ar_result.scalar() or 0)
        
        # DSO formula: (Accounts Receivable / Total Revenue) * Number of Days
        dso = (total_ar / total_revenue * period_days) if total_revenue > 0 else 0
        
        # Get aging buckets
        aging = await AdvancedAnalyticsService._calculate_ar_aging(db, org_id)
        
        return {
            "dso_days": round(dso, 1),
            "period_days": period_days,
            "total_revenue": round(total_revenue, 2),
            "total_accounts_receivable": round(total_ar, 2),
            "aging_buckets": aging,
            "interpretation": AdvancedAnalyticsService._interpret_dso(dso)
        }
    
    @staticmethod
    async def _calculate_ar_aging(
        db: AsyncSession,
        org_id: int
    ) -> Dict[str, Any]:
        """Calculate accounts receivable aging."""
        now = datetime.utcnow()
        
        # Get all pending sales
        query = select(Venta).where(
            Venta.organization_id == org_id,
            Venta.estado != 'pagado'
        )
        result = await db.execute(query)
        pending_sales = result.scalars().all()
        
        aging = {
            "current": {"count": 0, "amount": 0},  # 0-30 days
            "30_days": {"count": 0, "amount": 0},   # 31-60 days
            "60_days": {"count": 0, "amount": 0},   # 61-90 days
            "90_plus": {"count": 0, "amount": 0}    # 90+ days
        }
        
        for sale in pending_sales:
            days_outstanding = (now - sale.fecha).days
            outstanding_amount = float(sale.total - sale.total * 0)
            
            if days_outstanding <= 30:
                aging["current"]["count"] += 1
                aging["current"]["amount"] += outstanding_amount
            elif days_outstanding <= 60:
                aging["30_days"]["count"] += 1
                aging["30_days"]["amount"] += outstanding_amount
            elif days_outstanding <= 90:
                aging["60_days"]["count"] += 1
                aging["60_days"]["amount"] += outstanding_amount
            else:
                aging["90_plus"]["count"] += 1
                aging["90_plus"]["amount"] += outstanding_amount
        
        return aging
    
    @staticmethod
    def _interpret_dso(dso: float) -> str:
        """Interpret DSO value."""
        if dso < 30:
            return "Excellent - collecting payments quickly"
        elif dso < 45:
            return "Good - within industry standard"
        elif dso < 60:
            return "Fair - consider improving collection process"
        else:
            return "Poor - immediate action needed on collections"
    
    @staticmethod
    async def calculate_dpo(
        db: AsyncSession,
        org_id: int,
        period_days: int = 90
    ) -> Dict[str, Any]:
        """Calculate Days Payable Outstanding (DPO) - average payment period."""
        start_date = datetime.utcnow() - timedelta(days=period_days)
        
        # Total purchases (COGS)
        cogs_query = select(
            func.sum(Compra.total).label('total_cogs')
        ).where(
            Compra.organization_id == org_id,
            Compra.fecha >= start_date
        )
        cogs_result = await db.execute(cogs_query)
        total_cogs = float(cogs_result.scalar() or 0)
        
        # Accounts payable (pending purchases)
        ap_query = select(
            func.sum(Compra.total - Compra.total * 0).label('total_ap')
        ).where(
            Compra.organization_id == org_id,
            Compra.estado != 'pagado'
        )
        ap_result = await db.execute(ap_query)
        total_ap = float(ap_result.scalar() or 0)
        
        # DPO formula: (Accounts Payable / COGS) * Number of Days
        dpo = (total_ap / total_cogs * period_days) if total_cogs > 0 else 0
        
        return {
            "dpo_days": round(dpo, 1),
            "period_days": period_days,
            "total_cogs": round(total_cogs, 2),
            "total_accounts_payable": round(total_ap, 2),
            "interpretation": "Optimal DPO balances cash flow and supplier relationships"
        }
    
    @staticmethod
    async def calculate_cash_flow_forecast(
        db: AsyncSession,
        org_id: int,
        forecast_days: int = 30
    ) -> Dict[str, Any]:
        """Forecast cash flow based on historical patterns."""
        
        # Get historical cash flow data (90 days)
        historical_days = 90
        start_date = datetime.utcnow() - timedelta(days=historical_days)
        
        # Daily revenue
        revenue_query = select(
            func.date(Venta.fecha).label('date'),
            func.sum(Venta.total).label('inflow')
        ).where(
            Venta.organization_id == org_id,
            Venta.fecha >= start_date
        ).group_by(
            func.date(Venta.fecha)
        )
        revenue_result = await db.execute(revenue_query)
        daily_revenue = {row.date: float(row.inflow) for row in revenue_result.all()}
        
        # Daily expenses
        expenses_query = select(
            func.date(Compra.fecha).label('date'),
            func.sum(Compra.total).label('outflow')
        ).where(
            Compra.organization_id == org_id,
            Compra.fecha >= start_date
        ).group_by(
            func.date(Compra.fecha)
        )
        expenses_result = await db.execute(expenses_query)
        daily_expenses = {row.date: float(row.outflow) for row in expenses_result.all()}
        
        # Calculate average daily cash flow
        all_dates = set(list(daily_revenue.keys()) + list(daily_expenses.keys()))
        daily_net_cash_flow = []
        
        for date_val in all_dates:
            net = daily_revenue.get(date_val, 0) - daily_expenses.get(date_val, 0)
            daily_net_cash_flow.append(net)
        
        avg_daily_cash_flow = statistics.mean(daily_net_cash_flow) if daily_net_cash_flow else 0
        std_dev = statistics.stdev(daily_net_cash_flow) if len(daily_net_cash_flow) > 1 else 0
        
        # Forecast
        forecast = []
        cumulative = 0
        
        for day in range(1, forecast_days + 1):
            forecast_date = datetime.utcnow().date() + timedelta(days=day)
            expected_cash_flow = avg_daily_cash_flow
            cumulative += expected_cash_flow
            
            forecast.append({
                "date": forecast_date.isoformat(),
                "expected_cash_flow": round(expected_cash_flow, 2),
                "cumulative_cash_flow": round(cumulative, 2),
                "confidence_range": {
                    "low": round(expected_cash_flow - std_dev, 2),
                    "high": round(expected_cash_flow + std_dev, 2)
                }
            })
        
        return {
            "forecast_period_days": forecast_days,
            "historical_period_days": historical_days,
            "avg_daily_cash_flow": round(avg_daily_cash_flow, 2),
            "forecasted_net_cash_flow": round(cumulative, 2),
            "forecast": forecast,
            "insights": {
                "trend": "positive" if avg_daily_cash_flow > 0 else "negative",
                "volatility": "high" if std_dev > abs(avg_daily_cash_flow) else "low"
            }
        }
    
    # ================== INVENTORY KPIs ==================
    
    @staticmethod
    async def calculate_inventory_turnover(
        db: AsyncSession,
        org_id: int,
        period_days: int = 365
    ) -> Dict[str, Any]:
        """Calculate inventory turnover ratio."""
        start_date = datetime.utcnow() - timedelta(days=period_days)
        
        # Cost of Goods Sold (COGS)
        cogs_query = select(
            func.sum(VentaDetalle.cantidad * Producto.precio_compra).label('cogs')
        ).join(
            Producto, Producto.id == VentaDetalle.producto_id
        ).join(
            Venta, Venta.id == VentaDetalle.venta_id
        ).where(
            Producto.organization_id == org_id,
            Venta.fecha >= start_date
        )
        cogs_result = await db.execute(cogs_query)
        cogs = float(cogs_result.scalar() or 0)
        
        # Average Inventory Value
        inventory_query = select(
            func.sum(Producto.stock_actual * Producto.precio_compra).label('inventory_value')
        ).where(
            Producto.organization_id == org_id,
            Producto.activo == True
        )
        inventory_result = await db.execute(inventory_query)
        avg_inventory_value = float(inventory_result.scalar() or 0)
        
        # Turnover ratio
        turnover_ratio = (cogs / avg_inventory_value) if avg_inventory_value > 0 else 0
        days_inventory_outstanding = (365 / turnover_ratio) if turnover_ratio > 0 else 999
        
        # Get slow-moving items
        slow_movers = await AdvancedAnalyticsService._identify_slow_movers(db, org_id)
        
        return {
            "turnover_ratio": round(turnover_ratio, 2),
            "days_inventory_outstanding": round(days_inventory_outstanding, 1),
            "cogs": round(cogs, 2),
            "avg_inventory_value": round(avg_inventory_value, 2),
            "slow_moving_items": slow_movers,
            "interpretation": AdvancedAnalyticsService._interpret_turnover(turnover_ratio)
        }
    
    @staticmethod
    async def _identify_slow_movers(
        db: AsyncSession,
        org_id: int,
        threshold_days: int = 90
    ) -> List[Dict[str, Any]]:
        """Identify slow-moving inventory items."""
        cutoff_date = datetime.utcnow() - timedelta(days=threshold_days)
        
        # Products with no recent sales
        query = select(Producto).where(
            Producto.organization_id == org_id,
            Producto.activo == True,
            Producto.stock_actual > 0
        )
        result = await db.execute(query)
        products = result.scalars().all()
        
        slow_movers = []
        for product in products[:20]:  # Top 20
            # Check last sale
            last_sale_query = select(func.max(Venta.fecha)).join(
                VentaDetalle, VentaDetalle.venta_id == Venta.id
            ).where(
                VentaDetalle.producto_id == product.id
            )
            last_sale_result = await db.execute(last_sale_query)
            last_sale = last_sale_result.scalar()
            
            if not last_sale or last_sale < cutoff_date:
                days_since_sale = (datetime.utcnow() - last_sale).days if last_sale else 999
                
                slow_movers.append({
                    "product_id": product.id,
                    "product_name": product.nombre,
                    "current_stock": product.stock_actual,
                    "stock_value": round(float(product.stock_actual * product.precio_compra), 2),
                    "days_since_last_sale": days_since_sale,
                    "recommendation": "Consider promotion or clearance"
                })
        
        return slow_movers
    
    @staticmethod
    def _interpret_turnover(turnover: float) -> str:
        """Interpret inventory turnover ratio."""
        if turnover > 12:
            return "Excellent - inventory moving very fast"
        elif turnover > 6:
            return "Good - healthy inventory turnover"
        elif turnover > 3:
            return "Fair - consider optimizing stock levels"
        else:
            return "Poor - high risk of obsolete inventory"
    
    # ================== OPERATIONAL KPIs ==================
    
    @staticmethod
    async def calculate_otif(
        db: AsyncSession,
        org_id: int,
        period_days: int = 30
    ) -> Dict[str, Any]:
        """Calculate On-Time In-Full (OTIF) delivery performance."""
        start_date = datetime.utcnow() - timedelta(days=period_days)
        
        # Get all completed sales
        query = select(Venta).where(
            Venta.organization_id == org_id,
            Venta.fecha >= start_date,
            Venta.estado.in_(['completado', 'entregado'])
        )
        result = await db.execute(query)
        completed_sales = result.scalars().all()
        
        if not completed_sales:
            return {
                "otif_percentage": 0,
                "total_orders": 0,
                "on_time": 0,
                "in_full": 0,
                "otif": 0
            }
        
        on_time_count = 0
        in_full_count = 0
        otif_count = 0
        
        for sale in completed_sales:
            # Assume delivery expected within 7 days
            expected_delivery = sale.fecha + timedelta(days=7)
            delivered_on_time = (datetime.utcnow() <= expected_delivery)
            
            # Check if order was fulfilled completely (simplified)
            delivered_in_full = (sale.estado == 'completado')
            
            if delivered_on_time:
                on_time_count += 1
            
            if delivered_in_full:
                in_full_count += 1
            
            if delivered_on_time and delivered_in_full:
                otif_count += 1
        
        total = len(completed_sales)
        
        return {
            "period_days": period_days,
            "total_orders": total,
            "on_time_count": on_time_count,
            "in_full_count": in_full_count,
            "otif_count": otif_count,
            "on_time_percentage": round((on_time_count / total * 100), 1),
            "in_full_percentage": round((in_full_count / total * 100), 1),
            "otif_percentage": round((otif_count / total * 100), 1),
            "target": 95.0,
            "performance": "Excellent" if (otif_count / total * 100) >= 95 else "Needs improvement"
        }
    
    @staticmethod
    async def calculate_order_fill_rate(
        db: AsyncSession,
        org_id: int,
        period_days: int = 30
    ) -> Dict[str, Any]:
        """Calculate order fill rate (ability to fulfill orders from stock)."""
        start_date = datetime.utcnow() - timedelta(days=period_days)
        
        # Get all order lines
        query = select(VentaDetalle).join(
            Venta, Venta.id == VentaDetalle.venta_id
        ).where(
            Venta.organization_id == org_id,
            Venta.fecha >= start_date
        )
        result = await db.execute(query)
        order_lines = result.scalars().all()
        
        total_lines = len(order_lines)
        fulfilled_lines = 0
        
        for line in order_lines:
            # Get product current stock
            product_query = select(Producto).where(Producto.id == line.producto_id)
            product_result = await db.execute(product_query)
            product = product_result.scalar_one_or_none()
            
            if product and product.stock_actual >= line.cantidad:
                fulfilled_lines += 1
        
        fill_rate = (fulfilled_lines / total_lines * 100) if total_lines > 0 else 0
        
        return {
            "period_days": period_days,
            "total_order_lines": total_lines,
            "fulfilled_lines": fulfilled_lines,
            "unfulfilled_lines": total_lines - fulfilled_lines,
            "fill_rate_percentage": round(fill_rate, 1),
            "target": 98.0,
            "performance": "Excellent" if fill_rate >= 98 else "Needs improvement"
        }
    
    # ================== ROLE-BASED DASHBOARDS ==================
    
    @staticmethod
    async def get_executive_dashboard(
        db: AsyncSession,
        org_id: int
    ) -> Dict[str, Any]:
        """Executive-level dashboard with high-level KPIs."""
        period_days = 30
        start_date = datetime.utcnow() - timedelta(days=period_days)
        prev_start = start_date - timedelta(days=period_days)
        
        # Revenue metrics
        current_revenue_query = select(func.sum(Venta.total)).where(
            Venta.organization_id == org_id,
            Venta.fecha >= start_date
        )
        current_revenue = float((await db.execute(current_revenue_query)).scalar() or 0)
        
        prev_revenue_query = select(func.sum(Venta.total)).where(
            Venta.organization_id == org_id,
            Venta.fecha >= prev_start,
            Venta.fecha < start_date
        )
        prev_revenue = float((await db.execute(prev_revenue_query)).scalar() or 0)
        
        revenue_growth = ((current_revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0
        
        # Get DSO
        dso_data = await AdvancedAnalyticsService.calculate_dso(db, org_id, period_days)
        
        # Get cash flow forecast
        cash_flow = await AdvancedAnalyticsService.calculate_cash_flow_forecast(db, org_id, 30)
        
        # Get inventory turnover
        inventory = await AdvancedAnalyticsService.calculate_inventory_turnover(db, org_id, 90)
        
        return {
            "dashboard_type": "executive",
            "period": f"Last {period_days} days",
            "revenue": {
                "current": round(current_revenue, 2),
                "previous": round(prev_revenue, 2),
                "growth_percentage": round(revenue_growth, 1),
                "trend": "up" if revenue_growth > 0 else "down"
            },
            "cash_collection": {
                "dso_days": dso_data["dso_days"],
                "interpretation": dso_data["interpretation"]
            },
            "cash_flow": {
                "forecasted_30_days": cash_flow["forecasted_net_cash_flow"],
                "trend": cash_flow["insights"]["trend"]
            },
            "inventory": {
                "turnover_ratio": inventory["turnover_ratio"],
                "interpretation": inventory["interpretation"]
            }
        }
    
    @staticmethod
    async def get_sales_dashboard(
        db: AsyncSession,
        org_id: int
    ) -> Dict[str, Any]:
        """Sales team dashboard."""
        period_days = 30
        start_date = datetime.utcnow() - timedelta(days=period_days)
        
        # Sales metrics
        sales_query = select(
            func.count(Venta.id).label('total_orders'),
            func.sum(Venta.total).label('total_revenue'),
            func.avg(Venta.total).label('avg_order_value')
        ).where(
            Venta.organization_id == org_id,
            Venta.fecha >= start_date
        )
        sales_result = await db.execute(sales_query)
        sales_metrics = sales_result.first()
        
        # Top customers
        top_customers_query = select(
            Cliente.nombre,
            func.sum(Venta.total).label('total_spent')
        ).join(
            Venta, Venta.cliente_id == Cliente.id
        ).where(
            Venta.organization_id == org_id,
            Venta.fecha >= start_date
        ).group_by(
            Cliente.nombre
        ).order_by(
            func.sum(Venta.total).desc()
        ).limit(10)
        
        top_customers_result = await db.execute(top_customers_query)
        top_customers = [
            {"customer": row.nombre, "total_spent": float(row.total_spent)}
            for row in top_customers_result.all()
        ]
        
        return {
            "dashboard_type": "sales",
            "period": f"Last {period_days} days",
            "metrics": {
                "total_orders": sales_metrics.total_orders or 0,
                "total_revenue": round(float(sales_metrics.total_revenue or 0), 2),
                "avg_order_value": round(float(sales_metrics.avg_order_value or 0), 2)
            },
            "top_customers": top_customers
        }
    
    @staticmethod
    async def get_operations_dashboard(
        db: AsyncSession,
        org_id: int
    ) -> Dict[str, Any]:
        """Operations dashboard with fulfillment metrics."""
        
        # Get OTIF
        otif = await AdvancedAnalyticsService.calculate_otif(db, org_id, 30)
        
        # Get fill rate
        fill_rate = await AdvancedAnalyticsService.calculate_order_fill_rate(db, org_id, 30)
        
        # Inventory health
        inventory_turnover = await AdvancedAnalyticsService.calculate_inventory_turnover(db, org_id, 90)
        
        return {
            "dashboard_type": "operations",
            "period": "Last 30 days",
            "otif": {
                "percentage": otif["otif_percentage"],
                "target": otif["target"],
                "status": otif["performance"]
            },
            "fill_rate": {
                "percentage": fill_rate["fill_rate_percentage"],
                "target": fill_rate["target"],
                "status": fill_rate["performance"]
            },
            "inventory": {
                "turnover_ratio": inventory_turnover["turnover_ratio"],
                "days_on_hand": inventory_turnover["days_inventory_outstanding"],
                "slow_movers_count": len(inventory_turnover["slow_moving_items"])
            }
        }
    
    @staticmethod
    async def get_financial_dashboard(
        db: AsyncSession,
        org_id: int
    ) -> Dict[str, Any]:
        """Financial controller dashboard."""
        
        # DSO
        dso = await AdvancedAnalyticsService.calculate_dso(db, org_id, 90)
        
        # DPO
        dpo = await AdvancedAnalyticsService.calculate_dpo(db, org_id, 90)
        
        # Cash flow
        cash_flow = await AdvancedAnalyticsService.calculate_cash_flow_forecast(db, org_id, 30)
        
        # Working capital metrics
        ar = dso["total_accounts_receivable"]
        ap = dpo["total_accounts_payable"]
        working_capital = ar - ap
        
        return {
            "dashboard_type": "financial",
            "period": "Last 90 days",
            "accounts_receivable": {
                "total": round(ar, 2),
                "dso_days": dso["dso_days"],
                "aging": dso["aging_buckets"]
            },
            "accounts_payable": {
                "total": round(ap, 2),
                "dpo_days": dpo["dpo_days"]
            },
            "working_capital": {
                "amount": round(working_capital, 2),
                "status": "positive" if working_capital > 0 else "negative"
            },
            "cash_flow_forecast": {
                "next_30_days": cash_flow["forecasted_net_cash_flow"],
                "trend": cash_flow["insights"]["trend"]
            }
        }


# Global instance
advanced_analytics_service = AdvancedAnalyticsService()
