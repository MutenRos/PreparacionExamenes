"""
MÓDULO DE AUTOMATIZACIONES INTERNAS - Documentación Completa

Tu ERP ahora tiene un sistema de automatizaciones NATIVO sin necesidad de Zapier.
Los usuarios pueden crear reglas que se ejecutan automáticamente cuando ocurren eventos.

═══════════════════════════════════════════════════════════════════════════════
CARACTERÍSTICAS
═══════════════════════════════════════════════════════════════════════════════

✅ TRIGGERS (Eventos que activan automatizaciones):
   • Venta creada/completada
   • Compra creada/recibida
   • Stock bajo
   • Cliente creado
   • Pago recibido/atrasado
   • Cita creada/confirmada
   • Hora programada (para ejecutar cada día/semana)

✅ ACCIONES (Lo que hace la automatización):
   • Enviar emails (cliente, proveedor, personalizado)
   • Enviar WhatsApp
   • Crear eventos en calendario
   • Crear tareas
   • Generar órdenes de compra automáticamente
   • Cambiar estado de registros
   • Hacer POST a webhooks externos
   • Realizar backups

✅ CONDICIONES:
   • Evaluar variables (ej: si monto > 1000)
   • Condiciones complejas (Y/O)
   • Interpolación de variables en mensajes ({{venta.monto}})

✅ ESTADÍSTICAS:
   • Registrar cada ejecución
   • Ver histórico de ejecuciones
   • Métricas de tasa de éxito

═══════════════════════════════════════════════════════════════════════════════
ENDPOINTS API
═══════════════════════════════════════════════════════════════════════════════

GET /api/automatizaciones/templates
   → Obtiene templates predefinidos de automatizaciones

GET /api/automatizaciones/
   → Lista todas las automatizaciones de la organización
   Parámetros opcionales:
   - estado: "activa", "pausada", "desactivada"
   - trigger: "venta_creada", "stock_bajo", etc.

POST /api/automatizaciones/
   → Crea una nueva automatización
   Body:
   {
     "nombre": "Notificar venta nueva",
     "descripcion": "Envía email al cliente cuando se registra una venta",
     "tipo_trigger": "venta_creada",
     "condiciones": {
       "condiciones": [
         {
           "campo": "monto",
           "operador": ">",
           "valor": "1000"
         }
       ]
     },
     "acciones": [
       {
         "tipo_accion": "enviar_email_cliente",
         "parametros": {
           "asunto": "¡Venta registrada!",
           "cuerpo": "Tu venta {{venta.numero}} por {{venta.monto}} ha sido registrada"
         },
         "orden": 1
       },
       {
         "tipo_accion": "crear_evento_calendario",
         "parametros": {
           "titulo": "Venta {{venta.numero}}",
           "descripcion": "Monto: {{venta.monto}}",
           "fecha_inicio": "{{venta.fecha}}"
         },
         "orden": 2
       }
     ],
     "continuar_en_error": false,
     "tiempo_espera_minutos": 0
   }

GET /api/automatizaciones/{id}
   → Obtiene una automatización específica

PUT /api/automatizaciones/{id}
   → Actualiza una automatización

DELETE /api/automatizaciones/{id}
   → Elimina una automatización

POST /api/automatizaciones/{id}/activar
   → Activa una automatización

POST /api/automatizaciones/{id}/desactivar
   → Desactiva una automatización

GET /api/automatizaciones/{id}/registros?limite=50
   → Obtiene el histórico de ejecuciones

GET /api/automatizaciones/{id}/estadisticas
   → Obtiene estadísticas de ejecuciones

═══════════════════════════════════════════════════════════════════════════════
EJEMPLOS DE CASOS DE USO
═══════════════════════════════════════════════════════════════════════════════

1. NOTIFICACIÓN DE VENTA
   Cuando se crea una venta:
   - Enviar email al cliente con detalles
   - Crear evento en calendario
   - Guardar nota con datos importantes

2. ALERTAS DE STOCK
   Cuando el stock baja del mínimo:
   - Generar orden de compra automática
   - Crear tarea para revisar
   - Notificar al gerente

3. RECORDATORIO DE PAGO
   Cuando un pago está atrasado:
   - Enviar email de recordatorio
   - Enviar WhatsApp
   - Crear tarea para seguimiento

4. CONFIRMACIÓN DE CITA
   Cuando se crea una cita:
   - Enviar email de confirmación al cliente
   - Crear evento en calendario
   - Enviar recordatorio 24 horas antes

5. FACTURACIÓN AUTOMÁTICA
   Cuando se completa una venta:
   - Generar factura automáticamente
   - Enviar PDF al cliente
   - Registrar en contabilidad

═══════════════════════════════════════════════════════════════════════════════
INTEGRACIÓN CON MÓDULOS EXISTENTES
═══════════════════════════════════════════════════════════════════════════════

Para integrar automatizaciones en un módulo (ej: ventas), agregar en el endpoint:

```python
from fastapi import BackgroundTasks
from dario_app.modules.automatizaciones.hooks import trigger_venta_creada

@router.post("/", response_model=VentaResponse)
async def create_venta(
    venta: VentaCreate,
    background_tasks: BackgroundTasks,  # ← Agregar
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db)
):
    # ... código para crear venta ...
    
    db_venta = Venta(...)
    db.add(db_venta)
    await db.commit()
    await db.refresh(db_venta)
    
    # Ejecutar automatizaciones en background
    async def ejecutar_automatizaciones():
        try:
            await trigger_venta_creada(db, org_id, {
                "venta_id": db_venta.id,
                "venta_numero": db_venta.numero,
                "cliente_nombre": db_venta.cliente_nombre,
                "cliente_email": db_venta.cliente_email,
                "monto": float(db_venta.total),
                "fecha": db_venta.fecha.isoformat(),
                "estado": db_venta.estado
            })
        except Exception as e:
            print(f"⚠️ Error en automatizaciones: {e}")
    
    background_tasks.add_task(ejecutar_automatizaciones)
    
    return db_venta
```

═══════════════════════════════════════════════════════════════════════════════
VARIABLES DISPONIBLES POR TRIGGER
═══════════════════════════════════════════════════════════════════════════════

VENTA_CREADA:
  - venta_id, venta_numero
  - cliente_nombre, cliente_email
  - monto, fecha, estado

COMPRA_CREADA:
  - compra_id, compra_numero
  - proveedor_nombre, proveedor_email
  - monto, fecha, estado

STOCK_BAJO:
  - producto_id, producto_nombre
  - stock_actual, stock_minimo
  - falta: stock_minimo - stock_actual

CLIENTE_CREADO:
  - cliente_id, cliente_nombre, cliente_email
  - tipo, telefono, direccion

PAGO_RECIBIDO:
  - pago_id, monto, fecha
  - venta_id, cliente_nombre

PAGO_ATRASADO:
  - venta_id, venta_numero
  - cliente_nombre, cliente_email
  - monto, dias_atraso

CITA_CREADA:
  - cita_id, titulo, descripcion
  - cliente_nombre, cliente_email
  - fecha_hora, duracion_minutos

═══════════════════════════════════════════════════════════════════════════════
MODELOS DE BASE DE DATOS
═══════════════════════════════════════════════════════════════════════════════

Tabla: automatizaciones
  - id
  - organization_id (multi-tenant)
  - nombre, descripcion
  - tipo_trigger (enum)
  - condiciones (JSON)
  - estado (activa/pausada/desactivada)
  - estadísticas: total_ejecuciones, ejecuciones_exitosas, etc.

Tabla: acciones_automatizacion
  - id
  - automatizacion_id (FK)
  - tipo_accion (enum)
  - parametros (JSON)
  - orden (para ejecutar secuencialmente)

Tabla: registros_automatizacion
  - id
  - automatizacion_id (FK)
  - trigger_data (JSON)
  - resultado (exito/error)
  - mensaje_error
  - acciones_ejecutadas (JSON con detalles)
  - ejecutado_en

═══════════════════════════════════════════════════════════════════════════════
VENTAJAS SOBRE ZAPIER
═══════════════════════════════════════════════════════════════════════════════

✅ Sin costos de terceros (todo integrado)
✅ Datos siempre en tu servidor
✅ Más rápido (sin latencia de API externa)
✅ Mejor privacidad
✅ Condiciones y acciones personalizables
✅ Integración perfecta con todos tus módulos
✅ Historial completo de ejecuciones
✅ Debugging más fácil

═══════════════════════════════════════════════════════════════════════════════
"""

if __name__ == "__main__":
    print(__doc__)
