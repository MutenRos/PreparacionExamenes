"""Voice Assistant Routes - API endpoints for voice interaction."""

import os
import re
import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from uuid import uuid4
from datetime import datetime, timedelta
from typing import Optional

from dario_app.core.dependencies import get_db
from dario_app.core.auth import require_auth, get_org_id, get_tenant_db
from dario_app.modules.inventario.models import Producto, Proveedor
from dario_app.modules.ventas.models import Venta, VentaDetalle
from .models import VoiceInput, VoiceResponse, ConversationContext
from .nlu import IntentRecognizer, CommandProcessor, ResponseGenerator
from .erp_actions import ERPActionExecutor

router = APIRouter(prefix="/api/voice-assistant", tags=["voice_assistant"])

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

# In-memory conversation store (in production, use database)
CONVERSATIONS = {}


async def _get_basic_assistant_context(db: AsyncSession, org_id: int) -> dict:
    """Obtiene contexto del asistente básico: sugerencias de compra y recordatorios."""
    try:
        # Productos con stock bajo
        productos_res = await db.execute(
            select(Producto).where(
                Producto.organization_id == org_id,
                Producto.activo == True,
                Producto.stock_actual <= Producto.stock_minimo
            ).limit(5)
        )
        productos_bajo_stock = productos_res.scalars().all()
        
        # Productos de alquiler (si la columna existe)
        alquileres = []
        try:
            alquileres_res = await db.execute(
                select(Producto).where(
                    Producto.organization_id == org_id,
                    Producto.es_alquiler == True,
                    Producto.activo == True
                ).limit(3)
            )
            alquileres = alquileres_res.scalars().all()
        except Exception:
            pass  # Columna no existe
        
        # Ventas recientes (últimos 7 días)
        fecha_limite = datetime.utcnow() - timedelta(days=7)
        ventas_res = await db.execute(
            select(func.count(Venta.id), func.sum(Venta.total))
            .where(Venta.organization_id == org_id, Venta.fecha >= fecha_limite)
        )
        venta_stats = ventas_res.first()
        
        return {
            "productos_bajo_stock": [
                f"{p.codigo} ({p.nombre}): {p.stock_actual}/{p.stock_minimo}"
                for p in productos_bajo_stock
            ],
            "alquileres_disponibles": [
                f"{a.nombre} (alquiler)" for a in alquileres
            ],
            "ventas_semana": {
                "cantidad": venta_stats[0] or 0,
                "total": float(venta_stats[1] or 0)
            }
        }
    except Exception as e:
        print(f"Error obteniendo contexto básico: {e}")
        return {
            "productos_bajo_stock": [],
            "alquileres_disponibles": [],
            "ventas_semana": {"cantidad": 0, "total": 0}
        }


def _build_voice_system_prompt(basic_context: dict, history: str) -> str:
    """Construye prompt para Ollama con contexto del ERP y asistente básico."""
    bajo_stock = "\n".join(basic_context.get("productos_bajo_stock", [])) or "- Ninguno"
    alquileres = "\n".join(basic_context.get("alquileres_disponibles", [])) or "- Ninguno"
    ventas = basic_context.get("ventas_semana", {})
    
    return f"""Eres el ASISTENTE DE VOZ del ERP Dario. Tu misión: permitir al usuario usar el sistema COMPLETAMENTE sin teclado.

PERSONALIDAD:
- Conversacional, amigable, conciso
- Respondes en español con tono natural
- Das información útil e inmediata basada en datos REALES del sistema
- Ejecutas comandos de voz y confirmas resultados

CONTEXTO ACTUAL DEL ERP (del asistente básico):
📦 Productos con stock bajo:
{bajo_stock}

🎪 Equipos de alquiler disponibles:
{alquileres}

📊 Ventas última semana: {ventas.get('cantidad', 0)} ventas, €{ventas.get('total', 0):.2f}

CAPACIDADES AVANZADAS (con ejecución real):
✅ BÚSQUEDA: "busca producto X", "encuentra cliente Y", "alquileres disponibles"
   → Ejecuto búsqueda real en BD y muestro resultados
✅ CONSULTAS: "¿cuánto stock de X?", "¿precio de Y?", "¿qué productos están bajos?"
   → Leo datos reales y respondo con números exactos
✅ ESTADÍSTICAS: "¿cuántas ventas hoy?", "ventas de la semana", "total vendido"
   → Calculo estadísticas reales del sistema
✅ NAVEGACIÓN: "ve a inventario", "abre ventas", "muestra reportes"
   → Redirijo al módulo solicitado
✅ FILTRADO: "muestra solo alquileres", "productos con stock bajo"
   → Aplico filtros en la consulta

IMPORTANTE: Cuando recibes datos entre [CORCHETES], son resultados REALES del sistema. Úsalos en tu respuesta.

REGLAS:
- Si hay [RESULTADOS], resúmelos brevemente y menciona lo más relevante
- Si preguntan por datos específicos, usa los números exactos proporcionados
- Si no hay datos entre corchetes, respondo basado en contexto general
- Máximo 2-3 frases, directo al grano
- Uso emojis para claridad visual

HISTORIAL RECIENTE:
{history}"""


