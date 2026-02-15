"""API endpoints that return Bombas Omni data for demo purposes."""

from fastapi import APIRouter
from typing import List, Dict, Any

from dario_app.modules.seed_bombas_omni import (
    PRODUCTOS_INVENTARIO,
    CLIENTES,
    PROVEEDORES,
    VENTAS_EJEMPLO,
    COMPRAS_EJEMPLO,
)

router = APIRouter(prefix="/api/bombas-omni", tags=["bombas-omni"])


@router.get("/productos")
async def get_productos() -> List[Dict[str, Any]]:
    """Get all products in inventory."""
    return PRODUCTOS_INVENTARIO


@router.get("/productos/bajo-stock")
async def get_productos_bajo_stock() -> List[Dict[str, Any]]:
    """Get products with stock below minimum."""
    return [p for p in PRODUCTOS_INVENTARIO if p["stock"] < p["stock_minimo"]]


@router.get("/clientes")
async def get_clientes() -> List[Dict[str, Any]]:
    """Get all clients."""
    return CLIENTES


@router.get("/proveedores")
async def get_proveedores() -> List[Dict[str, Any]]:
    """Get all suppliers."""
    return PROVEEDORES


@router.get("/ventas")
async def get_ventas() -> List[Dict[str, Any]]:
    """Get recent sales."""
    return [
        {
            **venta,
            "fecha": venta["fecha"].isoformat(),
        }
        for venta in VENTAS_EJEMPLO
    ]


@router.get("/compras")
async def get_compras() -> List[Dict[str, Any]]:
    """Get recent purchases."""
    return [
        {
            **compra,
            "fecha": compra["fecha"].isoformat(),
            "fecha_pago_prevista": compra["fecha_pago_prevista"].isoformat(),
        }
        for compra in COMPRAS_EJEMPLO
    ]


@router.get("/stats")
async def get_stats() -> Dict[str, Any]:
    """Get general statistics."""
    total_productos = len(PRODUCTOS_INVENTARIO)
    productos_bajo_stock = len([p for p in PRODUCTOS_INVENTARIO if p["stock"] < p["stock_minimo"]])
    valor_inventario = sum(p["stock"] * p["precio_compra"] for p in PRODUCTOS_INVENTARIO)
    
    total_ventas = sum(v["total"] for v in VENTAS_EJEMPLO)
    total_compras = sum(c["total"] for c in COMPRAS_EJEMPLO)
    
    return {
        "inventario": {
            "total_productos": total_productos,
            "productos_bajo_stock": productos_bajo_stock,
            "valor_total": round(valor_inventario, 2),
        },
        "ventas": {
            "total": round(total_ventas, 2),
            "cantidad_ordenes": len(VENTAS_EJEMPLO),
        },
        "compras": {
            "total": round(total_compras, 2),
            "cantidad_ordenes": len(COMPRAS_EJEMPLO),
        },
        "clientes": len(CLIENTES),
        "proveedores": len(PROVEEDORES),
    }
