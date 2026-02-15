"""Tutorial definitions for each module/section."""

# POS Tutorial
POS_TUTORIAL = [
    {
        "step": 1,
        "title": "💳 Bienvenido al POS",
        "description": "Sistema de punto de venta rápido. Crea tickets, cobra y gestiona caja.",
        "selector": ".pos-container",
        "position": "center",
        "highlight": False,
    },
    {
        "step": 2,
        "title": "🛒 Catálogo de productos",
        "description": "Busca productos por código o nombre. Click para añadir al ticket.",
        "selector": ".product-grid",
        "position": "center",
        "highlight": True,
    },
    {
        "step": 3,
        "title": "🧾 Ticket actual",
        "description": "Revisa líneas, modifica cantidades y aplica descuentos antes de cobrar.",
        "selector": ".ticket-panel",
        "position": "center",
        "highlight": True,
    },
    {
        "step": 4,
        "title": "💵 Métodos de pago",
        "description": "Acepta efectivo, tarjeta o mixto. Calcula cambio automáticamente.",
        "selector": ".payment-methods",
        "position": "center",
        "highlight": True,
    },
    {
        "step": 5,
        "title": "🎉 ¡Listo para vender!",
        "description": "Empieza a crear tickets y gestionar ventas. Imprime tickets desde el historial.",
        "selector": "body",
        "position": "center",
        "highlight": False,
    },
]

# Inventario Tutorial
INVENTARIO_TUTORIAL = [
    {
        "step": 1,
        "title": "📦 Gestión de Inventario",
        "description": "Control total de stock, alertas de mínimos y movimientos.",
        "selector": "body",
        "position": "center",
        "highlight": False,
    },
    {
        "step": 2,
        "title": "📋 Tabla de productos",
        "description": "Lista completa: stock actual, mínimos, proveedores y precios.",
        "selector": ".table",
        "position": "center",
        "highlight": True,
    },
    {
        "step": 3,
        "title": "➕ Crear producto",
        "description": "Añade productos con código, nombre, categoría y stock inicial.",
        "selector": "button:contains('Nuevo')",
        "position": "center",
        "highlight": True,
    },
    {
        "step": 4,
        "title": "⚠️ Alertas de stock",
        "description": "Productos bajo mínimo se destacan. Genera órdenes de compra automáticas.",
        "selector": ".alert-badge",
        "position": "center",
        "highlight": True,
    },
    {
        "step": 5,
        "title": "📊 Movimientos",
        "description": "Historial de entradas/salidas, ajustes y transferencias entre almacenes.",
        "selector": ".movements-tab",
        "position": "center",
        "highlight": True,
    },
]

# Logística Tutorial
LOGISTICA_TUTORIAL = [
    {
        "step": 1,
        "title": "🚚 Centro de Logística",
        "description": "Gestiona envíos, transportistas y seguimiento en tiempo real.",
        "selector": "body",
        "position": "center",
        "highlight": False,
    },
    {
        "step": 2,
        "title": "📦 Tarjetas de acción",
        "description": "Recepción, preparación, envíos y devoluciones. Click para acceder.",
        "selector": ".action-card:first",
        "position": "center",
        "highlight": True,
    },
    {
        "step": 3,
        "title": "🔍 Tracking",
        "description": "Número de seguimiento y estado de cada envío actualizado.",
        "selector": ".tracking-section",
        "position": "center",
        "highlight": True,
    },
    {
        "step": 4,
        "title": "🚛 Transportistas",
        "description": "Configura transportistas, tarifas y zonas de cobertura.",
        "selector": ".carriers-config",
        "position": "center",
        "highlight": True,
    },
]

# Producción Tutorial
PRODUCCION_TUTORIAL = [
    {
        "step": 1,
        "title": "🏭 Órdenes de Producción",
        "description": "Planifica fabricación, asigna recursos y controla avances.",
        "selector": "body",
        "position": "center",
        "highlight": False,
    },
    {
        "step": 2,
        "title": "📋 Lista de órdenes",
        "description": "Nuevas, en proceso, completadas. Filtra por estado y prioridad.",
        "selector": ".orders-table",
        "position": "center",
        "highlight": True,
    },
    {
        "step": 3,
        "title": "🔧 Crear orden",
        "description": "Producto, cantidad, fecha objetivo y BOM asociado.",
        "selector": ".new-order-btn",
        "position": "center",
        "highlight": True,
    },
    {
        "step": 4,
        "title": "👷 Asignar operarios",
        "description": "Selecciona equipo, define turnos y registra tiempos.",
        "selector": ".assign-workers",
        "position": "center",
        "highlight": True,
    },
    {
        "step": 5,
        "title": "✅ Control de calidad",
        "description": "Validaciones, rechazos y scrap. Trazabilidad completa.",
        "selector": ".quality-section",
        "position": "center",
        "highlight": True,
    },
]

