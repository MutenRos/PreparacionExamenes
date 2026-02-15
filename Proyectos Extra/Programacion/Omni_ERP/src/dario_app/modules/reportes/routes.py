"""Reports and analytics API routes."""

from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.core.auth import get_org_id, get_tenant_db
from dario_app.modules.clientes.models import Cliente
from dario_app.modules.compras.models import Compra
from dario_app.modules.inventario.models import Producto
from dario_app.modules.pos.models import VentaPOS
from dario_app.modules.usuarios.models import Usuario
from dario_app.modules.ventas.models import Venta, VentaDetalle

router = APIRouter(prefix="/api/reportes", tags=["reportes"])


class VentasPorDiaResponse(BaseModel):
    fecha: str
    total: float
    cantidad: int


class ProductoTopResponse(BaseModel):
    producto_id: int
    nombre: str
    cantidad_vendida: int
    total_ventas: float


class InventarioBajoResponse(BaseModel):
    id: int
    codigo: str
    nombre: str
    stock_actual: int
    stock_minimo: int

    class Config:
        from_attributes = True


class ResumenResponse(BaseModel):
    ventas_hoy: float
    ventas_mes: float
    compras_mes: float
    productos_bajo_stock: int
    total_clientes: int


class DashboardSummaryResponse(BaseModel):
    productos_total: int
    ventas_mes: float
    usuarios_activos: int
    ordenes_pendientes: int


@router.get("/ventas-por-dia", response_model=List[VentasPorDiaResponse])
async def ventas_por_dia(
    dias: int = 7, org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_tenant_db)
):
    """Get sales grouped by day for the last N days."""
    fecha_inicio = datetime.utcnow() - timedelta(days=dias)

    # Query Venta (pedidos)
    result_venta = await db.execute(
        select(
            func.date(Venta.creado_en).label("fecha"),
            func.sum(Venta.total).label("total"),
            func.count(Venta.id).label("cantidad"),
        )
        .where(
            Venta.organization_id == org_id,
            Venta.creado_en >= fecha_inicio,
            Venta.estado != "cancelada",
        )
        .group_by(func.date(Venta.creado_en))
    )

    # Query POS sales
    result_pos = await db.execute(
        select(
            func.date(VentaPOS.creado_en).label("fecha"),
            func.sum(VentaPOS.total).label("total"),
            func.count(VentaPOS.id).label("cantidad"),
        )
        .where(VentaPOS.organization_id == org_id, VentaPOS.creado_en >= fecha_inicio)
        .group_by(func.date(VentaPOS.creado_en))
    )

    # Combinar resultados por fecha
    ventas_dict = {}

    for row in result_venta:
        fecha_key = str(row.fecha)
        if fecha_key not in ventas_dict:
            ventas_dict[fecha_key] = {"total": 0, "cantidad": 0}
        ventas_dict[fecha_key]["total"] += float(row.total or 0)
        ventas_dict[fecha_key]["cantidad"] += row.cantidad or 0

    for row in result_pos:
        fecha_key = str(row.fecha)
        if fecha_key not in ventas_dict:
            ventas_dict[fecha_key] = {"total": 0, "cantidad": 0}
        ventas_dict[fecha_key]["total"] += float(row.total or 0)
        ventas_dict[fecha_key]["cantidad"] += row.cantidad or 0

    # Convertir a lista ordenada
    ventas = [
        {"fecha": fecha, "total": datos["total"], "cantidad": datos["cantidad"]}
        for fecha, datos in sorted(ventas_dict.items())
    ]

    return ventas


@router.get("/productos-top", response_model=List[ProductoTopResponse])
async def productos_top(
    limite: int = 10, org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_tenant_db)
):
    """Get top selling products."""
    # Obtener productos más vendidos desde VentaDetalle
    result = await db.execute(
        select(
            Producto.id,
            Producto.nombre,
            func.sum(VentaDetalle.cantidad).label("cantidad_vendida"),
            func.sum(VentaDetalle.subtotal).label("total_ventas"),
        )
        .join(VentaDetalle, VentaDetalle.producto_id == Producto.id)
        .join(Venta, Venta.id == VentaDetalle.venta_id)
        .where(Producto.organization_id == org_id, Venta.estado != "cancelada")
        .group_by(Producto.id, Producto.nombre)
        .order_by(func.sum(VentaDetalle.cantidad).desc())
        .limit(limite)
    )

    productos = []
    for row in result:
        productos.append(
            {
                "producto_id": row.id,
                "nombre": row.nombre,
                "cantidad_vendida": row.cantidad_vendida or 0,
                "total_ventas": float(row.total_ventas or 0),
            }
        )

    # Si no hay datos de Venta, retornar productos por defecto
    if not productos:
        result = await db.execute(
            select(Producto).where(Producto.organization_id == org_id).limit(limite)
        )

        for producto in result.scalars():
            productos.append(
                {
                    "producto_id": producto.id,
                    "nombre": producto.nombre,
                    "cantidad_vendida": 0,
                    "total_ventas": 0.0,
                }
            )

    return productos


