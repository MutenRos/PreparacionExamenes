"""Supply Chain service - MRP, EOQ, Reorder logic, Landed Cost calculations."""

from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Dict, Any, Optional
import math

from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from .models import (
    ReorderPolicy, MRPRun, MRPRequirement, LandedCostHeader, 
    LandedCostLine, LandedCostAllocation, InventoryLocation, InventoryByLocation
)


class SupplyChainService:
    """Supply chain planning and optimization service."""
    
    @staticmethod
    async def calculate_eoq(
        annual_demand: Decimal,
        ordering_cost: Decimal,
        holding_cost_percent: Decimal,
        unit_cost: Decimal
    ) -> Dict[str, Any]:
        """Calculate Economic Order Quantity (EOQ)."""
        
        # EOQ formula: sqrt((2 * D * S) / H)
        # D = annual demand
        # S = ordering cost per order
        # H = holding cost per unit per year = unit_cost * holding_cost_percent
        
        annual_demand_float = float(annual_demand)
        ordering_cost_float = float(ordering_cost)
        holding_cost_per_unit = float(unit_cost) * (float(holding_cost_percent) / 100)
        
        if holding_cost_per_unit <= 0:
            return {"error": "Holding cost must be positive"}
        
        eoq = math.sqrt((2 * annual_demand_float * ordering_cost_float) / holding_cost_per_unit)
        
        # Number of orders per year
        orders_per_year = annual_demand_float / eoq if eoq > 0 else 0
        
        # Total annual cost
        annual_ordering_cost = orders_per_year * ordering_cost_float
        annual_holding_cost = (eoq / 2) * holding_cost_per_unit
        total_annual_cost = annual_ordering_cost + annual_holding_cost
        
        return {
            "eoq": round(Decimal(str(eoq)), 2),
            "orders_per_year": round(Decimal(str(orders_per_year)), 2),
            "days_between_orders": round(Decimal(str(365 / orders_per_year)), 1) if orders_per_year > 0 else Decimal("0"),
            "annual_ordering_cost": round(Decimal(str(annual_ordering_cost)), 2),
            "annual_holding_cost": round(Decimal(str(annual_holding_cost)), 2),
            "total_annual_cost": round(Decimal(str(total_annual_cost)), 2)
        }
    
    @staticmethod
    async def calculate_reorder_point(
        daily_demand: Decimal,
        lead_time_days: int,
        safety_stock: Decimal
    ) -> Decimal:
        """Calculate reorder point."""
        # ROP = (average daily demand × lead time) + safety stock
        return (daily_demand * Decimal(str(lead_time_days))) + safety_stock
    
    @staticmethod
    async def check_reorder_needed(
        db: AsyncSession,
        organization_id: int,
        producto_id: int
    ) -> Optional[Dict[str, Any]]:
        """Check if product needs reordering based on policy."""
        from dario_app.modules.inventario.models import Producto
        
        # Get reorder policy
        stmt = select(ReorderPolicy).where(
            ReorderPolicy.organization_id == organization_id,
            ReorderPolicy.producto_id == producto_id,
            ReorderPolicy.activo == True
        )
        result = await db.execute(stmt)
        policy = result.scalar_one_or_none()
        
        if not policy:
            return None
        
        # Get current inventory
        stmt_prod = select(Producto).where(
            Producto.id == producto_id,
            Producto.organization_id == organization_id
        )
        result_prod = await db.execute(stmt_prod)
        producto = result_prod.scalar_one_or_none()
        
        if not producto:
            return None
        
        current_stock = producto.stock_actual or Decimal("0")
        
        # Check based on policy type
        reorder_needed = False
        reorder_quantity = Decimal("0")
        reason = ""
        
        if policy.policy_type == "reorder_point":
            if current_stock <= policy.reorder_point:
                reorder_needed = True
                reorder_quantity = policy.reorder_quantity
                reason = f"Stock ({current_stock}) below reorder point ({policy.reorder_point})"
        
        elif policy.policy_type == "min_max":
            if current_stock < policy.min_quantity:
                reorder_needed = True
                reorder_quantity = policy.max_quantity - current_stock
                reason = f"Stock ({current_stock}) below minimum ({policy.min_quantity})"
        
        elif policy.policy_type == "economic_order_quantity":
            # Calculate EOQ
            if policy.annual_demand and policy.ordering_cost and policy.holding_cost_percent and producto.precio_compra:
                eoq_result = await SupplyChainService.calculate_eoq(
                    policy.annual_demand,
                    policy.ordering_cost,
                    policy.holding_cost_percent,
                    producto.precio_compra
                )
                
                # Check if below reorder point (if set), otherwise use safety stock
                threshold = policy.reorder_point if policy.reorder_point > 0 else policy.safety_stock
                if current_stock <= threshold:
                    reorder_needed = True
                    reorder_quantity = eoq_result["eoq"]
                    reason = f"EOQ triggered: stock ({current_stock}) at/below threshold ({threshold})"
        
        if reorder_needed:
            return {
                "producto_id": producto_id,
                "producto_codigo": producto.codigo,
                "producto_nombre": producto.nombre,
                "current_stock": current_stock,
                "policy_type": policy.policy_type,
                "reorder_quantity": reorder_quantity,
                "preferred_supplier_id": policy.preferred_supplier_id,
                "preferred_supplier_name": policy.preferred_supplier_name,
                "lead_time_days": policy.lead_time_days,
                "reason": reason,
                "auto_reorder_enabled": policy.auto_reorder_enabled
            }
        
        return None
    
    @staticmethod
    async def run_mrp(
        db: AsyncSession,
        organization_id: int,
        horizon_days: int = 90,
        user_id: Optional[int] = None,
        user_name: Optional[str] = None
    ) -> MRPRun:
        """Run MRP calculation."""
        from dario_app.modules.ventas.models import Venta, VentaDetalle
        
        # Create MRP run
        mrp_run = MRPRun(
            organization_id=organization_id,
            horizon_days=horizon_days,
            run_by_user_id=user_id,
            run_by_user_name=user_name,
            status="running",
            started_at=datetime.utcnow()
        )
        db.add(mrp_run)
        await db.flush()
        
        try:
            # Calculate requirements from sales orders
            end_date = datetime.utcnow() + timedelta(days=horizon_days)
            
            stmt = select(VentaDetalle).join(Venta).where(
                Venta.organization_id == organization_id,
                Venta.fecha_entrega <= end_date,
                Venta.fecha_entrega >= datetime.utcnow(),
                Venta.estado.in_(["pendiente", "confirmado"])
            )
            
            result = await db.execute(stmt)
            ventas_detalle = result.scalars().all()
            
            requirements_created = 0
            
            for detalle in ventas_detalle:
                # Get current inventory
                from dario_app.modules.inventario.models import Producto
                stmt_prod = select(Producto).where(
                    Producto.id == detalle.producto_id,
                    Producto.organization_id == organization_id
                )
                result_prod = await db.execute(stmt_prod)
                producto = result_prod.scalar_one_or_none()
                
                if not producto:
                    continue
                
                on_hand = producto.stock_actual or Decimal("0")
                allocated = Decimal("0")  # TODO: calculate from pending orders
                available = on_hand - allocated
                
                required_qty = detalle.cantidad - detalle.cantidad_entregada
                
                if required_qty <= 0:
                    continue
                
                # Determine action
                suggested_action = "none"
                order_quantity = Decimal("0")
                
                if available < required_qty:
                    shortage = required_qty - available
                    
                    # Check if product can be produced or needs to be purchased
                    # TODO: Check BOM existence
                    suggested_action = "purchase"  # Default to purchase
                    order_quantity = shortage
                
                # Create requirement
                requirement = MRPRequirement(
                    organization_id=organization_id,
                    mrp_run_id=mrp_run.id,
                    producto_id=detalle.producto_id,
                    producto_codigo=producto.codigo,
                    producto_nombre=producto.nombre,
                    required_quantity=required_qty,
                    required_date=detalle.venta.fecha_entrega,
                    on_hand_quantity=on_hand,
                    allocated_quantity=allocated,
                    available_quantity=available,
                    source_type="sales_order",
                    source_id=detalle.venta_id,
                    source_reference=detalle.venta.numero_venta,
                    suggested_action=suggested_action,
                    order_quantity=order_quantity if order_quantity > 0 else None
                )
                db.add(requirement)
                requirements_created += 1
            
            # Complete MRP run
            mrp_run.status = "completed"
            mrp_run.completed_at = datetime.utcnow()
            mrp_run.duration_seconds = int((mrp_run.completed_at - mrp_run.started_at).total_seconds())
            mrp_run.total_requirements = requirements_created
            
            await db.commit()
            await db.refresh(mrp_run)
            
        except Exception as e:
            mrp_run.status = "failed"
            mrp_run.completed_at = datetime.utcnow()
            mrp_run.error_message = str(e)
            await db.commit()
            await db.refresh(mrp_run)
        
        return mrp_run
    
    @staticmethod
    async def calculate_landed_cost(
        db: AsyncSession,
        organization_id: int,
        landed_cost_header_id: int
    ) -> LandedCostHeader:
        """Calculate and allocate landed costs to products."""
        from dario_app.modules.compras.models import Compra, CompraDetalle
        
        # Get landed cost header
        stmt = select(LandedCostHeader).where(
            LandedCostHeader.id == landed_cost_header_id,
            LandedCostHeader.organization_id == organization_id
        )
        result = await db.execute(stmt)
        header = result.scalar_one_or_none()
        
        if not header:
            raise ValueError("Landed cost header not found")
        
        # Get purchase order details
        stmt_compra = select(CompraDetalle).join(Compra).where(
            Compra.id == header.compra_id,
            Compra.organization_id == organization_id
        )
        result_compra = await db.execute(stmt_compra)
        compra_detalles = result_compra.scalars().all()
        
        # Calculate total merchandise value
        total_value = sum(d.precio_unitario * d.cantidad for d in compra_detalles)
        header.merchandise_value = total_value
        
        # Get all cost lines
        stmt_lines = select(LandedCostLine).where(
            LandedCostLine.landed_cost_header_id == header.id
        )
        result_lines = await db.execute(stmt_lines)
        cost_lines = result_lines.scalars().all()
        
        # Calculate total landed costs
        total_landed_costs = sum(line.cost_amount for line in cost_lines)
        header.total_landed_costs = total_landed_costs
        header.total_value = total_value + total_landed_costs
        
        # Delete existing allocations
        stmt_del = select(LandedCostAllocation).where(
            LandedCostAllocation.landed_cost_header_id == header.id
        )
        result_del = await db.execute(stmt_del)
        existing_allocs = result_del.scalars().all()
        for alloc in existing_allocs:
            await db.delete(alloc)
        
        # Allocate costs to products
        for line in cost_lines:
            for detalle in compra_detalles:
                # Calculate allocation based on method
                allocation_ratio = Decimal("0")
                
                if line.allocation_method == "by_value":
                    line_value = detalle.precio_unitario * detalle.cantidad
                    allocation_ratio = line_value / total_value if total_value > 0 else Decimal("0")
                
                elif line.allocation_method == "by_quantity":
                    total_qty = sum(d.cantidad for d in compra_detalles)
                    allocation_ratio = detalle.cantidad / total_qty if total_qty > 0 else Decimal("0")
                
                # TODO: Implement by_weight, by_volume when product has those attributes
                
                allocated_amount = line.cost_amount * allocation_ratio
                allocated_per_unit = allocated_amount / detalle.cantidad if detalle.cantidad > 0 else Decimal("0")
                
                # Create allocation
                allocation = LandedCostAllocation(
                    organization_id=organization_id,
                    landed_cost_header_id=header.id,
                    landed_cost_line_id=line.id,
                    producto_id=detalle.producto_id,
                    producto_codigo=detalle.producto_codigo,
                    producto_nombre=detalle.producto_nombre,
                    compra_detalle_id=detalle.id,
                    quantity=detalle.cantidad,
                    unit_cost=detalle.precio_unitario,
                    total_value=detalle.precio_unitario * detalle.cantidad,
                    allocated_cost=allocated_amount,
                    allocated_cost_per_unit=allocated_per_unit,
                    new_unit_cost=detalle.precio_unitario + allocated_per_unit
                )
                db.add(allocation)
        
        header.status = "calculated"
        await db.commit()
        await db.refresh(header)
        
        return header
    
    @staticmethod
    async def apply_landed_cost(
        db: AsyncSession,
        organization_id: int,
        landed_cost_header_id: int,
        user_id: Optional[int] = None,
        user_name: Optional[str] = None
    ) -> LandedCostHeader:
        """Apply landed costs to product inventory costs."""
        from dario_app.modules.inventario.models import Producto
        
        # Get header
        stmt = select(LandedCostHeader).where(
            LandedCostHeader.id == landed_cost_header_id,
            LandedCostHeader.organization_id == organization_id
        )
        result = await db.execute(stmt)
        header = result.scalar_one_or_none()
        
        if not header:
            raise ValueError("Landed cost header not found")
        
        if header.status != "calculated":
            raise ValueError("Landed cost must be calculated before applying")
        
        # Get allocations
        stmt_allocs = select(LandedCostAllocation).where(
            LandedCostAllocation.landed_cost_header_id == header.id
        )
        result_allocs = await db.execute(stmt_allocs)
        allocations = result_allocs.scalars().all()
        
        # Update product costs
        for allocation in allocations:
            stmt_prod = select(Producto).where(
                Producto.id == allocation.producto_id,
                Producto.organization_id == organization_id
            )
            result_prod = await db.execute(stmt_prod)
            producto = result_prod.scalar_one_or_none()
            
            if producto:
                # Update unit cost with landed cost
                producto.precio_compra = allocation.new_unit_cost
        
        # Mark as applied
        header.status = "applied"
        header.applied_at = datetime.utcnow()
        header.applied_by_user_id = user_id
        header.applied_by_user_name = user_name
        
        await db.commit()
        await db.refresh(header)
        
        return header
