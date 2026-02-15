"""AI assistant routes using Ollama."""

import math
import os
from datetime import datetime, timedelta

import httpx
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.core.auth import get_org_id, get_tenant_db
from dario_app.modules.inventario.models import Producto, Proveedor
from dario_app.modules.ventas.models import Venta, VentaDetalle

router = APIRouter(prefix="/api/ai", tags=["ai-assistant"])

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
OLLAMA_MODEL_BASIC = os.getenv("OLLAMA_MODEL_BASIC", OLLAMA_MODEL)


class ChatRequest(BaseModel):
    message: str
    history: list[dict[str, str]] | None = None


class ChatResponse(BaseModel):
    reply: str


class FeedbackRequest(BaseModel):
    feedback: str  # "positive" or "negative"
    timestamp: str
    context: str | None = None


@router.post("/feedback")
async def submit_feedback(
    payload: FeedbackRequest,
    org_id: int = Depends(get_org_id)
):
    """
    Recibe feedback del usuario sobre sugerencias del asistente básico.
    Usado para Machine Learning: recompensa positiva cuando la sugerencia fue útil.
    """
    # TODO: Almacenar en BD para entrenamiento ML
    # Por ahora solo loguear
    print(f"[ML FEEDBACK] org={org_id} feedback={payload.feedback} time={payload.timestamp}")
    return {"status": "ok", "message": "Feedback recibido. ¡Gracias por ayudarme a mejorar!"}


def _build_prompt(message: str) -> str:
    """Compose a concise system prompt + user message tailored to the ERP."""
    system = (
        "Eres el ASISTENTE DE SOPORTE del ERP Dario. Tu función es resolver CUALQUIER DUDA sobre procesos del ERP. "
        "Explica paso a paso cómo realizar tareas, dónde encontrar opciones, qué permisos se necesitan. "
        "Responde de forma clara y pedagógica. Si no sabes algo, admítelo pero sugiere alternativas."
        "\n\nMÓDULOS DEL SISTEMA:\n"
        "• Inventario: Productos (código, nombre, categoría, precio compra/venta, stock, stock mínimo, es_alquiler). "
        "ALQUILERES: productos con flag 'es_alquiler=true' son gestionables para renta temporal.\n"
        "• Ventas/Compras: Facturas, pedidos, descuentos, IVA 21% (España).\n"
        "• POS: Punto de venta con métodos de pago (efectivo, tarjeta, transferencia), tickets, turnos.\n"
        "• Clientes/Proveedores: NIF/NIE/CIF, dirección fiscal, contactos.\n"
        "• Usuarios/Roles: Permisos granulares por módulo (admin, vendedor, almacén, finanzas, etc).\n"
        "• Producción: Órdenes de fabricación, BOM (lista de materiales), trazabilidad.\n"
        "• Reportes: Ventas por período, inventario valorado, margen, estadísticas.\n"
        "• Documentos: Plantillas (facturas, albaranes), histórico, generación PDF.\n"
        "• Automatizaciones: Reglas de reorden, alertas stock, notificaciones email.\n"
        "\nPROCESOS CLAVE:\n"
        "1. Crear producto: Inventario → Nuevo → Rellenar código, nombre, precio, marcar 'es_alquiler' si aplica.\n"
        "2. Registrar venta: Ventas → Nueva venta → Añadir productos/servicios → Confirmar.\n"
        "3. Alquilar equipo: Marcar producto con 'es_alquiler', crear venta temporal, devolver en plazo acordado.\n"
        "4. Generar reporte: Reportes → Elegir tipo → Filtrar fechas → Exportar PDF/Excel.\n"
        "5. Gestionar permisos: Usuarios → Roles → Asignar módulos permitidos."
    )
    return f"{system}\n\nPregunta del usuario: {message}\nRespuesta detallada:"


@router.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest) -> ChatResponse:
    """Answer ERP usage questions via Ollama."""
    prompt = _build_prompt(payload.message)
    url = f"{OLLAMA_HOST}/api/generate"
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(
                url, json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}
            )
            resp.raise_for_status()
            data = resp.json()
    except httpx.RequestError as exc:
        raise HTTPException(status_code=503, detail=f"Ollama no disponible: {exc}")
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=502, detail=f"Error en Ollama: {exc.response.text}")

    reply = data.get("response") or data.get("message") or "No se obtuvo respuesta"
    return ChatResponse(reply=reply.strip())


