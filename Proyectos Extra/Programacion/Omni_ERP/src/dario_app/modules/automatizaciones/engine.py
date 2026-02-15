"""Motor de ejecución de automatizaciones."""

import asyncio
import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from dario_app.core.email_service import EmailService
from dario_app.modules.automatizaciones.models import (
    Automatizacion,
    Accion,
    RegistroAutomatizacion,
    TipoAccion,
    TipoTrigger,
)


class AutomatizacionesEngine:
    """Motor de ejecución de automatizaciones."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.email_service = EmailService()
    
    async def ejecutar_trigger(
        self,
        org_id: int,
        tipo_trigger: TipoTrigger,
        datos_trigger: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Ejecuta todas las automatizaciones asociadas a un trigger.
        
        Args:
            org_id: ID de la organización
            tipo_trigger: Tipo de trigger (ej: VENTA_CREADA)
            datos_trigger: Datos del evento (ej: {"venta_id": 123, "monto": 5000})
            
        Returns:
            Lista de resultados de ejecuciones
        """
        resultados = []
        
        # Obtener todas las automatizaciones activas para este trigger
        query = select(Automatizacion).where(
            (Automatizacion.organization_id == org_id) &
            (Automatizacion.tipo_trigger == tipo_trigger) &
            (Automatizacion.activa == True)
        )
        result = await self.db.execute(query)
        automatizaciones = result.scalars().all()
        
        for automatizacion in automatizaciones:
            try:
                # Evaluar condiciones
                if not await self._evaluar_condiciones(automatizacion, datos_trigger):
                    continue
                
                # Ejecutar acciones
                resultado = await self._ejecutar_acciones(
                    automatizacion,
                    org_id,
                    datos_trigger
                )
                
                resultados.append(resultado)
                
                # Registrar ejecución
                await self._registrar_ejecucion(
                    automatizacion.id,
                    org_id,
                    datos_trigger,
                    resultado
                )
                
            except Exception as e:
                print(f"❌ Error ejecutando automatización {automatizacion.id}: {str(e)}")
        
        return resultados
    
    async def _evaluar_condiciones(
        self,
        automatizacion: Automatizacion,
        datos: Dict[str, Any]
    ) -> bool:
        """Evalúa si se deben ejecutar las acciones según las condiciones."""
        if not automatizacion.condiciones:
            return True
        
        # Evaluar condiciones JSON
        condiciones = automatizacion.condiciones
        
        # Lógica simple: AND de todas las condiciones
        for cond in condiciones.get("condiciones", []):
            campo = cond.get("campo")
            operador = cond.get("operador")
            valor_esperado = cond.get("valor")
            
            # Extraer valor del campo (soporta notación de punto: "cliente.nombre")
            valor_actual = self._obtener_valor_anidado(datos, campo)
            
            # Comparar
            if not self._comparar_valores(valor_actual, operador, valor_esperado):
                return False
        
        return True
    
    def _obtener_valor_anidado(self, dict_obj: Dict, ruta: str) -> Any:
        """Obtiene un valor de un diccionario usando notación de punto."""
        partes = ruta.split(".")
        valor = dict_obj
        
        for parte in partes:
            if isinstance(valor, dict):
                valor = valor.get(parte)
            else:
                return None
        
        return valor
    
    def _comparar_valores(self, actual: Any, operador: str, esperado: Any) -> bool:
        """Compara dos valores según un operador."""
        if operador == "=":
            return actual == esperado
        elif operador == "!=":
            return actual != esperado
        elif operador == ">":
            return actual > esperado
        elif operador == "<":
            return actual < esperado
        elif operador == ">=":
            return actual >= esperado
        elif operador == "<=":
            return actual <= esperado
        elif operador == "contains":
            return esperado in str(actual)
        elif operador == "in":
            return actual in esperado.split(",")
        else:
            return True
    
    async def _ejecutar_acciones(
        self,
        automatizacion: Automatizacion,
        org_id: int,
        datos_trigger: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Ejecuta todas las acciones de una automatización."""
        resultado = {
            "automatizacion_id": automatizacion.id,
            "estado": "exito",
            "acciones": []
        }
        
        # Obtener acciones ordenadas
        query = select(Accion).where(
            (Accion.automatizacion_id == automatizacion.id) &
            (Accion.activa == True)
        ).order_by(Accion.orden)
        
        result = await self.db.execute(query)
        acciones = result.scalars().all()
        
        for accion in acciones:
            try:
                resultado_accion = await self._ejecutar_accion_individual(
                    accion,
                    org_id,
                    datos_trigger
                )
                resultado["acciones"].append(resultado_accion)
                
            except Exception as e:
                print(f"❌ Error en acción {accion.id}: {str(e)}")
                resultado["acciones"].append({
                    "accion_id": accion.id,
                    "tipo": accion.tipo_accion.value,
                    "estado": "error",
                    "error": str(e)
                })
                
                # Si no continuar en error, parar aquí
                if not automatizacion.continuar_en_error:
                    resultado["estado"] = "error"
                    break
        
        return resultado
    
    async def _ejecutar_accion_individual(
        self,
        accion: Accion,
        org_id: int,
        datos_trigger: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Ejecuta una acción individual."""
        tipo = accion.tipo_accion
        params = accion.parametros
        
        resultado = {
            "accion_id": accion.id,
            "tipo": tipo.value,
            "estado": "exito"
        }
        
        # Reemplazar variables en parámetros
        params = self._interpolar_variables(params, datos_trigger)
        
        if tipo == TipoAccion.ENVIAR_EMAIL:
            await self._accion_enviar_email(params)
        
        elif tipo == TipoAccion.ENVIAR_EMAIL_CLIENTE:
            await self._accion_enviar_email_cliente(params, datos_trigger)
        
        elif tipo == TipoAccion.ENVIAR_WHATSAPP:
            await self._accion_enviar_whatsapp(params)
        
        elif tipo == TipoAccion.CREAR_EVENTO_CALENDARIO:
            await self._accion_crear_evento(org_id, params)
        
        elif tipo == TipoAccion.CREAR_TAREA:
            await self._accion_crear_tarea(org_id, params)
        
        elif tipo == TipoAccion.GENERAR_ORDEN_COMPRA:
            await self._accion_generar_orden_compra(org_id, params, datos_trigger)
        
        elif tipo == TipoAccion.CAMBIAR_ESTADO:
            await self._accion_cambiar_estado(org_id, params)
        
        elif tipo == TipoAccion.WEBHOOK:
            await self._accion_webhook(params)
        
        else:
            resultado["estado"] = "pendiente"
            resultado["mensaje"] = f"Acción {tipo.value} no implementada aún"
        
        return resultado
    
    def _interpolar_variables(self, params: Dict, datos: Dict) -> Dict:
        """Reemplaza variables en parámetros (ej: {{venta.monto}})."""
        resultado = {}
        
        for clave, valor in params.items():
            if isinstance(valor, str):
                # Buscar variables {{...}}
                import re
                def reemplazar(match):
                    var = match.group(1)
                    return str(self._obtener_valor_anidado(datos, var) or "")
                
                valor = re.sub(r'\{\{(\w+(?:\.\w+)*)\}\}', reemplazar, valor)
            
            resultado[clave] = valor
        
        return resultado
    
    async def _accion_enviar_email(self, params: Dict):
        """Envía un email."""
        destinatario = params.get("destinatario")
        asunto = params.get("asunto")
        cuerpo = params.get("cuerpo")
        html = params.get("html", False)
        
        if html:
            self.email_service.send_html_email(destinatario, asunto, cuerpo)
        else:
            self.email_service.send_email(destinatario, asunto, cuerpo)
    
    async def _accion_enviar_email_cliente(self, params: Dict, datos: Dict):
        """Envía email al cliente de una venta."""
        cliente_email = datos.get("cliente_email") or datos.get("cliente", {}).get("email")
        cliente_nombre = datos.get("cliente_nombre") or datos.get("cliente", {}).get("nombre")
        
        asunto = params.get("asunto", "Notificación")
        cuerpo = params.get("cuerpo", "")
        
        if cliente_email:
            self.email_service.send_email(cliente_email, asunto, cuerpo)
    
    async def _accion_enviar_whatsapp(self, params: Dict):
        """Envía un mensaje por WhatsApp (stub - requiere configuración)."""
        numero = params.get("numero")
        mensaje = params.get("mensaje")
        
        print(f"📱 WhatsApp a {numero}: {mensaje}")
        # TODO: Integrar con WhatsApp Business API
    
    async def _accion_crear_evento(self, org_id: int, params: Dict):
        """Crea un evento en el calendario."""
        from dario_app.modules.calendario.models import Evento
        from datetime import datetime as dt
        
        evento = Evento(
            organization_id=org_id,
            titulo=params.get("titulo"),
            descripcion=params.get("descripcion"),
            fecha_inicio=dt.fromisoformat(params.get("fecha_inicio")),
            fecha_fin=dt.fromisoformat(params.get("fecha_fin")),
            tipo=params.get("tipo", "tarea"),
            completado=False
        )
        self.db.add(evento)
        await self.db.commit()
    
    async def _accion_crear_tarea(self, org_id: int, params: Dict):
        """Crea una tarea (nota en calendario)."""
        from datetime import datetime as dt
        
        # Crear como evento
        await self._accion_crear_evento(org_id, {
            "titulo": params.get("titulo"),
            "descripcion": params.get("descripcion"),
            "fecha_inicio": params.get("fecha_vencimiento", dt.now().isoformat()),
            "fecha_fin": params.get("fecha_vencimiento", dt.now().isoformat()),
            "tipo": "tarea"
        })
    
    async def _accion_generar_orden_compra(self, org_id: int, params: Dict, datos: Dict):
        """Genera automáticamente una orden de compra."""
        # TODO: Implementar generación de orden de compra
        print(f"📋 Generando orden de compra con parámetros: {params}")
    
    async def _accion_cambiar_estado(self, org_id: int, params: Dict):
        """Cambia el estado de un registro."""
        tipo_registro = params.get("tipo_registro")  # "venta", "compra", etc.
        registro_id = params.get("registro_id")
        nuevo_estado = params.get("nuevo_estado")
        
        # TODO: Implementar cambio de estado genérico
        print(f"🔄 Cambiando {tipo_registro} {registro_id} a estado {nuevo_estado}")
    
    async def _accion_webhook(self, params: Dict):
        """Realiza POST a un webhook externo."""
        import aiohttp
        
        url = params.get("url")
        datos = params.get("datos", {})
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=datos, timeout=10) as resp:
                    print(f"✅ Webhook ejecutado: {resp.status}")
        except Exception as e:
            print(f"❌ Error en webhook: {e}")
    
    async def _registrar_ejecucion(
        self,
        automatizacion_id: int,
        org_id: int,
        datos_trigger: Dict,
        resultado: Dict
    ):
        """Registra la ejecución de una automatización."""
        registro = RegistroAutomatizacion(
            automatizacion_id=automatizacion_id,
            organization_id=org_id,
            trigger_data=datos_trigger,
            resultado="exito" if resultado.get("estado") == "exito" else "error",
            acciones_ejecutadas=resultado.get("acciones"),
            ejecutado_en=datetime.utcnow()
        )
        self.db.add(registro)
        await self.db.commit()
        
        # Actualizar estadísticas de la automatización
        automatizacion = await self.db.get(Automatizacion, automatizacion_id)
        if automatizacion:
            automatizacion.total_ejecuciones += 1
            if resultado.get("estado") == "exito":
                automatizacion.ejecuciones_exitosas += 1
            else:
                automatizacion.ejecuciones_fallidas += 1
            automatizacion.ultima_ejecucion = datetime.utcnow()
            await self.db.commit()
