"""Advanced analytics and Business Intelligence service."""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from decimal import Decimal

from dario_app.modules.ventas.models import Venta, VentaDetalle
from dario_app.modules.compras.models import Compra, CompraDetalle
from dario_app.modules.inventario.models import Producto
from dario_app.modules.clientes.models import Cliente


class AnalyticsService:
    """Enterprise analytics and BI service."""
    
    @staticmethod
    async def get_revenue_forecast(
        db: AsyncSession,
        org_id: int,
        days: int = 30
    ) -> Dict[str, Any]:
        """Predict revenue using linear regression on historical data."""
        from datetime import date
        
        # Get historical sales (last 90 days)
        start_date = datetime.utcnow() - timedelta(days=90)
        
        query = select(
            func.date(Venta.fecha_venta).label('date'),
            func.sum(Venta.total).label('revenue')
        ).where(
            Venta.organization_id == org_id,
            Venta.fecha_venta >= start_date
        ).group_by(
            func.date(Venta.fecha_venta)
        ).order_by('date')
        
        result = await db.execute(query)
        historical = result.all()
        
        if len(historical) < 7:
            return {"error": "Insufficient historical data"}
        
        # Simple linear regression
        x = list(range(len(historical)))
        y = [float(row.revenue) for row in historical]
        
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_x2 = sum(xi * xi for xi in x)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        intercept = (sum_y - slope * sum_x) / n
        
        # Forecast next days
        forecast = []
        for i in range(days):
            future_x = len(historical) + i
            predicted_revenue = slope * future_x + intercept
            forecast_date = datetime.utcnow().date() + timedelta(days=i)
            
            forecast.append({
                "date": forecast_date.isoformat(),
                "predicted_revenue": round(predicted_revenue, 2)
            })
        
        return {
            "forecast_period_days": days,
            "model": {
                "slope": round(slope, 2),
                "intercept": round(intercept, 2)
            },
            "forecast": forecast,
            "total_predicted_revenue": round(sum(f["predicted_revenue"] for f in forecast), 2)
        }
    
    @staticmethod
    async def get_customer_segmentation(
        db: AsyncSession,
        org_id: int
    ) -> Dict[str, Any]:
        """Segment customers by RFM (Recency, Frequency, Monetary)."""
        # Get all customers with their purchase stats
        query = select(
            Cliente.id,
            Cliente.nombre,
            func.max(Venta.fecha_venta).label('last_purchase'),
            func.count(Venta.id).label('purchase_count'),
            func.sum(Venta.total).label('total_spent')
        ).join(
            Venta, Venta.cliente_id == Cliente.id
        ).where(
            Cliente.organization_id == org_id
        ).group_by(
            Cliente.id, Cliente.nombre
        )
        
        result = await db.execute(query)
        customers = result.all()
        
        if not customers:
            return {"segments": []}
        
        # Calculate RFM scores
        now = datetime.utcnow()
        rfm_data = []
        
        for customer in customers:
            recency = (now - customer.last_purchase).days if customer.last_purchase else 999
            frequency = customer.purchase_count
            monetary = float(customer.total_spent) if customer.total_spent else 0
            
            rfm_data.append({
                "customer_id": customer.id,
                "customer_name": customer.nombre,
                "recency": recency,
                "frequency": frequency,
                "monetary": monetary
            })
        
        # Simple segmentation
        segments = {
            "champions": [],  # High frequency, high monetary, low recency
            "loyal": [],      # High frequency, medium monetary
            "at_risk": [],    # High monetary but high recency
            "lost": []        # High recency, low frequency
        }
        
        for data in rfm_data:
            if data["recency"] < 30 and data["frequency"] >= 5 and data["monetary"] >= 1000:
                segments["champions"].append(data)
            elif data["frequency"] >= 3:
                segments["loyal"].append(data)
            elif data["recency"] > 90 and data["monetary"] >= 500:
                segments["at_risk"].append(data)
            elif data["recency"] > 180:
                segments["lost"].append(data)
        
        return {
            "total_customers": len(customers),
            "segments": {
                key: {
                    "count": len(value),
                    "customers": value[:10]  # Top 10
                }
                for key, value in segments.items()
            }
        }
    
    @staticmethod
    async def get_product_performance(
        db: AsyncSession,
        org_id: int,
        days: int = 30
    ) -> Dict[str, Any]:
        """Analyze product performance metrics."""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Sales by product
        query = select(
            Producto.id,
            Producto.nombre,
            Producto.precio_venta,
            func.sum(VentaDetalle.cantidad).label('units_sold'),
            func.sum(VentaDetalle.subtotal).label('revenue')
        ).join(
            VentaDetalle, VentaDetalle.producto_id == Producto.id
        ).join(
            Venta, Venta.id == VentaDetalle.venta_id
        ).where(
            Producto.organization_id == org_id,
            Venta.fecha_venta >= start_date
        ).group_by(
            Producto.id, Producto.nombre, Producto.precio_venta
        ).order_by(
            func.sum(VentaDetalle.subtotal).desc()
        ).limit(50)
        
        result = await db.execute(query)
        products = result.all()
        
        # Calculate metrics
        performance = []
        total_revenue = sum(float(p.revenue) for p in products)
        
        for product in products:
            revenue = float(product.revenue)
            contribution = (revenue / total_revenue * 100) if total_revenue > 0 else 0
            
            performance.append({
                "product_id": product.id,
                "product_name": product.nombre,
                "units_sold": product.units_sold,
                "revenue": revenue,
                "contribution_percentage": round(contribution, 2),
                "avg_price": round(revenue / product.units_sold, 2) if product.units_sold > 0 else 0
            })
        
        # Pareto analysis (80/20 rule)
        cumulative = 0
        pareto_products = []
        for p in performance:
            cumulative += p["contribution_percentage"]
            pareto_products.append(p["product_id"])
            if cumulative >= 80:
                break
        
        return {
            "period_days": days,
            "total_revenue": round(total_revenue, 2),
            "products_analyzed": len(products),
            "top_performers": performance[:10],
            "pareto_80_20": {
                "products_generating_80_percent": len(pareto_products),
                "product_ids": pareto_products
            }
        }
    
    @staticmethod
    async def get_inventory_optimization(
        db: AsyncSession,
        org_id: int
    ) -> Dict[str, Any]:
        """Recommend inventory optimization actions."""
        # Get products with stock and sales data
        query = select(Producto).where(
            Producto.organization_id == org_id,
            Producto.activo == True
        )
        
        result = await db.execute(query)
        products = result.scalars().all()
        
        recommendations = {
            "overstock": [],
            "understock": [],
            "optimal": [],
            "dead_stock": []
        }
        
        for product in products:
            stock_days = (product.stock_actual / product.stock_minimo * 30) if product.stock_minimo > 0 else 999
            
            if stock_days > 90:
                recommendations["overstock"].append({
                    "product_id": product.id,
                    "product_name": product.nombre,
                    "current_stock": product.stock_actual,
                    "stock_days": round(stock_days, 1),
                    "action": "Reduce orders or run promotion"
                })
            elif product.stock_actual < product.stock_minimo:
                recommendations["understock"].append({
                    "product_id": product.id,
                    "product_name": product.nombre,
                    "current_stock": product.stock_actual,
                    "minimum_stock": product.stock_minimo,
                    "action": "Reorder immediately"
                })
            elif stock_days > 180 and product.stock_actual > 0:
                recommendations["dead_stock"].append({
                    "product_id": product.id,
                    "product_name": product.nombre,
                    "current_stock": product.stock_actual,
                    "action": "Consider clearance sale"
                })
            else:
                recommendations["optimal"].append({
                    "product_id": product.id,
                    "product_name": product.nombre,
                    "current_stock": product.stock_actual
                })
        
        return {
            "total_products": len(products),
            "recommendations": {
                key: {"count": len(value), "items": value[:10]}
                for key, value in recommendations.items()
            }
        }
    
    @staticmethod
    async def get_kpi_dashboard(
        db: AsyncSession,
        org_id: int,
        period_days: int = 30
    ) -> Dict[str, Any]:
        """Get comprehensive KPI dashboard."""
        start_date = datetime.utcnow() - timedelta(days=period_days)
        prev_start_date = start_date - timedelta(days=period_days)
        
        # Current period sales
        current_query = select(
            func.count(Venta.id).label('order_count'),
            func.sum(Venta.total).label('revenue'),
            func.avg(Venta.total).label('avg_order_value')
        ).where(
            Venta.organization_id == org_id,
            Venta.fecha_venta >= start_date
        )
        
        current_result = await db.execute(current_query)
        current = current_result.first()
        
        # Previous period sales
        prev_query = select(
            func.count(Venta.id).label('order_count'),
            func.sum(Venta.total).label('revenue')
        ).where(
            Venta.organization_id == org_id,
            Venta.fecha_venta >= prev_start_date,
            Venta.fecha_venta < start_date
        )
        
        prev_result = await db.execute(prev_query)
        previous = prev_result.first()
        
        # Calculate growth
        revenue_growth = 0
        if previous.revenue and previous.revenue > 0:
            revenue_growth = ((float(current.revenue or 0) - float(previous.revenue)) / float(previous.revenue)) * 100
        
        order_growth = 0
        if previous.order_count and previous.order_count > 0:
            order_growth = ((current.order_count - previous.order_count) / previous.order_count) * 100
        
        return {
            "period_days": period_days,
            "kpis": {
                "revenue": {
                    "current": round(float(current.revenue or 0), 2),
                    "growth_percentage": round(revenue_growth, 2)
                },
                "orders": {
                    "current": current.order_count or 0,
                    "growth_percentage": round(order_growth, 2)
                },
                "average_order_value": {
                    "current": round(float(current.avg_order_value or 0), 2)
                }
            }
        }