# ==== SUGERENCIAS BÁSICAS PARA PLAN LIGERO ====
class CompraSugerida(BaseModel):
    producto_id: int
    codigo: str
    nombre: str
    proveedor: str | None
    stock_actual: int
    stock_minimo: int
    consumo_diario: float | None
    cobertura_dias: float | None
    dias_entrega: int | None
    cantidad_sugerida: int
    motivo: str


class Recordatorio(BaseModel):
    tipo: str
    entidad: str
    mensaje: str


class SugerenciasResponse(BaseModel):
    compras_sugeridas: list[CompraSugerida]
    recordatorios: list[Recordatorio]
    resumen_llm: str


async def _consumo_diario_por_producto(
    db: AsyncSession, org_id: int, dias: int = 30
) -> dict[int, float]:
    """Calcula consumo promedio diario por producto usando ventas de los últimos N días."""
    fecha_limite = datetime.utcnow() - timedelta(days=dias)
    query = (
        select(VentaDetalle.producto_id, func.sum(VentaDetalle.cantidad).label("total"))
        .join(Venta, VentaDetalle.venta_id == Venta.id)
        .where(Venta.organization_id == org_id, Venta.fecha >= fecha_limite)
        .group_by(VentaDetalle.producto_id)
    )
    result = await db.execute(query)
    rows = result.all()
    return {r.producto_id: float(r.total) / dias for r in rows if r.total}


def _build_llm_prompt(compras: list[CompraSugerida], recordatorios: list[Recordatorio]) -> str:
    """Prompt breve para el modelo básico, en español, con tono accionable."""
    compras_txt = (
        "\n".join(
            [
                f"- {c.codigo} ({c.nombre}) | prov: {c.proveedor or 'sin proveedor'} | stock {c.stock_actual}/{c.stock_minimo} | cobertura {c.cobertura_dias:.1f}d | sug {c.cantidad_sugerida} uds ({c.motivo})"
                for c in compras[:8]
            ]
        )
        or "- Sin compras urgentes"
    )
    rec_txt = (
        "\n".join([f"- {r.tipo}: {r.mensaje}" for r in recordatorios[:8]]) or "- Sin pendientes"
    )
    system = (
        "Eres el ASISTENTE BÁSICO del ERP Dario. Monitorizas TODO el sistema del cliente en tiempo real. "
        "Ofreces recordatorios proactivos, información rápida y sugerencias con MACHINE LEARNING (cada acción con reseña positiva es tu recompensa). "
        "Das respuestas breves, accionables, con emojis. Considera productos de alquiler ('es_alquiler') como equipos rentables."
    )
    return (
        f"{system}\n\nCompras sugeridas:\n{compras_txt}\n\nRecordatorios:\n{rec_txt}\n\n"
        "Devuelve un resumen ULTRA corto en viñetas (3-5 bullets) con emojis y llamada a la acción. "
        "Termina SIEMPRE con: '¿Lo he hecho bien? 👍 Sí / 👎 No' para feedback de ML."
    )


