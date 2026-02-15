"""
Script para crear roles y permisos iniciales del sistema.
"""

import asyncio
import sys
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import select

from dario_app.database import async_session_maker
from dario_app.modules.usuarios.models import Permission, Role, RolePermission


async def crear_permisos():
    """Crea los permisos del sistema."""
    permisos = [
        # Usuarios
        {
            "codigo": "usuarios.ver",
            "nombre": "Ver Usuarios",
            "descripcion": "Ver lista de usuarios",
        },
        {
            "codigo": "usuarios.crear",
            "nombre": "Crear Usuarios",
            "descripcion": "Crear nuevos usuarios",
        },
        {
            "codigo": "usuarios.editar",
            "nombre": "Editar Usuarios",
            "descripcion": "Editar usuarios existentes",
        },
        {
            "codigo": "usuarios.eliminar",
            "nombre": "Eliminar Usuarios",
            "descripcion": "Eliminar usuarios",
        },
        {
            "codigo": "usuarios.roles.ver",
            "nombre": "Ver Roles de Usuario",
            "descripcion": "Ver roles asignados a usuarios",
        },
        {
            "codigo": "usuarios.roles.asignar",
            "nombre": "Asignar Roles",
            "descripcion": "Asignar roles a usuarios",
        },
        # Roles
        {"codigo": "roles.ver", "nombre": "Ver Roles", "descripcion": "Ver lista de roles"},
        {"codigo": "roles.crear", "nombre": "Crear Roles", "descripcion": "Crear nuevos roles"},
        {
            "codigo": "roles.editar",
            "nombre": "Editar Roles",
            "descripcion": "Editar roles existentes",
        },
        {"codigo": "roles.eliminar", "nombre": "Eliminar Roles", "descripcion": "Eliminar roles"},
        # Permisos
        {
            "codigo": "permisos.ver",
            "nombre": "Ver Permisos",
            "descripcion": "Ver lista de permisos",
        },
        {
            "codigo": "permisos.crear",
            "nombre": "Crear Permisos",
            "descripcion": "Crear nuevos permisos",
        },
        {
            "codigo": "permisos.asignar",
            "nombre": "Asignar Permisos",
            "descripcion": "Asignar permisos a roles",
        },
        # Ventas
        {"codigo": "ventas.ver", "nombre": "Ver Ventas", "descripcion": "Ver lista de ventas"},
        {"codigo": "ventas.crear", "nombre": "Crear Ventas", "descripcion": "Crear nuevas ventas"},
        {
            "codigo": "ventas.editar",
            "nombre": "Editar Ventas",
            "descripcion": "Editar ventas existentes",
        },
        {
            "codigo": "ventas.eliminar",
            "nombre": "Eliminar Ventas",
            "descripcion": "Eliminar ventas",
        },
        {
            "codigo": "ventas.facturas.generar",
            "nombre": "Generar Facturas",
            "descripcion": "Generar facturas de ventas",
        },
        # Compras
        {"codigo": "compras.ver", "nombre": "Ver Compras", "descripcion": "Ver lista de compras"},
        {
            "codigo": "compras.crear",
            "nombre": "Crear Compras",
            "descripcion": "Crear nuevas compras",
        },
        {
            "codigo": "compras.editar",
            "nombre": "Editar Compras",
            "descripcion": "Editar compras existentes",
        },
        {
            "codigo": "compras.eliminar",
            "nombre": "Eliminar Compras",
            "descripcion": "Eliminar compras",
        },
        # Inventario
        {
            "codigo": "inventario.ver",
            "nombre": "Ver Inventario",
            "descripcion": "Ver inventario de productos",
        },
        {
            "codigo": "inventario.crear",
            "nombre": "Crear Productos",
            "descripcion": "Crear nuevos productos",
        },
        {
            "codigo": "inventario.editar",
            "nombre": "Editar Productos",
            "descripcion": "Editar productos existentes",
        },
        {
            "codigo": "inventario.eliminar",
            "nombre": "Eliminar Productos",
            "descripcion": "Eliminar productos",
        },
        # Clientes
        {
            "codigo": "clientes.ver",
            "nombre": "Ver Clientes",
            "descripcion": "Ver lista de clientes",
        },
        {
            "codigo": "clientes.crear",
            "nombre": "Crear Clientes",
            "descripcion": "Crear nuevos clientes",
        },
        {
            "codigo": "clientes.editar",
            "nombre": "Editar Clientes",
            "descripcion": "Editar clientes existentes",
        },
        {
            "codigo": "clientes.eliminar",
            "nombre": "Eliminar Clientes",
            "descripcion": "Eliminar clientes",
        },
        # Proveedores
        {
            "codigo": "proveedores.ver",
            "nombre": "Ver Proveedores",
            "descripcion": "Ver lista de proveedores",
        },
        {
            "codigo": "proveedores.crear",
            "nombre": "Crear Proveedores",
            "descripcion": "Crear nuevos proveedores",
        },
        {
            "codigo": "proveedores.editar",
            "nombre": "Editar Proveedores",
            "descripcion": "Editar proveedores existentes",
        },
        {
            "codigo": "proveedores.eliminar",
            "nombre": "Eliminar Proveedores",
            "descripcion": "Eliminar proveedores",
        },
        # Reportes
        {
            "codigo": "reportes.ver",
            "nombre": "Ver Reportes",
            "descripcion": "Ver reportes del sistema",
        },
        {
            "codigo": "reportes.exportar",
            "nombre": "Exportar Reportes",
            "descripcion": "Exportar reportes en PDF/Excel",
        },
        # Configuración
        {
            "codigo": "configuracion.ver",
            "nombre": "Ver Configuración",
            "descripcion": "Ver configuración del sistema",
        },
        {
            "codigo": "configuracion.editar",
            "nombre": "Editar Configuración",
            "descripcion": "Editar configuración del sistema",
        },
    ]

    async with async_session_maker() as db:
        created_count = 0
        for permiso_data in permisos:
            # Verificar si ya existe
            stmt = select(Permission).where(Permission.codigo == permiso_data["codigo"])
            result = await db.execute(stmt)
            existing = result.scalar_one_or_none()

            if not existing:
                permiso = Permission(**permiso_data)
                db.add(permiso)
                created_count += 1

        await db.commit()
        print(f"✅ Creados {created_count} permisos (Total: {len(permisos)})")


