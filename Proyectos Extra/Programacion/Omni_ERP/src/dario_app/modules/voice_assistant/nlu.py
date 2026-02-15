"""Voice Assistant NLU Engine - Natural Language Understanding for command processing."""

import re
import unicodedata
from typing import Optional, Tuple, Dict, Any
from datetime import datetime


class IntentRecognizer:
    """Recognizes user intent from natural language."""

    # Command mappings: intent -> keywords/patterns
    INTENT_PATTERNS = {
        "search": {
            "keywords": [
                "buscar", "busca", "busco", "buscando", "search", "find",
                "encuentra", "encuentro", "hay", "dime", "cuál", "cual", "cuáles", "cuales",
                "listar", "muéstrame", "muestrame", "alquileres", "rentados", "disponibles"
            ],
            "entity_types": ["producto", "cliente", "proveedor", "factura", "orden", "usuario", "proveedor", "venta", "compra", "alquiler", "renta"],
        },
        "navigate": {
            "keywords": [
                "ir a", "go to", "abre", "open", "show", "mostrar", "mostr", "voy a", "entra", "enter", "ve a", "vaya", "vamos a", "llévame", "llevar", "redirige"
            ],
            "sections": [
                "dashboard", "inicio", "home",
                "inventario", "existencias", "stock",
                "almacen", "warehouse", "bodega",
                "produccion", "production", "manufactura", "fabricacion",
                "ventas", "compras", "pos", "punto de venta",
                "reportes", "reporting", "analytics",
                "calendario", "agenda",
                "configuracion", "config", "ajustes", "settings",
                "contabilidad", "finanzas",
                "usuarios", "roles", "proveedores", "clientes",
                "correo", "email", "bandeja",
                "documentos", "historico-documentos", "historico documentos", "erp",
                "alquileres", "rentals", "rentas"
            ],
        },
        "create": {
            "keywords": ["crear", "create", "nueva", "new", "agregar", "add", "registr", "hacer", "make", "alta", "alquilar", "rentar"],
            "entities": ["producto", "cliente", "proveedor", "factura", "orden", "compra", "venta", "usuario", "reporte", "alquiler", "renta"],
        },
        "report": {
            "keywords": ["reporte", "report", "analisis", "analysis", "resumen", "summary", "estadística", "estadisticas", "mostrar datos", "analytics"],
            "types": ["ventas", "inventario", "ingresos", "gastos", "clientes", "proveedores", "compras", "alquileres", "rentabilidad"],
        },
        "filter": {
            "keywords": ["filtrar", "filter", "donde", "where", "que", "with", "por", "by", "solo", "muestrame", "alquilados", "disponibles", "rentados"],
        },
        "edit": {
            "keywords": ["editar", "edit", "modificar", "modify", "cambiar", "change", "actualizar", "update", "corrige"],
        },
        "delete": {
            "keywords": ["eliminar", "delete", "borrar", "remove", "quitar", "dar de baja"],
        },
        "calculate": {
            "keywords": ["calcular", "calculate", "total", "sum", "cuánto", "cuanto", "costo", "precio", "margen", "porcentaje", "impuestos", "beneficio"],
        },
        "email_draft": {
            "keywords": ["redacta", "escribe", "correo", "email", "mensaje", "responde", "respuesta", "contesta"],
        },
        "help": {
            "keywords": ["ayuda", "help", "cómo", "como", "qué puedo", "que puedo", "instrucciones", "guía", "no entiendo", "que sabes hacer", "comandos"],
        },
    }

    @staticmethod
    def normalize_text(text: str) -> str:
        """Normalize text for comparison (UTF-8, lowercase, remove accents)."""
        # Ensure UTF-8
        text = text.encode('utf-8').decode('utf-8')
        # Lowercase
        text = text.lower()
        # Remove accents using unicode normalization
        text = ''.join(
            c for c in unicodedata.normalize('NFD', text)
            if unicodedata.category(c) != 'Mn'
        )
        return text

    @classmethod
    def recognize(cls, text: str) -> Tuple[str, float, Optional[Dict[str, Any]]]:
        """
        Recognize intent from user input.
        
        Returns: (intent, confidence, entities_dict)
        """
        text_lower = cls.normalize_text(text).strip()
        
        # Score each intent based on keyword matches (contains + token overlap)
        tokens = set(text_lower.split())
        intent_scores = {}
        for intent, patterns in cls.INTENT_PATTERNS.items():
            score = 0
            for keyword in patterns.get("keywords", []):
                keyword_norm = cls.normalize_text(keyword)
                keyword_tokens = set(keyword_norm.split())
                if keyword_norm in text_lower:
                    score += 1
                # Token overlap gives partial credit
                if tokens and keyword_tokens and tokens.intersection(keyword_tokens):
                    score += 0.5
            intent_scores[intent] = score
        
        # Get top intent
        if max(intent_scores.values()) == 0:
            return "help", 0.3, None
        
        top_intent = max(intent_scores, key=intent_scores.get)
        confidence = min(intent_scores[top_intent] / 3, 1.0)  # Normalize to 0-1
        
        # Extract entities based on intent
        entities = cls._extract_entities(text_lower, top_intent)
        
        return top_intent, confidence, entities

    @classmethod
    def _extract_entities(cls, text: str, intent: str) -> Dict[str, Any]:
        """Extract relevant entities from text for given intent."""
        entities = {}
        
        if intent == "search":
            # Extract search terms after keywords
            text_normalized = cls.normalize_text(text)
            for keyword in cls.INTENT_PATTERNS["search"]["keywords"]:
                keyword_norm = cls.normalize_text(keyword)
                if keyword_norm in text_normalized:
                    parts = text.split(keyword, 1)
                    if len(parts) > 1:
                        entities["query"] = parts[1].strip()
                        break
        
        elif intent == "navigate":
            # Extract destination section
            text_normalized = cls.normalize_text(text)
            synonym_map = {
                "inicio": "dashboard",
                "home": "dashboard",
                "existencias": "inventario",
                "stock": "inventario",
                "bodega": "almacen",
                "warehouse": "almacen",
                "punto de venta": "pos",
                "reporting": "reportes",
                "analytics": "reportes",
                "agenda": "calendario",
                "ajustes": "configuracion",
                "settings": "configuracion",
                "finanzas": "contabilidad",
                "production": "produccion",
                "manufactura": "produccion",
                "fabricacion": "produccion",
                "email": "correo",
                "bandeja": "correo",
            }
            for section in cls.INTENT_PATTERNS["navigate"]["sections"]:
                section_norm = cls.normalize_text(section)
                if section_norm in text_normalized:
                    entities["destination"] = synonym_map.get(section_norm, section)
                    break
        
        elif intent == "create" or intent == "edit" or intent == "delete":
            # Extract entity type
            text_normalized = cls.normalize_text(text)
            for entity in cls.INTENT_PATTERNS["create"]["entities"]:
                entity_norm = cls.normalize_text(entity)
                if entity_norm in text_normalized:
                    entities["entity_type"] = entity
                    break
        
        elif intent == "report":
            # Extract report type
            text_normalized = cls.normalize_text(text)
            for report_type in cls.INTENT_PATTERNS["report"]["types"]:
                report_norm = cls.normalize_text(report_type)
                if report_norm in text_normalized:
                    entities["report_type"] = report_type
                    break

        elif intent == "email_draft":
            # Simple heuristic: split by palabras comunes
            text_norm = cls.normalize_text(text)
            # Try to capture subject/body cues
            if "sobre" in text_norm:
                parts = text_norm.split("sobre", 1)
                if len(parts) > 1:
                    entities["subject"] = parts[1].strip()
            if "que diga" in text_norm:
                parts = text_norm.split("que diga", 1)
                if len(parts) > 1:
                    entities["body"] = parts[1].strip()
        
        # Extract numbers (quantities, prices, etc.)
        numbers = re.findall(r'\b\d+(?:[.,]\d+)?\b', text)
        if numbers:
            entities["numbers"] = [float(n.replace(',', '.')) for n in numbers]
        
        return entities if entities else None