@router.get("/sugerencias-basico", response_model=SugerenciasResponse)
async def sugerencias_basico(
    org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_tenant_db)
):
    """Sugiere compras y pendientes usando modelo ligero y reglas básicas."""
    # Datos base
    productos_res = await db.execute(
        select(Producto).where(Producto.organization_id == org_id, Producto.activo is True)
    )
    productos = productos_res.scalars().all()

    proveedores_res = await db.execute(select(Proveedor).where(Proveedor.organization_id == org_id))
    proveedores = proveedores_res.scalars().all()
    proveedores_map = {p.id: p for p in proveedores}

    consumo_map = await _consumo_diario_por_producto(db, org_id)

    compras_sugeridas: list[CompraSugerida] = []
    recordatorios: list[Recordatorio] = []
    colchon_dias = 3

    for p in productos:
        consumo = consumo_map.get(p.id)
        cobertura = (p.stock_actual / consumo) if consumo and consumo > 0 else None
        proveedor = proveedores_map.get(p.proveedor_id) if p.proveedor_id else None
        lead_time = proveedor.dias_entrega_promedio if proveedor else None
        lead_time = lead_time if lead_time is not None else 7

        # Necesidad de compra
        necesita = False
        motivo = []
        cantidad_sugerida = 0

        if p.stock_actual <= p.stock_minimo:
            necesita = True
            motivo.append("stock por debajo del mínimo")

        if cobertura is not None and cobertura < (lead_time + colchon_dias):
            necesita = True
            motivo.append(f"cobertura {cobertura:.1f}d < lead {lead_time + colchon_dias}d")

        if necesita:
            if consumo and consumo > 0:
                deficit_dias = (lead_time + colchon_dias) - (cobertura or 0)
                cantidad_sugerida = math.ceil(max(deficit_dias, 1) * consumo)
            else:
                cantidad_sugerida = max(
                    (p.stock_minimo - p.stock_actual), p.cantidad_minima_compra or 1, 1
                )
            if p.cantidad_minima_compra:
                cantidad_sugerida = max(cantidad_sugerida, p.cantidad_minima_compra)

            compras_sugeridas.append(
                CompraSugerida(
                    producto_id=p.id,
                    codigo=p.codigo,
                    nombre=p.nombre,
                    proveedor=proveedor.nombre if proveedor else None,
                    stock_actual=p.stock_actual,
                    stock_minimo=p.stock_minimo,
                    consumo_diario=consumo,
                    cobertura_dias=cobertura,
                    dias_entrega=lead_time,
                    cantidad_sugerida=cantidad_sugerida,
                    motivo="; ".join(motivo) or "reposición",
                )
            )

        # Recordatorios de ficha incompleta
        if not p.sku:
            recordatorios.append(
                Recordatorio(tipo="producto", entidad=p.nombre, mensaje="Falta SKU")
            )
        if not p.categoria:
            recordatorios.append(
                Recordatorio(tipo="producto", entidad=p.nombre, mensaje="Falta categoría")
            )
        if p.margen_porcentaje is None:
            recordatorios.append(
                Recordatorio(tipo="producto", entidad=p.nombre, mensaje="Falta margen %")
            )
        if not p.proveedor_id:
            recordatorios.append(
                Recordatorio(tipo="producto", entidad=p.nombre, mensaje="Asigna proveedor")
            )
        if not p.descripcion:
            recordatorios.append(
                Recordatorio(tipo="producto", entidad=p.nombre, mensaje="Añade descripción")
            )
        try:
            precio_calc = float(p.precio_compra) * (1 + (float(p.margen_porcentaje or 0) / 100))
            if float(p.precio_venta or 0) < round(precio_calc, 2) - 0.01:
                recordatorios.append(
                    Recordatorio(
                        tipo="producto",
                        entidad=p.nombre,
                        mensaje="Precio venta por debajo del margen",
                    )
                )
        except Exception:
            pass

    for prov in proveedores:
        if not prov.email:
            recordatorios.append(
                Recordatorio(tipo="proveedor", entidad=prov.nombre, mensaje="Falta email")
            )
        if not prov.telefono:
            recordatorios.append(
                Recordatorio(tipo="proveedor", entidad=prov.nombre, mensaje="Falta teléfono")
            )
        if not prov.contacto_nombre:
            recordatorios.append(
                Recordatorio(tipo="proveedor", entidad=prov.nombre, mensaje="Falta contacto")
            )
        if prov.dias_entrega_promedio is None:
            recordatorios.append(
                Recordatorio(
                    tipo="proveedor", entidad=prov.nombre, mensaje="Añadir días de entrega"
                )
            )

    # Llamar al modelo ligero para resumen
    resumen_llm = ""
    prompt = _build_llm_prompt(compras_sugeridas, recordatorios)
    url = f"{OLLAMA_HOST}/api/generate"
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                url, json={"model": OLLAMA_MODEL_BASIC, "prompt": prompt, "stream": False}
            )
            resp.raise_for_status()
            data = resp.json()
            resumen_llm = (data.get("response") or "").strip()
    except Exception:
        resumen_llm = "No se pudo generar el resumen con el modelo básico."

    return SugerenciasResponse(
        compras_sugeridas=compras_sugeridas, recordatorios=recordatorios, resumen_llm=resumen_llm
    )