async def _call_ollama(prompt: str) -> str:
    """Llama a Ollama para generar respuesta conversacional."""
    url = f"{OLLAMA_HOST}/api/generate"
    try:
        # Increase timeout because local Ollama responses can take longer than 30s
        async with httpx.AsyncClient(timeout=90, http2=False) as client:
            resp = await client.post(
                url,
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "num_predict": 150
                    }
                }
            )
            resp.raise_for_status()
            data = resp.json()
            response = data.get("response", "").strip()
            if not response:
                return "No entendí bien. ¿Puedes repetir?"
            print(f"[VOICE] Ollama respondió: {response[:100]}...")
            return response
    except httpx.HTTPStatusError as e:
        print(f"Error HTTP de Ollama: {e.response.status_code} - {e.response.text}")
        return "Disculpa, tengo problemas para procesar tu solicitud. Inténtalo de nuevo."
    except Exception as e:
        import traceback
        print(f"Error llamando a Ollama: {type(e).__name__}: {str(e)}")
        print(traceback.format_exc())
        return "Disculpa, tengo problemas para procesar tu solicitud. Inténtalo de nuevo."


@router.post("/chat", response_model=VoiceResponse)
async def voice_chat(
    voice_input: VoiceInput,
    user_context: dict = Depends(require_auth),
    db: AsyncSession = Depends(get_tenant_db),
):
    """
    Process voice input and generate response using Ollama.
    
    Conversacional con contexto. Integra sugerencias del asistente básico.
    """
    try:
        # Ensure UTF-8 encoding for input text
        text = voice_input.text.encode('utf-8').decode('utf-8')
        
        # Extract user info from context
        user_id = str(user_context.get("user_id", "anonymous"))
        org_id = int(user_context.get("org_id", 1))
        
        # Get or create conversation
        conv_id = voice_input.conversation_id or str(uuid4())
        if conv_id not in CONVERSATIONS:
            CONVERSATIONS[conv_id] = ConversationContext(
                conversation_id=conv_id,
                user_id=user_id,
                org_id=org_id,
            )
        
        conversation = CONVERSATIONS[conv_id]
        
        # Detectar intención rápida para acciones (navegación, crear, etc.)
        intent, confidence, entities = IntentRecognizer.recognize(text)
        command = CommandProcessor.process(intent, entities)
        
        # EJECUTAR ACCIONES REALES EN EL ERP
        erp_data = None
        action = None
        action_params = None
        action_executed = False
        original_text = text
        
        try:
            # BÚSQUEDA DE PRODUCTOS
            if intent == "search" and entities and "query" in entities:
                query = entities["query"]
                filters = {}
                
                # Detectar filtros en el texto
                if "alquiler" in text.lower() or "renta" in text.lower():
                    filters["es_alquiler"] = True
                if "stock bajo" in text.lower() or "poco stock" in text.lower():
                    filters["stock_bajo"] = True
                
                print(f"[VOICE] Ejecutando búsqueda de productos: query='{query}', filters={filters}")
                productos = await ERPActionExecutor.search_products(db, org_id, query, filters)
                erp_data = {"productos": productos}
                print(f"[VOICE] Productos encontrados: {len(productos)}")
                
                # Añadir resultados al contexto para Ollama
                if productos:
                    result_text = "\n".join([
                        f"• {p['codigo']} - {p['nombre']} (Stock: {p['stock_actual']}, Precio: €{p['precio_venta']:.2f})"
                        for p in productos[:5]
                    ])
                    text += f"\n\n[RESULTADOS DE BÚSQUEDA]:\n{result_text}"
                    print(f"[VOICE] Contexto actualizado con {len(productos)} productos")
                else:
                    text += "\n\n[No se encontraron productos]"
                    print("[VOICE] No se encontraron productos")
                action_executed = True
            
            # DETALLES DE PRODUCTO ESPECÍFICO
            elif "cuánto" in text.lower() or "cuanto" in text.lower() or "stock de" in text.lower():
                # Extraer nombre del producto
                match = re.search(r'(?:stock de|precio de|info de|información de)\s+(.+?)(?:\?|$)', text.lower())
                if match:
                    identifier = match.group(1).strip()
                    producto = await ERPActionExecutor.get_product_details(db, org_id, identifier)
                    if producto:
                        erp_data = {"producto": producto}
                        text += f"\n\n[PRODUCTO]: {producto['nombre']}, Stock: {producto['stock_actual']}, Precio: €{producto['precio_venta']:.2f}"
                        action_executed = True
            
            # PRODUCTOS CON STOCK BAJO
            elif "stock bajo" in text.lower() or "poco stock" in text.lower() or "reponer" in text.lower():
                productos = await ERPActionExecutor.get_low_stock_products(db, org_id)
                erp_data = {"productos_bajo_stock": productos}
                if productos:
                    result_text = "\n".join([
                        f"• {p['codigo']} - {p['nombre']}: {p['stock_actual']}/{p['stock_minimo']} (falta {p['deficit']})"
                        for p in productos[:5]
                    ])
                    text += f"\n\n[PRODUCTOS CON STOCK BAJO]:\n{result_text}"
                else:
                    text += "\n\n[Todos los productos tienen stock suficiente]"
                action_executed = True
            
            # PRODUCTOS DE ALQUILER
            elif "alquileres" in text.lower() or "equipos de alquiler" in text.lower() or "rentas" in text.lower():
                alquileres = await ERPActionExecutor.get_rental_products(db, org_id)
                erp_data = {"alquileres": alquileres}
                if alquileres:
                    result_text = "\n".join([
                        f"• {a['nombre']}: {'✅ Disponible' if a['disponible'] else '❌ No disponible'} (€{a['precio_venta']:.2f}/día)"
                        for a in alquileres[:5]
                    ])
                    text += f"\n\n[EQUIPOS DE ALQUILER]:\n{result_text}"
                action_executed = True
            
            # ESTADÍSTICAS DE VENTAS
            elif "ventas" in text.lower() and any(word in text.lower() for word in ["hoy", "semana", "mes", "cuántas", "cuantas"]):
                period = "today" if "hoy" in text.lower() else "week" if "semana" in text.lower() else "month"
                stats = await ERPActionExecutor.get_sales_stats(db, org_id, period)
                erp_data = {"ventas_stats": stats}
                text += f"\n\n[ESTADÍSTICAS DE VENTAS]: {stats['cantidad_ventas']} ventas, Total: €{stats['total_vendido']:.2f}, Promedio: €{stats['ticket_promedio']:.2f}"
                action_executed = True
            
            # BUSCAR CLIENTES
            elif intent == "search" and ("cliente" in text.lower() or "clientes" in text.lower()):
                if entities and "query" in entities:
                    query = entities["query"]
                    clientes = await ERPActionExecutor.search_clients(db, org_id, query)
                    erp_data = {"clientes": clientes}
                    if clientes:
                        result_text = "\n".join([
                            f"• {c['nombre']} - {c['email']} - {c['telefono']}"
                            for c in clientes[:5]
                        ])
                        text += f"\n\n[CLIENTES ENCONTRADOS]:\n{result_text}"
                    action_executed = True
            
        except Exception as e:
            print(f"Error ejecutando acción ERP: {e}")
            text += f"\n\n[Error al ejecutar operación: {str(e)}]"
        
        # Obtener contexto del asistente básico (sugerencias, recordatorios)
        basic_context = await _get_basic_assistant_context(db, org_id)
        
        # Construir historial de conversación para Ollama
        history = "\n".join([
            f"{'Usuario' if m['is_user'] else 'Asistente'}: {m['text']}"
            for m in conversation.messages[-6:]  # últimas 6 mensajes
        ])
        
        # Prompt para Ollama con contexto ERP
        system_prompt = _build_voice_system_prompt(basic_context, history)
        full_prompt = f"{system_prompt}\n\nUsuario: {text}\nAsistente:"
        
        print(f"[VOICE] Llamando a Ollama con prompt de {len(full_prompt)} caracteres")
        print(f"[VOICE] Texto del usuario (con contexto): {text[:200]}...")
        
        # Llamar a Ollama
        response_text = await _call_ollama(full_prompt)
        print(f"[VOICE] Respuesta de Ollama: {response_text[:150]}...")
        
        # Si detectamos acción específica de navegación, ejecutarla
        if confidence > 0.7 and intent in ["navigate", "create"]:
            action = command.get("action")
            action_params = command.get("params")
            # Añadir confirmación de acción a la respuesta
            if action == "navigate" and entities:
                dest = entities.get("destination", "")
                response_text += f"\n\n✅ Te llevo a {dest}."
            elif action == "open_form" and entities:
                entity_type = entities.get("entity_type", "registro")
                response_text += f"\n\n✅ Abriendo formulario de {entity_type}."
        
        # Create response
        response = VoiceResponse(
            message=response_text,
            intent=intent,
            action=action,
            action_params=action_params,
            conversation_id=conv_id,
            timestamp=datetime.utcnow(),
            data=erp_data,
            success=True
        )
        
        # Store in conversation history
        conversation.last_intent = intent
        conversation.last_action = action
        conversation.messages.append({
            "id": str(uuid4()),
            "text": original_text,
            "is_user": True,
            "timestamp": datetime.utcnow(),
            "confidence": voice_input.audio_confidence,
            "intent": intent,
            "action": action,
        })
        conversation.messages.append({
            "id": str(uuid4()),
            "text": response_text,
            "is_user": False,
            "timestamp": datetime.utcnow(),
            "intent": intent,
        })
        
        return response
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Voice processing error: {str(e)}"
        )