@router.get("/inventario-bajo", response_model=List[InventarioBajoResponse])
async def inventario_bajo(
    org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_tenant_db)
):
    """Get products with low stock levels."""
    result = await db.execute(
        select(Producto).where(
            Producto.organization_id == org_id, Producto.stock_actual <= Producto.stock_minimo
        )
    )
    return result.scalars().all()


@router.get("/resumen", response_model=ResumenResponse)
async def resumen(org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_tenant_db)):
    """Get dashboard summary statistics."""
    hoy = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    inicio_mes = hoy.replace(day=1)

    # Ventas hoy (suma de Venta y VentaPOS)
    result = await db.execute(
        select(func.sum(Venta.total)).where(
            Venta.organization_id == org_id, Venta.creado_en >= hoy, Venta.estado != "cancelada"
        )
    )
    ventas_hoy_venta = result.scalar() or 0

    result = await db.execute(
        select(func.sum(VentaPOS.total)).where(
            VentaPOS.organization_id == org_id, VentaPOS.creado_en >= hoy
        )
    )
    ventas_hoy_pos = result.scalar() or 0
    ventas_hoy = float(ventas_hoy_venta) + float(ventas_hoy_pos)

    # Ventas mes
    result = await db.execute(
        select(func.sum(Venta.total)).where(
            Venta.organization_id == org_id,
            Venta.creado_en >= inicio_mes,
            Venta.estado != "cancelada",
        )
    )
    ventas_mes_venta = result.scalar() or 0

    result = await db.execute(
        select(func.sum(VentaPOS.total)).where(
            VentaPOS.organization_id == org_id, VentaPOS.creado_en >= inicio_mes
        )
    )
    ventas_mes_pos = result.scalar() or 0
    ventas_mes = float(ventas_mes_venta) + float(ventas_mes_pos)

    # Compras mes
    result = await db.execute(
        select(func.sum(Compra.total)).where(
            Compra.organization_id == org_id,
            Compra.creado_en >= inicio_mes,
            Compra.estado != "cancelada",
        )
    )
    compras_mes = result.scalar() or 0

    # Productos bajo stock
    result = await db.execute(
        select(func.count(Producto.id)).where(
            Producto.organization_id == org_id, Producto.stock_actual <= Producto.stock_minimo
        )
    )
    productos_bajo_stock = result.scalar() or 0

    # Total de clientes
    result = await db.execute(
        select(func.count(Cliente.id)).where(Cliente.organization_id == org_id)
    )
    total_clientes = result.scalar() or 0

    return {
        "ventas_hoy": float(ventas_hoy),
        "ventas_mes": float(ventas_mes),
        "compras_mes": float(compras_mes),
        "productos_bajo_stock": productos_bajo_stock,
        "total_clientes": total_clientes,
    }


@router.get("/resumen-dashboard", response_model=DashboardSummaryResponse)
async def resumen_dashboard(
    org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_tenant_db)
):
    """Resumen compacto para el dashboard principal."""
    inicio_mes = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Productos totales
    prod_res = await db.execute(
        select(func.count(Producto.id)).where(Producto.organization_id == org_id)
    )
    productos_total = prod_res.scalar() or 0

    # Ventas del mes (Venta + VentaPOS)
    venta_res = await db.execute(
        select(func.sum(Venta.total)).where(
            Venta.organization_id == org_id,
            Venta.creado_en >= inicio_mes,
            Venta.estado != "cancelada",
        )
    )
    ventas_mes_venta = venta_res.scalar() or 0

    pos_res = await db.execute(
        select(func.sum(VentaPOS.total)).where(
            VentaPOS.organization_id == org_id, VentaPOS.creado_en >= inicio_mes
        )
    )
    ventas_mes_pos = pos_res.scalar() or 0
    ventas_mes = float(ventas_mes_venta) + float(ventas_mes_pos)

    # Usuarios activos
    user_res = await db.execute(
        select(func.count(Usuario.id)).where(
            Usuario.organization_id == org_id, Usuario.activo is True
        )
    )
    usuarios_activos = user_res.scalar() or 0

    # Órdenes pendientes (compras no completadas ni canceladas)
    ordenes_res = await db.execute(
        select(func.count(Compra.id)).where(
            Compra.organization_id == org_id, Compra.estado.notin_(["completada", "cancelada"])
        )
    )
    ordenes_pendientes = ordenes_res.scalar() or 0

    return {
        "productos_total": productos_total,
        "ventas_mes": float(ventas_mes),
        "usuarios_activos": usuarios_activos,
        "ordenes_pendientes": ordenes_pendientes,
    }
