"""
Configuration of Permissions and Roles for the ERP system.
Organized by categories (Discord-like structure).
"""

PERMISSIONS_BY_CATEGORY = {
    "General": [
        {"code": "view_dashboard", "name": "Ver Dashboard", "desc": "Acceso al panel principal"},
        {"code": "manage_settings", "name": "Gestionar Configuración", "desc": "Acceso a configuración global"},
    ],
    "Ventas (Sales)": [
        {"code": "view_sales", "name": "Ver Ventas", "desc": "Ver historial de ventas"},
        {"code": "create_sale", "name": "Crear Venta", "desc": "Registrar nuevas ventas"},
        {"code": "approve_sale", "name": "Aprobar Venta", "desc": "Aprobar ventas pendientes o grandes"},
        {"code": "void_sale", "name": "Anular Venta", "desc": "Cancelar o anular ventas"},
    ],
    "Inventario (Inventory)": [
        {"code": "view_inventory", "name": "Ver Inventario", "desc": "Ver stock y productos"},
        {"code": "manage_products", "name": "Gestionar Productos", "desc": "Crear, editar, eliminar productos"},
        {"code": "adjust_stock", "name": "Ajustar Stock", "desc": "Realizar ajustes manuales de inventario"},
        {"code": "view_costs", "name": "Ver Costos", "desc": "Ver precios de costo y márgenes"},
    ],
    "Compras (Purchasing)": [
        {"code": "view_purchases", "name": "Ver Compras", "desc": "Ver órdenes de compra"},
        {"code": "create_purchase", "name": "Crear Compra", "desc": "Crear órdenes de compra a proveedores"},
        {"code": "approve_purchase", "name": "Aprobar Compra", "desc": "Autorizar compras"},
    ],
    "RRHH (HR)": [
        {"code": "view_employees", "name": "Ver Empleados", "desc": "Ver lista de empleados"},
        {"code": "manage_employees", "name": "Gestionar Empleados", "desc": "Contratar, editar, despedir empleados"},
        {"code": "manage_payroll", "name": "Gestionar Nóminas", "desc": "Procesar pagos de nómina"},
    ],
    "Usuarios y Roles": [
        {"code": "view_users", "name": "Ver Usuarios", "desc": "Ver usuarios del sistema"},
        {"code": "manage_users", "name": "Gestionar Usuarios", "desc": "Crear y editar usuarios"},
        {"code": "manage_roles", "name": "Gestionar Roles", "desc": "Crear y asignar roles y permisos"},
    ],
    "CRM": [
        {"code": "view_crm", "name": "Ver CRM", "desc": "Acceso a clientes y leads"},
        {"code": "manage_leads", "name": "Gestionar Leads", "desc": "Crear y mover leads"},
    ]
}

DEFAULT_ROLES = {
    "Admin": {
        "description": "Acceso total al sistema",
        "permissions": ["*"]  # Wildcard for all
    },
    "Gerente": {
        "description": "Gestión de negocio, sin acceso a configuración técnica profunda",
        "permissions": [
            "view_dashboard", "view_sales", "approve_sale", "void_sale",
            "view_inventory", "view_costs", "view_purchases", "approve_purchase",
            "view_employees", "view_crm", "view_users"
        ]
    },
    "Vendedor": {
        "description": "Acceso limitado a ventas y clientes",
        "permissions": [
            "view_dashboard", "view_sales", "create_sale", 
            "view_inventory", "view_crm", "manage_leads"
        ]
    },
    "Almacenero": {
        "description": "Gestión de stock y productos",
        "permissions": [
            "view_inventory", "manage_products", "adjust_stock", "view_purchases"
        ]
    },
    "RRHH": {
        "description": "Gestión de personal",
        "permissions": [
            "view_employees", "manage_employees", "manage_payroll"
        ]
    }
}