async def crear_roles():
    """Crea los roles del sistema para la organización 1."""
    roles_data = [
        {
            "nombre": "Administrador",
            "descripcion": "Acceso total al sistema",
            "permisos": "*",  # Todos los permisos
        },
        {
            "nombre": "Gerente",
            "descripcion": "Gestión de ventas, compras e inventario",
            "permisos": [
                "ventas.*",
                "compras.*",
                "inventario.*",
                "clientes.*",
                "proveedores.*",
                "reportes.ver",
                "reportes.exportar",
            ],
        },
        {
            "nombre": "Vendedor",
            "descripcion": "Gestión de ventas y clientes",
            "permisos": [
                "ventas.ver",
                "ventas.crear",
                "ventas.facturas.generar",
                "clientes.ver",
                "clientes.crear",
                "clientes.editar",
                "inventario.ver",
            ],
        },
        {
            "nombre": "Cajero",
            "descripcion": "Registro de ventas",
            "permisos": [
                "ventas.ver",
                "ventas.crear",
                "ventas.facturas.generar",
                "clientes.ver",
                "inventario.ver",
            ],
        },
        {
            "nombre": "Almacenero",
            "descripcion": "Gestión de inventario y compras",
            "permisos": [
                "inventario.ver",
                "inventario.crear",
                "inventario.editar",
                "compras.ver",
                "compras.crear",
                "proveedores.ver",
            ],
        },
        {
            "nombre": "Comprador",
            "descripcion": "Gestión de compras y proveedores",
            "permisos": ["compras.*", "proveedores.*", "inventario.ver"],
        },
        {
            "nombre": "Visualizador",
            "descripcion": "Solo visualización de datos",
            "permisos": ["*.ver", "reportes.ver"],
        },
    ]

    async with async_session_maker() as db:
        # Obtener todos los permisos
        stmt = select(Permission)
        result = await db.execute(stmt)
        all_permissions = result.scalars().all()
        permissions_by_code = {p.codigo: p for p in all_permissions}

        created_count = 0
        for role_data in roles_data:
            # Verificar si ya existe el rol
            stmt = select(Role).where(Role.organization_id == 1, Role.nombre == role_data["nombre"])
            result = await db.execute(stmt)
            existing = result.scalar_one_or_none()

            if existing:
                print(f"⚠️  Rol '{role_data['nombre']}' ya existe")
                continue

            # Crear el rol
            role = Role(
                organization_id=1,
                nombre=role_data["nombre"],
                descripcion=role_data["descripcion"],
                es_sistema=True,
            )
            db.add(role)
            await db.flush()  # Para obtener el ID

            # Asignar permisos
            permisos_a_asignar = []
            if role_data["permisos"] == "*":
                # Todos los permisos
                permisos_a_asignar = all_permissions
            else:
                # Permisos específicos con soporte para wildcards
                for pattern in role_data["permisos"]:
                    if pattern.endswith(".*"):
                        # Wildcard: todos los permisos que empiecen con el prefijo
                        prefix = pattern[:-2]
                        matching = [p for p in all_permissions if p.codigo.startswith(prefix + ".")]
                        permisos_a_asignar.extend(matching)
                    elif pattern == "*.ver":
                        # Todos los permisos de ver
                        matching = [p for p in all_permissions if p.codigo.endswith(".ver")]
                        permisos_a_asignar.extend(matching)
                    else:
                        # Permiso específico
                        if pattern in permissions_by_code:
                            permisos_a_asignar.append(permissions_by_code[pattern])

            # Remover duplicados
            permisos_a_asignar = list(set(permisos_a_asignar))

            # Crear relaciones role-permission
            for permiso in permisos_a_asignar:
                role_permission = RolePermission(role_id=role.id, permission_id=permiso.id)
                db.add(role_permission)

            created_count += 1
            print(f"✅ Rol '{role.nombre}' creado con {len(permisos_a_asignar)} permisos")

        await db.commit()
        print(f"\n✅ Creados {created_count} roles (Total: {len(roles_data)})")


async def main():
    """Ejecuta el script de inicialización."""
    print("🔧 Inicializando roles y permisos del sistema...\n")

    print("1️⃣ Creando permisos...")
    await crear_permisos()

    print("\n2️⃣ Creando roles...")
    await crear_roles()

    print("\n✅ Proceso completado!")


if __name__ == "__main__":
    asyncio.run(main())