# Ventas Tutorial
VENTAS_TUTORIAL = [
    {
        "step": 1,
        "title": "💰 Pipeline de Ventas",
        "description": "Oportunidades, presupuestos y cierre de ventas.",
        "selector": "body",
        "position": "center",
        "highlight": False,
    },
    {
        "step": 2,
        "title": "🎯 Etapas del pipeline",
        "description": "Lead → Calificado → Propuesta → Negociación → Ganado/Perdido.",
        "selector": ".pipeline-stages",
        "position": "center",
        "highlight": True,
    },
    {
        "step": 3,
        "title": "📝 Crear oportunidad",
        "description": "Cliente, valor estimado, probabilidad y fecha cierre.",
        "selector": ".new-opportunity",
        "position": "center",
        "highlight": True,
    },
    {
        "step": 4,
        "title": "📄 Generar presupuesto",
        "description": "Líneas de producto, descuentos y condiciones. Exporta PDF.",
        "selector": ".generate-quote",
        "position": "center",
        "highlight": True,
    },
]

# Compras Tutorial
COMPRAS_TUTORIAL = [
    {
        "step": 1,
        "title": "🛒 Gestión de Compras",
        "description": "Órdenes a proveedores, recepción y costos.",
        "selector": "body",
        "position": "center",
        "highlight": False,
    },
    {
        "step": 2,
        "title": "📋 Órdenes de compra",
        "description": "Borrador, enviada, parcial, recibida. Seguimiento completo.",
        "selector": ".purchase-orders",
        "position": "center",
        "highlight": True,
    },
    {
        "step": 3,
        "title": "➕ Nueva orden",
        "description": "Proveedor, productos, cantidades y precios acordados.",
        "selector": ".new-purchase",
        "position": "center",
        "highlight": True,
    },
    {
        "step": 4,
        "title": "📦 Recepción parcial",
        "description": "Valida cantidades recibidas, marca diferencias y actualiza stock.",
        "selector": ".receive-goods",
        "position": "center",
        "highlight": True,
    },
]

# RRHH Tutorial
HR_TUTORIAL = [
    {
        "step": 1,
        "title": "🧑‍💼 Recursos Humanos",
        "description": "Empleados, vacaciones, nómina y partes de trabajo.",
        "selector": "body",
        "position": "center",
        "highlight": False,
    },
    {
        "step": 2,
        "title": "👥 Ficha de empleados",
        "description": "Datos personales, contrato, cargo y departamento.",
        "selector": ".employees-list",
        "position": "center",
        "highlight": True,
    },
    {
        "step": 3,
        "title": "📅 Solicitar vacaciones",
        "description": "Rango de fechas, motivo y flujo de aprobación.",
        "selector": ".request-leave",
        "position": "center",
        "highlight": True,
    },
    {
        "step": 4,
        "title": "🕒 Partes de trabajo",
        "description": "Registro de horas por proyecto, tarea y cliente.",
        "selector": ".timesheets",
        "position": "center",
        "highlight": True,
    },
]

# Financial Tutorial
FINANCIAL_TUTORIAL = [
    {
        "step": 1,
        "title": "🏦 Suite Financiera",
        "description": "Presupuestos, conciliación bancaria y cash-flow.",
        "selector": "body",
        "position": "center",
        "highlight": False,
    },
    {
        "step": 2,
        "title": "💵 Dashboard financiero",
        "description": "Ingresos, gastos, margen y ratios en tiempo real.",
        "selector": ".financial-dashboard",
        "position": "center",
        "highlight": True,
    },
    {
        "step": 3,
        "title": "📊 Presupuestos",
        "description": "Define objetivos mensuales por categoría y compara con real.",
        "selector": ".budgets-section",
        "position": "center",
        "highlight": True,
    },
    {
        "step": 4,
        "title": "🏦 Conciliación",
        "description": "Importa extractos, empareja transacciones y cierra períodos.",
        "selector": ".reconciliation",
        "position": "center",
        "highlight": True,
    },
]

# Marketing Tutorial
MARKETING_TUTORIAL = [
    {
        "step": 1,
        "title": "📢 Marketing Hub",
        "description": "Campañas, journeys automatizados y plantillas de correo.",
        "selector": "body",
        "position": "center",
        "highlight": False,
    },
    {
        "step": 2,
        "title": "🎯 Crear campaña",
        "description": "Email, SMS o mixta. Define audiencia, contenido y programación.",
        "selector": ".new-campaign",
        "position": "center",
        "highlight": True,
    },
    {
        "step": 3,
        "title": "🔄 Customer Journey",
        "description": "Flujos automáticos: triggers, condiciones y acciones.",
        "selector": ".journey-builder",
        "position": "center",
        "highlight": True,
    },
    {
        "step": 4,
        "title": "📈 Métricas",
        "description": "Aperturas, clicks, conversiones y ROI por campaña.",
        "selector": ".campaign-stats",
        "position": "center",
        "highlight": True,
    },
]

# All module tutorials mapping
MODULE_TUTORIALS = {
    "pos": POS_TUTORIAL,
    "inventario": INVENTARIO_TUTORIAL,
    "logistica": LOGISTICA_TUTORIAL,
    "produccion": PRODUCCION_TUTORIAL,
    "produccion-ordenes": PRODUCCION_TUTORIAL,
    "ventas": VENTAS_TUTORIAL,
    "compras": COMPRAS_TUTORIAL,
    "hr": HR_TUTORIAL,
    "financial": FINANCIAL_TUTORIAL,
    "marketing": MARKETING_TUTORIAL,
}


def get_module_tutorial(module_name: str) -> list[dict] | None:
    """Get tutorial steps for a specific module."""
    return MODULE_TUTORIALS.get(module_name)


def get_available_modules() -> list[str]:
    """Get list of modules with tutorials."""
    return list(MODULE_TUTORIALS.keys())
