"""Crear productos de suscripción en el inventario del admin."""

import asyncio
from decimal import Decimal

from sqlalchemy import select

from dario_app.database import async_session_maker
from dario_app.modules.inventario.models import Producto


async def crear_productos_suscripcion():
    """Crea los productos de suscripción en el inventario de admin (org_id=1)."""
    ADMIN_ORG_ID = 1

    async with async_session_maker() as db:
        # Verificar si ya existen
        result = await db.execute(
            select(Producto).where(
                Producto.organization_id == ADMIN_ORG_ID, Producto.codigo.like("PLAN-%")
            )
        )
        existing = result.scalars().all()

        if existing:
            print(f"⚠️  Ya existen {len(existing)} productos de suscripción")
            for p in existing:
                print(f"   - {p.codigo}: {p.nombre} - ${p.precio_venta}")
            return

        # Productos de suscripción
        productos = [
            Producto(
                codigo="PLAN-TRIAL",
                nombre="Plan Trial - 14 días gratis",
                descripcion="Prueba gratuita de 14 días con todas las funcionalidades",
                categoria="Suscripciones",
                precio_compra=Decimal("0.00"),
                precio_venta=Decimal("0.00"),
                stock_actual=9999,
                stock_minimo=0,
                unidad_medida="suscripción",
                organization_id=ADMIN_ORG_ID,
            ),
            Producto(
                codigo="PLAN-BASIC",
                nombre="Plan Básico - Mensual",
                descripcion="1 usuario, 500 productos, inventario básico, ventas y compras",
                categoria="Suscripciones",
                precio_compra=Decimal("15.00"),
                precio_venta=Decimal("29.00"),
                stock_actual=9999,
                stock_minimo=0,
                unidad_medida="suscripción",
                organization_id=ADMIN_ORG_ID,
            ),
            Producto(
                codigo="PLAN-PRO",
                nombre="Plan Profesional - Mensual",
                descripcion="5 usuarios, productos ilimitados, POS avanzado, reportes completos",
                categoria="Suscripciones",
                precio_compra=Decimal("40.00"),
                precio_venta=Decimal("79.00"),
                stock_actual=9999,
                stock_minimo=0,
                unidad_medida="suscripción",
                organization_id=ADMIN_ORG_ID,
            ),
            Producto(
                codigo="PLAN-ENTERPRISE",
                nombre="Plan Enterprise - Mensual",
                descripcion="Usuarios ilimitados, API personalizada, servidor dedicado, soporte 24/7",
                categoria="Suscripciones",
                precio_compra=Decimal("150.00"),
                precio_venta=Decimal("299.00"),
                stock_actual=9999,
                stock_minimo=0,
                unidad_medida="suscripción",
                organization_id=ADMIN_ORG_ID,
            ),
        ]

        for producto in productos:
            db.add(producto)

        await db.commit()

        print("✅ Productos de suscripción creados exitosamente!")
        print("\n" + "=" * 60)
        print("📦 PRODUCTOS DE SUSCRIPCIÓN REGISTRADOS")
        print("=" * 60)
        for p in productos:
            print(f"• {p.codigo}: {p.nombre}")
            print(f"  Precio: ${p.precio_venta} | Categoría: {p.categoria}")
        print("=" * 60)
        print("\n💡 Estos productos se usarán automáticamente cuando alguien")
        print("   se registre desde la landing page, creando ventas POS")
        print("   en la organización admin (org_id=1)")


if __name__ == "__main__":
    asyncio.run(crear_productos_suscripcion())
