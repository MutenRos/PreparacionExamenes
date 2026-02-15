"""Crear cuenta de prueba con plan básico."""

import asyncio
from datetime import datetime

import bcrypt
from sqlalchemy import select

from dario_app.database import async_session_maker
from dario_app.modules.tenants.models import Organization
from dario_app.modules.usuarios.models import Usuario


async def crear_cuenta_basico():
    """Crea una cuenta de prueba con plan básico."""
    async with async_session_maker() as db:
        # Verificar si ya existe
        result = await db.execute(select(Usuario).where(Usuario.email == "demo@tiendaretail.com"))
        existing_user = result.scalar_one_or_none()

        if existing_user:
            print("⚠️  La cuenta demo@tiendaretail.com ya existe")
            # Mostrar info de la cuenta
            org_result = await db.execute(
                select(Organization).where(Organization.id == existing_user.organization_id)
            )
            org = org_result.scalar_one()
            print("\n📊 Información de la cuenta existente:")
            print(f"   Organización: {org.nombre}")
            print(f"   Plan: {org.plan}")
            print("   Email: demo@tiendaretail.com")
            print("   Password: demo123")
            print(f"   Max Usuarios: {org.max_usuarios}")
            print(f"   Max Productos: {org.max_productos}")
            print(f"   Estado: {org.estado}")
            return

        # Crear organización con plan básico
        org = Organization(
            nombre="Tienda Demo - Plan Básico",
            slug=f"demo-basico-{int(datetime.now().timestamp())}",
            email="demo@tiendaretail.com",
            tipo_negocio="retail",
            descripcion="Cuenta de demostración con plan básico",
            plan="basic",
            estado="active",
            trial_hasta=None,  # Plan básico no tiene trial
            max_usuarios=1,
            max_productos=500,
            max_sucursales=1,
            activo=True,
        )
        db.add(org)
        await db.flush()

        # Crear usuario admin
        password_bytes = "demo123".encode("utf-8")
        hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")

        user = Usuario(
            organization_id=org.id,
            username="demo",
            email="demo@tiendaretail.com",
            hashed_password=hashed_password,
            nombre_completo="Usuario Demo",
            es_admin=True,
            activo=True,
        )
        db.add(user)

        await db.commit()

        print("✅ Cuenta de prueba creada exitosamente!")
        print("\n" + "=" * 60)
        print("📋 CREDENCIALES DE LA CUENTA DEMO - PLAN BÁSICO")
        print("=" * 60)
        print(f"Organización: {org.nombre}")
        print(f"Plan:         {org.plan.upper()}")
        print("Email:        demo@tiendaretail.com")
        print("Password:     demo123")
        print(f"Estado:       {org.estado}")
        print("\n📊 LÍMITES DEL PLAN:")
        print(f"   • Usuarios:    {org.max_usuarios} usuario")
        print(f"   • Productos:   {org.max_productos} productos")
        print(f"   • Sucursales:  {org.max_sucursales} sucursal")
        print("\n🔗 ACCESO:")
        print("   http://localhost:5000/app/login")
        print("\n✨ CARACTERÍSTICAS DEL PLAN BÁSICO:")
        print("   ✓ 1 usuario")
        print("   ✓ 500 productos")
        print("   ✓ Inventario básico")
        print("   ✓ Ventas y compras")
        print("   ✓ Soporte email")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(crear_cuenta_basico())
