"""Production module routes."""

from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime, timedelta

from .models import (
    OrdenInternal,
    OrdenExterna,
    Alerta,
    EstadisticasProduccion,
)
from .seed_data import ORDENES_EJEMPLO, SECCIONES_PRODUCCION, TIPOS_BOMBAS

router = APIRouter(prefix="/api/produccion", tags=["produccion"])

# Build internal orders from seed data
ORDENES_INTERNAS = []
for orden_data in ORDENES_EJEMPLO:
    if "proveedor_externo" not in orden_data:  # Solo internas
        ORDENES_INTERNAS.append(
            OrdenInternal(
                id=orden_data["numero"].lower().replace("-", ""),
                numero=orden_data["numero"],
                producto=orden_data["producto"],
                seccion_produccion=orden_data["seccion"],
                etapa=orden_data["etapa"],
                avance=orden_data["avance"],
                estado=orden_data["estado"],
                fecha_inicio=datetime.now() - timedelta(days=orden_data["dias_desde_inicio"]),
                fecha_prevista=datetime.now() + timedelta(days=orden_data["dias_hasta_prevista"]),
                responsable="Supervisor " + orden_data["seccion"].split("-")[-1].capitalize(),
            )
        )

ORDENES_EXTERNAS = []
for orden_data in ORDENES_EJEMPLO:
    if "proveedor_externo" in orden_data:  # Solo externas
        ORDENES_EXTERNAS.append(
            OrdenExterna(
                id=orden_data["numero"].lower().replace("-", ""),
                numero=orden_data["numero"],
                proveedor=orden_data["proveedor_externo"],
                estado="en_proceso",
                fecha_envio=datetime.now() - timedelta(days=orden_data["dias_desde_inicio"]),
                eta=datetime.now() + timedelta(days=orden_data["dias_hasta_prevista"]),
                notas=f"Mecanizado de {orden_data['producto']}",
            )
        )

ALERTAS = [
    Alerta(
        id="alerta-1",
        orden="OP-2402",
        motivo="Mecanizado externo retrasado - proveedor",
        severidad="media",
        fecha=datetime.now() - timedelta(hours=3),
    ),
    Alerta(
        id="alerta-2",
        orden="OP-2405",
        motivo="Stock bajo de motores 1.8HP",
        severidad="alta",
        fecha=datetime.now() - timedelta(hours=1),
    ),
    Alerta(
        id="alerta-3",
        orden="OP-2404",
        motivo="Falta componente: Manguito 75mm en picking",
        severidad="alta",
        fecha=datetime.now() - timedelta(minutes=30),
    ),
]


@router.get("/estadisticas", response_model=EstadisticasProduccion)
async def get_estadisticas():
    """Get production statistics."""
    ordenes_activas = len([o for o in ORDENES_INTERNAS if o.estado != "completada"])
    ordenes_internas = len(ORDENES_INTERNAS)
    ordenes_externas = len(ORDENES_EXTERNAS)
    
    # Calculate compliance: average progress of active orders
    if ordenes_activas > 0:
        avg_progress = sum(o.avance for o in ORDENES_INTERNAS if o.estado != "completada") / ordenes_activas
        cumplimiento = avg_progress
    else:
        cumplimiento = 100.0
    
    return EstadisticasProduccion(
        ordenes_activas=ordenes_activas,
        ordenes_internas=ordenes_internas,
        ordenes_externas=ordenes_externas,
        cumplimiento_vs_plan=cumplimiento,
    )


@router.get("/ordenes-internas", response_model=List[OrdenInternal])
async def get_ordenes_internas():
    """Get internal production orders."""
    return ORDENES_INTERNAS


@router.get("/ordenes-externas", response_model=List[OrdenExterna])
async def get_ordenes_externas():
    """Get external production orders."""
    return ORDENES_EXTERNAS


@router.get("/alertas", response_model=List[Alerta])
async def get_alertas():
    """Get production alerts."""
    return ALERTAS


@router.post("/ordenes-internas")
async def create_orden_interna(orden: OrdenInternal):
    """Create new internal production order."""
    ORDENES_INTERNAS.append(orden)
    return {"id": orden.id, "numero": orden.numero, "status": "created"}


@router.put("/ordenes-internas/{orden_id}")
async def update_orden_interna(orden_id: str, orden: OrdenInternal):
    """Update internal production order."""
    for i, o in enumerate(ORDENES_INTERNAS):
        if o.id == orden_id:
            ORDENES_INTERNAS[i] = orden
            return {"id": orden_id, "status": "updated"}
    raise HTTPException(status_code=404, detail="Order not found")


@router.delete("/ordenes-internas/{orden_id}")
async def delete_orden_interna(orden_id: str):
    """Delete internal production order."""
    global ORDENES_INTERNAS
    ORDENES_INTERNAS = [o for o in ORDENES_INTERNAS if o.id != orden_id]
    return {"id": orden_id, "status": "deleted"}


@router.get("/secciones")
async def get_secciones():
    """Get production sections."""
    return SECCIONES_PRODUCCION


@router.get("/tipos-bombas")
async def get_tipos_bombas():
    """Get pump types."""
    return TIPOS_BOMBAS
