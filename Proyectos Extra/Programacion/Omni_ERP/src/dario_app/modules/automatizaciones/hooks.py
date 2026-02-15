"""Hooks de automatizaciones para eventos del sistema."""

from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.modules.automatizaciones.engine import AutomatizacionesEngine
from dario_app.modules.automatizaciones.models import TipoTrigger


# Instancia global del engine (se inicializa por sesión en cada uso)
async def obtener_engine(db: AsyncSession) -> AutomatizacionesEngine:
    """Factory para obtener instancia del engine."""
    return AutomatizacionesEngine(db)


# ═══════════════════════════════════════════════════════════════════════════════
# HOOKS PARA VENTAS
# ═══════════════════════════════════════════════════════════════════════════════

async def trigger_venta_creada(
    db: AsyncSession,
    org_id: int,
    venta_data: Dict[str, Any]
):
    """Se ejecuta cuando se crea una venta."""
    engine = await obtener_engine(db)
    await engine.ejecutar_trigger(
        org_id,
        TipoTrigger.VENTA_CREADA,
        venta_data
    )


async def trigger_venta_completada(
    db: AsyncSession,
    org_id: int,
    venta_id: int,
    venta_data: Dict[str, Any]
):
    """Se ejecuta cuando se completa una venta."""
    engine = await obtener_engine(db)
    await engine.ejecutar_trigger(
        org_id,
        TipoTrigger.VENTA_COMPLETADA,
        venta_data
    )


# ═══════════════════════════════════════════════════════════════════════════════
# HOOKS PARA COMPRAS
# ═══════════════════════════════════════════════════════════════════════════════

async def trigger_compra_creada(
    db: AsyncSession,
    org_id: int,
    compra_data: Dict[str, Any]
):
    """Se ejecuta cuando se crea una compra."""
    engine = await obtener_engine(db)
    await engine.ejecutar_trigger(
        org_id,
        TipoTrigger.COMPRA_CREADA,
        compra_data
    )


async def trigger_compra_recibida(
    db: AsyncSession,
    org_id: int,
    compra_id: int,
    compra_data: Dict[str, Any]
):
    """Se ejecuta cuando se recibe una compra."""
    engine = await obtener_engine(db)
    await engine.ejecutar_trigger(
        org_id,
        TipoTrigger.COMPRA_RECIBIDA,
        compra_data
    )


# ═══════════════════════════════════════════════════════════════════════════════
# HOOKS PARA INVENTARIO
# ═══════════════════════════════════════════════════════════════════════════════

async def trigger_stock_bajo(
    db: AsyncSession,
    org_id: int,
    producto_data: Dict[str, Any]
):
    """Se ejecuta cuando el stock baja del mínimo."""
    engine = await obtener_engine(db)
    await engine.ejecutar_trigger(
        org_id,
        TipoTrigger.STOCK_BAJO,
        producto_data
    )


# ═══════════════════════════════════════════════════════════════════════════════
# HOOKS PARA CLIENTES
# ═══════════════════════════════════════════════════════════════════════════════

async def trigger_cliente_creado(
    db: AsyncSession,
    org_id: int,
    cliente_data: Dict[str, Any]
):
    """Se ejecuta cuando se crea un cliente."""
    engine = await obtener_engine(db)
    await engine.ejecutar_trigger(
        org_id,
        TipoTrigger.CLIENTE_CREADO,
        cliente_data
    )


# ═══════════════════════════════════════════════════════════════════════════════
# HOOKS PARA PAGOS
# ═══════════════════════════════════════════════════════════════════════════════

async def trigger_pago_recibido(
    db: AsyncSession,
    org_id: int,
    pago_data: Dict[str, Any]
):
    """Se ejecuta cuando se recibe un pago."""
    engine = await obtener_engine(db)
    await engine.ejecutar_trigger(
        org_id,
        TipoTrigger.PAGO_RECIBIDO,
        pago_data
    )


async def trigger_pago_atrasado(
    db: AsyncSession,
    org_id: int,
    venta_data: Dict[str, Any]
):
    """Se ejecuta cuando un pago se atrasa."""
    engine = await obtener_engine(db)
    await engine.ejecutar_trigger(
        org_id,
        TipoTrigger.PAGO_ATRASADO,
        venta_data
    )


# ═══════════════════════════════════════════════════════════════════════════════
# HOOKS PARA CITAS
# ═══════════════════════════════════════════════════════════════════════════════

async def trigger_cita_creada(
    db: AsyncSession,
    org_id: int,
    cita_data: Dict[str, Any]
):
    """Se ejecuta cuando se crea una cita."""
    engine = await obtener_engine(db)
    await engine.ejecutar_trigger(
        org_id,
        TipoTrigger.CITA_CREADA,
        cita_data
    )


async def trigger_cita_confirmada(
    db: AsyncSession,
    org_id: int,
    cita_data: Dict[str, Any]
):
    """Se ejecuta cuando se confirma una cita."""
    engine = await obtener_engine(db)
    await engine.ejecutar_trigger(
        org_id,
        TipoTrigger.CITA_CONFIRMADA,
        cita_data
    )
