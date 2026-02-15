"""Command Palette - Quick actions interface (like VS Code)."""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class Command:
    """Command definition."""
    id: str
    title: str
    category: str
    action: str
    shortcut: Optional[str] = None
    icon: Optional[str] = None
    keywords: List[str] = None


# Enterprise command registry
COMMANDS = [
    # Navigation
    Command(
        id="nav.dashboard",
        title="Ir al Dashboard",
        category="Navegación",
        action="/app/dashboard",
        shortcut="Ctrl+D",
        icon="📊",
        keywords=["inicio", "home", "dashboard"]
    ),
    Command(
        id="nav.inventory",
        title="Abrir Inventario",
        category="Navegación",
        action="/app/inventario",
        shortcut="Ctrl+I",
        icon="📦",
        keywords=["productos", "stock", "inventario"]
    ),
    Command(
        id="nav.sales",
        title="Abrir Ventas",
        category="Navegación",
        action="/app/ventas",
        shortcut="Ctrl+V",
        icon="💰",
        keywords=["ventas", "órdenes", "pedidos"]
    ),
    Command(
        id="nav.purchases",
        title="Abrir Compras",
        category="Navegación",
        action="/app/compras",
        shortcut="Ctrl+P",
        icon="🛒",
        keywords=["compras", "proveedores", "órdenes"]
    ),
    Command(
        id="nav.pos",
        title="Abrir Punto de Venta",
        category="Navegación",
        action="/app/pos",
        shortcut="Ctrl+Shift+P",
        icon="🏪",
        keywords=["pos", "caja", "venta rápida"]
    ),
    
    # Quick Actions
    Command(
        id="create.product",
        title="Crear Nuevo Producto",
        category="Acciones Rápidas",
        action="modal:new-product",
        shortcut="Ctrl+N P",
        icon="➕",
        keywords=["nuevo", "producto", "crear"]
    ),
    Command(
        id="create.sale",
        title="Nueva Venta",
        category="Acciones Rápidas",
        action="modal:new-sale",
        shortcut="Ctrl+N V",
        icon="➕",
        keywords=["nueva", "venta", "orden"]
    ),
    Command(
        id="create.purchase",
        title="Nueva Compra",
        category="Acciones Rápidas",
        action="modal:new-purchase",
        shortcut="Ctrl+N C",
        icon="➕",
        keywords=["nueva", "compra", "orden"]
    ),
    Command(
        id="create.customer",
        title="Nuevo Cliente",
        category="Acciones Rápidas",
        action="modal:new-customer",
        shortcut="Ctrl+N K",
        icon="➕",
        keywords=["nuevo", "cliente", "crear"]
    ),
    
    # Reports
    Command(
        id="report.sales",
        title="Reporte de Ventas",
        category="Reportes",
        action="/app/reportes?tipo=ventas",
        icon="📈",
        keywords=["reporte", "ventas", "estadísticas"]
    ),
    Command(
        id="report.inventory",
        title="Reporte de Inventario",
        category="Reportes",
        action="/app/reportes?tipo=inventario",
        icon="📊",
        keywords=["reporte", "inventario", "stock"]
    ),
    Command(
        id="report.analytics",
        title="Analytics Dashboard",
        category="Reportes",
        action="/app/reportes?tipo=analytics",
        icon="📊",
        keywords=["analytics", "bi", "inteligencia"]
    ),
    
    # Settings
    Command(
        id="settings.profile",
        title="Mi Perfil",
        category="Configuración",
        action="/app/settings?tab=profile",
        icon="👤",
        keywords=["perfil", "usuario", "cuenta"]
    ),
    Command(
        id="settings.org",
        title="Configuración de Organización",
        category="Configuración",
        action="/app/settings?tab=organization",
        icon="🏢",
        keywords=["organización", "empresa", "configuración"]
    ),
    Command(
        id="settings.security",
        title="Seguridad",
        category="Configuración",
        action="/app/settings?tab=security",
        icon="🔒",
        keywords=["seguridad", "2fa", "contraseña"]
    ),
    
    # Search
    Command(
        id="search.products",
        title="Buscar Productos",
        category="Búsqueda",
        action="search:productos",
        shortcut="Ctrl+K P",
        icon="🔍",
        keywords=["buscar", "productos", "inventario"]
    ),
    Command(
        id="search.customers",
        title="Buscar Clientes",
        category="Búsqueda",
        action="search:clientes",
        shortcut="Ctrl+K C",
        icon="🔍",
        keywords=["buscar", "clientes", "crm"]
    ),
    
    # Help
    Command(
        id="help.docs",
        title="Documentación",
        category="Ayuda",
        action="window.open('/docs')",
        shortcut="F1",
        icon="📖",
        keywords=["ayuda", "docs", "documentación"]
    ),
    Command(
        id="help.shortcuts",
        title="Atajos de Teclado",
        category="Ayuda",
        action="modal:shortcuts",
        shortcut="Ctrl+/",
        icon="⌨️",
        keywords=["atajos", "shortcuts", "teclado"]
    ),
]


def get_all_commands() -> List[Dict[str, Any]]:
    """Get all available commands."""
    return [
        {
            "id": cmd.id,
            "title": cmd.title,
            "category": cmd.category,
            "action": cmd.action,
            "shortcut": cmd.shortcut,
            "icon": cmd.icon,
            "keywords": cmd.keywords or []
        }
        for cmd in COMMANDS
    ]


def search_commands(query: str) -> List[Dict[str, Any]]:
    """Search commands by query."""
    query_lower = query.lower()
    results = []
    
    for cmd in COMMANDS:
        score = 0
        
        # Title match
        if query_lower in cmd.title.lower():
            score += 10
        
        # Category match
        if query_lower in cmd.category.lower():
            score += 5
        
        # Keywords match
        if cmd.keywords:
            for keyword in cmd.keywords:
                if query_lower in keyword.lower():
                    score += 7
        
        if score > 0:
            results.append({
                "id": cmd.id,
                "title": cmd.title,
                "category": cmd.category,
                "action": cmd.action,
                "shortcut": cmd.shortcut,
                "icon": cmd.icon,
                "score": score
            })
    
    # Sort by score
    results.sort(key=lambda x: x["score"], reverse=True)
    
    return results[:10]  # Top 10 results