class CommandProcessor:
    """Converts recognized intents into executable commands."""

    COMMAND_MAP = {
        "search": {
            "api_endpoint": "/api/search",
            "method": "POST",
        },
        "navigate": {
            "action": "navigate",
            "method": "frontend",
        },
        "create": {
            "action": "open_form",
            "method": "frontend",
        },
        "report": {
            "api_endpoint": "/api/reportes/resumen-dashboard",
            "method": "GET",
        },
        "filter": {
            "action": "apply_filter",
            "method": "frontend",
        },
        "edit": {
            "action": "open_editor",
            "method": "frontend",
        },
        "delete": {
            "action": "confirm_delete",
            "method": "frontend",
        },
        "calculate": {
            "api_endpoint": "/api/calculate",
            "method": "POST",
        },
        "email_draft": {
            "action": "draft_email",
            "method": "frontend",
        },
        "help": {
            "action": "show_help",
            "method": "frontend",
        },
    }

    @classmethod
    def process(cls, intent: str, entities: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process intent and entities into command.
        
        Returns: command dict with action, parameters, etc.
        """
        command = cls.COMMAND_MAP.get(intent, cls.COMMAND_MAP["help"]).copy()
        
        if entities:
            command["params"] = entities
        
        return command


class ResponseGenerator:
    """Generates natural language responses with human touch."""

    # Secciones con descripciones amigables
    SECTION_NAMES = {
        "dashboard": "Panel Principal",
        "inventario": "Gestión de Inventario",
        "almacen": "Gestión de Almacén",
        "produccion": "Gestión de Producción",
        "ventas": "Módulo de Ventas",
        "compras": "Módulo de Compras",
        "pos": "Punto de Venta",
        "reportes": "Reportes y Analíticas",
        "calendario": "Calendario de Eventos",
        "configuracion": "Configuración del Sistema",
        "config": "Configuración del Sistema",
        "contabilidad": "Contabilidad",
        "usuarios": "Gestión de Usuarios",
        "roles": "Gestión de Roles",
        "proveedores": "Proveedores",
        "clientes": "Base de Clientes",
        "correo": "Módulo de Correo",
        "documentos": "Documentos",
        "historico-documentos": "Histórico de Documentos",
        "historico documentos": "Histórico de Documentos",
        "erp": "Sistema ERP",
    }

    RESPONSE_TEMPLATES = {
        "search": {
            "found": "Perfecto, encontré {count} resultado(s) para '{query}'. ¿Necesitas más información?",
            "not_found": "No encontré nada con '{query}'. ¿Quizás buscas algo diferente?",
            "error": "Disculpa, tuve un problema al buscar. Inténtalo de nuevo en un momento.",
        },
        "navigate": {
            "success": "Excelente, te llevo a {destination_name}. Un momento...",
            "error": "Disculpa, no reconozco esa sección. ¿Quizás quisiste decir otra cosa?",
        },
        "create": {
            "confirm": "Entendido, voy a preparar el formulario para crear un {entity_type}. ¿Está bien?",
            "success": "¡Listo! He creado el {entity_type} correctamente.",
            "error": "Disculpa, ocurrió un problema al crear el {entity_type}. Inténtalo nuevamente.",
        },
        "report": {
            "generating": "Claro, estoy generando el reporte de {report_type}. Espera un momento...",
            "success": "Aquí tienes el reporte de {report_type}. ¿Necesitas más detalles?",
            "error": "No pude generar ese reporte. ¿Quizás otro tipo de reporte?",
        },
        "filter": {
            "applied": "Hecho, he aplicado los filtros que solicitaste.",
            "error": "Tuve un problema al aplicar los filtros. Inténtalo de nuevo.",
        },
        "edit": {
            "confirm": "Entendido, voy a abrir el editor para modificar el {entity_type}.",
            "success": "Perfecto, he actualizado el {entity_type} correctamente.",
            "error": "Disculpa, no pude editar el {entity_type}. Verifica los datos e inténtalo nuevamente.",
        },
        "delete": {
            "confirm": "¿Estás seguro? Voy a eliminar el {entity_type}.",
            "success": "Listo, he eliminado el {entity_type} exitosamente.",
            "error": "No pude eliminar el {entity_type}. ¿Quizás ya fue eliminado?",
        },
        "calculate": {
            "result": "El resultado es {value}. ¿Necesitas otro cálculo?",
            "error": "Tuve problemas al realizar el cálculo. Verifica los números e inténtalo de nuevo.",
        },
        "email_draft": {
            "success": "Aquí tienes un borrador rápido:\nAsunto: {subject}\nCuerpo: {body}",
            "fallback": "Te preparo un borrador general. Ajusta lo que necesites:\nAsunto: Consulta pendiente\nCuerpo: Hola, espero que estés bien. Te escribo para dar seguimiento. ¿Podemos coordinar?",
        },
        "help": {
            "default": "¡Hola! Soy tu asistente de voz para usar el ERP SIN TECLADO. Puedo ayudarte a:\n"
                      "🔍 Buscar productos, clientes, facturas o alquileres\n"
                      "📍 Navegar a cualquier sección (inventario, ventas, pos, reportes, etc.)\n"
                      "➕ Crear nuevos registros (productos de compra o alquiler, ventas, clientes...)\n"
                      "📊 Generar reportes y analíticas\n"
                      "🔧 Filtrar y organizar datos (ej: 'muestra solo alquileres')\n"
                      "✏️ Editar información existente\n"
                      "🗑️ Eliminar registros\n"
                      "🧮 Calcular totales, márgenes, impuestos\n"
                      "✉️ Redactar correos y mensajes\n\n"
                      "Di comandos como: 'Crea un producto de alquiler', 'Ve a inventario', 'Busca escenarios'.\n"
                      "¿Qué deseas hacer?",
        },
    }

    @classmethod
    def generate(cls, intent: str, status: str = "default", entities: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate response based on intent and status.
        
        Returns: natural language response
        """
        templates = cls.RESPONSE_TEMPLATES.get(intent, {})
        template = templates.get(status, "¿Cómo puedo ayudarte?")
        
        # Format template with entities
        if entities:
            try:
                # Add friendly section name if navigating
                if intent == "navigate" and "destination" in entities:
                    dest = entities["destination"]
                    entities["destination_name"] = cls.SECTION_NAMES.get(dest, dest)
                if intent == "email_draft":
                    entities.setdefault("subject", "Seguimiento pendiente")
                    entities.setdefault("body", "Hola, te escribo para dar seguimiento. Confírmame por favor cuándo podemos avanzar.")
                
                template = template.format(**entities)
            except KeyError:
                pass
        
        return template