@router.get("/conversation/{conversation_id}")
async def get_conversation(
    conversation_id: str,
    user_context: dict = Depends(require_auth),
):
    """Retrieve conversation history."""
    if conversation_id not in CONVERSATIONS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    conversation = CONVERSATIONS[conversation_id]
    
    # Verify user owns this conversation
    if conversation.user_id != str(user_context.get("user_id")):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return {
        "conversation_id": conversation.conversation_id,
        "messages": conversation.messages,
        "created_at": conversation.created_at,
        "last_intent": conversation.last_intent,
    }


@router.delete("/conversation/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    user_context: dict = Depends(require_auth),
):
    """Clear conversation history."""
    if conversation_id not in CONVERSATIONS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    conversation = CONVERSATIONS[conversation_id]
    
    # Verify user owns this conversation
    if conversation.user_id != str(user_context.get("user_id")):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    del CONVERSATIONS[conversation_id]
    
    return {"message": "Conversation deleted"}


@router.get("/intents")
async def list_intents(user_context: dict = Depends(require_auth)):
    """List available intents and their descriptions."""
    intents = {
        "search": "Buscar productos, clientes o documentos",
        "navigate": "Navegar a diferentes secciones de la aplicación",
        "create": "Crear nuevos registros (productos, facturas, etc.)",
        "report": "Generar reportes y análisis",
        "filter": "Filtrar resultados mostrados",
        "edit": "Modificar registros existentes",
        "delete": "Eliminar registros",
        "calculate": "Realizar cálculos (totales, márgenes, etc.)",
        "help": "Obtener ayuda sobre qué puedo hacer",
    }
    
    return {"intents": intents}


@router.post("/test-intent")
async def test_intent(
    text: str,
    user_context: dict = Depends(require_auth),
):
    """Test intent recognition (debug endpoint)."""
    intent, confidence, entities = IntentRecognizer.recognize(text)
    
    return {
        "input": text,
        "intent": intent,
        "confidence": confidence,
        "entities": entities,
    }
